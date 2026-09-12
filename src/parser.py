"""
Text Chat Parser for ChatRecall
===============================
Parses raw exported chat text files (.txt from WhatsApp, Telegram, or custom formats)
and structured .json files, converting them into normalized ChatRecall messages for
embedding, dense retrieval, and inverted indexing.
"""

import re
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Supported WhatsApp / Telegram / Export patterns
PATTERNS = [
    # 1. 12/10/23, 7:15 PM - Name: Message OR 12/10/2023, 19:15 - Name: Message
    r"^(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\s*[-–—]\s*([^:]+):\s*(.*)$",
    # 2. [12/10/23, 19:15:20] Name: Message OR [12/10/2023, 7:15:20 PM] Name: Message
    r"^\[(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\]\s*([^:]+):\s*(.*)$",
    # 3. 2023-10-12 19:15:00 - Name: Message OR 2023-10-12T19:15:00 - Name: Message
    r"^(\d{4}[/.-]\d{1,2}[/.-]\d{1,2})[T\s](\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\s*[-–—]?\s*([^:]+):\s*(.*)$",
    # 4. 12/10/23 19:15: Name: Message (no hyphen)
    r"^(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\s*:\s*([^:]+):\s*(.*)$",
]

# Common system notices in WhatsApp exports to skip if no author
SYSTEM_NOTICES = [
    "messages and calls are end-to-end encrypted",
    "messages to this chat and calls are secured",
    "created group",
    "changed the subject",
    "changed the group description",
    "added",
    "left",
    "removed",
    "joined using this group's invite link",
    "security code changed",
    "waiting for this message",
]


def clean_line_text(line: str) -> str:
    """Strips invisible Unicode control characters and normalizes whitespace/dashes."""
    # Strip left-to-right / right-to-left marks and BOM
    cleaned = (
        line.replace("\u200e", "")
        .replace("\u200f", "")
        .replace("\ufeff", "")
        .replace("\u202a", "")
        .replace("\u202b", "")
        .replace("\u202c", "")
        .replace("\u202d", "")
        .replace("\u202e", "")
        .replace("\u202f", " ")
        .replace("\xa0", " ")
    )
    return cleaned.strip()


def parse_timestamp(date_str: str, time_str: str) -> str:
    """Attempts multiple datetime formats and normalizes to YYYY-MM-DD HH:MM:SS."""
    d_norm = date_str.strip().replace("-", "/").replace(".", "/")
    t_norm = time_str.strip()
    
    # Normalize 2-digit vs 4-digit parts
    combined = f"{d_norm} {t_norm}"
    formats = [
        "%d/%m/%y %I:%M %p",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%y %I:%M:%S %p",
        "%d/%m/%Y %I:%M:%S %p",
        "%d/%m/%y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%y %H:%M",
        "%d/%m/%Y %H:%M",
        "%m/%d/%y %I:%M %p",
        "%m/%d/%Y %I:%M %p",
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %I:%M %p",
        "%Y/%m/%d %I:%M:%S %p",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(combined, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    # Fallback to current timestamp
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_chat_content(content: str) -> List[Dict[str, Any]]:
    """
    Parses raw text content into structured ChatRecall messages.
    """
    lines = content.splitlines()
    messages: List[Dict[str, Any]] = []
    msg_counter = 1
    current_msg: Optional[Dict[str, Any]] = None

    for line in lines:
        line_clean = clean_line_text(line)
        if not line_clean:
            continue

        matched = False
        for pat in PATTERNS:
            m = re.match(pat, line_clean)
            if m:
                d_str, t_str, sender, text = m.groups()
                sender = sender.strip()
                text = text.strip()

                # Check if it's a known system message
                if any(notice in line_clean.lower() for notice in SYSTEM_NOTICES) and ":" not in text:
                    matched = True
                    break

                ts = parse_timestamp(d_str, t_str)
                is_media = "<media omitted>" in text.lower() or "image omitted" in text.lower() or "video omitted" in text.lower()
                is_fwd = "[forwarded" in text.lower() or "forwarded:" in text.lower()

                current_msg = {
                    "id": f"MSG_{msg_counter:05d}",
                    "timestamp": ts,
                    "sender": sender,
                    "message": text,
                    "reply_to_id": None,
                    "thread_id": None,
                    "is_decision": False,
                    "is_forward": is_fwd,
                    "media_omitted": is_media,
                }
                messages.append(current_msg)
                msg_counter += 1
                matched = True
                break

        if not matched:
            # Check simple "Sender: Message" without timestamp
            simple_match = re.match(r"^([^:]+):\s*(.*)$", line_clean)
            if simple_match and not any(notice in line_clean.lower() for notice in SYSTEM_NOTICES):
                sender, text = simple_match.groups()
                current_msg = {
                    "id": f"MSG_{msg_counter:05d}",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sender": sender.strip(),
                    "message": text.strip(),
                    "reply_to_id": None,
                    "thread_id": None,
                    "is_decision": False,
                    "is_forward": False,
                    "media_omitted": False,
                }
                messages.append(current_msg)
                msg_counter += 1
            elif current_msg:
                # Multi-line message continuation
                current_msg["message"] += f"\n{line_clean}"

    return messages


def parse_chat_txt(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses any exported text file (.txt) into a list of structured messages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    return parse_chat_content(content)


def parse_chat_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses JSON chat files (ChatRecall schema or arbitrary Telegram/Discord exports)
    and normalizes them to the ChatRecall format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    raw_list = []
    if isinstance(data, list):
        raw_list = data
    elif isinstance(data, dict):
        if "messages" in data and isinstance(data["messages"], list):
            raw_list = data["messages"]
        elif "chats" in data and isinstance(data["chats"], list):
            raw_list = data["chats"]
        else:
            raw_list = [data]

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_list):
        if not isinstance(item, dict):
            continue
        msg_id = item.get("id") or f"MSG_{idx + 1:05d}"
        sender = item.get("sender") or item.get("author") or item.get("user") or item.get("from") or "Unknown"
        text = item.get("message") or item.get("text") or item.get("content") or item.get("body") or ""
        ts = item.get("timestamp") or item.get("date") or item.get("time") or item.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Clean sender if dict (e.g. Telegram {"from": {"name": "..."}})
        if isinstance(sender, dict):
            sender = sender.get("name") or sender.get("username") or "Unknown"

        # Clean text if list (e.g. Telegram formatted text blocks)
        if isinstance(text, list):
            text = " ".join([t if isinstance(t, str) else t.get("text", "") for t in text])

        normalized.append({
            "id": str(msg_id),
            "timestamp": str(ts),
            "sender": str(sender).strip(),
            "message": str(text).strip(),
            "reply_to_id": item.get("reply_to_id"),
            "thread_id": item.get("thread_id"),
            "is_decision": bool(item.get("is_decision", False)),
            "is_forward": bool(item.get("is_forward", False)),
            "media_omitted": bool(item.get("media_omitted", False)),
        })

    return normalized


def load_custom_txt_to_json(txt_path: str, output_json_path: str = "data/custom_chat.json") -> str:
    """
    Parses a .txt file and saves it as structured JSON ready for indexing.
    """
    msgs = parse_chat_txt(txt_path)
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(msgs, f, indent=2, ensure_ascii=False)
    return output_json_path
