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

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AetherCrown20 Backend", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
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

# ---------------------------------------------------------------------
# Sweep & Monitoring Endpoints
# ---------------------------------------------------------------------
@app.get("/sweep/status")
async def sweep_status():
    """Get current system status without full sweep."""
    return JSONResponse({
        "env": ENV,
        "services": {
            "backend": "running",
            "database": bool(os.getenv("DATABASE_URL")),
            "redis": bool(os.getenv("REDIS_URL")),
        }
    })

@app.post("/sweep/run")
async def run_sweep(background_tasks: BackgroundTasks, auto_fix: bool = False):
    """
    Run a full system sweep.
    
    Query params:
        auto_fix: Enable automatic fixes (default: false)
    """
    try:
        from backend.sweep import SweepAgent
        
        # Run sweep in background
        async def sweep_task():
            agent = SweepAgent(auto_fix=auto_fix)
            report = await agent.run_full_sweep()
            # Store report somewhere for retrieval
            report_path = f"/tmp/sweep_report_{ENV}.json"
            with open(report_path, 'w') as f:
                f.write(report.to_json())
            logger.info(f"Sweep report saved to {report_path}")
        
        background_tasks.add_task(sweep_task)
        
        return JSONResponse({
            "status": "started",
            "message": "Sweep operation started in background",
            "auto_fix": auto_fix
        })
    except Exception as e:
        logger.error(f"Error starting sweep: {e}")
        return JSONResponse({
            "status": "error",
            "error": str(e)
        }, status_code=500)

@app.get("/sweep/report")
async def get_sweep_report(format: str = "json"):
    """
    Get the latest sweep report.
    
    Query params:
        format: json or markdown (default: json)
    """
    try:
        report_path = f"/tmp/sweep_report_{ENV}.json"
        
        if not os.path.exists(report_path):
            return JSONResponse({
                "status": "not_found",
                "message": "No sweep report found. Run /sweep/run first."
            }, status_code=404)
        
        with open(report_path, 'r') as f:
            report_data = f.read()
        
        if format == "markdown":
            import json
            from backend.sweep import SweepReport
            # Recreate report from JSON to convert to markdown
            data = json.loads(report_data)
            # Return as plain text
            return JSONResponse({
                "status": "success",
                "format": "markdown",
                "report": "Markdown conversion requires full SweepReport object"
            })
        else:
            import json
            return JSONResponse({
                "status": "success",
                "format": "json",
                "report": json.loads(report_data)
            })
    except Exception as e:
        logger.error(f"Error retrieving sweep report: {e}")
        return JSONResponse({
            "status": "error",
            "error": str(e)
        }, status_code=500)

# Run locally with reload only in non-production
if __name__ == "__main__":
    import uvicorn
    # Use app directly so running python backend/main.py works regardless of CWD
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=(ENV != "production"))
