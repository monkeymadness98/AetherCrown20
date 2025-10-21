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

# Load .env only in non-production environments
env = os.getenv("ENV") or os.getenv("ENVIRONMENT")
if env != "production":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

# Configure logging level based on environment
log_level = logging.INFO if env == "production" else logging.DEBUG
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI

app = FastAPI()

# Add startup log
@app.on_event("startup")
async def startup_event():
    logger.info(f"Application starting up in {env or 'development'} mode")

@app.get("/healthz")
async def healthz():
    return {"ok": True, "db": bool(sqlalchemy), "redis": bool(redis_asyncio)}

@app.get("/clocks")
async def clocks():
    return {"clocks": [{"name": "UTC", "time": "12:00"}, {"name": "PST", "time": "04:00"}]}
