"""Multi-tenant management and auto-provisioning."""
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TenantTier:
    """Tenant tier definitions."""
    STARTER = "starter"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"


class TenantManager:
    """Manage multi-tenant provisioning and isolation."""
    
    def __init__(self):
        self.tenants = {}
        self.resource_limits = {
            TenantTier.STARTER: {
                "max_users": 10,
                "storage_gb": 10,
                "api_calls_per_day": 1000,
                "ai_tasks_per_hour": 50,
                "dashboards": ["basic"],
                "features": ["core"]
            },
            TenantTier.GROWTH: {
                "max_users": 50,
                "storage_gb": 100,
                "api_calls_per_day": 10000,
                "ai_tasks_per_hour": 500,
                "dashboards": ["basic", "analytics"],
                "features": ["core", "advanced_analytics", "integrations"]
            },
            TenantTier.ENTERPRISE: {
                "max_users": -1,  # unlimited
                "storage_gb": 1000,
                "api_calls_per_day": 100000,
                "ai_tasks_per_hour": 5000,
                "dashboards": ["basic", "analytics", "executive", "custom"],
                "features": ["core", "advanced_analytics", "integrations", "custom_ai", "dedicated_support"]
            }
        }
    
    def create_tenant(self, tenant_data: Dict) -> Dict:
        """
        Provision a new tenant with isolated resources.
        
        Args:
            tenant_data: Tenant configuration and metadata
            
        Returns:
            Provisioned tenant details
        """
        tenant_id = f"tenant_{datetime.utcnow().timestamp()}"
        tenant_name = tenant_data.get("name")
        tier = tenant_data.get("tier", TenantTier.STARTER)
        
        if tier not in self.resource_limits:
            raise ValueError(f"Invalid tier: {tier}")
        
        # Provision resources
        resources = self._provision_resources(tenant_id, tier)
        
        # Create isolated environment
        environment = self._create_environment(tenant_id, tier)
        
        # Provision dashboards
        dashboards = self._provision_dashboards(tenant_id, tier)
        
        # Setup AI agents
        ai_agents = self._provision_ai_agents(tenant_id, tier)
        
        tenant = {
            "tenant_id": tenant_id,
            "name": tenant_name,
            "tier": tier,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "resources": resources,
            "environment": environment,
            "dashboards": dashboards,
            "ai_agents": ai_agents,
            "metadata": tenant_data.get("metadata", {})
        }
        
        self.tenants[tenant_id] = tenant
        
        logger.info(f"Provisioned tenant {tenant_name}: {tenant_id}")
        return tenant
    
    def _provision_resources(self, tenant_id: str, tier: str) -> Dict:
        """Allocate resources for tenant based on tier."""
        limits = self.resource_limits[tier]
        
        return {
            "database": {
                "schema": f"tenant_{tenant_id}",
                "connection_pool_size": 10 if tier == TenantTier.ENTERPRISE else 5,
                "backup_retention_days": 30 if tier == TenantTier.ENTERPRISE else 7
            },
            "storage": {
                "bucket": f"s3://tenants/{tenant_id}",
                "limit_gb": limits["storage_gb"],
                "used_gb": 0
            },
            "compute": {
                "ai_workers": 4 if tier == TenantTier.ENTERPRISE else 2,
                "api_rate_limit": limits["api_calls_per_day"],
                "task_throughput": limits["ai_tasks_per_hour"]
            },
            "network": {
                "subdomain": f"{tenant_id}.aethercrown.com",
                "custom_domain_allowed": tier == TenantTier.ENTERPRISE
            }
        }
    
    def _create_environment(self, tenant_id: str, tier: str) -> Dict:
        """Create isolated tenant environment."""
        return {
            "environment_id": f"env_{tenant_id}",
            "isolation_level": "schema" if tier != TenantTier.ENTERPRISE else "database",
            "api_endpoint": f"https://api.aethercrown.com/tenants/{tenant_id}",
            "data_region": "us-east-1",
            "encryption_enabled": True,
            "audit_logging": tier == TenantTier.ENTERPRISE
        }
    
    def _provision_dashboards(self, tenant_id: str, tier: str) -> List[Dict]:
        """Provision dashboards for tenant."""
        dashboards = []
        allowed = self.resource_limits[tier]["dashboards"]
        
        dashboard_configs = {
            "basic": {
                "name": "Basic Dashboard",
                "widgets": ["user_count", "api_usage", "system_health"]
            },
            "analytics": {
                "name": "Analytics Dashboard",
                "widgets": ["revenue_metrics", "growth_trends", "conversion_funnel"]
            },
            "executive": {
                "name": "Executive Dashboard",
                "widgets": ["kpi_summary", "revenue_forecast", "churn_analysis", "ai_performance"]
            },
            "custom": {
                "name": "Custom Dashboard",
                "widgets": ["custom_metrics", "integrations", "custom_reports"]
            }
        }
        
        for dashboard_type in allowed:
            if dashboard_type in dashboard_configs:
                config = dashboard_configs[dashboard_type]
                dashboards.append({
                    "id": f"{tenant_id}_{dashboard_type}",
                    "type": dashboard_type,
                    "name": config["name"],
                    "widgets": config["widgets"],
                    "url": f"https://app.aethercrown.com/{tenant_id}/dashboard/{dashboard_type}"
                })
        
        return dashboards
    
    def _provision_ai_agents(self, tenant_id: str, tier: str) -> List[Dict]:
        """Provision AI agents for tenant."""
        agents = []
        
        # Base agents for all tiers
        base_agents = [
            {"type": "task_scheduler", "name": "Task Optimization Agent"},
            {"type": "health_monitor", "name": "System Health Agent"}
        ]
        
        # Additional agents for higher tiers
        if tier in [TenantTier.GROWTH, TenantTier.ENTERPRISE]:
            base_agents.extend([
                {"type": "churn_predictor", "name": "Churn Prevention Agent"},
                {"type": "content_generator", "name": "Content Automation Agent"}
            ])
        
        if tier == TenantTier.ENTERPRISE:
            base_agents.extend([
                {"type": "custom_ml", "name": "Custom ML Agent"},
                {"type": "advanced_analytics", "name": "Advanced Analytics Agent"}
            ])
        
        for agent_config in base_agents:
            agents.append({
                "agent_id": f"{tenant_id}_{agent_config['type']}",
                "type": agent_config["type"],
                "name": agent_config["name"],
                "status": "active",
                "created_at": datetime.utcnow().isoformat()
            })
        
        return agents
    
    def scale_tenant(self, tenant_id: str, new_tier: str) -> Dict:
        """
        Scale tenant to different tier.
        
        Args:
            tenant_id: Tenant identifier
            new_tier: New tier to scale to
            
        Returns:
            Updated tenant configuration
        """
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant = self.tenants[tenant_id]
        old_tier = tenant["tier"]
        
        if old_tier == new_tier:
            return tenant
        
        logger.info(f"Scaling tenant {tenant_id} from {old_tier} to {new_tier}")
        
        # Update resources
        tenant["tier"] = new_tier
        tenant["resources"] = self._provision_resources(tenant_id, new_tier)
        tenant["dashboards"] = self._provision_dashboards(tenant_id, new_tier)
        tenant["ai_agents"] = self._provision_ai_agents(tenant_id, new_tier)
        tenant["scaled_at"] = datetime.utcnow().isoformat()
        
        return tenant
    
    def get_tenant_metrics(self, tenant_id: str) -> Dict:
        """Get usage metrics for a tenant."""
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant = self.tenants[tenant_id]
        tier = tenant["tier"]
        limits = self.resource_limits[tier]
        
        # Simulated usage data (in production, query from monitoring systems)
        return {
            "tenant_id": tenant_id,
            "tier": tier,
            "usage": {
                "users": {
                    "current": 8,
                    "limit": limits["max_users"],
                    "usage_percent": 80 if limits["max_users"] > 0 else 0
                },
                "storage": {
                    "used_gb": 7.5,
                    "limit_gb": limits["storage_gb"],
                    "usage_percent": 75
                },
                "api_calls": {
                    "today": 850,
                    "limit_per_day": limits["api_calls_per_day"],
                    "usage_percent": 85
                },
                "ai_tasks": {
                    "last_hour": 45,
                    "limit_per_hour": limits["ai_tasks_per_hour"],
                    "usage_percent": 90
                }
            },
            "health": {
                "status": "healthy",
                "uptime_percent": 99.9,
                "avg_response_time_ms": 125
            },
            "recommendations": self._generate_scaling_recommendations(tenant_id)
        }
    
    def _generate_scaling_recommendations(self, tenant_id: str) -> List[str]:
        """Generate scaling recommendations based on usage."""
        metrics = self.get_tenant_metrics(tenant_id)
        recommendations = []
        
        usage = metrics["usage"]
        
        # Check each resource
        for resource, data in usage.items():
            usage_percent = data.get("usage_percent", 0)
            
            if usage_percent > 90:
                recommendations.append(
                    f"⚠️ {resource.upper()} at {usage_percent}% - consider upgrading tier"
                )
            elif usage_percent > 75:
                recommendations.append(
                    f"⚡ {resource.upper()} at {usage_percent}% - approaching limit"
                )
        
        return recommendations
    
    def monitor_all_tenants(self) -> Dict:
        """Monitor all tenants and generate summary."""
        summary = {
            "total_tenants": len(self.tenants),
            "by_tier": {},
            "active": 0,
            "requires_attention": [],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        for tenant_id, tenant in self.tenants.items():
            tier = tenant["tier"]
            summary["by_tier"][tier] = summary["by_tier"].get(tier, 0) + 1
            
            if tenant["status"] == "active":
                summary["active"] += 1
            
            # Check if tenant needs attention
            metrics = self.get_tenant_metrics(tenant_id)
            if metrics["recommendations"]:
                summary["requires_attention"].append({
                    "tenant_id": tenant_id,
                    "name": tenant["name"],
                    "recommendations": metrics["recommendations"]
                })
        
        return summary
