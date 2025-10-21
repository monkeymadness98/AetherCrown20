"""
Minimal Render-ready FastAPI app for backend.main:app (import-safe)
"""

import os
import logging

# Optional imports with guards
try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

try:
    import redis.asyncio as redis_asyncio
except ImportError:
    redis_asyncio = None

# Environment detection: prefer ENV or ENVIRONMENT, default to production
ENV = os.getenv("ENV", os.getenv("ENVIRONMENT", "production"))

# Load .env only in non-production (local dev)
if ENV != "production":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

# Configure logging
log_level = logging.INFO if ENV == "production" else logging.DEBUG
logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)
logger.info("Starting backend; ENV=%s", ENV)

from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"ok": True, "db": bool(sqlalchemy), "redis": bool(redis_asyncio)}

@app.get("/clocks")
async def clocks():
    return {"clocks": [{"name": "UTC", "time": "12:00"}, {"name": "PST", "time": "04:00"}]}
