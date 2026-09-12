# ChatRecall 💬🔍
> **Semantic Retrieval over a Synthetic Group Chat Archive**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Hinglish-Ready](https://img.shields.io/badge/Hinglish-Multilingual%20Embedding-orange.svg)]()
[![Zero--Word--Overlap](https://img.shields.io/badge/Zero--Word--Overlap-Evaluated-success.svg)]()

---

## 🎯 Problem Statement
Standard keyword/text search fails when you remember the *meaning* of a conversation but not the exact words used. For example, asking *"When did we decide on the mountain trip?"* fails if the original message was in code-mixed Hinglish: *"chalo Manali fix hai Dec 28 se"*.

**ChatRecall** is a semantic retrieval engine designed for messy, real-world group chat archives. It delivers:
1. **Zero-Word-Overlap Retrieval**: Finds the correct message even when query and target share zero vocabulary.
2. **Three Query Shapes**: Handles **Semantic/Meaning-based**, **Person-based** (sender filter), and **Time-based** (relative & absolute date ranges).
3. **Decision-Resolution Awareness**: Surfaces the actual resolution message over 40+ messages of debate.
4. **Thread Context**: Presents matched messages with surrounding conversational dialogue, not bare strings.
5. **Hinglish & Code-Mixed Support**: Native support for multilingual, code-mixed colloquial text.

---

## 🏗️ Project Architecture

```
ChatRecall/
├── data/
│   ├── generate_chat.py       # Deterministic 4,200+ message generator (seed=42)
│   └── chat.json              # 8 participants, 6-month timeline, 3 resolving threads
├── src/
│   ├── embed.py               # Multilingual embedding generator (Hinglish-validated)
│   ├── index.py               # Vector and metadata indexing pipeline
│   ├── retrieve.py            # Multi-strategy query router & ranker
│   ├── context.py             # Thread & conversational burst reconstructor
│   └── cli.py                 # Interactive terminal search interface
├── web/
│   ├── app.py                 # FastAPI web application
│   └── static/index.html      # Modern dark-mode web UI with thread explorer
├── eval/
│   ├── queries.json           # 40 ground-truth test queries (including 8+ hard zero-word-overlap)
│   ├── run_eval.py            # Automated evaluation runner & comparative benchmarking
│   └── results.md             # In-depth evaluation report & accuracy breakdown
└── tests/
    ├── test_generator.py      # Dataset integrity & messiness validation
    └── test_hinglish_embed.py # Early Hinglish embedding cosine similarity tests
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/Kartik247-coder/ChatRecall.git
cd ChatRecall
pip install -r requirements.txt
```

### 2. Generate Dataset & Index
```bash
# Generate 4,200+ synthetic chat messages
python data/generate_chat.py

# Build semantic vector index
python -m src.index
```

### 3. Run Search
```bash
# Interactive CLI
python -m src.cli --query "When did we decide on the mountain trip?"

# Or start the Web UI
python -m web.app
```

---

## 📊 Benchmark & Evaluation Summary
*(Updated progressively as evaluation is run)*
- **Total Test Queries**: 40
- **Hard Zero-Word-Overlap Queries**: 8+
- Detailed metric breakdown available in [`eval/results.md`](eval/results.md).
