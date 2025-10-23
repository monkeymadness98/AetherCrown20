"""Executive summary dashboard with KPIs and metrics."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ExecutiveDashboard:
    """Generate executive-level summaries and KPIs."""
    
    def __init__(self):
        self.kpis = {}
    
    def calculate_revenue_metrics(self, revenue_data: List[Dict]) -> Dict:
        """Calculate revenue-related KPIs."""
        if not revenue_data:
            return {
                "total_revenue": 0,
                "mrr": 0,
                "arr": 0,
                "revenue_growth_rate": 0,
                "average_contract_value": 0
            }
        
        total_revenue = sum(d.get("amount", 0) for d in revenue_data)
        
        # Monthly Recurring Revenue
        monthly_revenue = [d for d in revenue_data 
                          if d.get("type") == "subscription"]
        mrr = sum(d.get("amount", 0) for d in monthly_revenue)
        arr = mrr * 12
        
        # Growth rate (comparing last 30 days to previous 30 days)
        now = datetime.utcnow()
        last_30_days = [d for d in revenue_data 
                       if datetime.fromisoformat(d.get("date")) > now - timedelta(days=30)]
        previous_30_days = [d for d in revenue_data 
                           if now - timedelta(days=60) < datetime.fromisoformat(d.get("date")) <= now - timedelta(days=30)]
        
        current_revenue = sum(d.get("amount", 0) for d in last_30_days)
        previous_revenue = sum(d.get("amount", 0) for d in previous_30_days)
        
        growth_rate = 0
        if previous_revenue > 0:
            growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100
        
        # Average contract value
        acv = total_revenue / len(revenue_data) if revenue_data else 0
        
        return {
            "total_revenue": total_revenue,
            "mrr": mrr,
            "arr": arr,
            "revenue_growth_rate": growth_rate,
            "average_contract_value": acv
        }
    
    def calculate_ai_metrics(self, task_data: List[Dict]) -> Dict:
        """Calculate AI task completion and performance metrics."""
        if not task_data:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "success_rate": 0,
                "avg_completion_time": 0,
                "tasks_per_hour": 0
            }
        
        total_tasks = len(task_data)
        completed = len([t for t in task_data if t.get("status") == "completed"])
        failed = len([t for t in task_data if t.get("status") == "failed"])
        
        success_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0
        
        # Average completion time
        completed_tasks = [t for t in task_data if t.get("status") == "completed" 
                          and t.get("completed_at") and t.get("started_at")]
        
        avg_time = 0
        if completed_tasks:
            total_time = sum(
                (datetime.fromisoformat(t["completed_at"]) - 
                 datetime.fromisoformat(t["started_at"])).total_seconds()
                for t in completed_tasks
            )
            avg_time = total_time / len(completed_tasks)
        
        # Tasks per hour
        if task_data:
            earliest = min(datetime.fromisoformat(t.get("created_at")) 
                          for t in task_data if t.get("created_at"))
            hours = (datetime.utcnow() - earliest).total_seconds() / 3600
            tasks_per_hour = total_tasks / hours if hours > 0 else 0
        else:
            tasks_per_hour = 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "success_rate": success_rate,
            "avg_completion_time": avg_time,
            "tasks_per_hour": tasks_per_hour
        }
    
    def calculate_system_health(self, health_data: Dict) -> Dict:
        """Calculate system health metrics."""
        return {
            "api_uptime": health_data.get("api_uptime", 100.0),
            "avg_response_time": health_data.get("avg_response_time_ms", 0),
            "error_rate": health_data.get("error_rate", 0),
            "active_users": health_data.get("active_users", 0),
            "cpu_usage": health_data.get("cpu_usage_percent", 0),
            "memory_usage": health_data.get("memory_usage_percent", 0),
            "database_connections": health_data.get("db_connections", 0)
        }
    
    def calculate_growth_kpis(self, user_data: List[Dict]) -> Dict:
        """Calculate user growth and acquisition metrics."""
        if not user_data:
            return {
                "total_users": 0,
                "new_users_last_30_days": 0,
                "user_growth_rate": 0,
                "trial_conversion_rate": 0,
                "churn_rate": 0
            }
        
        total_users = len(user_data)
        
        now = datetime.utcnow()
        new_users = len([u for u in user_data 
                        if datetime.fromisoformat(u.get("created_at")) > now - timedelta(days=30)])
        
        # Growth rate
        previous_total = len([u for u in user_data 
                             if datetime.fromisoformat(u.get("created_at")) <= now - timedelta(days=30)])
        growth_rate = 0
        if previous_total > 0:
            growth_rate = (new_users / previous_total) * 100
        
        # Trial conversion
        trial_users = [u for u in user_data if u.get("is_trial")]
        converted_users = [u for u in trial_users if u.get("converted_to_paid")]
        trial_conversion = (len(converted_users) / len(trial_users) * 100) if trial_users else 0
        
        # Churn rate
        churned_users = len([u for u in user_data if u.get("churned")])
        churn_rate = (churned_users / total_users * 100) if total_users > 0 else 0
        
        return {
            "total_users": total_users,
            "new_users_last_30_days": new_users,
            "user_growth_rate": growth_rate,
            "trial_conversion_rate": trial_conversion,
            "churn_rate": churn_rate
        }
    
    def generate_executive_summary(self, data: Dict) -> Dict:
        """
        Generate comprehensive executive summary.
        
        Args:
            data: Dictionary containing revenue_data, task_data, health_data, user_data
        """
        revenue_metrics = self.calculate_revenue_metrics(data.get("revenue_data", []))
        ai_metrics = self.calculate_ai_metrics(data.get("task_data", []))
        health_metrics = self.calculate_system_health(data.get("health_data", {}))
        growth_metrics = self.calculate_growth_kpis(data.get("user_data", []))
        
        # Overall health score
        health_score = self._calculate_overall_health(
            revenue_metrics, ai_metrics, health_metrics, growth_metrics
        )
        
        summary = {
            "generated_at": datetime.utcnow().isoformat(),
            "overall_health_score": health_score,
            "revenue": revenue_metrics,
            "ai_performance": ai_metrics,
            "system_health": health_metrics,
            "growth": growth_metrics,
            "alerts": self._generate_alerts(revenue_metrics, ai_metrics, health_metrics, growth_metrics),
            "recommendations": self._generate_recommendations(revenue_metrics, ai_metrics, health_metrics, growth_metrics)
        }
        
        logger.info(f"Generated executive summary with health score: {health_score}")
        return summary
    
    def _calculate_overall_health(self, revenue: Dict, ai: Dict, 
                                  health: Dict, growth: Dict) -> float:
        """Calculate overall health score (0-100)."""
        score = 100.0
        
        # Revenue health
        if revenue["revenue_growth_rate"] < 0:
            score -= 15
        elif revenue["revenue_growth_rate"] < 5:
            score -= 5
        
        # AI performance
        if ai["success_rate"] < 90:
            score -= 10
        elif ai["success_rate"] < 95:
            score -= 5
        
        # System health
        if health["api_uptime"] < 99:
            score -= 10
        if health["error_rate"] > 1:
            score -= 10
        
        # Growth health
        if growth["churn_rate"] > 5:
            score -= 10
        elif growth["churn_rate"] > 3:
            score -= 5
        
        return max(score, 0)
    
    def _generate_alerts(self, revenue: Dict, ai: Dict, 
                        health: Dict, growth: Dict) -> List[Dict]:
        """Generate alerts for critical issues."""
        alerts = []
        
        if revenue["revenue_growth_rate"] < 0:
            alerts.append({
                "severity": "critical",
                "category": "revenue",
                "message": f"Revenue declining at {abs(revenue['revenue_growth_rate']):.1f}%"
            })
        
        if ai["success_rate"] < 90:
            alerts.append({
                "severity": "high",
                "category": "ai_performance",
                "message": f"AI task success rate at {ai['success_rate']:.1f}%"
            })
        
        if health["api_uptime"] < 99:
            alerts.append({
                "severity": "critical",
                "category": "system_health",
                "message": f"API uptime below 99%: {health['api_uptime']:.2f}%"
            })
        
        if growth["churn_rate"] > 5:
            alerts.append({
                "severity": "high",
                "category": "churn",
                "message": f"High churn rate: {growth['churn_rate']:.1f}%"
            })
        
        return alerts
    
    def _generate_recommendations(self, revenue: Dict, ai: Dict, 
                                 health: Dict, growth: Dict) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if revenue["revenue_growth_rate"] < 5:
            recommendations.append("Focus on customer acquisition and upsell opportunities")
        
        if ai["success_rate"] < 95:
            recommendations.append("Review AI task failures and optimize error handling")
        
        if health["error_rate"] > 0.5:
            recommendations.append("Investigate and fix API errors to improve reliability")
        
        if growth["trial_conversion_rate"] < 20:
            recommendations.append("Improve onboarding experience to boost trial conversions")
        
        if growth["churn_rate"] > 3:
            recommendations.append("Implement retention campaigns for at-risk users")
        
        return recommendations
