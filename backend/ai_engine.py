"""
Responsive AI – AI Engine
=========================
Intent-based response pipeline. Swap `_rule_based_response` for
a Transformers / LLM call to upgrade to a neural backend.
"""

from __future__ import annotations

import re
import logging
from datetime import datetime, timezone
from typing import Callable

logger = logging.getLogger(__name__)

# ── Intent registry ───────────────────────────────────────────────────────────
# Each entry: (compiled pattern, handler function)
_INTENT_REGISTRY: list[tuple[re.Pattern, Callable[[str, str], str]]] = []


def _register(pattern: str):
    """Decorator to register an intent handler."""
    def decorator(fn: Callable[[str, str], str]):
        _INTENT_REGISTRY.append((re.compile(pattern, re.IGNORECASE), fn))
        return fn
    return decorator


# ── Intent Handlers ───────────────────────────────────────────────────────────

@_register(r"\b(hi|hello|hey|howdy|greetings)\b")
def _greet(user: str, _msg: str) -> str:
    return f"Hello, {user}! 👋 Welcome to Responsive AI. Type *help* to see what I can do."


@_register(r"\b(time|clock|hour|what time)\b")
def _time(_user: str, _msg: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"🕐 Current UTC time: **{now}**"


@_register(r"\b(weather|temperature|forecast|rain|sunny)\b")
def _weather(_user: str, _msg: str) -> str:
    return (
        "🌤️ The weather module is ready to be wired up! "
        "Integrate an OpenWeatherMap or WeatherAPI key in `config.py` to enable live forecasts."
    )


@_register(r"\b(ai|artificial intelligence|machine learning|ml|neural|deep learning)\b")
def _about_ai(_user: str, _msg: str) -> str:
    return (
        "🤖 Responsive AI is a real-time adaptive framework built on FastAPI + PyTorch. "
        "It learns from every interaction and can be extended with custom intent handlers, "
        "Transformer models, or external APIs."
    )


@_register(r"\b(help|commands|features|what can you do)\b")
def _help(_user: str, _msg: str) -> str:
    return (
        "📋 **Available commands**\n"
        "- `hello` – greeting\n"
        "- `time` – current UTC time\n"
        "- `weather` – forecast (requires API key)\n"
        "- `ai` – about this framework\n"
        "- `history` – your past interactions (via `/history/<username>`)\n"
        "- anything else – adaptive fallback response"
    )


@_register(r"\b(bye|goodbye|see you|cya|quit|exit)\b")
def _farewell(user: str, _msg: str) -> str:
    return f"Goodbye, {user}! 👋 Come back anytime."


# ── Main Entry Point ───────────────────────────────────────────────────────────

def generate_response(user: str, message: str) -> str:
    """
    Route *message* to the first matching intent handler.
    Falls back to a generic adaptive reply if no intent matches.
    """
    for pattern, handler in _INTENT_REGISTRY:
        if pattern.search(message):
            logger.debug(f"Intent matched: {handler.__name__} for user={user}")
            return handler(user, message)

    logger.debug(f"No intent matched for user={user}; using fallback.")
    return (
        f"🧠 I'm continuously learning, {user}. "
        "I didn't catch a specific intent in your message—try rephrasing, "
        "or type *help* for available commands."
    )
