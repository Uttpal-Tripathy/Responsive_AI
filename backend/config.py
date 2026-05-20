"""
Responsive AI – Configuration
==============================
All tunable knobs in one place.
Override via environment variables (recommended for production).
"""

import os

# ── Application ───────────────────────────────────────────────────────────────
APP_NAME: str = os.getenv("APP_NAME", "Responsive AI")
VERSION: str = "1.1.0"
AUTHOR: str = "Open Source Community"

# ── Server ────────────────────────────────────────────────────────────────────
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"

# ── CORS ──────────────────────────────────────────────────────────────────────
ALLOWED_ORIGINS: list[str] = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173"
).split(",")

# ── Memory ────────────────────────────────────────────────────────────────────
MEMORY_PATH: str = os.getenv("MEMORY_PATH", "conversation_memory.json")

# ── External APIs (add your keys here or via .env) ───────────────────────────
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")  # optional LLM upgrade
