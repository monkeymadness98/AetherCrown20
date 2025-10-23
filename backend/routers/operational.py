"""API endpoints for operational automation."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.operational.health_checks import HealthCheckManager
from backend.security.key_rotation import KeyRotationManager
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/operational", tags=["operational"])

# Initialize services
health_check = HealthCheckManager()
key_rotation = KeyRotationManager()


# Request Models
class KeyRegistrationRequest(BaseModel):
    key_id: str
    key_type: str
    security_level: str = "medium"


# Endpoints
@router.get("/health/check")
async def perform_health_check():
    """Perform health checks for all system components."""
    try:
        report = await health_check.perform_all_checks()
        
        return BaseResponse(
            success=True,
            message="Health check completed",
            data={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/trends")
async def get_health_trends():
    """Get health check trends and analytics."""
    try:
        trends = health_check.get_health_trends()
        
        return BaseResponse(
            success=True,
            message="Health trends retrieved",
            data={"trends": trends}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/keys/register")
async def register_key(request: KeyRegistrationRequest):
    """Register a key for rotation tracking."""
    try:
        key_info = key_rotation.register_key(
            request.key_id,
            request.key_type,
            request.security_level
        )
        
        return BaseResponse(
            success=True,
            message="Key registered for rotation",
            data={"key_info": key_info}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/security/keys/due-rotation")
async def get_keys_due_rotation():
    """Get keys that are due for rotation."""
    try:
        due_keys = key_rotation.get_keys_due_for_rotation()
        
        return BaseResponse(
            success=True,
            message="Retrieved keys due for rotation",
            data={
                "due_keys": due_keys,
                "count": len(due_keys)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/keys/{key_id}/rotate")
async def rotate_key(key_id: str):
    """Rotate a specific key."""
    try:
        rotation = key_rotation.rotate_key(key_id)
        
        return BaseResponse(
            success=True,
            message="Key rotated successfully",
            data={"rotation": rotation}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/keys/auto-rotate")
async def auto_rotate_keys():
    """Automatically rotate all keys due for rotation."""
    try:
        rotations = key_rotation.schedule_auto_rotation()
        
        return BaseResponse(
            success=True,
            message="Auto-rotation completed",
            data={
                "rotations": rotations,
                "count": len(rotations)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/security/keys/report")
async def get_rotation_report():
    """Get key rotation status report."""
    try:
        report = key_rotation.get_rotation_report()
        
        return BaseResponse(
            success=True,
            message="Rotation report generated",
            data={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
