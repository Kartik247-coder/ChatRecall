"""
Hinglish and Zero-Word-Overlap Embedding Validation Tests
=========================================================
Validates that the selected multilingual embedding model captures semantic
equivalence between English queries and code-mixed/Hinglish chat messages
even when they share zero common words.
"""

import pytest
import numpy as np
from sentence_transformers import SentenceTransformer


# Multilingual MiniLM provides strong cross-lingual alignment and fast local inference
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


@pytest.fixture(scope="module")
def embedder():
    return SentenceTransformer(MODEL_NAME)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def test_hinglish_zero_word_overlap_pairs(embedder):
    """
    Test suite of English queries vs Hinglish messages with ZERO word overlap.
    Semantic similarity between query and positive target MUST be significantly
    higher than similarity with negative distractors (margin >= 0.20).
    """
    test_cases = [
        {
            "query": "When did we decide on the mountain holiday?",
            "target": "Chalo sab lock ho gaya: Manali trip finalized for Dec 28 to Jan 2! Booked the riverside cottage in Old Manali, ticket confirmation emailed to all.",
            "distractor": "Fastag recharged with 1000 for highway toll booth passing.",
            "min_sim": 0.25,
            "min_margin": 0.20,
        },
        {
            "query": "What is the penalty for skipping exercise streak?",
            "target": "Priya's rule: whoever misses workout 3 days in a row pays for weekend breakfast!",
            "distractor": "Air quality index is 180 today, wear N95 mask outside.",
            "min_sim": 0.35,
            "min_margin": 0.20,
        },
        {
            "query": "Surprise reading gadget ordered for our friend moving abroad",
            "target": "Purchased the Kindle Paperwhite 32GB with green leather cover on Amazon, and table booked at Toit Indiranagar this Friday at 8:30 PM.",
            "distractor": "Splitwise balance settled for electricity and broadband bill.",
            "min_sim": 0.35,
            "min_margin": 0.20,
        },
        {
            "query": "What was the final negotiated house security amount?",
            "target": "Agreement signed! 3BHK in Koramangala 4th block locked at 48k monthly rent with 2 lakh security deposit split equally between the four of us.",
            "distractor": "Zomato gold 50% discount coupon code working on Meghana Biryani right now!",
            "min_sim": 0.35,
            "min_margin": 0.20,
        },
        {
            "query": "Who is commuting to the tech corridor by vehicle?",
            "target": "Anyone commuting towards Electronic City phase 1 today? Driving via elevated toll road.",
            "distractor": "night shift emergency casualty duty finished, sleeping now do not call.",
            "min_sim": 0.35,
            "min_margin": 0.20,
        },
    ]

    for tc in test_cases:
        q_emb = embedder.encode(tc["query"], normalize_embeddings=True)
        t_emb = embedder.encode(tc["target"], normalize_embeddings=True)
        d_emb = embedder.encode(tc["distractor"], normalize_embeddings=True)

        sim_target = cosine_similarity(q_emb, t_emb)
        sim_distractor = cosine_similarity(q_emb, d_emb)
        margin = sim_target - sim_distractor

        assert sim_target >= tc["min_sim"], (
            f"Query: '{tc['query']}' -> Target: '{tc['target']}' had similarity {sim_target:.3f} < {tc['min_sim']}"
        )
        assert margin >= tc["min_margin"], (
            f"Target similarity ({sim_target:.3f}) margin over distractor ({sim_distractor:.3f}) was {margin:.3f} < {tc['min_margin']}"
        )
