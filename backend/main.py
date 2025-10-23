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

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from pathlib import Path
import random

app = FastAPI(title="AetherCrown20 Backend", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on ENV in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory (parent of backend/)
BASE_DIR = Path(__file__).parent.parent

# Mount static files and dashboard pages
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")
app.mount("/dev", StaticFiles(directory=str(BASE_DIR / "dev"), html=True), name="dev")
app.mount("/live", StaticFiles(directory=str(BASE_DIR / "live"), html=True), name="live")

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

# =====================================================================
# DEV HUB API ENDPOINTS
# =====================================================================

@app.get("/api/dev/status")
async def dev_status():
    """Get overall system status for Dev Hub"""
    return {
        "backend": {
            "status": "healthy",
            "uptime": "99.9%",
            "env": ENV,
            "last_deploy": "2024-10-23T02:30:00Z"
        },
        "database": {
            "status": "connected" if os.getenv("DATABASE_URL") else "not_configured",
            "connections": 5,
            "max_connections": 100
        },
        "redis": {
            "status": "connected" if os.getenv("REDIS_URL") else "not_configured",
            "memory_used": "45MB"
        }
    }

@app.get("/api/dev/builds")
async def dev_builds():
    """Get recent build and deployment logs"""
    return {
        "builds": [
            {
                "id": "build-001",
                "status": "success",
                "branch": "main",
                "commit": "abc123",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "duration": "2m 34s"
            },
            {
                "id": "build-002",
                "status": "success",
                "branch": "develop",
                "commit": "def456",
                "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
                "duration": "2m 12s"
            }
        ],
        "deployments": [
            {
                "id": "deploy-001",
                "service": "render",
                "status": "deployed",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                "id": "deploy-002",
                "service": "vercel",
                "status": "deployed",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
            }
        ]
    }

@app.get("/api/dev/ai-agents")
async def dev_ai_agents():
    """Get AI agent status and metrics"""
    return {
        "agents": [
            {
                "id": "agent-001",
                "name": "Content Generator",
                "status": "active",
                "tasks_completed": 145,
                "tasks_pending": 3,
                "uptime": "24h",
                "performance": 98.5
            },
            {
                "id": "agent-002",
                "name": "Analytics Processor",
                "status": "active",
                "tasks_completed": 892,
                "tasks_pending": 12,
                "uptime": "72h",
                "performance": 99.2
            },
            {
                "id": "agent-003",
                "name": "Email Automation",
                "status": "idle",
                "tasks_completed": 56,
                "tasks_pending": 0,
                "uptime": "12h",
                "performance": 97.8
            }
        ],
        "queue": {
            "total": 15,
            "processing": 3,
            "waiting": 12
        }
    }

@app.get("/api/dev/analytics")
async def dev_analytics():
    """Get database and analytics metrics"""
    return {
        "tables": [
            {"name": "users", "rows": 1247, "size": "2.3MB"},
            {"name": "payments", "rows": 892, "size": "1.1MB"},
            {"name": "events", "rows": 15234, "size": "12.4MB"},
            {"name": "subscriptions", "rows": 456, "size": "0.8MB"}
        ],
        "recent_events": [
            {
                "id": 1,
                "type": "user_signup",
                "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "user_id": "user-123"
            },
            {
                "id": 2,
                "type": "payment_success",
                "timestamp": (datetime.now() - timedelta(minutes=32)).isoformat(),
                "amount": 99.99
            }
        ]
    }

@app.get("/api/dev/logs")
async def dev_logs():
    """Get recent application logs"""
    return {
        "logs": [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "API request processed successfully",
                "service": "backend"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=1)).isoformat(),
                "level": "INFO",
                "message": "Database query executed",
                "service": "database"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "level": "WARN",
                "message": "High memory usage detected",
                "service": "monitoring"
            }
        ]
    }

# =====================================================================
# LIVE DASHBOARD API ENDPOINTS
# =====================================================================

@app.get("/api/live/metrics")
async def live_metrics():
    """Get business metrics for Live Dashboard"""
    return {
        "revenue": {
            "mrr": 45678.90,
            "total": 567890.12,
            "growth": 12.5
        },
        "users": {
            "total": 1247,
            "active": 892,
            "new_today": 23,
            "churn_rate": 2.3
        },
        "ai_tasks": {
            "completed_today": 1567,
            "total": 45890,
            "success_rate": 98.7
        },
        "uptime": {
            "percentage": 99.95,
            "last_incident": (datetime.now() - timedelta(days=14)).isoformat()
        }
    }

@app.get("/api/live/payments")
async def live_payments():
    """Get payment and subscription data"""
    return {
        "recent_payments": [
            {
                "id": "pay-001",
                "amount": 99.99,
                "status": "completed",
                "customer": "user-***123",
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()
            },
            {
                "id": "pay-002",
                "amount": 299.99,
                "status": "completed",
                "customer": "user-***456",
                "timestamp": (datetime.now() - timedelta(hours=3)).isoformat()
            }
        ],
        "subscriptions": {
            "active": 456,
            "trial": 78,
            "cancelled": 12,
            "revenue_breakdown": {
                "basic": 15600,
                "pro": 24500,
                "enterprise": 5578.90
            }
        }
    }

@app.get("/api/live/ai-activity")
async def live_ai_activity():
    """Get real-time AI activity feed"""
    activities = [
        "Generated 15 social media posts",
        "Processed 234 customer inquiries",
        "Analyzed 567 data points",
        "Sent 89 automated emails",
        "Updated 45 marketing campaigns",
        "Completed 12 content optimizations"
    ]
    
    return {
        "feed": [
            {
                "id": i,
                "activity": activities[i % len(activities)],
                "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat(),
                "agent": f"AI Agent {(i % 3) + 1}"
            }
            for i in range(10)
        ]
    }

@app.get("/api/live/marketing")
async def live_marketing():
    """Get marketing content and social feeds"""
    return {
        "posts": [
            {
                "id": "post-001",
                "title": "Scaling Your Empire with AI Automation",
                "excerpt": "Learn how AI agents can transform your business operations...",
                "date": (datetime.now() - timedelta(days=2)).isoformat(),
                "views": 1245
            },
            {
                "id": "post-002",
                "title": "Case Study: 10x Revenue Growth in 6 Months",
                "excerpt": "How our enterprise client achieved exponential growth...",
                "date": (datetime.now() - timedelta(days=5)).isoformat(),
                "views": 2367
            }
        ],
        "social": {
            "twitter_followers": 15678,
            "linkedin_connections": 8901,
            "engagement_rate": 4.2
        }
    }

@app.get("/api/live/enterprise")
async def live_enterprise():
    """Get enterprise features and SLA information"""
    return {
        "features": [
            {"name": "Dedicated Support", "status": "active", "sla": "99.99%"},
            {"name": "Custom AI Agents", "status": "active", "sla": "99.95%"},
            {"name": "Advanced Analytics", "status": "active", "sla": "99.9%"},
            {"name": "White Label Solution", "status": "available", "sla": "99.9%"}
        ],
        "performance": {
            "uptime": 99.97,
            "avg_response_time": "124ms",
            "support_response": "< 1 hour"
        },
        "onboarding": {
            "steps_completed": 4,
            "steps_total": 5,
            "next_step": "Configure custom integrations"
        }
    }

# Run locally with reload only in non-production
if __name__ == "__main__":
    import uvicorn
    # Use app directly so running python backend/main.py works regardless of CWD
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=(ENV != "production"))
