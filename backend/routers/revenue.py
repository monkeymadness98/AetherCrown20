"""API endpoints for revenue expansion features."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

from backend.revenue_expansion.dynamic_pricing import DynamicPricingEngine
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/revenue", tags=["revenue"])

# Initialize services
pricing_engine = DynamicPricingEngine()


# Request Models
class DynamicPricingRequest(BaseModel):
    tier: str
    usage_data: Dict
    engagement_data: Dict
    company_data: Optional[Dict] = None


class UpsellAnalysisRequest(BaseModel):
    current_tier: str
    usage_data: Dict


# Endpoints
@router.post("/pricing/calculate")
async def calculate_dynamic_pricing(request: DynamicPricingRequest):
    """
    Calculate dynamic pricing based on usage, engagement, and company size.
    
    Returns detailed pricing breakdown and recommendations.
    """
    try:
        pricing = pricing_engine.calculate_dynamic_price(
            request.tier,
            request.usage_data,
            request.engagement_data,
            request.company_data
        )
        
        return BaseResponse(
            success=True,
            message="Dynamic pricing calculated",
            data={"pricing": pricing}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pricing/recommend-tier")
async def recommend_pricing_tier(usage_data: Dict, company_data: Optional[Dict] = None):
    """
    Recommend appropriate pricing tier based on usage patterns.
    """
    try:
        recommended_tier = pricing_engine.recommend_tier(usage_data, company_data)
        
        return BaseResponse(
            success=True,
            message="Tier recommendation generated",
            data={
                "recommended_tier": recommended_tier,
                "reason": "Based on usage patterns and company profile"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upsell/analyze")
async def analyze_upsell_opportunity(request: UpsellAnalysisRequest):
    """
    Analyze potential upsell opportunities based on usage.
    
    Returns upsell recommendations if applicable.
    """
    try:
        upsell = pricing_engine.calculate_upsell_opportunity(
            request.current_tier,
            request.usage_data
        )
        
        if upsell:
            return BaseResponse(
                success=True,
                message="Upsell opportunity identified",
                data={"upsell": upsell, "has_opportunity": True}
            )
        else:
            return BaseResponse(
                success=True,
                message="No upsell opportunity at this time",
                data={"has_opportunity": False}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tiers")
async def get_pricing_tiers():
    """Get all available pricing tiers and their features."""
    try:
        tiers = {
            name: {
                "name": tier.name,
                "base_price": tier.base_price,
                "features": tier.features
            }
            for name, tier in pricing_engine.base_tiers.items()
        }
        
        return BaseResponse(
            success=True,
            message="Pricing tiers retrieved",
            data={"tiers": tiers}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
