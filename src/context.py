"""
Thread Context Engine for ChatRecall
====================================
Reconstructs and formats the conversational neighborhood surrounding any matched message.
Ensures search results are never presented as isolated strings, providing full
conversational dialogue, reply chains, and thread decision resolution highlights.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.index import ChatIndex


class ThreadContextBuilder:
    def __init__(self, index: ChatIndex):
        self.index = index

    def get_context_window(
        self,
        msg_idx: int,
        window_before: int = 3,
        window_after: int = 3,
        max_time_gap_minutes: int = 30
    ) -> Dict[str, Any]:
        """
        Extracts surrounding conversational messages around target index `msg_idx`.
        If the message is part of an explicit thread_id, preserves thread continuity.
        """
        target_msg = self.index.messages[msg_idx]
        target_time = self.index.timestamps[msg_idx]
        thread_id = target_msg.get("thread_id")

        if thread_id:
            # If explicit thread, collect all messages in this thread block
            thread_msgs = [
                (idx, m) for idx, m in enumerate(self.index.messages)
                if m.get("thread_id") == thread_id
            ]
            # Find position of target message in thread
            target_pos = next((i for i, (idx, _) in enumerate(thread_msgs) if idx == msg_idx), 0)
            start_slice = max(0, target_pos - window_before)
            end_slice = min(len(thread_msgs), target_pos + window_after + 1)
            selected_items = thread_msgs[start_slice:end_slice]
        else:
            # General chat burst
            start_idx = max(0, msg_idx - window_before)
            end_idx = min(len(self.index.messages), msg_idx + window_after + 1)
            
            selected_items = []
            for i in range(start_idx, end_idx):
                t = self.index.timestamps[i]
                # Keep within time gap
                if abs((t - target_time).total_seconds()) <= max_time_gap_minutes * 60:
                    selected_items.append((i, self.index.messages[i]))

        formatted_messages = []
        for idx, m in selected_items:
            dt = datetime.strptime(m["timestamp"], "%Y-%m-%d %H:%M:%S")
            formatted_messages.append({
                "id": m["id"],
                "idx": idx,
                "sender": m["sender"],
                "raw_timestamp": m["timestamp"],
                "formatted_time": dt.strftime("%b %d, %Y • %I:%M %p"),
                "message": m["message"],
                "is_target": (idx == msg_idx),
                "is_decision": m.get("is_decision", False),
                "is_forward": m.get("is_forward", False),
                "media_omitted": m.get("media_omitted", False),
                "reply_to_id": m.get("reply_to_id")
            })

        return {
            "target_id": target_msg["id"],
            "target_idx": msg_idx,
            "thread_id": thread_id,
            "is_decision": target_msg.get("is_decision", False),
            "total_context_messages": len(formatted_messages),
            "messages": formatted_messages
        }
