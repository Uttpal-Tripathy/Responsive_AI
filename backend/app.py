"""
Responsive AI – FastAPI Application Entry Point
================================================
Handles routing, middleware, CORS, and lifecycle events.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import time
import logging

from ai_engine import generate_response
from memory import save_interaction, get_history
from config import APP_NAME, VERSION, AUTHOR, ALLOWED_ORIGINS

# ── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 {APP_NAME} v{VERSION} starting up …")
    yield
    logger.info("🛑 Shutting down gracefully.")


# ── App Instance ─────────────────────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    description="Real-Time Responsive AI Framework",
    version=VERSION,
    contact={"name": AUTHOR},
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware: Request Timing ────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(elapsed)
    return response


# ── Schemas ───────────────────────────────────────────────────────────────────
class UserInput(BaseModel):
    username: str = Field(..., min_length=1, max_length=64, example="Uttpal")
    message: str = Field(..., min_length=1, max_length=2048, example="Hello")


class ChatResponse(BaseModel):
    user: str
    message: str
    response: str
    timestamp: float


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def home():
    """Health-check / welcome endpoint."""
    return {
        "status": "running",
        "app": APP_NAME,
        "version": VERSION,
    }


@app.post("/chat", response_model=ChatResponse, tags=["AI Chat"])
def chat(user_input: UserInput):
    """
    Send a message and receive an AI-generated response.
    Interaction is persisted to conversation memory.
    """
    try:
        response = generate_response(user_input.username, user_input.message)
        ts = save_interaction(user_input.username, user_input.message, response)
        return ChatResponse(
            user=user_input.username,
            message=user_input.message,
            response=response,
            timestamp=ts,
        )
    except Exception as exc:
        logger.error(f"Chat error for {user_input.username}: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.get("/history/{username}", tags=["Memory"])
def history(username: str, limit: int = 20):
    """Retrieve the last *limit* interactions for a user."""
    records = get_history(username, limit)
    return {"username": username, "count": len(records), "history": records}


@app.delete("/history/{username}", tags=["Memory"])
def clear_history(username: str):
    """Clear all stored interactions for a given user."""
    from memory import clear_user_history
    cleared = clear_user_history(username)
    return {"username": username, "cleared": cleared}
