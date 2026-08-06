import os
import sqlite3
import threading
import time
from datetime import datetime, timezone

import redis
from celery import Celery
from fastapi import FastAPI, Header, HTTPException, Query
from contextlib import asynccontextmanager

def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()



RATE_LIMIT = 10
WINDOW_SECONDS = 60

DB_PATH = "requests.db"

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

celery_app = Celery("redis_app", broker="redis://localhost:6379/0")

app = FastAPI(lifespan=lifespan)

_db_lock = threading.Lock()


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS request_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )"""
    )
    return conn


@celery_app.task
def log_request(user_id: str, endpoint: str, status: str):
    with _db_lock:
        conn = get_db()
        conn.execute(
            "INSERT INTO request_logs (user_id, endpoint, status, created_at) VALUES (?, ?, ?, ?)",
            (user_id, endpoint, status, int(time.time())),
        )
        conn.commit()
        conn.close()


@app.get("/rate-limited")
def rate_limited(
    user_id: str = Query(default=""),
    x_forwarded_for: str = Header(default=None),
):
    identity = user_id or (x_forwarded_for or "unknown")
    key = f"limit:{identity}:{int(time.time()) // WINDOW_SECONDS}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, WINDOW_SECONDS)

    endpoint = "/rate-limited"

    if count > RATE_LIMIT:
        log_request.delay(identity, endpoint, "denied")
        remaining = 0
        retry_after = WINDOW_SECONDS - (int(time.time()) % WINDOW_SECONDS)
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded: max 10 requests per minute.",
            headers={"X-RateLimit-Remaining": str(remaining), "Retry-After": str(retry_after)},
        )

    log_request.delay(identity, endpoint, "allowed")
    return {
        "message": "Request accepted",
        "user_id": identity,
        "requests_remaining": RATE_LIMIT - count,
    }

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}