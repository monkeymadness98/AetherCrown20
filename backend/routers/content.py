"""API endpoints for content marketing automation."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

from backend.content_marketing.content_generator import ContentGenerator, ContentType
from backend.content_marketing.ab_testing import ABTestingManager
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/content", tags=["content"])

# Initialize services
content_gen = ContentGenerator()
ab_testing = ABTestingManager()


# Request Models
class BlogPostRequest(BaseModel):
    topic: str
    keywords: List[str]
    tone: str = "professional"


class SocialPostRequest(BaseModel):
    campaign: str
    platform: str
    message: str
    hashtags: Optional[List[str]] = []


class ABTestRequest(BaseModel):
    name: str
    variants: List[Dict]
    test_type: str = "conversion"


# Endpoints
@router.post("/generate/blog")
async def generate_blog_post(request: BlogPostRequest):
    """Generate AI-powered blog post."""
    try:
        content = content_gen.generate_blog_post(
            request.topic,
            request.keywords,
            request.tone
        )
        
        return BaseResponse(
            success=True,
            message="Blog post generated",
            data={"content": content}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/social")
async def generate_social_post(request: SocialPostRequest):
    """Generate social media post optimized for platform."""
    try:
        content = content_gen.generate_social_media_post(
            request.campaign,
            request.platform,
            request.message,
            request.hashtags
        )
        
        return BaseResponse(
            success=True,
            message="Social media post generated",
            data={"content": content}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_content_metrics():
    """Get content generation metrics."""
    try:
        metrics = content_gen.get_content_metrics()
        
        return BaseResponse(
            success=True,
            message="Content metrics retrieved",
            data={"metrics": metrics}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ab-test/create")
async def create_ab_test(request: ABTestRequest):
    """Create new A/B test."""
    try:
        test = ab_testing.create_test(
            request.name,
            request.variants,
            request.test_type
        )
        
        return BaseResponse(
            success=True,
            message="A/B test created",
            data={
                "test_id": test.test_id,
                "name": test.name,
                "variants": [v["id"] for v in test.variants]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ab-test/{test_id}/results")
async def get_test_results(test_id: str):
    """Get A/B test results."""
    try:
        results = ab_testing.get_test_results(test_id)
        
        if not results:
            raise HTTPException(status_code=404, detail="Test not found")
        
        recommendations = ab_testing.generate_recommendations(test_id)
        results["recommendations"] = recommendations
        
        return BaseResponse(
            success=True,
            message="Test results retrieved",
            data={"results": results}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ab-test/active")
async def get_active_tests():
    """Get all active A/B tests."""
    try:
        tests = ab_testing.get_active_tests_summary()
        
        return BaseResponse(
            success=True,
            message="Active tests retrieved",
            data={"tests": tests}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ab-test/{test_id}/track")
async def track_conversion(test_id: str, variant_id: str):
    """Track conversion for A/B test variant."""
    try:
        ab_testing.track_conversion(test_id, variant_id)
        
        return BaseResponse(
            success=True,
            message="Conversion tracked",
            data={"test_id": test_id, "variant_id": variant_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
