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

app = FastAPI(
    title="AetherCrown20 Backend", 
    version="1.0",
    description="Autonomous optimization and decision-making platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
try:
    from backend.routers.optimization import router as optimization_router
    from backend.routers.revenue import router as revenue_router
    from backend.routers.dashboard import router as dashboard_router
    from backend.routers.content import router as content_router
    from backend.routers.enterprise import router as enterprise_router
    from backend.routers.operational import router as operational_router
    from backend.routers.multi_tenant import router as multi_tenant_router
    from backend.routers.investor import router as investor_router
    
    app.include_router(optimization_router)
    app.include_router(revenue_router)
    app.include_router(dashboard_router)
    app.include_router(content_router)
    app.include_router(enterprise_router)
    app.include_router(operational_router)
    app.include_router(multi_tenant_router)
    app.include_router(investor_router)
    logger.info("All routers loaded successfully")
except Exception as e:
    logger.warning(f"Could not load some routers: {e}")

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
    # Use app directly so running python backend/main.py works regardless of CWD
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=(ENV != "production"))
