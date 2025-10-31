"""API endpoints for multi-tenant management."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

from backend.multi_tenant.tenant_manager import TenantManager
from backend.models.base import BaseResponse

router = APIRouter(prefix="/api/v1/tenants", tags=["multi-tenant"])

# Initialize service
tenant_manager = TenantManager()


# Request Models
class TenantCreationRequest(BaseModel):
    name: str
    tier: str
    metadata: Optional[Dict] = {}


class TenantScaleRequest(BaseModel):
    new_tier: str


# Endpoints
@router.post("/create")
async def create_tenant(request: TenantCreationRequest):
    """Provision a new tenant with isolated resources."""
    try:
        tenant = tenant_manager.create_tenant({
            "name": request.name,
            "tier": request.tier,
            "metadata": request.metadata
        })
        
        return BaseResponse(
            success=True,
            message="Tenant provisioned successfully",
            data={"tenant": tenant}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: str):
    """Get tenant details."""
    try:
        if tenant_id not in tenant_manager.tenants:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        tenant = tenant_manager.tenants[tenant_id]
        
        return BaseResponse(
            success=True,
            message="Tenant retrieved",
            data={"tenant": tenant}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tenant_id}/scale")
async def scale_tenant(tenant_id: str, request: TenantScaleRequest):
    """Scale tenant to different tier."""
    try:
        tenant = tenant_manager.scale_tenant(tenant_id, request.new_tier)
        
        return BaseResponse(
            success=True,
            message="Tenant scaled successfully",
            data={"tenant": tenant}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tenant_id}/metrics")
async def get_tenant_metrics(tenant_id: str):
    """Get usage metrics for a tenant."""
    try:
        metrics = tenant_manager.get_tenant_metrics(tenant_id)
        
        return BaseResponse(
            success=True,
            message="Tenant metrics retrieved",
            data={"metrics": metrics}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def monitor_all_tenants():
    """Get monitoring summary for all tenants."""
    try:
        summary = tenant_manager.monitor_all_tenants()
        
        return BaseResponse(
            success=True,
            message="Tenant monitoring summary generated",
            data={"summary": summary}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
