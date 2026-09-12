# MessageEmbedder

> 12 nodes · cohesion 0.21

## Key Concepts

- **MessageEmbedder** (5 connections) — `src/embed.py`
- **.encode_messages()** (5 connections) — `src/embed.py`
- **.format_message_for_embedding()** (4 connections) — `src/embed.py`
- **embed.py** (3 connections) — `src/embed.py`
- **.encode_query()** (3 connections) — `src/embed.py`
- **Any** (2 connections)
- **ndarray** (2 connections)
- **.__init__()** (1 connections) — `src/embed.py`
- **Embedding Pipeline for ChatRecall ================================= Provides…** (1 connections) — `src/embed.py`
- **Formats a chat message with rich contextual metadata before vector encoding.…** (1 connections) — `src/embed.py`
- **Encodes a single natural language search query into a normalized vector.** (1 connections) — `src/embed.py`
- **Encodes a list of chat message dictionaries into an (N, D) normalized numpy…** (1 connections) — `src/embed.py`

## Relationships

- [index.py](index.py.md) (1 shared connections)

## Source Files

- `src/embed.py`

## Audit Trail

- EXTRACTED: 15 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*