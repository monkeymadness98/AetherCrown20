"""API endpoints for dashboards and monitoring."""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pydantic import BaseModel

from backend.dashboards.executive_dashboard import ExecutiveDashboard
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

# Initialize services
exec_dashboard = ExecutiveDashboard()


# Request Models
class ExecutiveSummaryRequest(BaseModel):
    revenue_data: List[Dict] = []
    task_data: List[Dict] = []
    health_data: Dict = {}
    user_data: List[Dict] = []


# Endpoints
@router.post("/executive/summary")
async def get_executive_summary(request: ExecutiveSummaryRequest):
    """
    Generate comprehensive executive summary with all KPIs.
    
    Returns revenue, AI performance, system health, and growth metrics.
    """
    try:
        summary = exec_dashboard.generate_executive_summary({
            "revenue_data": request.revenue_data,
            "task_data": request.task_data,
            "health_data": request.health_data,
            "user_data": request.user_data
        })
        
        return BaseResponse(
            success=True,
            message="Executive summary generated",
            data={"summary": summary}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics/revenue")
async def get_revenue_metrics(revenue_data: List[Dict]):
    """Get detailed revenue metrics and KPIs."""
    try:
        metrics = exec_dashboard.calculate_revenue_metrics(revenue_data)
        
        return BaseResponse(
            success=True,
            message="Revenue metrics calculated",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics/ai-performance")
async def get_ai_metrics(task_data: List[Dict]):
    """Get AI task completion and performance metrics."""
    try:
        metrics = exec_dashboard.calculate_ai_metrics(task_data)
        
        return BaseResponse(
            success=True,
            message="AI metrics calculated",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics/system-health")
async def get_system_health(health_data: Dict):
    """Get system health metrics."""
    try:
        metrics = exec_dashboard.calculate_system_health(health_data)
        
        return BaseResponse(
            success=True,
            message="System health metrics retrieved",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/metrics/growth")
async def get_growth_metrics(user_data: List[Dict]):
    """Get user growth and acquisition metrics."""
    try:
        metrics = exec_dashboard.calculate_growth_kpis(user_data)
        
        return BaseResponse(
            success=True,
            message="Growth metrics calculated",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
