"""

Minimal Render-ready FastAPI app for backend.main:app

Features:
- app = FastAPI() (uvicorn backend.main:app)
- Loads .env via python-dotenv if present
- Reads env vars: DATABASE_URL, REDIS_URL, PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_URL_KEY
- Async startup/shutdown event handlers that attempt to initialize optional DB/Redis clients
- CORS enabled for public access (adjust origins for production)
- Example /clocks endpoint returning sample JSON (replace with real implementation)

"""

import os
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Optional imports that will be used only if corresponding env vars exist
import sqlalchemy
from sqlalchemy import text  # for a lightweight optional DB health check
import redis.asyncio as aioredis  # requires redis package
from dotenv import load_dotenv

# Load .env if present (safe — will not error if absent)
load_dotenv()

# Basic logger
logger = logging.getLogger("backend")
logging.basicConfig(level=logging.INFO)

# Environment variables (read once)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
PAYPAL_CLIENT_ID: Optional[str] = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET: Optional[str] = os.getenv("PAYPAL_SECRET")
PAYPAL_URL_KEY: Optional[str] = os.getenv("PAYPAL_URL_KEY")

# FastAPI app (this is the entrypoint for uvicorn: backend.main:app)
app = FastAPI(title="AetherCrown20 Backend")

# Allow CORS for the frontend; restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change to your frontend URL(s) in prod
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global placeholders for connections (initialized in startup)
_db_engine: Optional[sqlalchemy.engine.Engine] = None
_redis_client: Optional[aioredis.Redis] = None


@app.on_event("startup")
async def startup_event():
    global _db_engine, _redis_client

    # Initialize DB engine lazily — does not perform blocking IO at import time
    if DATABASE_URL:
        try:
            _db_engine = sqlalchemy.create_engine(DATABASE_URL, future=True)
            try:
                with _db_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info("Database engine initialized and health check succeeded.")
            except Exception as e:
                logger.warning("Database engine created but health check failed: %s", e)
        except Exception as e:
            logger.exception("Failed to create DB engine: %s", e)
            _db_engine = None
    else:
        logger.info("No DATABASE_URL provided; DB engine will not be initialized.")

    # Initialize Redis client if REDIS_URL is present
    if REDIS_URL:
        try:
            _redis_client = aioredis.from_url(REDIS_URL)
            try:
                await _redis_client.ping()
                logger.info("Connected to Redis.")
            except Exception as e:
                logger.warning("Redis ping failed: %s", e)
        except Exception as e:
            logger.exception("Failed to create Redis client: %s", e)
            _redis_client = None
    else:
        logger.info("No REDIS_URL provided; Redis client will not be initialized.")

    # Validate PayPal env vars presence (do not fail startup, but warn)
    if not (PAYPAL_CLIENT_ID and PAYPAL_SECRET) and not PAYPAL_URL_KEY:
        logger.warning(
            "PayPal credentials not fully configured (PAYPAL_CLIENT_ID/PAYPAL_SECRET or PAYPAL_URL_KEY). "
            "Payment features may be disabled."
        )


@app.on_event("shutdown")
async def shutdown_event():
    global _db_engine, _redis_client
    if _redis_client:
        try:
            await _redis_client.close()
            logger.info("Redis client closed.")
        except Exception:
            logger.exception("Error closing Redis client.")
    if _db_engine:
        try:
            _db_engine.dispose()
            logger.info("DB engine disposed.")
        except Exception:
            logger.exception("Error disposing DB engine.")


@app.get("/healthz")
async def healthz():
    status = {"ok": True, "db": False, "redis": False}
    if _db_engine:
        try:
            with _db_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            status["db"] = True
        except Exception:
            status["db"] = False
    if _redis_client:
        try:
            pong = await _redis_client.ping()
            status["redis"] = bool(pong)
        except Exception:
            status["redis"] = False
    return status


@app.get("/clocks")
async def get_clocks():
    example = {
        "clocks": [
            {"id": "utc", "label": "UTC", "tz": "UTC", "offset_hours": 0},
            {"id": "local", "label": "Local", "tz": "local", "offset_hours": None},
        ],
        "message": "Replace /clocks with your real implementation.",
    }
    return example