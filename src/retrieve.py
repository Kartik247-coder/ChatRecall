"""
Multi-Strategy Query Router & Retrieval Engine for ChatRecall
============================================================
Handles the 3 core query shapes:
1. Semantic / Meaning-based (with Decision-Resolution awareness)
2. Person-based (Author entity extraction & sender filtering)
3. Time-based (Relative and absolute date parsing relative to archive window)
"""

import re
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from src.index import ChatIndex

ARCHIVE_START = datetime(2023, 10, 1, 0, 0, 0)
ARCHIVE_END = datetime(2024, 3, 31, 23, 59, 59)
ARCHIVE_REFERENCE_NOW = datetime(2024, 3, 31, 23, 59, 59)

PERSONA_ALIASES = {
    "rohan": "Rohan Mehta",
    "priya": "Priya Sharma",
    "kabir": "Kabir Sen",
    "ananya": "Ananya Iyer",
    "vikram": "Vikram Malhotra",
    "neha": "Neha Gupta",
    "sid": "Siddharth Verma",
    "siddharth": "Siddharth Verma",
    "tanvi": "Tanvi Desai",
}

DECISION_KEYWORDS = [
    "decide", "decided", "decision", "final", "finalize", "finalized", "lock",
    "locked", "agree", "agreed", "agreement", "settle", "settled", "resolution",
    "outcome", "conclude", "fixed", "fix", "chalo", "booked"
]

MONTH_MAP = {
    "october": (datetime(2023, 10, 1), datetime(2023, 10, 31, 23, 59, 59)),
    "nov": (datetime(2023, 11, 1), datetime(2023, 11, 30, 23, 59, 59)),
    "november": (datetime(2023, 11, 1), datetime(2023, 11, 30, 23, 59, 59)),
    "dec": (datetime(2023, 12, 1), datetime(2023, 12, 31, 23, 59, 59)),
    "december": (datetime(2023, 12, 1), datetime(2023, 12, 31, 23, 59, 59)),
    "jan": (datetime(2024, 1, 1), datetime(2024, 1, 31, 23, 59, 59)),
    "january": (datetime(2024, 1, 1), datetime(2024, 1, 31, 23, 59, 59)),
    "feb": (datetime(2024, 2, 1), datetime(2024, 2, 29, 23, 59, 59)),
    "february": (datetime(2024, 2, 1), datetime(2024, 2, 29, 23, 59, 59)),
    "mar": (datetime(2024, 3, 1), datetime(2024, 3, 31, 23, 59, 59)),
    "march": (datetime(2024, 3, 1), datetime(2024, 3, 31, 23, 59, 59)),
}


class StrategyType(str, Enum):
    SEMANTIC = "semantic"
    PERSON = "person_filtered"
    TIME = "time_filtered"
    HYBRID = "hybrid"


class QueryPlan:
    def __init__(
        self,
        raw_query: str,
        strategy: StrategyType,
        target_person: Optional[str] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        is_decision_query: bool = False,
        clean_query: Optional[str] = None
    ):
        self.raw_query = raw_query
        self.strategy = strategy
        self.target_person = target_person
        self.time_range = time_range
        self.is_decision_query = is_decision_query
        self.clean_query = clean_query or raw_query

    def __repr__(self):
        return (
            f"QueryPlan(strategy={self.strategy}, person={self.target_person}, "
            f"time_range={self.time_range}, decision={self.is_decision_query})"
        )


