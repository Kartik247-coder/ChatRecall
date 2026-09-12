# RetrievalEngine

> 12 nodes · cohesion 0.21

## Key Concepts

- **RetrievalEngine** (12 connections) — `src/retrieve.py`
- **run_eval.py** (8 connections) — `eval/run_eval.py`
- **run_benchmark()** (6 connections) — `eval/run_eval.py`
- **engine()** (5 connections) — `tests/test_retrieval.py`
- **compute_metrics()** (3 connections) — `eval/run_eval.py`
- **.search()** (3 connections) — `src/retrieve.py`
- **generate_markdown_report()** (2 connections) — `eval/run_eval.py`
- **Any** (1 connections)
- **Comprehensive Evaluation Runner for ChatRecall…** (1 connections) — `eval/run_eval.py`
- **Any** (1 connections)
- **Executes query through the router and multi-strategy retrieval pipeline.** (1 connections) — `src/retrieve.py`
- **fixture** (1 connections)

## Relationships

- [ChatIndex](ChatIndex.md) (11 shared connections)
- [retrieve.py](retrieve.py.md) (5 shared connections)

## Source Files

- `eval/run_eval.py`
- `src/retrieve.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 26 (87%)
- INFERRED: 4 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*