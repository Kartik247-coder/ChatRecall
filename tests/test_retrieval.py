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

    # Person query
    p_plan = router.analyze("What did Priya say about the budget?")
    assert p_plan.strategy == StrategyType.PERSON
    assert p_plan.target_person == "Priya Sharma"

    # Time query
    t_plan = router.analyze("What did we discuss in December?")
    assert t_plan.strategy == StrategyType.TIME
    assert t_plan.time_range is not None

    # Semantic decision query
    d_plan = router.analyze("When did we decide on the mountain trip?")
    assert d_plan.is_decision_query is True


def test_zero_word_overlap_decision_retrieval(engine):
    # Hard query with 0 word overlap
    query = "When did we decide on the mountain holiday?"
    res = engine.search(query, top_k=1)
    
    assert len(res["results"]) > 0
    top1 = res["results"][0]
    assert "Manali" in top1["message"]
    assert top1["is_decision"] is True


def test_person_filtered_retrieval(engine):
    query = "Priya's advice on buying flight tickets"
    res = engine.search(query, top_k=1)
    
    assert len(res["results"]) > 0
    top1 = res["results"][0]
    assert top1["sender"] == "Priya Sharma"
    assert "Tuesday" in top1["message"]