class QueryRouter:
    @staticmethod
    def analyze(query: str) -> QueryPlan:
        q_lower = query.lower()
        words = set(re.findall(r"\b\w+[\w']*\b", q_lower))

        # 1. Detect Decision Intent
        is_decision = any(dk in words for dk in DECISION_KEYWORDS)

        # 2. Detect Person mention — distinguish between SENDER (author) vs SUBJECT ("for Siddharth")
        detected_person = None
        is_subject_only = bool(re.search(r"\b(for|about|surprise|gift)\s+(siddharth|sid|priya|rohan|ananya|vikram|neha|tanvi|kabir)\b", q_lower))

        if not is_subject_only:
            for alias, full_name in PERSONA_ALIASES.items():
                # Matches "priya said", "priya's", "did priya", "what did priya", "priya message", "priya advice"
                pattern = rf"\b({alias}'s|{alias}\s+said|did\s+{alias}|what\s+did\s+{alias}|from\s+{alias}|{alias}\s+mention|{alias}\s+share|{alias}\s+tell|{alias}\s+advice|{alias}\s+message|{alias}\s+report|{alias}\s+cab)\b"
                if re.search(pattern, q_lower):
                    detected_person = full_name
                    break

        # 3. Detect Temporal Constraints
        time_range = None
        
        for m_name, (start_dt, end_dt) in MONTH_MAP.items():
            if re.search(rf"\b{re.escape(m_name)}\b", q_lower):
                time_range = (start_dt, end_dt)
                break

        if not time_range:
            if "last month" in q_lower or "previous month" in q_lower:
                time_range = (datetime(2024, 2, 1), datetime(2024, 2, 29, 23, 59, 59))
            elif "diwali" in q_lower:
                time_range = (datetime(2023, 11, 1), datetime(2023, 11, 20, 23, 59, 59))
            elif "new year" in q_lower or "new years" in q_lower:
                time_range = (datetime(2023, 12, 20), datetime(2024, 1, 10, 23, 59, 59))
            elif "beginning of the year" in q_lower or "early this year" in q_lower:
                time_range = (datetime(2024, 1, 1), datetime(2024, 1, 31, 23, 59, 59))
            elif "late last year" in q_lower or "end of last year" in q_lower:
                time_range = (datetime(2023, 11, 1), datetime(2023, 12, 31, 23, 59, 59))

        # 4. Decide strategy
        if detected_person and time_range:
            strategy = StrategyType.HYBRID
        elif detected_person:
            strategy = StrategyType.PERSON
        elif time_range:
            strategy = StrategyType.TIME
        else:
            strategy = StrategyType.SEMANTIC

        # Clean query for embedding
        clean_q = query
        if detected_person:
            clean_q = re.sub(r"(?i)\b(what did|did|what does|has)\s+\w+('s)?\s+(say|said|tell|mention|recommend|ask|share|report)\s+(about)?", "", query).strip()
            if not clean_q or len(clean_q.split()) < 2:
                clean_q = query

        return QueryPlan(
            raw_query=query,
            strategy=strategy,
            target_person=detected_person,
            time_range=time_range,
            is_decision_query=is_decision,
            clean_query=clean_q
        )


class RetrievalEngine:
    def __init__(self, index: ChatIndex):
        self.index = index
        self.router = QueryRouter()

    def search(
        self,
        query: str,
        top_k: int = 5,
        decision_boost: float = 0.35
    ) -> Dict[str, Any]:
        """
        Executes query through the router and multi-strategy retrieval pipeline.
        """
        plan = self.router.analyze(query)
        candidates: Optional[List[int]] = None

        # Apply Person Filter
        if plan.target_person:
            p_lower = plan.target_person.lower()
            candidates = self.index.sender_index.get(p_lower, [])

        # Apply Time Filter
        if plan.time_range:
            start_dt, end_dt = plan.time_range
            time_candidates = [
                idx for idx, dt in enumerate(self.index.timestamps)
                if start_dt <= dt <= end_dt
            ]
            if candidates is not None:
                time_set = set(time_candidates)
                candidates = [idx for idx in candidates if idx in time_set]
            else:
                candidates = time_candidates

        # Encode query
        q_vec = self.index.embedder.encode_query(plan.clean_query)

        # Dense similarity search
        raw_results = self.index.dense_search(
            query_vector=q_vec,
            candidate_indices=candidates,
            top_k=min(100, len(self.index.messages) if candidates is None else len(candidates))
        )

        # Re-ranking
        scored_results = []
        for msg_idx, base_sim in raw_results:
            msg = self.index.messages[msg_idx]
            final_score = base_sim

            # Decision boost
            if plan.is_decision_query and msg.get("is_decision", False):
                final_score += decision_boost

            # Penalize media omitted and bare 1-word replies
            if msg.get("media_omitted", False):
                final_score -= 0.20
            elif len(msg.get("message", "").split()) <= 1 and not msg.get("is_decision", False):
                final_score -= 0.15

            scored_results.append((msg_idx, final_score, base_sim))

        scored_results.sort(key=lambda x: -x[1])
        top_matches = scored_results[:top_k]

        results = []
        for rank, (idx, final_score, base_sim) in enumerate(top_matches, start=1):
            msg = self.index.messages[idx]
            results.append({
                "rank": rank,
                "msg_idx": idx,
                "id": msg["id"],
                "sender": msg["sender"],
                "timestamp": msg["timestamp"],
                "message": msg["message"],
                "is_decision": msg.get("is_decision", False),
                "thread_id": msg.get("thread_id"),
                "score": round(final_score, 4),
                "raw_similarity": round(base_sim, 4),
            })

        return {
            "query": query,
            "plan": {
                "strategy": plan.strategy.value,
                "target_person": plan.target_person,
                "time_range": [dt.strftime("%Y-%m-%d") for dt in plan.time_range] if plan.time_range else None,
                "is_decision_query": plan.is_decision_query,
                "clean_query": plan.clean_query
            },
            "candidate_count": len(candidates) if candidates is not None else len(self.index.messages),
            "results": results
        }
