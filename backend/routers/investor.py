"""API endpoints for investor dashboards."""
from fastapi import APIRouter, HTTPException
from typing import Optional

from backend.investor.investor_dashboard import InvestorDashboard
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/investor", tags=["investor"])

# Initialize service
investor_dashboard = InvestorDashboard()


# Endpoints
@router.get("/dashboard/live")
async def get_live_dashboard(include_forecasts: bool = True):
    """Get live investor dashboard with real-time KPIs."""
    try:
        dashboard = investor_dashboard.generate_live_dashboard(include_forecasts)
        
        return BaseResponse(
            success=True,
            message="Live dashboard generated",
            data={"dashboard": dashboard}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity-feed")
async def get_activity_feed(limit: int = 50, sanitize: bool = True):
    """Get real-time AI task activity feed."""
    try:
        activities = investor_dashboard.generate_ai_activity_feed(limit, sanitize)
        
        return BaseResponse(
            success=True,
            message="Activity feed retrieved",
            data={
                "activities": activities,
                "count": len(activities)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/monthly")
async def get_monthly_report(month: Optional[str] = None):
    """Generate comprehensive monthly report for stakeholders."""
    try:
        report = investor_dashboard.generate_monthly_report(month)
        
        return BaseResponse(
            success=True,
            message="Monthly report generated",
            data={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/public")
async def get_public_metrics():
    """Get sanitized public metrics safe for display."""
    try:
        metrics = investor_dashboard.get_public_metrics()
        
        return BaseResponse(
            success=True,
            message="Public metrics retrieved",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpis")
async def get_investor_kpis():
    """Calculate key investor KPIs."""
    try:
        kpis = investor_dashboard.calculate_investor_kpis()
        
        return BaseResponse(
            success=True,
            message="Investor KPIs calculated",
            data={"kpis": kpis}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
