"""
Text Chat Parser for ChatRecall
===============================
Parses raw exported chat text files (.txt from WhatsApp, Telegram, or custom formats)
and converts them into structured ChatRecall messages for embedding and indexing.
"""

import re
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

# Supported WhatsApp/Telegram formats:
# 1. "12/10/23, 7:15 PM - Rohan Mehta: Chalo Manali chalte hain"
# 2. "[12/10/23, 19:15:20] Rohan Mehta: Chalo Manali chalte hain"
# 3. "2023-10-12 19:15:00 - Rohan Mehta: Chalo Manali chalte hain"
# 4. "Rohan Mehta: Chalo Manali chalte hain"

PATTERNS = [
    # 12/10/23, 7:15 PM - Name: Message
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\s*-\s*([^:]+):\s*(.*)$",
    # [12/10/23, 19:15:20] Name: Message
    r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\]\s*([^:]+):\s*(.*)$",
    # 2023-10-12 19:15:00 - Name: Message
    r"^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}(?::\d{2})?)\s*-\s*([^:]+):\s*(.*)$",
]


def parse_timestamp(date_str: str, time_str: str) -> str:
    """Attempts multiple datetime formats and normalizes to YYYY-MM-DD HH:MM:SS."""
    combined = f"{date_str.strip()} {time_str.strip()}"
    formats = [
        "%d/%m/%y %I:%M %p",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%y %H:%M",
        "%d/%m/%Y %H:%M",
        "%m/%d/%y %I:%M %p",
        "%m/%d/%Y %I:%M %p",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(combined, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    # Fallback to current timestamp
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_chat_txt(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses any exported text file (.txt) into a list of structured messages.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    messages: List[Dict[str, Any]] = []
    msg_counter = 1
    current_msg: Optional[Dict[str, Any]] = None

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        matched = False
        for pat in PATTERNS:
            m = re.match(pat, line_clean)
            if m:
                d_str, t_str, sender, text = m.groups()
                ts = parse_timestamp(d_str, t_str)
                is_media = "<Media omitted>" in text or "image omitted" in text.lower()
                is_fwd = "[Forwarded" in text or "Forwarded:" in text

                current_msg = {
                    "id": f"MSG_{msg_counter:05d}",
                    "timestamp": ts,
                    "sender": sender.strip(),
                    "message": text.strip(),
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
            if simple_match:
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


def load_custom_txt_to_json(txt_path: str, output_json_path: str = "data/custom_chat.json") -> str:
    """
    Parses a .txt file and saves it as structured JSON ready for indexing.
    """
    msgs = parse_chat_txt(txt_path)
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(msgs, f, indent=2, ensure_ascii=False)
    return output_json_path
