# Graph Report - Group Chat Search  (2026-09-12)

## Corpus Check
- 24 files · ~122,462 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 150 nodes · 230 edges · 17 communities (10 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d8ffcacf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ChatIndex
- generate_synthetic_chat
- MessageEmbedder
- retrieve.py
- ChatRecall 💬🔍
- RetrievalEngine
- Evaluation Report: ChatRecall Semantic Retrieval Performance
- test_hinglish_embed.py
- generate_queries.py
- .get_context_window
- rules/graphify.md
- workflows/graphify.md
- src/__init__.py
- web/__init__.py
- index.py

## God Nodes (most connected - your core abstractions)
1. `ChatIndex` - 22 edges
2. `RetrievalEngine` - 14 edges
3. `generate_synthetic_chat()` - 11 edges
4. `ThreadContextBuilder` - 9 edges
5. `MessageEmbedder` - 9 edges
6. `parse_chat_txt()` - 9 edges
7. `ChatRecall 💬🔍` - 8 edges
8. `get_services()` - 7 edges
9. `Evaluation Report: ChatRecall Semantic Retrieval Performance` - 7 edges
10. `run_benchmark()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `run_benchmark()` --uses--> `ChatIndex`  [INFERRED]
  eval/run_eval.py → src/index.py
- `test_txt_parser_and_search()` --uses--> `ChatIndex`  [INFERRED]
  tests/test_parser.py → src/index.py
- `engine()` --uses--> `ChatIndex`  [INFERRED]
  tests/test_retrieval.py → src/index.py
- `get_services()` --uses--> `ChatIndex`  [INFERRED]
  web/app.py → src/index.py
- `test_query_router_intent_classification()` --uses--> `StrategyType`  [INFERRED]
  tests/test_retrieval.py → src/retrieve.py

## Import Cycles
- None detected.

## Communities (17 total, 5 thin omitted)

### Community 0 - "ChatIndex"
Cohesion: 0.20
Nodes (13): get, display_results(), main(), Interactive Terminal Interface for ChatRecall…, Thread Context Engine for ChatRecall ====================================…, ThreadContextBuilder, ChatIndex, Performs BM25 keyword search. (+5 more)

### Community 1 - "generate_synthetic_chat"
Cohesion: 0.16
Nodes (15): generate_synthetic_chat(), main(), Any, Synthetic Group Chat Generator for ChatRecall…, Unit tests for Synthetic Chat Dataset Generator, Ensure generator produces identical output for the same seed., Ensure at least 4000 messages and exactly 8 participants., Ensure messages span 6 months and are strictly chronological. (+7 more)

### Community 2 - "MessageEmbedder"
Cohesion: 0.14
Nodes (10): MessageEmbedder, Any, ndarray, Embedding Pipeline for ChatRecall ================================= Provides…, Formats a chat message with rich contextual metadata before vector encoding.…, Encodes a single natural language search query into a normalized vector., Encodes a list of chat message dictionaries into an (N, D) normalized numpy…, Any (+2 more)

### Community 3 - "retrieve.py"
Cohesion: 0.18
Nodes (9): datetime, Enum, QueryPlan, QueryRouter, Multi-Strategy Query Router & Retrieval Engine for ChatRecall…, StrategyType, str, Unit tests for Retrieval Engine and Query Router (+1 more)

### Community 4 - "ChatRecall 💬🔍"
Cohesion: 0.12
Nodes (14): 1. Installation, 2. Generate Dataset & Build Index, 3. Run Search, 4. Run Automated Evaluation, 🏗️ Architecture & Pipeline, ChatRecall 💬🔍, 📊 Evaluation & Benchmark Results, ✨ Key Capabilities (+6 more)

### Community 5 - "RetrievalEngine"
Cohesion: 0.21
Nodes (10): compute_metrics(), generate_markdown_report(), Any, Comprehensive Evaluation Runner for ChatRecall…, run_benchmark(), Any, Executes query through the router and multi-strategy retrieval pipeline., RetrievalEngine (+2 more)

### Community 6 - "Evaluation Report: ChatRecall Semantic Retrieval Performance"
Cohesion: 0.22
Nodes (9): 1. Executive Summary, 2. Core Benchmark Results, 3.1 The Zero-Word-Overlap Collapse of Keyword Search, 3.2 The Performance Gap, 3. The Honest Accuracy Gap Analysis, 4. Breakdown by Category & Query Shape, 5. Detailed Query-by-Query Evaluation Log, 6. Latency & System Throughput (+1 more)

### Community 7 - "test_hinglish_embed.py"
Cohesion: 0.29
Nodes (7): cosine_similarity(), embedder(), fixture, ndarray, Hinglish and Zero-Word-Overlap Embedding Validation Tests…, Test suite of English queries vs Hinglish messages with ZERO word overlap.…, test_hinglish_zero_word_overlap_pairs()

### Community 8 - "generate_queries.py"
Cohesion: 0.67
Nodes (3): build_evaluation_set(), extract_content_words(), Test Set Generator for ChatRecall Evaluation…

### Community 16 - "index.py"
Cohesion: 0.18
Nodes (13): main(), Chat Indexer for ChatRecall =========================== Builds, caches, and…, Loads chat data (from .json or .txt) and cached embeddings, or builds them if…, load_custom_txt_to_json(), parse_chat_txt(), parse_timestamp(), Any, Text Chat Parser for ChatRecall =============================== Parses raw… (+5 more)

## Knowledge Gaps
- **20 isolated node(s):** `graphify`, `Workflow: graphify`, `🎯 Problem Statement`, `✨ Key Capabilities`, `📊 Evaluation & Benchmark Results` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 75 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatIndex` connect `ChatIndex` to `index.py`, `MessageEmbedder`, `retrieve.py`, `RetrievalEngine`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `MessageEmbedder` connect `MessageEmbedder` to `index.py`, `ChatIndex`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `generate_synthetic_chat()` connect `generate_synthetic_chat` to `retrieve.py`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ChatIndex` (e.g. with `run_benchmark()` and `main()`) actually correct?**
  _`ChatIndex` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `RetrievalEngine` (e.g. with `ChatIndex` and `engine()`) actually correct?**
  _`RetrievalEngine` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `ThreadContextBuilder` (e.g. with `display_results()` and `ChatIndex`) actually correct?**
  _`ThreadContextBuilder` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `🎯 Problem Statement` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._