# MessageEmbedder

> 17 nodes · cohesion 0.14

## Key Concepts

- **MessageEmbedder** (9 connections) — `src/embed.py`
- **.encode_messages()** (5 connections) — `src/embed.py`
- **.format_message_for_embedding()** (4 connections) — `src/embed.py`
- **.__init__()** (4 connections) — `src/index.py`
- **embed.py** (3 connections) — `src/embed.py`
- **.encode_query()** (3 connections) — `src/embed.py`
- **.dense_search()** (3 connections) — `src/index.py`
- **Any** (2 connections)
- **ndarray** (2 connections)
- **ndarray** (2 connections)
- **.__init__()** (1 connections) — `src/embed.py`
- **Embedding Pipeline for ChatRecall ================================= Provides…** (1 connections) — `src/embed.py`
- **Formats a chat message with rich contextual metadata before vector encoding.…** (1 connections) — `src/embed.py`
- **Encodes a single natural language search query into a normalized vector.** (1 connections) — `src/embed.py`
- **Encodes a list of chat message dictionaries into an (N, D) normalized numpy…** (1 connections) — `src/embed.py`
- **Any** (1 connections)
- **Performs cosine similarity search against candidates or the entire corpus.…** (1 connections) — `src/index.py`

## Relationships

- [ChatIndex](ChatIndex.md) (6 shared connections)

## Source Files

- `src/embed.py`
- `src/index.py`

## Audit Trail

- EXTRACTED: 24 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*