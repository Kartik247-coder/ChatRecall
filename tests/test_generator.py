"""
Unit tests for Synthetic Chat Dataset Generator
"""

import os
import json
import pytest
from datetime import datetime
from data.generate_chat import generate_synthetic_chat, SEED, START_DATE, END_DATE


def test_generator_deterministic():
    """Ensure generator produces identical output for the same seed."""
    chat_a = generate_synthetic_chat()
    chat_b = generate_synthetic_chat()
    assert len(chat_a) == len(chat_b)
    assert chat_a[0] == chat_b[0]
    assert chat_a[100] == chat_b[100]
    assert chat_a[-1] == chat_b[-1]


def test_generator_volume_and_participants():
    """Ensure at least 4000 messages and exactly 8 participants."""
    messages = generate_synthetic_chat()
    assert len(messages) >= 4000, f"Expected >= 4000 messages, got {len(messages)}"
    
    senders = set(m["sender"] for m in messages)
    assert len(senders) == 8, f"Expected exactly 8 participants, got {len(senders)}: {senders}"
    
    expected_senders = {
        "Rohan Mehta", "Priya Sharma", "Kabir Sen", "Ananya Iyer",
        "Vikram Malhotra", "Neha Gupta", "Siddharth Verma", "Tanvi Desai"
    }
    assert senders == expected_senders


def test_generator_time_range_and_chronology():
    """Ensure messages span 6 months and are strictly chronological."""
    messages = generate_synthetic_chat()
    
    timestamps = [datetime.strptime(m["timestamp"], "%Y-%m-%d %H:%M:%S") for m in messages]
    assert timestamps[0] >= START_DATE
    assert timestamps[-1] <= END_DATE
    
    # Check date span is at least 175 days
    delta_days = (timestamps[-1].date() - timestamps[0].date()).days
    assert delta_days >= 175
    
    # Check chronological ordering
    for i in range(len(timestamps) - 1):
        assert timestamps[i] <= timestamps[i + 1], f"Out of order at index {i}"


def test_generator_decision_threads():
    """Ensure 3 long resolving threads exist and have marked decision messages."""
    messages = generate_synthetic_chat()
    decisions = [m for m in messages if m["is_decision"]]
    assert len(decisions) == 3, f"Expected 3 decision messages, got {len(decisions)}"
    
    decision_threads = set(d["thread_id"] for d in decisions)
    expected_threads = {"thread_year_end_trip", "thread_flat_lease", "thread_farewell_gift"}
    assert decision_threads == expected_threads


def test_generator_messiness_artifacts():
    """Ensure presence of media omitted, forwards, and short replies."""
    messages = generate_synthetic_chat()
    media_count = sum(1 for m in messages if m["media_omitted"])
    fwd_count = sum(1 for m in messages if m["is_forward"])
    one_word_count = sum(1 for m in messages if len(m["message"].split()) == 1)
    
    assert media_count > 100, f"Expected >100 media omitted, got {media_count}"
    assert fwd_count > 100, f"Expected >100 forwarded messages, got {fwd_count}"
    assert one_word_count > 200, f"Expected >200 one-word replies, got {one_word_count}"
