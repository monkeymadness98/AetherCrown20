"""
Minimal Render-ready FastAPI app for backend.main:app (import-safe)
"""

import os
import logging

# Optional imports with guards (preserve ability to run even if deps missing)
try:
    import sqlalchemy  # type: ignore
except Exception:
    sqlalchemy = None

try:
    import redis.asyncio as redis_asyncio  # type: ignore
except Exception:
    redis_asyncio = None

# Environment detection: prefer ENV or ENVIRONMENT, default to production
ENV = os.getenv("ENV", os.getenv("ENVIRONMENT", "production"))

# Load .env only in non-production (local development)
if ENV != "production":
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception as e:
        print(f"Warning: could not load .env file ({e})")

# Configure logging level and format
log_level = logging.INFO if ENV == "production" else logging.DEBUG
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("Starting backend; ENV=%s", ENV)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AetherCrown20 Backend", version="1.0")

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    """
    Health check endpoint for Render.
    Keep response minimal and non-sensitive.
    """
    return JSONResponse({"ok": True, "env": ENV})

@app.get("/clocks")
async def get_clock():
    return {"message": "Backend is alive and connected."}

# ---------------------------------------------------------------------
# Temporary: environment variable presence check
# Remove this endpoint after verification (do NOT expose secrets).
# ---------------------------------------------------------------------
@app.get("/_env_check")
async def env_check():
    return JSONResponse({
        "ENV": ENV,
        "paypal_client_exists": bool(os.getenv("PAYPAL_CLIENT_ID")),
        "db_url_present": bool(os.getenv("DATABASE_URL")),
    })

# Run locally with reload only in non-production
if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment or default to 8000 for local dev
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=(ENV != "production"))
