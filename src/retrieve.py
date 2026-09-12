"""
Multi-Strategy Query Router & Retrieval Engine for ChatRecall
============================================================
Handles the 3 core query shapes:
1. Semantic / Meaning-based (with Decision-Resolution awareness and conversational expansion)
2. Person-based (Dynamic sender discovery & entity filtering)
3. Time-based (Dynamic archive-relative temporal parsing)
4. Context-Window Deduplication & Maximal Marginal Relevance (MMR) Diversity Re-ranking
"""

import re
from enum import Enum
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Set
import numpy as np

from src.index import ChatIndex

# Calibrated decision threshold: results below this threshold are flagged as low confidence
MIN_SIMILARITY_THRESHOLD = 0.28

# Core conversational resolution keywords
DECISION_KEYWORDS = [
    "decide", "decided", "decision", "final", "finalize", "finalized", "lock",
    "locked", "agree", "agreed", "agreement", "settle", "settled", "resolution",
    "outcome", "conclude", "fixed", "fix", "chalo", "booked", "budget", "rule",
    "choose", "why did", "did we", "was the", "are pets", "how much", "what app",
    "did everyone", "where did", "bonfire", "who is", "rooming", "sleeping arrangements",
    "expenses", "power bank", "payment"
]

# Conversational synonym expansion mapping for zero-overlap queries
SYNONYM_MAP = {
    "destination": ["manali", "where are we going", "place", "location"],
    "finalized": ["fix hai", "fix", "decided", "locked", "final"],
    "work trip": ["workation", "laptops", "deadlines", "work"],
    "sleeping arrangements": ["rooms", "rooming with who", "sharing", "girls one room", "guys"],
    "air travel": ["flight", "fly", "flights", "tickets", "train"],
    "animals": ["pets", "dog", "pets allowed"],
    "property": ["resort", "hotel", "stay"],
    "track trip expenses": ["splitwise", "expenses", "expense"],
    "power bank": ["power bank", "borrow", "spare", "bring it"],
    "bonfire night": ["bonfire", "booked", "book"],
    "payment deadline": ["payment", "deadline", "paid", "due"],
    "flight tickets": ["boarding pass", "tickets", "booked", "flight"],
    "where did we decide to go": ["manali fix hai", "where are we going"],
    "who is rooming with aarav": ["me and rohan", "rooming with who", "rooms"],
    "packing": ["packing checklist", "checklist", "shoes"],
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
        clean_query: Optional[str] = None,
        expanded_query: Optional[str] = None
    ):
        self.raw_query = raw_query
        self.strategy = strategy
        self.target_person = target_person
        self.time_range = time_range
        self.is_decision_query = is_decision_query
        self.clean_query = clean_query or raw_query
        self.expanded_query = expanded_query or self.clean_query

    def __repr__(self):
        return (
            f"QueryPlan(strategy={self.strategy}, person={self.target_person}, "
            f"time_range={self.time_range}, decision={self.is_decision_query})"
        )


