"""
Chat Indexer for ChatRecall
===========================
Builds, caches, and loads:
1. Dense semantic vector index (direct and contextual normalized matrices for dot-product search)
2. Inverted sender and chronological timestamp indices for ultra-fast filtering
3. BM25 keyword index for lexical comparison and hybrid retrieval.
"""

import os
import json
import re
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from rank_bm25 import BM25Okapi
from src.embed import MessageEmbedder

CHAT_DATA_PATH = "data/chat.json"
EMBEDDINGS_PATH = "data/embeddings.npy"
CONTEXT_EMBEDDINGS_PATH = "data/context_embeddings.npy"


class ChatIndex:
    def __init__(
        self,
        messages: List[Dict[str, Any]],
        embeddings: np.ndarray,
        context_embeddings: Optional[np.ndarray] = None,
        embedder: Optional[MessageEmbedder] = None
    ):
        self.messages = messages
        self.embeddings = embeddings  # (N, D) normalized float32
        self.context_embeddings = context_embeddings if context_embeddings is not None else embeddings
        self.embedder = embedder or MessageEmbedder()
        self.id_to_idx: Dict[str, int] = {str(m["id"]): i for i, m in enumerate(messages)}

        # Build sender inverted index (lowercase sender & aliases)
        self.sender_index: Dict[str, List[int]] = {}
        # Pre-parse timestamps for fast date range filtering
        self.timestamps: List[datetime] = []

        # Tokenized corpus for BM25
        tokenized_corpus = []

        for idx, msg in enumerate(messages):
            sender_lower = msg["sender"].lower().strip()
            self.sender_index.setdefault(sender_lower, []).append(idx)

            # Map first name / aliases
            first_name = sender_lower.split()[0]
            if first_name not in self.sender_index:
                self.sender_index[first_name] = self.sender_index[sender_lower]

            try:
                dt = datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S")
            except Exception:
                dt = datetime.now()
            self.timestamps.append(dt)

            tokens = re.findall(r"\b\w+\b", f"{msg['sender']} {msg['message']}".lower())
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
            messages = parse_chat_txt(chat_path)
            base_name = os.path.splitext(os.path.basename(chat_path))[0]
            embeddings_path = f"data/{base_name}_embeddings.npy"
            ctx_embeddings_path = f"data/{base_name}_context_embeddings.npy"
        else:
            with open(chat_path, "r", encoding="utf-8") as f:
                messages = json.load(f)
            ctx_embeddings_path = CONTEXT_EMBEDDINGS_PATH

        embedder = MessageEmbedder()

        # Build / load direct embeddings
        if os.path.exists(embeddings_path) and not force_rebuild:
            embeddings = np.load(embeddings_path)
            if len(embeddings) != len(messages):
                embeddings = embedder.encode_messages(messages, use_context=False)
                np.save(embeddings_path, embeddings)
        else:
            embeddings = embedder.encode_messages(messages, use_context=False)
            os.makedirs(os.path.dirname(embeddings_path), exist_ok=True)
            np.save(embeddings_path, embeddings)

        # Build / load contextual embeddings
        if os.path.exists(ctx_embeddings_path) and not force_rebuild:
            context_embeddings = np.load(ctx_embeddings_path)
            if len(context_embeddings) != len(messages):
                context_embeddings = embedder.encode_messages(messages, use_context=True)
                np.save(ctx_embeddings_path, context_embeddings)
        else:
            context_embeddings = embedder.encode_messages(messages, use_context=True)
            os.makedirs(os.path.dirname(ctx_embeddings_path), exist_ok=True)
            np.save(ctx_embeddings_path, context_embeddings)

        return cls(
            messages=messages,
            embeddings=embeddings,
            context_embeddings=context_embeddings,
            embedder=embedder
        )

    def dense_search(
        self,
        query_vector: np.ndarray,
        context_query_vector: Optional[np.ndarray] = None,
        candidate_indices: Optional[List[int]] = None,
        top_k: int = 10
    ) -> List[Tuple[int, float, float]]:
        """
        Performs blended cosine similarity search against candidates or the entire corpus.
        Returns list of (msg_idx, blended_score, raw_direct_sim).
        """
        if context_query_vector is None:
            context_query_vector = query_vector

        if candidate_indices is not None:
            if not candidate_indices:
                return []
            sub_emb = self.embeddings[candidate_indices]
            sub_ctx = self.context_embeddings[candidate_indices]
            direct_scores = np.dot(sub_emb, query_vector)
            ctx_scores = np.dot(sub_ctx, context_query_vector)

            blended = 0.45 * direct_scores + 0.55 * ctx_scores
            top_local = np.argsort(-blended)[:top_k]
            return [(candidate_indices[i], float(blended[i]), float(direct_scores[i])) for i in top_local]
        else:
            direct_scores = np.dot(self.embeddings, query_vector)
            ctx_scores = np.dot(self.context_embeddings, context_query_vector)
            blended = 0.45 * direct_scores + 0.55 * ctx_scores
            top_indices = np.argsort(-blended)[:top_k]
            return [(int(i), float(blended[i]), float(direct_scores[i])) for i in top_indices]

    def lexical_search(
        self,
        query: str,
        candidate_indices: Optional[List[int]] = None,
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Performs BM25 keyword search.
        """
        tokens = re.findall(r"\b\w+\b", query.lower())
        raw_scores = self.bm25.get_scores(tokens)
        if candidate_indices is not None:
            candidate_set = set(candidate_indices)
            filtered_scores = [(idx, float(raw_scores[idx])) for idx in candidate_set]
            filtered_scores.sort(key=lambda x: -x[1])
            return filtered_scores[:top_k]
        else:
            top_indices = np.argsort(-raw_scores)[:top_k]
            return [(int(i), float(raw_scores[i])) for i in top_indices]
