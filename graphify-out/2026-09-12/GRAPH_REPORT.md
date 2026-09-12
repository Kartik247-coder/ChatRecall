# Graph Report - Group Chat Search  (2026-09-12)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 156 nodes · 237 edges · 19 communities (11 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4700fb45`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ChatIndex
- generate_synthetic_chat
- retrieve.py
- app.py
- ChatRecall 💬🔍
- MessageEmbedder
- Evaluation Report: ChatRecall Semantic Retrieval Performance
- index.py
- test_hinglish_embed.py
- .__init__
- generate_queries.py
- .search
- rules/graphify.md
- workflows/graphify.md
- src/__init__.py
- web/__init__.py
- ndarray

## God Nodes (most connected - your core abstractions)
1. `ChatIndex` - 23 edges
2. `RetrievalEngine` - 13 edges
3. `generate_synthetic_chat()` - 11 edges
4. `parse_chat_txt()` - 10 edges
5. `ThreadContextBuilder` - 7 edges
6. `upload_custom_chat()` - 7 edges
7. `get_services()` - 7 edges
8. `ChatRecall 💬🔍` - 7 edges
9. `Evaluation Report: ChatRecall Semantic Retrieval Performance` - 7 edges
10. `StrategyType` - 6 edges

## Surprising Connections (you probably didn't know these)
- `get_services()` --uses--> `ChatIndex`  [INFERRED]
  web/app.py → src/index.py
- `engine()` --uses--> `RetrievalEngine`  [INFERRED]
  tests/test_retrieval.py → src/retrieve.py
- `get_services()` --calls--> `RetrievalEngine`  [EXTRACTED]
  web/app.py → src/retrieve.py
- `run_benchmark()` --uses--> `ChatIndex`  [INFERRED]
  eval/run_eval.py → src/index.py
- `test_txt_parser_and_search()` --uses--> `ChatIndex`  [INFERRED]
  tests/test_parser.py → src/index.py

## Import Cycles
- None detected.

## Communities (19 total, 6 thin omitted)

### Community 0 - "ChatIndex"
Cohesion: 0.11
Nodes (25): compute_metrics(), generate_markdown_report(), Any, Comprehensive Evaluation Runner for ChatRecall…, run_benchmark(), post, ChatIndex, Performs BM25 keyword search. (+17 more)

### Community 1 - "generate_synthetic_chat"
Cohesion: 0.16
Nodes (15): generate_synthetic_chat(), main(), Any, Synthetic Group Chat Generator for ChatRecall…, Unit tests for Synthetic Chat Dataset Generator, Ensure generator produces identical output for the same seed., Ensure at least 4000 messages and exactly 8 participants., Ensure messages span 6 months and are strictly chronological. (+7 more)

### Community 2 - "retrieve.py"
Cohesion: 0.20
Nodes (9): datetime, Enum, QueryPlan, QueryRouter, Multi-Strategy Query Router & Retrieval Engine for ChatRecall…, StrategyType, str, Unit tests for Retrieval Engine and Query Router (+1 more)

### Community 3 - "app.py"
Cohesion: 0.21
Nodes (9): get, Any, Extracts surrounding conversational messages around target index `msg_idx`. If…, ThreadContextBuilder, api_search(), api_stats(), get_services(), FastAPI Server for ChatRecall Web Interface… (+1 more)

### Community 4 - "ChatRecall 💬🔍"
Cohesion: 0.15
Nodes (13): 1. Installation, 2. Generate Dataset & Build Index, 3. Run Search, 4. Run Automated Evaluation, 🏗️ Architecture & Pipeline, ChatRecall 💬🔍, 📊 Evaluation & Benchmark Results, ✨ Key Capabilities (+5 more)

### Community 5 - "MessageEmbedder"
Cohesion: 0.21
Nodes (7): MessageEmbedder, Any, ndarray, Embedding Pipeline for ChatRecall ================================= Provides…, Formats a chat message with rich contextual metadata before vector encoding.…, Encodes a single natural language search query into a normalized vector., Encodes a list of chat message dictionaries into an (N, D) normalized numpy…

### Community 6 - "Evaluation Report: ChatRecall Semantic Retrieval Performance"
Cohesion: 0.18
Nodes (9): 1. Executive Summary, 2. Core Benchmark Results, 3.1 The Zero-Word-Overlap Collapse of Keyword Search, 3.2 The Performance Gap, 3. The Honest Accuracy Gap Analysis, 4. Breakdown by Category & Query Shape, 5. Detailed Query-by-Query Evaluation Log, 6. Latency & System Throughput (+1 more)

### Community 7 - "index.py"
Cohesion: 0.27
Nodes (7): display_results(), main(), Interactive Terminal Interface for ChatRecall…, Thread Context Engine for ChatRecall ====================================…, main(), Chat Indexer for ChatRecall =========================== Builds, caches, and…, ThreadContextBuilder

### Community 8 - "test_hinglish_embed.py"
Cohesion: 0.29
Nodes (7): cosine_similarity(), embedder(), fixture, ndarray, Hinglish and Zero-Word-Overlap Embedding Validation Tests…, Test suite of English queries vs Hinglish messages with ZERO word overlap.…, test_hinglish_zero_word_overlap_pairs()

### Community 9 - ".__init__"
Cohesion: 0.33
Nodes (4): MessageEmbedder, ndarray, Any, Performs cosine similarity search against candidates or the entire corpus.…

### Community 10 - "generate_queries.py"
Cohesion: 0.67
Nodes (3): build_evaluation_set(), extract_content_words(), Test Set Generator for ChatRecall Evaluation…

## Knowledge Gaps
- **19 isolated node(s):** `graphify`, `Workflow: graphify`, `1. Installation`, `2. Generate Dataset & Build Index`, `4. Run Automated Evaluation` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 76 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatIndex` connect `ChatIndex` to `.__init__`, `retrieve.py`, `app.py`, `index.py`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `generate_synthetic_chat()` connect `generate_synthetic_chat` to `retrieve.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `ChatIndex` (e.g. with `run_benchmark()` and `main()`) actually correct?**
  _`ChatIndex` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `RetrievalEngine` (e.g. with `ChatIndex` and `engine()`) actually correct?**
  _`RetrievalEngine` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `1. Installation` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ChatIndex` be split into smaller, more focused modules?**
  _Cohesion score 0.11397849462365592 - nodes in this community are weakly interconnected._