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

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"ok": True, "db": bool(sqlalchemy), "redis": bool(redis_asyncio)}

@app.get("/clocks")
async def clocks():
    return {"clocks": [{"name": "UTC", "time": "12:00"}, {"name": "PST", "time": "04:00"}]}
