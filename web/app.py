"""
FastAPI Server for ChatRecall Web Interface
===========================================
Serves semantic search API, thread exploration interface, and live .txt / .json file upload.
"""

import os
import shutil
from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List, Dict, Any

from src.index import ChatIndex
from src.retrieve import RetrievalEngine
from src.context import ThreadContextBuilder
from src.parser import parse_chat_txt

app = FastAPI(title="ChatRecall Web API", version="0.2.0")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# In-memory active services
_current_source_name: str = "Synthetic Group Chat (Default)"
_index: Optional[ChatIndex] = None
_engine: Optional[RetrievalEngine] = None
_ctx_builder: Optional[ThreadContextBuilder] = None


def get_services():
    global _index, _engine, _ctx_builder, _current_source_name
    if _index is None:
        _index = ChatIndex.build_or_load()
        _engine = RetrievalEngine(_index)
        _ctx_builder = ThreadContextBuilder(_index)
        _current_source_name = "Synthetic Group Chat (Default)"
    return _index, _engine, _ctx_builder


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>ChatRecall UI</h1><p>Index file not found in static/</p>")


@app.get("/api/stats")
async def api_stats():
    index, _, _ = get_services()
    senders = sorted(list(set(m["sender"] for m in index.messages)))
    return {
        "source_name": _current_source_name,
        "total_messages": len(index.messages),
        "embedding_dim": index.embeddings.shape[1],
        "date_range": [index.messages[0]["timestamp"], index.messages[-1]["timestamp"]],
        "participants": senders
    }


@app.post("/api/upload")
async def upload_custom_chat(file: UploadFile = File(...)):
    global _index, _engine, _ctx_builder, _current_source_name
    
    filename = file.filename or "uploaded_chat.txt"
    if not (filename.endswith(".txt") or filename.endswith(".json")):
        raise HTTPException(status_code=400, detail="Only .txt (WhatsApp/Telegram export) or .json files are supported.")

    saved_path = os.path.join(UPLOAD_DIR, filename)
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Build fresh index for uploaded chat file
        new_index = ChatIndex.build_or_load(chat_path=saved_path, force_rebuild=True)
        if len(new_index.messages) == 0:
            raise HTTPException(status_code=400, detail="No valid chat messages could be parsed from this file.")

        _index = new_index
        _engine = RetrievalEngine(_index)
        _ctx_builder = ThreadContextBuilder(_index)
        _current_source_name = filename

        senders = sorted(list(set(m["sender"] for m in _index.messages)))
        return {
            "status": "success",
            "message": f"Successfully loaded and indexed {len(_index.messages)} messages from {filename}",
            "source_name": _current_source_name,
            "total_messages": len(_index.messages),
            "date_range": [_index.messages[0]["timestamp"], _index.messages[-1]["timestamp"]],
            "participants": senders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse and index chat file: {str(e)}")


@app.post("/api/reset")
async def reset_to_default_chat():
    global _index, _engine, _ctx_builder, _current_source_name
    _index = ChatIndex.build_or_load(chat_path="data/chat.json")
    _engine = RetrievalEngine(_index)
    _ctx_builder = ThreadContextBuilder(_index)
    _current_source_name = "Synthetic Group Chat (Default)"
    
    senders = sorted(list(set(m["sender"] for m in _index.messages)))
    return {
        "status": "success",
        "message": "Reset to default synthetic chat archive",
        "source_name": _current_source_name,
        "total_messages": len(_index.messages),
        "participants": senders
    }


@app.get("/api/search")
async def api_search(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results"),
    window: int = Query(3, description="Context window size")
):
    index, engine, ctx_builder = get_services()
    search_data = engine.search(q, top_k=top_k)

    # Attach context to each result
    enriched_results = []
    for r in search_data["results"]:
        ctx = ctx_builder.get_context_window(r["msg_idx"], window_before=window, window_after=window)
        r_copy = dict(r)
        r_copy["thread_context"] = ctx
        enriched_results.append(r_copy)

    # BM25 baseline top matches
    lexical_matches = index.lexical_search(q, top_k=3)
    lexical_results = []
    for idx, score in lexical_matches:
        m = index.messages[idx]
        lexical_results.append({
            "id": m["id"],
            "sender": m["sender"],
            "timestamp": m["timestamp"],
            "message": m["message"],
            "score": round(score, 4),
        })

    return {
        "query": q,
        "source_name": _current_source_name,
        "plan": search_data["plan"],
        "candidate_count": search_data["candidate_count"],
        "semantic_results": enriched_results,
        "lexical_baseline": lexical_results
    }


def main():
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
