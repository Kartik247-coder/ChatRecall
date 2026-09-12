# ChatIndex

> 24 nodes · cohesion 0.16

## Key Concepts

- **ChatIndex** (20 connections) — `src/index.py`
- **index.py** (12 connections) — `src/index.py`
- **app.py** (12 connections) — `web/app.py`
- **cli.py** (9 connections) — `src/cli.py`
- **ThreadContextBuilder** (9 connections) — `src/context.py`
- **.build_or_load()** (8 connections) — `src/index.py`
- **context.py** (7 connections) — `src/context.py`
- **get_services()** (7 connections) — `web/app.py`
- **main()** (6 connections) — `src/cli.py`
- **get** (3 connections)
- **display_results()** (3 connections) — `src/cli.py`
- **api_search()** (3 connections) — `web/app.py`
- **api_stats()** (3 connections) — `web/app.py`
- **.__init__()** (2 connections) — `src/context.py`
- **.lexical_search()** (2 connections) — `src/index.py`
- **main()** (2 connections) — `src/index.py`
- **serve_ui()** (2 connections) — `web/app.py`
- **Interactive Terminal Interface for ChatRecall…** (1 connections) — `src/cli.py`
- **Thread Context Engine for ChatRecall ====================================…** (1 connections) — `src/context.py`
- **Chat Indexer for ChatRecall =========================== Builds, caches, and…** (1 connections) — `src/index.py`
- **Performs BM25 keyword search.** (1 connections) — `src/index.py`
- **Loads chat data and cached embeddings, or builds them if not present.** (1 connections) — `src/index.py`
- **main()** (1 connections) — `web/app.py`
- **FastAPI Server for ChatRecall Web Interface…** (1 connections) — `web/app.py`

## Relationships

- [RetrievalEngine](RetrievalEngine.md) (11 shared connections)
- [retrieve.py](retrieve.py.md) (7 shared connections)
- [MessageEmbedder](MessageEmbedder.md) (6 shared connections)
- [generate_synthetic_chat](generate_synthetic_chat.md) (2 shared connections)
- [.get_context_window](get_context_window.md) (1 shared connections)

## Source Files

- `src/cli.py`
- `src/context.py`
- `src/index.py`
- `web/app.py`

## Audit Trail

- EXTRACTED: 64 (89%)
- INFERRED: 8 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*