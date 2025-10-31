"""API endpoints for AI optimization features."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from backend.ai_optimization.budget_optimizer import MarketingBudgetOptimizer
from backend.ai_optimization.churn_predictor import ChurnPredictor
from backend.ai_optimization.task_scheduler import TaskScheduler, AITask, TaskPriority
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/optimization", tags=["optimization"])

# Initialize services
budget_optimizer = MarketingBudgetOptimizer()
churn_predictor = ChurnPredictor()
task_scheduler = TaskScheduler()


# Request/Response Models
class BudgetOptimizationRequest(BaseModel):
    total_budget: float
    historical_data: List[Dict]


class ChurnPredictionRequest(BaseModel):
    users_data: List[Dict]


class TaskScheduleRequest(BaseModel):
    task_id: str
    task_type: str
    priority: int  # 1-4
    estimated_duration: int
    dependencies: Optional[List[str]] = []


# Endpoints
@router.post("/budget/optimize")
async def optimize_marketing_budget(request: BudgetOptimizationRequest):
    """
    Optimize marketing budget allocation across channels.
    
    Returns optimized allocation and recommendations.
    """
    try:
        allocations = budget_optimizer.optimize_allocation(
            request.total_budget,
            request.historical_data
        )
        
        channel_roi = budget_optimizer.analyze_channel_performance(request.historical_data)
        recommendations = budget_optimizer.get_recommendations(allocations, channel_roi)
        
        return BaseResponse(
            success=True,
            message="Budget optimization completed",
            data={
                "allocations": allocations,
                "channel_roi": channel_roi,
                "recommendations": recommendations,
                "total_budget": request.total_budget
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/churn/predict")
async def predict_churn(request: ChurnPredictionRequest):
    """
    Predict churn for users and generate retention campaigns.
    
    Returns predictions and automated campaign recommendations.
    """
    try:
        predictions = churn_predictor.predict_churn(request.users_data)
        campaigns = churn_predictor.trigger_campaigns(predictions)
        
        # Summary statistics
        at_risk_count = len([p for p in predictions 
                            if p["risk_level"] in ["medium", "high", "critical"]])
        critical_count = len([p for p in predictions 
                             if p["risk_level"] == "critical"])
        
        return BaseResponse(
            success=True,
            message="Churn prediction completed",
            data={
                "predictions": predictions,
                "campaigns": campaigns,
                "summary": {
                    "total_users": len(request.users_data),
                    "at_risk_users": at_risk_count,
                    "critical_risk_users": critical_count,
                    "campaigns_triggered": len(campaigns)
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/schedule")
async def schedule_task(request: TaskScheduleRequest):
    """Add a task to the AI task scheduler."""
    try:
        priority = TaskPriority(request.priority)
        task = AITask(
            task_id=request.task_id,
            task_type=request.task_type,
            priority=priority,
            estimated_duration=request.estimated_duration,
            dependencies=request.dependencies
        )
        
        task_scheduler.add_task(task)
        
        return BaseResponse(
            success=True,
            message="Task scheduled successfully",
            data={"task": task.to_dict()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/metrics")
async def get_task_metrics():
    """Get AI task scheduler metrics."""
    try:
        metrics = task_scheduler.get_metrics()
        bottlenecks = task_scheduler.identify_bottlenecks()
        
        return BaseResponse(
            success=True,
            message="Task metrics retrieved",
            data={
                "metrics": metrics,
                "bottlenecks": bottlenecks
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/assign")
async def assign_tasks():
    """Assign queued tasks to available workers."""
    try:
        assignments = task_scheduler.assign_tasks()
        
        return BaseResponse(
            success=True,
            message=f"Assigned {len(assignments)} tasks",
            data={
                "assignments": [
                    {"worker": w, "task": t.to_dict()} 
                    for w, t in assignments
                ]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: str, success: bool = True):
    """Mark a task as completed or failed."""
    try:
        task_scheduler.complete_task(task_id, success)
        
        return BaseResponse(
            success=True,
            message=f"Task {task_id} marked as {'completed' if success else 'failed'}",
            data={"task_id": task_id, "success": success}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
