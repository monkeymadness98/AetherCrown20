"""Base models and schemas for the platform."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Standard API response format."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class MetricData(BaseModel):
    """Base metric data structure."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    value: float
    metric_name: str
    metadata: Optional[Dict[str, Any]] = None


class AITaskResult(BaseModel):
    """AI task execution result."""
    task_id: str
    task_type: str
    status: str  # pending, running, completed, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PredictionResult(BaseModel):
    """ML prediction result."""
    prediction_id: str
    model_name: str
    prediction_value: float
    confidence: float
    features_used: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
