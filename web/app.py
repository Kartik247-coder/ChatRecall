"""
FastAPI Server for ChatRecall Web Interface
===========================================
Serves semantic search API and interactive thread exploration interface.
"""

import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List

from src.index import ChatIndex
from src.retrieve import RetrievalEngine
from src.context import ThreadContextBuilder

app = FastAPI(title="ChatRecall Web API", version="0.1.0")

# Mount static folder
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Lazy load index and engine
_index: Optional[ChatIndex] = None
_engine: Optional[RetrievalEngine] = None
_ctx_builder: Optional[ThreadContextBuilder] = None


def get_services():
    global _index, _engine, _ctx_builder
    if _index is None:
        _index = ChatIndex.build_or_load()
        _engine = RetrievalEngine(_index)
        _ctx_builder = ThreadContextBuilder(_index)
    return _index, _engine, _ctx_builder


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>ChatRecall UI</h1><p>Index file not found in static/</p>")


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

    # Also compute lexical BM25 baseline top matches for side-by-side comparison
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
        "plan": search_data["plan"],
        "candidate_count": search_data["candidate_count"],
        "semantic_results": enriched_results,
        "lexical_baseline": lexical_results
    }


@app.get("/api/stats")
async def api_stats():
    index, _, _ = get_services()
    senders = list(index.sender_index.keys())
    return {
        "total_messages": len(index.messages),
        "embedding_dim": index.embeddings.shape[1],
        "date_range": [index.messages[0]["timestamp"], index.messages[-1]["timestamp"]],
        "participants": [
            "Rohan Mehta", "Priya Sharma", "Kabir Sen", "Ananya Iyer",
            "Vikram Malhotra", "Neha Gupta", "Siddharth Verma", "Tanvi Desai"
        ]
    }


def main():
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