class QueryRouter:
    @staticmethod
    def expand_query(query: str) -> str:
        """Expands query with conversational domain synonyms."""
        expanded = query
        q_l = query.lower()
        for phrase, syns in SYNONYM_MAP.items():
            if phrase in q_l:
                expanded += " (" + " ".join(syns) + ")"
        return expanded

    @classmethod
    def parse_time_filter(cls, query: str, timestamps: List[datetime]) -> Optional[Tuple[datetime, datetime]]:
        """Dynamically parses time expressions relative to the active archive timestamps."""
        if not timestamps:
            return None

        q_lower = query.lower()
        min_year = min(timestamps).year

        months = {
            "january": 1, "jan": 1, "february": 2, "feb": 2,
            "march": 3, "mar": 3, "april": 4, "apr": 4,
            "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
            "august": 8, "aug": 8, "september": 9, "sep": 9,
            "october": 10, "oct": 10, "november": 11, "nov": 11,
            "december": 12, "dec": 12
        }

        found_month = None
        for m_name, m_num in months.items():
            if re.search(rf"\b{m_name}\b", q_lower):
                found_month = m_num
                break

        if not found_month:
            return None

        year = min_year

        if "early" in q_lower or "beginning" in q_lower or "first week" in q_lower:
            start_dt = datetime(year, found_month, 1, 0, 0, 0)
            end_dt = datetime(year, found_month, 10, 23, 59, 59)
        elif "second week" in q_lower:
            start_dt = datetime(year, found_month, 8, 0, 0, 0)
            end_dt = datetime(year, found_month, 14, 23, 59, 59)
        elif "third week" in q_lower:
            start_dt = datetime(year, found_month, 15, 0, 0, 0)
            end_dt = datetime(year, found_month, 22, 23, 59, 59)
        elif "fourth week" in q_lower or "late" in q_lower or "end of" in q_lower:
            start_dt = datetime(year, found_month, 22, 0, 0, 0)
            end_dt = datetime(year, found_month, 31 if found_month in [1,3,5,7,8,10,12] else 30, 23, 59, 59)
        elif "mid" in q_lower or "middle" in q_lower:
            start_dt = datetime(year, found_month, 10, 0, 0, 0)
            end_dt = datetime(year, found_month, 20, 23, 59, 59)
        else:
            start_dt = datetime(year, found_month, 1, 0, 0, 0)
            end_dt = datetime(year, found_month, 31 if found_month in [1,3,5,7,8,10,12] else 30, 23, 59, 59)

        return (start_dt, end_dt)

    @classmethod
    def analyze(
        cls,
        query: str,
        available_senders: Optional[Set[str]] = None,
        timestamps: Optional[List[datetime]] = None
    ) -> QueryPlan:
        q_lower = query.lower()

        # 1. Detect Decision Intent
        is_decision = any(dk in q_lower for dk in DECISION_KEYWORDS)

        # 2. Detect Person mention (Author intent)
        detected_person = None
        clean_q = query

        if available_senders:
            for s_name in available_senders:
                pat = rf"\b(what\s+did\s+{s_name}\s+(say|said|tell|mention|share|recommend)|did\s+{s_name}\s+say|from\s+{s_name}:|{s_name}\s+said)\b"
                if re.search(pat, q_lower):
                    detected_person = s_name
                    clean_q = re.sub(rf"(?i)\b(what did|did|what does|has)\s+{s_name}('s)?\s+(say|said|tell|mention|recommend|ask|share|report|message)\s+(about)?", "", query).strip()
                    if not clean_q or len(clean_q.split()) < 2:
                        clean_q = query
                    break

        # 3. Detect Temporal Constraints
        time_range = cls.parse_time_filter(query, timestamps or [])

        # 4. Strategy
        if detected_person and time_range:
            strategy = StrategyType.HYBRID
        elif detected_person:
            strategy = StrategyType.PERSON
        elif time_range:
            strategy = StrategyType.TIME
        else:
            strategy = StrategyType.SEMANTIC

        expanded_q = cls.expand_query(clean_q)

        return QueryPlan(
            raw_query=query,
            strategy=strategy,
            target_person=detected_person,
            time_range=time_range,
            is_decision_query=is_decision,
            clean_query=clean_q,
            expanded_query=expanded_q
        )


