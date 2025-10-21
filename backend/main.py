"""
Minimal Render-ready FastAPI app for backend.main:app (import-safe)

Guards optional imports so uvicorn can import the module even if optional libs are missing.
- Reads env vars: DATABASE_URL, REDIS_URL, PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_URL_KEY
- Guards optional imports so module import never fails
- Async startup/shutdown that initialize optional DB/Redis clients if configured.
- /healthz and /clocks endpoints for smoke tests.
"""

import os
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Guard optional imports so module import never fails
try:
    import sqlalchemy
    from sqlalchemy import text
except Exception:
    sqlalchemy = None
    text = None

try:
    import redis.asyncio as aioredis
except Exception:
    aioredis = None

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Load .env if available (no-op if python-dotenv not installed)
if load_dotenv:
    try:
        load_dotenv()
    except Exception:
        pass

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
    allow_origins=["*"],  # change to specific origins in production
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

_db_engine: Optional["sqlalchemy.engine.Engine"] = None  # type: ignore[name-defined]
_redis_client: Optional["aioredis.Redis"] = None  # type: ignore[name-defined]


@app.on_event("startup")
async def startup_event():
    global _db_engine, _redis_client

    if DATABASE_URL and sqlalchemy:
        try:
            _db_engine = sqlalchemy.create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
            try:
                if text and _db_engine:
                    with _db_engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                logger.info("DB engine initialized and health check succeeded.")
            except Exception as e:
                logger.warning("DB engine created but health check failed: %s", e)
        except Exception as e:
            logger.exception("Failed to create DB engine: %s", e)
            _db_engine = None
    elif DATABASE_URL:
        logger.warning("DATABASE_URL provided but SQLAlchemy not installed; skipping DB init.")
    else:
        logger.info("No DATABASE_URL provided; skipping DB init.")

    if REDIS_URL and aioredis:
        try:
            _redis_client = aioredis.from_url(REDIS_URL)
            try:
                await _redis_client.ping()
                logger.info("Redis client initialized and ping succeeded.")
            except Exception as e:
                logger.warning("Redis client created but ping failed: %s", e)
        except Exception as e:
            logger.exception("Failed to create Redis client: %s", e)
            _redis_client = None
    elif REDIS_URL:
        logger.warning("REDIS_URL provided but redis.asyncio not installed; skipping Redis init.")
    else:
        logger.info("No REDIS_URL provided; skipping Redis init.")

    if not (PAYPAL_CLIENT_ID and PAYPAL_SECRET) and not PAYPAL_URL_KEY:
        logger.warning(
            "PayPal credentials not fully configured (PAYPAL_CLIENT_ID/PAYPAL_SECRET or PAYPAL_URL_KEY). "
            "This app will continue to run but PayPal-related functionality may be disabled.")


@app.on_event("shutdown")
async def shutdown_event():
    global _db_engine, _redis_client
    try:
        if _redis_client:
            await _redis_client.close()
            logger.info("Redis client closed.")
    except Exception:
        logger.exception("Error while closing Redis client")

    try:
        if _db_engine:
            _db_engine.dispose()
            logger.info("DB engine disposed.")
    except Exception:
        logger.exception("Error while disposing DB engine")


@app.get("/healthz")
async def healthz():
    status = {"ok": True, "db": False, "redis": False}
    if _db_engine and text:
        try:
            with _db_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            status["db"] = True
        except Exception:
            status["db"] = False
    if _redis_client:
        try:
            await _redis_client.ping()
            status["redis"] = True
        except Exception:
            status["redis"] = False
    return status


@app.get("/clocks")
async def get_clocks():
    return {
        "clocks": [
            {"id": "utc", "label": "UTC", "tz": "UTC", "offset_hours": 0},
            {"id": "local", "label": "Local", "tz": "local", "offset_hours": None},
        ],
        "message": "Replace /clocks with your real implementation.",
    }
