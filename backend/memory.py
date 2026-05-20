"""
Responsive AI – Conversation Memory
====================================
Thread-safe JSON-backed persistence for user interactions.
Replace with a proper database (PostgreSQL, MongoDB, Redis) for production.
"""

from __future__ import annotations

import json
import os
import time
import threading
import logging
from typing import Any

logger = logging.getLogger(__name__)

_DATABASE = os.getenv("MEMORY_PATH", "conversation_memory.json")
_lock = threading.Lock()


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load() -> list[dict[str, Any]]:
    if not os.path.exists(_DATABASE):
        return []
    with open(_DATABASE, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError:
            logger.warning("Memory file corrupted – starting fresh.")
            return []


def _save(data: list[dict[str, Any]]) -> None:
    with open(_DATABASE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


# ── Public API ────────────────────────────────────────────────────────────────

def save_interaction(user: str, message: str, response: str) -> float:
    """
    Append an interaction record and return the UTC timestamp.
    Thread-safe via module-level lock.
    """
    ts = time.time()
    record = {
        "user": user,
        "message": message,
        "response": response,
        "timestamp": ts,
    }
    with _lock:
        data = _load()
        data.append(record)
        _save(data)
    logger.debug(f"Saved interaction for {user} at {ts}")
    return ts


def get_history(user: str, limit: int = 20) -> list[dict[str, Any]]:
    """Return the most recent *limit* interactions for *user*."""
    with _lock:
        data = _load()
    user_records = [r for r in data if r.get("user") == user]
    return user_records[-limit:]


def clear_user_history(user: str) -> int:
    """Delete all records for *user*. Returns the number of deleted records."""
    with _lock:
        data = _load()
        kept = [r for r in data if r.get("user") != user]
        removed = len(data) - len(kept)
        _save(kept)
    logger.info(f"Cleared {removed} record(s) for {user}")
    return removed
