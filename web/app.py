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


def get_dynamic_suggestions(index: ChatIndex, source_name: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Generates tailored query suggestions categorized by the 3 core query types:
    1. Meaning-based (Semantic)
    2. Person-based (Author entity filter)
    3. Time-based (Temporal constraints)
    4. Decision & Factual resolution
    """
    senders = sorted(list(set(m["sender"] for m in index.messages if m["sender"] and m["sender"] != "System")))
    src_lower = source_name.lower()

    if "sample_chat_3" in src_lower or any("washing machine" in m["message"].lower() for m in index.messages[:10]):
        return {
            "meaning": [
                {"title": "Washing Machine Cost", "query": "how much did the washing machine cost", "icon": "⚡", "desc": "Factual price retrieval"},
                {"title": "Housewarming Food Order", "query": "what did they order for food for the party", "icon": "🍕", "desc": "Catering outcome"},
                {"title": "Machine Replacement Reason", "query": "why did they decide to replace the washing machine", "icon": "🔧", "desc": "Conversational rationale"},
                {"title": "Flatmate Preference", "query": "hesitant about stranger moving in", "icon": "🏠", "desc": "Semantic zero-overlap"}
            ],
            "person": [
                {"title": "Dev's Rent Negotiation", "query": "what did Dev negotiate with the landlord", "icon": "👤", "desc": "Author: Dev"},
                {"title": "Zara's 4th Flatmate Suggestion", "query": "what did Zara suggest about the 4th flatmate", "icon": "👤", "desc": "Author: Zara"},
                {"title": "Ishaan on New Machine", "query": "what did Ishaan say about the new machine", "icon": "👤", "desc": "Author: Ishaan"}
            ],
            "time": [
                {"title": "Early January (Machine Issues)", "query": "what happened in early January", "icon": "📅", "desc": "Time: Jan 1 - Jan 10"},
                {"title": "Mid January (Negotiations)", "query": "discussions in mid January", "icon": "📅", "desc": "Time: Jan 10 - Jan 20"},
                {"title": "Late January (Party)", "query": "party discussion in late January", "icon": "📅", "desc": "Time: Jan 20 - Jan 31"}
            ],
            "decision": [
                {"title": "Rent Increase Outcome", "query": "how much did rent increase after negotiation", "icon": "🎯", "desc": "Negotiation agreement"},
                {"title": "Who is Moving In", "query": "who is moving in to the flat", "icon": "🎯", "desc": "Cousin flatmate resolution"},
                {"title": "Catering Confirmation", "query": "what did Zara confirm for catering", "icon": "🎯", "desc": "Biryani & starters order"}
            ]
        }
    elif "sample_chat_2" in src_lower or any("leather strap" in m["message"].lower() or "rahul" in m["message"].lower() for m in index.messages):
        return {
            "meaning": [
                {"title": "Farewell Gift Resolution", "query": "Surprise reading gadget ordered for our friend moving abroad", "icon": "🎁", "desc": "Zero-word-overlap gift intent"},
                {"title": "Owed Amount per Head", "query": "how much does each person owe for the gift", "icon": "💰", "desc": "Cost per person"},
                {"title": "Kasol Homestay Decision", "query": "where did Amit decide to go for the trip", "icon": "🏔️", "desc": "Trip destination"}
            ],
            "person": [
                {"title": "Neha's Gift Decision", "query": "what did Neha decide for Rahul's gift", "icon": "👤", "desc": "Author: Neha"},
                {"title": "Amit's Trip Choice", "query": "where did Amit decide to go", "icon": "👤", "desc": "Author: Amit"},
                {"title": "Pooja's Tax Reminder", "query": "what did Pooja say about investment declarations", "icon": "👤", "desc": "Author: Pooja"}
            ],
            "time": [
                {"title": "Early December Discussions", "query": "what did we discuss in early December", "icon": "📅", "desc": "Time: Dec 1 - Dec 10"},
                {"title": "Late December Tax Proofs", "query": "investment declarations due in late December", "icon": "📅", "desc": "Time: Dec 20 - Dec 31"}
            ],
            "decision": [
                {"title": "Rahul Gift Locked", "query": "what did Neha decide about Rahul's gift", "icon": "🎯", "desc": "Leather strap decision"},
                {"title": "Trip Destination Final", "query": "locking Kasol trip destination", "icon": "🎯", "desc": "Kasol homestay outcome"}
            ]
        }
    else:
        # Default Synthetic Chat / General Archive
        p1 = senders[0] if len(senders) > 0 else "Kabir"
        p2 = senders[1] if len(senders) > 1 else "Meera"
        p3 = senders[2] if len(senders) > 2 else "Priya"

        return {
            "meaning": [
                {"title": "Mountain Trip (Zero Overlap)", "query": "When did we decide on the mountain holiday?", "icon": "🏔️", "desc": "Zero-overlap semantics"},
                {"title": "Work Trip Suggestion", "query": "did anyone suggest turning this into a work trip", "icon": "💼", "desc": "Workation query"},
                {"title": "Pet Policy at Resort", "query": "are pets allowed at the resort", "icon": "🐾", "desc": "Zero-overlap rule check"},
                {"title": "Power Bank Borrowing", "query": "who is bringing a power bank", "icon": "🔋", "desc": "Item query"}
            ],
            "person": [
                {"title": f"What did {p1} say about resort", "query": f"what did {p1} say about the resort rooms", "icon": "👤", "desc": f"Author: {p1}"},
                {"title": f"What did {p2} say about tickets", "query": f"what did {p2} say about flight tickets", "icon": "👤", "desc": f"Author: {p2}"},
                {"title": f"What did {p3} say about packing", "query": f"what did {p3} say about packing", "icon": "👤", "desc": f"Author: {p3}"}
            ],
            "time": [
                {"title": "Early March Discussions", "query": "what did we discuss in early March", "icon": "📅", "desc": "Time: Mar 1 - Mar 10"},
                {"title": "Third Week of May", "query": "what happened in the chat during the third week of May", "icon": "📅", "desc": "Time: May 15 - May 22"},
                {"title": "Discussions in June", "query": "what was discussed in June", "icon": "📅", "desc": "Time: Full Month"}
            ],
            "decision": [
                {"title": "Trip Destination Finalized", "query": "was the destination ever finalized", "icon": "🎯", "desc": "Manali decision"},
                {"title": "Travel Budget per Head", "query": "what is the budget per person for travel and stay", "icon": "🎯", "desc": "8k final number"},
                {"title": "Rooming Arrangement", "query": "how are they splitting up the sleeping arrangements", "icon": "🎯", "desc": "Girls room outcome"}
            ]
        }


@app.get("/api/stats")
async def api_stats():
    index, _, _ = get_services()
    senders = sorted(list(set(m["sender"] for m in index.messages if m["sender"] and m["sender"] != "System")))
    suggestions = get_dynamic_suggestions(index, _current_source_name)
    return {
        "source_name": _current_source_name,
        "total_messages": len(index.messages),
        "embedding_dim": index.embeddings.shape[1],
        "date_range": [index.messages[0]["timestamp"], index.messages[-1]["timestamp"]],
        "participants": senders,
        "suggestions": suggestions
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
        "literal_query": q,
        "query": q,
        "clean_query": search_data.get("clean_query", q),
        "expanded_query": search_data.get("expanded_query", q),
        "source_name": _current_source_name,
        "plan": search_data["plan"],
        "candidate_count": search_data["candidate_count"],
        "threshold": search_data.get("threshold", 0.28),
        "no_confident_match": search_data.get("no_confident_match", False),
        "deduplicated": search_data.get("deduplicated", True),
        "semantic_results": enriched_results,
        "lexical_baseline": lexical_results
    }


def main():
    import uvicorn
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
