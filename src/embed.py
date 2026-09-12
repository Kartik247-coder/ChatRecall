"""
Embedding Pipeline for ChatRecall
=================================
Provides multilingual, Hinglish-aware embedding generation with contextual message
enrichment (sender prepending, decision metadata, and normalized vector representations).
"""

from typing import List, Dict, Any, Union
import numpy as np
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
        Formats a chat message with rich contextual metadata before vector encoding.
        Prepends sender name and marks decision resolutions to assist semantic matching.
        """
        sender = msg.get("sender", "")
        text = msg.get("message", "")
        is_decision = msg.get("is_decision", False)

        if is_decision:
            return f"[{sender} - Decision]: {text}"
        return f"{sender}: {text}"

    def encode_query(self, query: str) -> np.ndarray:
        """
        Encodes a single natural language search query into a normalized vector.
        """
        vec = self.model.encode(query.strip(), normalize_embeddings=True, convert_to_numpy=True)
        return vec.astype(np.float32)

    def encode_messages(self, messages: List[Dict[str, Any]], batch_size: int = 64) -> np.ndarray:
        """
        Encodes a list of chat message dictionaries into an (N, D) normalized numpy array.
        """
        texts = [self.format_message_for_embedding(m) for m in messages]
        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return vectors.astype(np.float32)
