"""
Tests for Responsive AI API endpoints.
Run with: pytest backend/tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import app

client = TestClient(app)


def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"


def test_chat_hello():
    r = client.post("/chat", json={"username": "TestUser", "message": "hello"})
    assert r.status_code == 200
    data = r.json()
    assert "TestUser" in data["response"]


def test_chat_time():
    r = client.post("/chat", json={"username": "TestUser", "message": "what time is it"})
    assert r.status_code == 200
    assert "UTC" in r.json()["response"]


def test_chat_help():
    r = client.post("/chat", json={"username": "TestUser", "message": "help"})
    assert r.status_code == 200
    assert "commands" in r.json()["response"].lower()


def test_chat_fallback():
    r = client.post("/chat", json={"username": "TestUser", "message": "xyzzy nonsense"})
    assert r.status_code == 200
    assert r.json()["response"]  # non-empty


def test_history():
    r = client.get("/history/TestUser")
    assert r.status_code == 200
    assert "history" in r.json()
