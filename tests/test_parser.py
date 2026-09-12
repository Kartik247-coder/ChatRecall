"""
Unit tests for Text Chat Parser (.txt export support)
"""

import os
import pytest
from src.parser import parse_chat_txt, parse_timestamp
from src.index import ChatIndex
from src.retrieve import RetrievalEngine


SAMPLE_TXT_CONTENT = """
12/10/23, 7:15 PM - Rohan Mehta: Where are we going for vacation?
12/10/23, 7:16 PM - Priya Sharma: Goa is too expensive right now.
12/10/23, 7:18 PM - Tanvi Desai: Chalo Manali cottage book karte hain!
12/10/23, 7:20 PM - Vikram Malhotra: Done, confirmed from my side.
"""


def test_txt_parser_and_search(tmp_path):
    txt_file = tmp_path / "sample_export.txt"
    txt_file.write_text(SAMPLE_TXT_CONTENT.strip(), encoding="utf-8")

    messages = parse_chat_txt(str(txt_file))
    assert len(messages) == 4
    assert messages[0]["sender"] == "Rohan Mehta"
    assert messages[2]["sender"] == "Tanvi Desai"
    assert "Manali" in messages[2]["message"]

    # Test indexing directly from .txt
    index = ChatIndex.build_or_load(chat_path=str(txt_file))
    assert len(index.messages) == 4

    engine = RetrievalEngine(index)
    res = engine.search("What did Tanvi say about the cottage?", top_k=1)
    assert len(res["results"]) > 0
    assert res["results"][0]["sender"] == "Tanvi Desai"
    assert "Manali" in res["results"][0]["message"]
