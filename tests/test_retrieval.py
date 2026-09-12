"""
Unit tests for Retrieval Engine and Query Router
"""

import pytest
from src.index import ChatIndex
from src.retrieve import RetrievalEngine, QueryRouter, StrategyType


@pytest.fixture(scope="module")
def engine():
    index = ChatIndex.build_or_load()
    return RetrievalEngine(index)


def test_query_router_intent_classification():
    router = QueryRouter()

    # Person query with available senders
    senders = {"priya", "priya sharma", "rohan", "rohan mehta"}
    p_plan = router.analyze("What did Priya say about the budget?", available_senders=senders)
    assert p_plan.strategy == StrategyType.PERSON
    assert p_plan.target_person in ["priya", "priya sharma"]

    # Time query with timestamps
    from datetime import datetime
    dummy_ts = [datetime(2023, 12, 1), datetime(2024, 1, 15)]
    t_plan = router.analyze("What did we discuss in December?", timestamps=dummy_ts)
    assert t_plan.strategy == StrategyType.TIME
    assert t_plan.time_range is not None

    # Semantic decision query
    d_plan = router.analyze("When did we decide on the mountain trip?")
    assert d_plan.is_decision_query is True


def test_zero_word_overlap_decision_retrieval(engine):
    # Hard query with 0 word overlap
    query = "When did we decide on the mountain holiday?"
    res = engine.search(query, top_k=5)
    
    assert len(res["results"]) > 0
    manali_matches = [r for r in res["results"] if "Manali" in r["message"] or "manali" in r["message"]]
    assert len(manali_matches) > 0


def test_person_filtered_retrieval(engine):
    query = "What did Priya say about flight tickets"
    res = engine.search(query, top_k=5)
    
    assert len(res["results"]) > 0
    top1 = res["results"][0]
    assert "Priya" in top1["sender"]


def test_context_window_deduplication_regression(engine):
    """
    Regression test: Verifies that for any top-K results, no two results share
    more than 1 common message in their context window (i.e. |msg_idx_A - msg_idx_B| > window_size).
    """
    queries = [
        "Decision Resolution",
        "flight tickets and boarding pass",
        "budget and payment link",
        "what did we finally decide about making this a work trip"
    ]
    window_size = 3

    for q in queries:
        res = engine.search(q, top_k=5, deduplicate_windows=True, window_size=window_size)
        results = res["results"]
        assert len(results) > 0

        # Check pairwise distances between all returned result indices
        msg_indices = [r["msg_idx"] for r in results]
        for i in range(len(msg_indices)):
            for j in range(i + 1, len(msg_indices)):
                idx_a, idx_b = msg_indices[i], msg_indices[j]
                # If they are from the same conversation cluster, distance must be strictly > window_size
                assert abs(idx_a - idx_b) > window_size, (
                    f"Duplicate/overlapping window detected for query '{q}': "
                    f"result {i} (msg {idx_a}) and result {j} (msg {idx_b}) are within window size {window_size}!"
                )


def test_similarity_confidence_threshold(engine):
    """
    Verifies that results have confidence flags and low-scoring noise is accurately marked.
    """
    res = engine.search("completely unrelated query about quantum computing and astrophysics", top_k=5)
    assert "threshold" in res
    assert res["threshold"] == 0.28
    for r in res["results"]:
        assert "confidence" in r
        assert "above_threshold" in r
