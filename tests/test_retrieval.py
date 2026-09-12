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
    # Checks that a Manali decision message is retrieved in top results
    manali_matches = [r for r in res["results"] if "Manali" in r["message"] or "manali" in r["message"]]
    assert len(manali_matches) > 0


def test_person_filtered_retrieval(engine):
    query = "What did Priya say about flight tickets"
    res = engine.search(query, top_k=5)
    
    assert len(res["results"]) > 0
    top1 = res["results"][0]
    assert "Priya" in top1["sender"]
