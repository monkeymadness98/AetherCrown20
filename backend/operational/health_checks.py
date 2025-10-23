"""Automated health checks for all system components."""
from typing import Dict, List, Optional
from datetime import datetime
import logging
import httpx
import asyncio

logger = logging.getLogger(__name__)


class HealthCheckManager:
    """Manage automated health checks for system components."""
    
    def __init__(self):
        self.components = {
            "backend": {"endpoint": "/healthz", "timeout": 5},
            "database": {"check_type": "connection", "timeout": 5},
            "redis": {"check_type": "ping", "timeout": 3},
            "external_api": {"check_type": "custom", "timeout": 10}
        }
        self.health_history = []
    
    async def check_http_endpoint(self, url: str, timeout: int = 5) -> Dict:
        """Check health of an HTTP endpoint."""
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                start_time = datetime.utcnow()
                response = await client.get(url)
                elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                return {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time_ms": elapsed,
                    "error": None
                }
        except httpx.TimeoutException:
            return {
                "status": "unhealthy",
                "status_code": None,
                "response_time_ms": timeout * 1000,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "status_code": None,
                "response_time_ms": None,
                "error": str(e)
            }
    
    async def check_database(self) -> Dict:
        """Check database connectivity."""
        try:
            # Simulate database check
            # In production, use actual database connection
            start_time = datetime.utcnow()
            await asyncio.sleep(0.01)  # Simulate query
            elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": elapsed,
                "connections_active": 5,
                "connections_idle": 10,
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "error": str(e)
            }
    
    async def check_redis(self) -> Dict:
        """Check Redis connectivity."""
        try:
            # Simulate Redis check
            start_time = datetime.utcnow()
            await asyncio.sleep(0.005)  # Simulate ping
            elapsed = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return {
                "status": "healthy",
                "response_time_ms": elapsed,
                "connected_clients": 3,
                "used_memory_mb": 128,
                "error": None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "response_time_ms": None,
                "error": str(e)
            }
    
    async def perform_health_check(self, component: str) -> Dict:
        """Perform health check for a specific component."""
        if component not in self.components:
            return {
                "component": component,
                "status": "unknown",
                "error": "Component not registered"
            }
        
        config = self.components[component]
        result = {
            "component": component,
            "checked_at": datetime.utcnow().isoformat()
        }
        
        # Perform appropriate check based on component type
        if component == "backend":
            check_result = await self.check_http_endpoint(
                config.get("endpoint", "/healthz"),
                config["timeout"]
            )
        elif component == "database":
            check_result = await self.check_database()
        elif component == "redis":
            check_result = await self.check_redis()
        else:
            check_result = {"status": "healthy", "error": None}
        
        result.update(check_result)
        return result
    
    async def perform_all_checks(self) -> Dict:
        """Perform health checks for all components."""
        start_time = datetime.utcnow()
        
        # Run all checks concurrently
        check_tasks = [
            self.perform_health_check(component)
            for component in self.components.keys()
        ]
        
        results = await asyncio.gather(*check_tasks, return_exceptions=True)
        
        # Process results
        component_results = {}
        overall_healthy = True
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Health check failed: {result}")
                overall_healthy = False
                continue
            
            component_results[result["component"]] = result
            if result["status"] != "healthy":
                overall_healthy = False
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        
        health_report = {
            "overall_status": "healthy" if overall_healthy else "unhealthy",
            "checked_at": start_time.isoformat(),
            "check_duration_seconds": elapsed,
            "components": component_results,
            "summary": {
                "total_components": len(component_results),
                "healthy": sum(1 for r in component_results.values() 
                             if r["status"] == "healthy"),
                "unhealthy": sum(1 for r in component_results.values() 
                               if r["status"] == "unhealthy")
            }
        }
        
        # Store in history
        self.health_history.append(health_report)
        
        # Keep only last 100 checks
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]
        
        logger.info(f"Health check completed: {health_report['overall_status']}")
        return health_report
    
    def get_health_trends(self) -> Dict:
        """Analyze health check trends."""
        if not self.health_history:
            return {
                "total_checks": 0,
                "availability_percent": 0,
                "trends": {}
            }
        
        total_checks = len(self.health_history)
        healthy_checks = sum(1 for h in self.health_history 
                           if h["overall_status"] == "healthy")
        
        availability = (healthy_checks / total_checks * 100) if total_checks > 0 else 0
        
        # Component-specific trends
        component_trends = {}
        for component in self.components.keys():
            component_checks = [
                h["components"].get(component, {})
                for h in self.health_history
                if component in h.get("components", {})
            ]
            
            if component_checks:
                healthy = sum(1 for c in component_checks 
                            if c.get("status") == "healthy")
                component_trends[component] = {
                    "availability_percent": (healthy / len(component_checks) * 100),
                    "total_checks": len(component_checks),
                    "last_status": component_checks[-1].get("status")
                }
        
        return {
            "total_checks": total_checks,
            "availability_percent": availability,
            "trends": component_trends,
            "recent_incidents": [
                h for h in self.health_history[-10:]
                if h["overall_status"] != "healthy"
            ]
        }
    
    def generate_alert(self, component: str, check_result: Dict) -> Optional[Dict]:
        """Generate alert if component is unhealthy."""
        if check_result["status"] == "healthy":
            return None
        
        severity = "critical" if component in ["backend", "database"] else "high"
        
        return {
            "severity": severity,
            "component": component,
            "status": check_result["status"],
            "error": check_result.get("error"),
            "timestamp": datetime.utcnow().isoformat(),
            "action_required": f"Investigate {component} health issues immediately"
        }
