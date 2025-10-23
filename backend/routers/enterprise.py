"""API endpoints for enterprise automation."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel

from backend.enterprise.onboarding import EnterpriseOnboarding
from backend.enterprise.usage_monitor import UsageMonitor
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/enterprise", tags=["enterprise"])

# Initialize services
onboarding = EnterpriseOnboarding()
usage_monitor = UsageMonitor()


# Request Models
class OnboardingRequest(BaseModel):
    company_name: str
    employee_count: int
    annual_revenue: float
    contact_email: str


class UsageTrackingRequest(BaseModel):
    client_id: str
    usage_data: Dict


class UpsellAnalysisRequest(BaseModel):
    client_id: str
    usage_history: List[Dict]
    current_tier: str


# Endpoints
@router.post("/onboarding/create")
async def create_onboarding_flow(request: OnboardingRequest):
    """Create automated onboarding flow for enterprise client."""
    try:
        flow = onboarding.create_onboarding_flow({
            "company_name": request.company_name,
            "employee_count": request.employee_count,
            "annual_revenue": request.annual_revenue,
            "contact_email": request.contact_email
        })
        
        return BaseResponse(
            success=True,
            message="Onboarding flow created",
            data={"flow": flow}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/onboarding/{onboarding_id}/status")
async def get_onboarding_status(onboarding_id: str):
    """Get current onboarding status."""
    try:
        status = onboarding.get_onboarding_status(onboarding_id)
        
        return BaseResponse(
            success=True,
            message="Onboarding status retrieved",
            data={"status": status}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/onboarding/{onboarding_id}/report")
async def get_onboarding_report(onboarding_id: str):
    """Generate onboarding progress report."""
    try:
        report = onboarding.generate_onboarding_report(onboarding_id)
        
        return BaseResponse(
            success=True,
            message="Onboarding report generated",
            data={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/usage/track")
async def track_usage(request: UsageTrackingRequest):
    """Track enterprise client usage."""
    try:
        summary = usage_monitor.track_usage(
            request.client_id,
            request.usage_data
        )
        
        return BaseResponse(
            success=True,
            message="Usage tracked",
            data={"summary": summary}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/usage/analyze-upsell")
async def analyze_upsell(request: UpsellAnalysisRequest):
    """Identify upsell opportunities based on usage."""
    try:
        opportunities = usage_monitor.identify_upsell_opportunities(
            request.client_id,
            request.usage_history,
            request.current_tier
        )
        
        return BaseResponse(
            success=True,
            message="Upsell analysis completed",
            data={
                "opportunities": opportunities,
                "count": len(opportunities)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage/{client_id}/report")
async def get_usage_report(client_id: str, period_days: int = 30):
    """Generate usage report for enterprise client."""
    try:
        report = usage_monitor.generate_usage_report(client_id, period_days)
        
        return BaseResponse(
            success=True,
            message="Usage report generated",
            data={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/usage/{client_id}/trigger-upsell")
async def trigger_upsell(client_id: str, opportunity: Dict):
    """Trigger automated upsell campaign."""
    try:
        campaign = usage_monitor.trigger_upsell_campaign(client_id, opportunity)
        
        return BaseResponse(
            success=True,
            message="Upsell campaign triggered",
            data={"campaign": campaign}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage/{client_id}/renewal-probability")
async def calculate_renewal_probability(client_id: str, usage_data: Dict):
    """Calculate contract renewal probability."""
    try:
        probability = usage_monitor.calculate_renewal_probability(
            client_id,
            usage_data
        )
        
        return BaseResponse(
            success=True,
            message="Renewal probability calculated",
            data={"probability": probability}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