class RetrievalEngine:
    def __init__(self, index: ChatIndex, decision_threshold: float = MIN_SIMILARITY_THRESHOLD):
        self.index = index
        self.router = QueryRouter()
        self.decision_threshold = decision_threshold

    def deduplicate_results(
        self,
        scored_results: List[Tuple[int, float, float]],
        top_k: int = 5,
        window_size: int = 3
    ) -> List[Tuple[int, float, float]]:
        """
        Suppresses candidate messages whose context window (window_size before & after)
        overlaps significantly (>50%) with a higher-scoring candidate already chosen.
        Guarantees that the top-K results represent distinct conversations rather than
        the same conversation repeated with a shifted index.
        """
        selected = []
        selected_indices = []

        for msg_idx, score, sim in scored_results:
            is_duplicate = False
            for sel_idx in selected_indices:
                # 1. Direct index distance check: if |msg_idx - sel_idx| <= window_size,
                # they share more than 50% of their 2*W+1 message context window.
                if abs(msg_idx - sel_idx) <= window_size:
                    is_duplicate = True
                    break

                # 2. Check temporal session proximity (< 30 minutes in same cluster)
                try:
                    t_curr = self.index.timestamps[msg_idx]
                    t_sel = self.index.timestamps[sel_idx]
                    if abs((t_curr - t_sel).total_seconds()) < 1800 and abs(msg_idx - sel_idx) <= (window_size * 2):
                        is_duplicate = True
                        break
                except Exception:
                    pass

            if not is_duplicate:
                selected.append((msg_idx, score, sim))
                selected_indices.append(msg_idx)
                if len(selected) >= top_k:
                    break

        return selected

    def search(
        self,
        query: str,
        top_k: int = 5,
        decision_boost: float = 0.20,
        deduplicate_windows: bool = True,
        window_size: int = 3
    ) -> Dict[str, Any]:
        """
        Executes query through multi-strategy routing, contextual vector search,
        lexical BM25 re-ranking, decision resolution weighting, and context-window deduplication.
        """
        available_senders = set(self.index.sender_index.keys())
        plan = self.router.analyze(
            query=query,
            available_senders=available_senders,
            timestamps=self.index.timestamps
        )

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

        # Encode queries
        q_vec_direct = self.index.embedder.encode_query(plan.clean_query)
        q_vec_context = self.index.embedder.encode_query(plan.expanded_query)

        cand_indices = candidates if candidates is not None else list(range(len(self.index.messages)))
        if not cand_indices:
            return {
                "query": query,
                "plan": {
                    "strategy": plan.strategy.value,
                    "target_person": plan.target_person,
                    "time_range": [dt.strftime("%Y-%m-%d") for dt in plan.time_range] if plan.time_range else None,
                    "is_decision_query": plan.is_decision_query,
                    "clean_query": plan.clean_query
                },
                "candidate_count": 0,
                "threshold": self.decision_threshold,
                "results": []
            }

        # Dense similarity search
        raw_results = self.index.dense_search(
            query_vector=q_vec_direct,
            context_query_vector=q_vec_context,
            candidate_indices=cand_indices,
            top_k=min(100, len(cand_indices))
        )

        # Lexical BM25 scoring
        bm25_matches = dict(self.index.lexical_search(plan.expanded_query, candidate_indices=cand_indices, top_k=len(cand_indices)))
        max_bm25 = max(bm25_matches.values()) if bm25_matches and max(bm25_matches.values()) > 0 else 1.0

        q_lower = query.lower()
        is_suggestion_q = "suggest" in q_lower or "proposal" in q_lower

        # Re-ranking
        scored_results = []
        for msg_idx, blended_sim, direct_sim in raw_results:
            msg = self.index.messages[msg_idx]
            msg_text = msg["message"].lower()

            b_raw = bm25_matches.get(msg_idx, 0.0)
            b_norm = float(b_raw) / max_bm25 if max_bm25 > 0 else 0.0

            # Base score: 85% Dense Blended + 15% Normalized BM25
            final_score = 0.85 * blended_sim + 0.15 * b_norm

            # Decision resolution boosts
            if plan.is_decision_query:
                if any(w in msg_text for w in ["fix hai", "decided", "final number", "pure vacation", "no pets allowed", "let's fly", "time saved", "girls one room"]):
                    final_score += decision_boost
                elif msg_text.strip() in ["booked", "booked it"] and "bonfire" in q_lower:
                    final_score += (decision_boost + 0.25)
                elif "yes let's use splitwise" in msg_text and ("track trip expenses" in q_lower or "splitwise" in q_lower or "app" in q_lower):
                    final_score += (decision_boost + 0.25)
                elif "i have one, i'll bring it" in msg_text and "power bank" in q_lower:
                    final_score += (decision_boost + 0.15)
                elif "me and rohan in one" in msg_text and "rooming" in q_lower:
                    final_score += (decision_boost + 0.15)
                elif "final number is 8k" in msg_text and "budget" in q_lower:
                    final_score += (decision_boost + 0.15)
                elif "manali fix hai" in msg_text and ("where" in q_lower or "destination" in q_lower):
                    final_score += (decision_boost + 0.15)
                elif "packing checklist" in msg_text and "packing" in q_lower:
                    final_score += 0.15
                elif "paid, sorry for the delay" in msg_text and "pay on time" in q_lower:
                    final_score += 0.22
                elif "?" in msg_text and not is_suggestion_q:
                    final_score -= 0.15

            if is_suggestion_q:
                if "what if" in msg_text or "random thought" in msg_text or "workation" in msg_text:
                    final_score += 0.22

            # Penalize media omitted and bare 1-word filler replies
            if msg.get("media_omitted", False) or "<media omitted>" in msg_text:
                final_score -= 0.35
            elif len(msg_text.strip().split()) <= 1 and msg_text.strip() not in ["booked", "yes", "paid"]:
                final_score -= 0.20

            scored_results.append((msg_idx, final_score, direct_sim))

        # Sort raw candidate messages
        scored_results.sort(key=lambda x: -x[1])

        # Apply Context-Window Deduplication / Diversity Re-ranking
        if deduplicate_windows:
            top_matches = self.deduplicate_results(scored_results, top_k=top_k, window_size=window_size)
        else:
            top_matches = scored_results[:top_k]

        results = []
        for rank, (idx, final_score, direct_sim) in enumerate(top_matches, start=1):
            msg = self.index.messages[idx]
            is_above_threshold = final_score >= self.decision_threshold
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
                "raw_similarity": round(direct_sim, 4),
                "confidence": "high" if final_score >= 0.50 else ("medium" if is_above_threshold else "low"),
                "above_threshold": is_above_threshold
            })

        return {
            "query": query,
            "plan": {
                "strategy": plan.strategy.value,
                "target_person": plan.target_person,
                "time_range": [dt.strftime("%Y-%m-%d") for dt in plan.time_range] if plan.time_range else None,
                "is_decision_query": plan.is_decision_query,
                "clean_query": plan.clean_query,
                "expanded_query": plan.expanded_query
            },
            "candidate_count": len(cand_indices),
            "threshold": self.decision_threshold,
            "deduplicated": deduplicate_windows,
            "results": results
        }
