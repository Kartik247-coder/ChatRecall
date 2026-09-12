# Graph Report - Group Chat Search  (2026-09-12)

## Corpus Check
- 24 files · ~123,149 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 153 nodes · 244 edges · 18 communities (11 shown, 5 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b28214f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ThreadContextBuilder
- generate_synthetic_chat
- index.py
- retrieve.py
- ChatRecall 💬🔍
- ChatIndex
- Evaluation Report: ChatRecall Semantic Retrieval Performance
- test_hinglish_embed.py
- generate_queries.py
- app.py
- rules/graphify.md
- workflows/graphify.md
- src/__init__.py
- web/__init__.py
- parse_chat_txt
- .search

## God Nodes (most connected - your core abstractions)
1. `ChatIndex` - 24 edges
2. `RetrievalEngine` - 16 edges
3. `generate_synthetic_chat()` - 11 edges
4. `ThreadContextBuilder` - 11 edges
5. `parse_chat_txt()` - 10 edges
6. `MessageEmbedder` - 9 edges
7. `get_services()` - 7 edges
8. `upload_custom_chat()` - 7 edges
9. `ChatRecall 💬🔍` - 7 edges
10. `Evaluation Report: ChatRecall Semantic Retrieval Performance` - 7 edges

## Surprising Connections (you probably didn't know these)
- `reset_to_default_chat()` --uses--> `ThreadContextBuilder`  [INFERRED]
  web/app.py → src/context.py
- `upload_custom_chat()` --uses--> `ThreadContextBuilder`  [INFERRED]
  web/app.py → src/context.py
- `get_services()` --uses--> `ChatIndex`  [INFERRED]
  web/app.py → src/index.py
- `run_benchmark()` --uses--> `ChatIndex`  [INFERRED]
  eval/run_eval.py → src/index.py
- `get_services()` --calls--> `ThreadContextBuilder`  [EXTRACTED]
  web/app.py → src/context.py

## Import Cycles
- None detected.

## Communities (18 total, 5 thin omitted)

### Community 0 - "ThreadContextBuilder"
Cohesion: 0.25
Nodes (7): display_results(), main(), Interactive Terminal Interface for ChatRecall…, Any, Thread Context Engine for ChatRecall ====================================…, Extracts surrounding conversational messages around target index `msg_idx`. If…, ThreadContextBuilder

### Community 1 - "generate_synthetic_chat"
Cohesion: 0.16
Nodes (16): generate_synthetic_chat(), main(), Any, Synthetic Group Chat Generator for ChatRecall…, datetime, Unit tests for Synthetic Chat Dataset Generator, Ensure generator produces identical output for the same seed., Ensure at least 4000 messages and exactly 8 participants. (+8 more)

### Community 2 - "index.py"
Cohesion: 0.12
Nodes (12): MessageEmbedder, Any, ndarray, Embedding Pipeline for ChatRecall ================================= Provides…, Formats a chat message with rich contextual metadata before vector encoding.…, Encodes a single natural language search query into a normalized vector., Encodes a list of chat message dictionaries into an (N, D) normalized numpy…, main() (+4 more)

### Community 3 - "retrieve.py"
Cohesion: 0.20
Nodes (8): Enum, QueryPlan, QueryRouter, Multi-Strategy Query Router & Retrieval Engine for ChatRecall…, StrategyType, str, Unit tests for Retrieval Engine and Query Router, test_query_router_intent_classification()

### Community 4 - "ChatRecall 💬🔍"
Cohesion: 0.15
Nodes (13): 1. Installation, 2. Generate Dataset & Build Index, 3. Run Search, 4. Run Automated Evaluation, 🏗️ Architecture & Pipeline, ChatRecall 💬🔍, 📊 Evaluation & Benchmark Results, ✨ Key Capabilities (+5 more)

### Community 5 - "ChatIndex"
Cohesion: 0.17
Nodes (17): compute_metrics(), generate_markdown_report(), Any, Comprehensive Evaluation Runner for ChatRecall…, run_benchmark(), post, ChatIndex, Performs BM25 keyword search. (+9 more)

### Community 6 - "Evaluation Report: ChatRecall Semantic Retrieval Performance"
Cohesion: 0.18
Nodes (9): 1. Executive Summary, 2. Core Benchmark Results, 3.1 The Zero-Word-Overlap Collapse of Keyword Search, 3.2 The Performance Gap, 3. The Honest Accuracy Gap Analysis, 4. Breakdown by Category & Query Shape, 5. Detailed Query-by-Query Evaluation Log, 6. Latency & System Throughput (+1 more)

### Community 7 - "test_hinglish_embed.py"
Cohesion: 0.29
Nodes (7): cosine_similarity(), embedder(), fixture, ndarray, Hinglish and Zero-Word-Overlap Embedding Validation Tests…, Test suite of English queries vs Hinglish messages with ZERO word overlap.…, test_hinglish_zero_word_overlap_pairs()

### Community 8 - "generate_queries.py"
Cohesion: 0.67
Nodes (3): build_evaluation_set(), extract_content_words(), Test Set Generator for ChatRecall Evaluation…

### Community 9 - "app.py"
Cohesion: 0.39
Nodes (6): get, api_search(), api_stats(), get_services(), FastAPI Server for ChatRecall Web Interface…, serve_ui()

### Community 16 - "parse_chat_txt"
Cohesion: 0.28
Nodes (8): load_custom_txt_to_json(), parse_chat_txt(), parse_timestamp(), Any, Text Chat Parser for ChatRecall =============================== Parses raw…, Parses a .txt file and saves it as structured JSON ready for indexing., Attempts multiple datetime formats and normalizes to YYYY-MM-DD HH:MM:SS., Parses any exported text file (.txt) into a list of structured messages.

## Knowledge Gaps
- **19 isolated node(s):** `graphify`, `Workflow: graphify`, `🎯 Problem Statement`, `✨ Key Capabilities`, `📊 Evaluation & Benchmark Results` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 75 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatIndex` connect `ChatIndex` to `ThreadContextBuilder`, `app.py`, `index.py`, `retrieve.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `MessageEmbedder` connect `index.py` to `ChatIndex`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ChatIndex` (e.g. with `run_benchmark()` and `main()`) actually correct?**
  _`ChatIndex` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `RetrievalEngine` (e.g. with `ChatIndex` and `engine()`) actually correct?**
  _`RetrievalEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ThreadContextBuilder` (e.g. with `display_results()` and `ChatIndex`) actually correct?**
  _`ThreadContextBuilder` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `🎯 Problem Statement` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `index.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12105263157894737 - nodes in this community are weakly interconnected._