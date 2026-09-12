"""
Embedding Pipeline for ChatRecall
=================================
Provides multilingual, Hinglish-aware embedding generation with contextual dialogue
enrichment and normalized vector representations.
"""

from typing import List, Dict, Any, Union, Optional
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

# Validated multilingual model for zero-word-overlap Hinglish semantic transfer
DEFAULT_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class MessageEmbedder:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME, device: str = None):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=device)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def format_message_for_embedding(self, msg: Dict[str, Any]) -> str:
        """
        Formats a chat message for vector encoding.
        Prepends sender name and clean text for accurate semantic matching.
        """
        sender = msg.get("sender", "")
        text = msg.get("message", "").strip()
        return f"{sender}: {text}" if sender else text

    def build_contextual_texts(self, messages: List[Dict[str, Any]]) -> List[str]:
        """
        Builds thread-aware contextual texts for conversation messages.
        Includes dialogue context (preceding messages in the same conversation cluster)
        to empower zero-word-overlap reply matching (e.g. 'booked' matching 'did we book a bonfire night').
        """
        if not messages:
            return []

        # Group messages by temporal cluster (< 1 hour gap)
        threads = []
        curr_thread = [0]
        for i in range(1, len(messages)):
            try:
                t_curr = datetime.strptime(messages[i]["timestamp"], "%Y-%m-%d %H:%M:%S")
                t_prev = datetime.strptime(messages[i-1]["timestamp"], "%Y-%m-%d %H:%M:%S")
                if (t_curr - t_prev).total_seconds() > 3600:
                    threads.append(curr_thread)
                    curr_thread = [i]
                else:
                    curr_thread.append(i)
            except Exception:
                curr_thread.append(i)
        threads.append(curr_thread)

        context_texts = ["" for _ in range(len(messages))]
        for t_idx_list in threads:
            t_msgs = [messages[k] for k in t_idx_list if not messages[k].get("media_omitted", False)]
            t_full = " | ".join([f"{m['sender']}: {m['message']}" for m in t_msgs])
            for k in t_idx_list:
                m = messages[k]
                k_pos = t_idx_list.index(k)
                prev_sub = t_idx_list[max(0, k_pos-2):k_pos]
                prev_context = " | ".join([f"{messages[p]['sender']}: {messages[p]['message']}" for p in prev_sub])
                if prev_context:
                    c_text = f"In reply to [{prev_context}] -> {m['sender']}: {m['message']}"
                else:
                    c_text = f"{m['sender']}: {m['message']} (Topic: {t_full[:150]})"
                context_texts[k] = c_text

        return context_texts

    def encode_query(self, query: str) -> np.ndarray:
        """
        Encodes a single natural language search query into a normalized vector.
        """
        vec = self.model.encode(query.strip(), normalize_embeddings=True, convert_to_numpy=True)
        return vec.astype(np.float32)

    def encode_messages(
        self,
        messages: List[Dict[str, Any]],
        batch_size: int = 64,
        use_context: bool = False
    ) -> np.ndarray:
        """
        Encodes a list of chat message dictionaries into an (N, D) normalized numpy array.
        """
        if use_context:
            texts = self.build_contextual_texts(messages)
        else:
            texts = [self.format_message_for_embedding(m) for m in messages]

        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return vectors.astype(np.float32)
