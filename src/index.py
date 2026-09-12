"""
Chat Indexer for ChatRecall
===========================
Builds, caches, and loads:
1. Dense semantic vector index (normalized numpy matrix for instantaneous dot-product search)
2. Inverted sender and chronological timestamp indices for ultra-fast filtering
3. BM25 keyword index for lexical comparison and hybrid retrieval.
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from rank_bm25 import BM25Okapi
from src.embed import MessageEmbedder

CHAT_DATA_PATH = "data/chat.json"
EMBEDDINGS_PATH = "data/embeddings.npy"
METADATA_INDEX_PATH = "data/index_meta.json"


class ChatIndex:
    def __init__(
        self,
        messages: List[Dict[str, Any]],
        embeddings: np.ndarray,
        embedder: Optional[MessageEmbedder] = None
    ):
        self.messages = messages
        self.embeddings = embeddings  # (N, D) normalized float32
        self.embedder = embedder or MessageEmbedder()
        self.id_to_idx: Dict[str, int] = {m["id"]: i for i, m in enumerate(messages)}
        
        # Build sender inverted index (lowercase sender & aliases)
        self.sender_index: Dict[str, List[int]] = {}
        # Pre-parse timestamps for fast date range filtering
        self.timestamps: List[datetime] = []

        # Tokenized corpus for BM25
        tokenized_corpus = []

        for idx, msg in enumerate(messages):
            sender_lower = msg["sender"].lower()
            self.sender_index.setdefault(sender_lower, []).append(idx)
            
            # Map first name / aliases
            first_name = sender_lower.split()[0]
            self.sender_index.setdefault(first_name, []).append(idx)
            
            dt = datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S")
            self.timestamps.append(dt)

            tokens = msg["message"].lower().split()
            tokenized_corpus.append(tokens)

        self.bm25 = BM25Okapi(tokenized_corpus)

    @classmethod
    def build_or_load(
        cls,
        chat_path: str = CHAT_DATA_PATH,
        embeddings_path: str = EMBEDDINGS_PATH,
        force_rebuild: bool = False
    ) -> "ChatIndex":
        """
        Loads chat data (from .json or .txt) and cached embeddings, or builds them if not present.
        """
        if not os.path.exists(chat_path):
            raise FileNotFoundError(f"Chat data file not found at {chat_path}.")

        # If user passed a .txt file, parse it using Text Chat Parser
        if chat_path.endswith(".txt"):
            from src.parser import parse_chat_txt
            print(f"Parsing raw text chat export from {chat_path}...")
            messages = parse_chat_txt(chat_path)
            # Custom embeddings file per text file
            base_name = os.path.splitext(os.path.basename(chat_path))[0]
            embeddings_path = f"data/{base_name}_embeddings.npy"
            force_rebuild = True
        else:
            with open(chat_path, "r", encoding="utf-8") as f:
                messages = json.load(f)

        embedder = MessageEmbedder()

        if os.path.exists(embeddings_path) and not force_rebuild:
            print(f"Loading cached vector embeddings from {embeddings_path}...")
            embeddings = np.load(embeddings_path)
            if len(embeddings) != len(messages):
                print("Warning: Cached embeddings count does not match messages. Rebuilding...")
                embeddings = embedder.encode_messages(messages)
                np.save(embeddings_path, embeddings)
        else:
            print(f"Building vector embeddings for {len(messages)} messages...")
            embeddings = embedder.encode_messages(messages)
            os.makedirs(os.path.dirname(embeddings_path), exist_ok=True)
            np.save(embeddings_path, embeddings)
            print(f"Saved embeddings to {embeddings_path}")

        return cls(messages=messages, embeddings=embeddings, embedder=embedder)

    def dense_search(
        self,
        query_vector: np.ndarray,
        candidate_indices: Optional[List[int]] = None,
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Performs cosine similarity search against candidates or the entire corpus.
        Returns list of (msg_idx, score).
        """
        if candidate_indices is not None:
            if not candidate_indices:
                return []
            sub_emb = self.embeddings[candidate_indices]
            scores = np.dot(sub_emb, query_vector)
            top_local = np.argsort(-scores)[:top_k]
            return [(candidate_indices[i], float(scores[i])) for i in top_local]
        else:
            scores = np.dot(self.embeddings, query_vector)
            top_indices = np.argsort(-scores)[:top_k]
            return [(int(i), float(scores[i])) for i in top_indices]

    def lexical_search(
        self,
        query: str,
        candidate_indices: Optional[List[int]] = None,
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Performs BM25 keyword search.
        """
        tokens = query.lower().split()
        raw_scores = self.bm25.get_scores(tokens)
        if candidate_indices is not None:
            candidate_set = set(candidate_indices)
            filtered_scores = [(idx, float(raw_scores[idx])) for idx in candidate_set]
            filtered_scores.sort(key=lambda x: -x[1])
            return filtered_scores[:top_k]
        else:
            top_indices = np.argsort(-raw_scores)[:top_k]
            return [(int(i), float(raw_scores[i])) for i in top_indices]


def main():
    print("Building / loading ChatRecall index...")
    index = ChatIndex.build_or_load()
    print(f"✓ Index ready with {len(index.messages)} messages and {index.embeddings.shape} embedding matrix.")


if __name__ == "__main__":
    main()
