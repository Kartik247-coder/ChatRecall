# Graph Report - Group Chat Search  (2026-09-12)

## Corpus Check
- 28 files · ~130,906 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 183 nodes · 287 edges · 20 communities (12 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0c63b3fe`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ChatIndex
- generate_synthetic_chat
- retrieve.py
- .get_context_window
- Evaluation Report: ChatRecall Semantic Retrieval Performance
- MessageEmbedder
- parse_chat_txt
- ChatRecall Tuning & Retrieval Evaluation Notes
- test_hinglish_embed.py
- run_demo_eval.py
- generate_queries.py
- run_eval.py
- rules/graphify.md
- workflows/graphify.md
- src/__init__.py
- web/__init__.py
- generate_demo_chat.py
- .search

## God Nodes (most connected - your core abstractions)
1. `ChatIndex` - 26 edges
2. `RetrievalEngine` - 19 edges
3. `generate_synthetic_chat()` - 11 edges
4. `ThreadContextBuilder` - 11 edges
5. `MessageEmbedder` - 10 edges
6. `parse_chat_txt()` - 10 edges
7. `QueryRouter` - 7 edges
8. `get_services()` - 7 edges
9. `upload_custom_chat()` - 7 edges
10. `ChatRecall 💬🔍` - 7 edges

## Surprising Connections (you probably didn't know these)
- `run_demo_benchmark()` --uses--> `ChatIndex`  [INFERRED]
  eval/run_demo_eval.py → src/index.py
- `run_benchmark()` --uses--> `ChatIndex`  [INFERRED]
  eval/run_eval.py → src/index.py
- `run_demo_benchmark()` --calls--> `RetrievalEngine`  [EXTRACTED]
  eval/run_demo_eval.py → src/retrieve.py
- `run_benchmark()` --calls--> `RetrievalEngine`  [EXTRACTED]
  eval/run_eval.py → src/retrieve.py
- `reset_to_default_chat()` --uses--> `ThreadContextBuilder`  [INFERRED]
  web/app.py → src/context.py

## Import Cycles
- None detected.

## Communities (20 total, 6 thin omitted)

### Community 0 - "ChatIndex"
Cohesion: 0.14
Nodes (23): get, post, display_results(), main(), Interactive Terminal Interface for ChatRecall…, Thread Context Engine for ChatRecall ====================================…, ThreadContextBuilder, ChatIndex (+15 more)

### Community 1 - "generate_synthetic_chat"
Cohesion: 0.16
Nodes (15): generate_synthetic_chat(), main(), Any, Synthetic Group Chat Generator for ChatRecall…, Unit tests for Synthetic Chat Dataset Generator, Ensure generator produces identical output for the same seed., Ensure at least 4000 messages and exactly 8 participants., Ensure messages span 6 months and are strictly chronological. (+7 more)

### Community 2 - "retrieve.py"
Cohesion: 0.11
Nodes (17): datetime, Enum, Embedding Pipeline for ChatRecall ================================= Provides…, Chat Indexer for ChatRecall =========================== Builds, caches, and…, QueryPlan, QueryRouter, Multi-Strategy Query Router & Retrieval Engine for ChatRecall…, Dynamically parses time expressions relative to active archive timestamps. (+9 more)

### Community 4 - "Evaluation Report: ChatRecall Semantic Retrieval Performance"
Cohesion: 0.08
Nodes (22): 1. Executive Summary, 2. Core Benchmark Results, 3.1 The Zero-Word-Overlap Collapse of Keyword Search, 3.2 The Performance Gap, 3. The Honest Accuracy Gap Analysis, 4. Breakdown by Category & Query Shape, 5. Detailed Query-by-Query Evaluation Log, 6. Latency & System Throughput (+14 more)

### Community 5 - "MessageEmbedder"
Cohesion: 0.15
Nodes (10): MessageEmbedder, Any, ndarray, Formats a chat message for vector encoding. Prepends sender name and clean text…, Builds thread-aware contextual texts for conversation messages. Includes…, Encodes a single natural language search query into a normalized vector., Encodes a list of chat message dictionaries into an (N, D) normalized numpy…, Any (+2 more)

### Community 6 - "parse_chat_txt"
Cohesion: 0.28
Nodes (8): load_custom_txt_to_json(), parse_chat_txt(), parse_timestamp(), Any, Text Chat Parser for ChatRecall =============================== Parses raw…, Parses a .txt file and saves it as structured JSON ready for indexing., Attempts multiple datetime formats and normalizes to YYYY-MM-DD HH:MM:SS., Parses any exported text file (.txt) into a list of structured messages.

### Community 7 - "ChatRecall Tuning & Retrieval Evaluation Notes"
Cohesion: 0.18
Nodes (10): 1. Executive Summary & Deliverable Metrics, 2. Top-K Context-Window Deduplication & Diversity Re-ranking, 3. Decision Threshold & Confidence Cutoffs, 4. Zero-Word-Overlap Hard Question Evaluation, ChatRecall Tuning & Retrieval Evaluation Notes, Deduplication Algorithm, Problem Observed, Quantitative Rationale: (+2 more)

### Community 8 - "test_hinglish_embed.py"
Cohesion: 0.29
Nodes (7): cosine_similarity(), embedder(), fixture, ndarray, Hinglish and Zero-Word-Overlap Embedding Validation Tests…, Test suite of English queries vs Hinglish messages with ZERO word overlap.…, test_hinglish_zero_word_overlap_pairs()

### Community 9 - "run_demo_eval.py"
Cohesion: 0.60
Nodes (4): compute_metrics(), Any, Evaluation Runner for sample_chat.txt and questions.json…, run_demo_benchmark()

### Community 10 - "generate_queries.py"
Cohesion: 0.67
Nodes (3): build_evaluation_set(), extract_content_words(), Test Set Generator for ChatRecall Evaluation…

### Community 11 - "run_eval.py"
Cohesion: 0.47
Nodes (5): compute_metrics(), generate_markdown_report(), Any, Comprehensive Evaluation Runner for ChatRecall…, run_benchmark()

### Community 19 - ".search"
Cohesion: 0.40
Nodes (3): Any, Suppresses candidate messages whose context window overlaps significantly…, Executes query through multi-strategy routing, contextual vector search,…

## Knowledge Gaps
- **26 isolated node(s):** `graphify`, `Workflow: graphify`, `🎯 Problem Statement`, `✨ Key Capabilities`, `📊 Evaluation & Benchmark Results` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 92 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatIndex` connect `ChatIndex` to `run_demo_eval.py`, `retrieve.py`, `run_eval.py`, `MessageEmbedder`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `MessageEmbedder` connect `MessageEmbedder` to `ChatIndex`, `retrieve.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `RetrievalEngine` connect `ChatIndex` to `.search`, `run_demo_eval.py`, `retrieve.py`, `run_eval.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `ChatIndex` (e.g. with `run_demo_benchmark()` and `run_benchmark()`) actually correct?**
  _`ChatIndex` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `RetrievalEngine` (e.g. with `ChatIndex` and `engine()`) actually correct?**
  _`RetrievalEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `datetime` (e.g. with `generate_synthetic_chat()` and `test_query_router_intent_classification()`) actually correct?**
  _`datetime` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ThreadContextBuilder` (e.g. with `display_results()` and `ChatIndex`) actually correct?**
  _`ThreadContextBuilder` has 4 INFERRED edges - model-reasoned connections that need verification._