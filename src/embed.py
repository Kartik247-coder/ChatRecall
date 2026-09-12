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
        Includes dialogue context (preceding and forward messages in the conversation cluster)
        to empower zero-word-overlap reply matching and factual answer targeting.
        """
        if not messages:
            return []

        context_texts = ["" for _ in range(len(messages))]
        n = len(messages)

        for i, m in enumerate(messages):
            sender = m.get("sender", "")
            text = m.get("message", "").strip()

            # Preceding dialogue turns (up to 3 non-media messages)
            prev_turns = []
            for p_idx in range(max(0, i - 3), i):
                pm = messages[p_idx]
                if not pm.get("media_omitted", False) and "<media omitted>" not in pm.get("message", "").lower():
                    prev_turns.append(f"{pm['sender']}: {pm['message']}")

            # Forward dialogue turns (up to 2 non-media messages for outcome context)
            fol_turns = []
            for f_idx in range(i + 1, min(n, i + 3)):
                fm = messages[f_idx]
                if not fm.get("media_omitted", False) and "<media omitted>" not in fm.get("message", "").lower():
                    fol_turns.append(f"{fm['sender']}: {fm['message']}")

            prev_context = " | ".join(prev_turns)
            fol_context = " | ".join(fol_turns)

            if prev_context and fol_context:
                c_text = f"In conversation [{prev_context}] -> {sender}: {text} (Next: {fol_context})"
            elif prev_context:
                c_text = f"In conversation [{prev_context}] -> {sender}: {text}"
            elif fol_context:
                c_text = f"{sender}: {text} (Topic flow: {fol_context})"
            else:
                c_text = f"{sender}: {text}"

            context_texts[i] = c_text

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
