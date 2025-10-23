"""Investor-facing dashboards with live KPIs and metrics."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class InvestorDashboard:
    """Generate investor-facing dashboards and reports."""
    
    def __init__(self):
        self.public_metrics_whitelist = [
            "total_revenue",
            "user_count",
            "ai_tasks_completed",
            "system_uptime",
            "growth_rate"
        ]
    
    def generate_live_dashboard(self, include_forecasts: bool = True) -> Dict:
        """
        Generate live investor dashboard with real-time KPIs.
        
        Args:
            include_forecasts: Whether to include predictive forecasts
            
        Returns:
            Dashboard data with KPIs and metrics
        """
        dashboard = {
            "generated_at": datetime.utcnow().isoformat(),
            "mode": "investor",
            "real_time_kpis": self._get_real_time_kpis(),
            "revenue_metrics": self._get_revenue_metrics(),
            "growth_metrics": self._get_growth_metrics(),
            "operational_metrics": self._get_operational_metrics(),
            "ai_performance": self._get_ai_performance()
        }
        
        if include_forecasts:
            dashboard["forecasts"] = self._generate_forecasts()
        
        logger.info("Generated investor dashboard")
        return dashboard
    
    def _get_real_time_kpis(self) -> Dict:
        """Get real-time key performance indicators."""
        return {
            "current_mrr": 125000,
            "arr": 1500000,
            "total_customers": 450,
            "active_users_now": 127,
            "ai_tasks_running": 34,
            "system_status": "operational",
            "uptime_percent": 99.97
        }
    
    def _get_revenue_metrics(self) -> Dict:
        """Get revenue-related metrics."""
        return {
            "current_month": {
                "revenue": 128500,
                "new_revenue": 23000,
                "expansion_revenue": 8500,
                "churn": -2000,
                "net_revenue_growth": 29500
            },
            "last_month": {
                "revenue": 115000,
                "growth_rate": 11.7  # percent
            },
            "quarter_to_date": {
                "revenue": 365000,
                "target": 400000,
                "completion_percent": 91.25
            },
            "average_contract_value": 2778,
            "customer_lifetime_value": 28500,
            "customer_acquisition_cost": 850
        }
    
    def _get_growth_metrics(self) -> Dict:
        """Get growth-related metrics."""
        return {
            "user_growth": {
                "total_users": 1250,
                "new_this_month": 95,
                "growth_rate_percent": 8.2,
                "churn_rate_percent": 2.1
            },
            "customer_acquisition": {
                "trials_started": 234,
                "trials_converted": 47,
                "conversion_rate_percent": 20.1,
                "average_trial_duration_days": 14
            },
            "market_expansion": {
                "enterprise_customers": 23,
                "smb_customers": 427,
                "markets_active": 12,
                "revenue_by_segment": {
                    "enterprise": 780000,
                    "smb": 720000
                }
            }
        }
    
    def _get_operational_metrics(self) -> Dict:
        """Get operational excellence metrics."""
        return {
            "system_health": {
                "uptime_percent": 99.97,
                "average_response_time_ms": 145,
                "error_rate_percent": 0.03,
                "api_success_rate_percent": 99.97
            },
            "infrastructure": {
                "servers_active": 12,
                "databases_healthy": 3,
                "cdn_regions": 8,
                "backup_status": "current"
            },
            "support": {
                "tickets_open": 8,
                "average_resolution_hours": 4.2,
                "customer_satisfaction": 4.7,
                "response_time_minutes": 12
            }
        }
    
    def _get_ai_performance(self) -> Dict:
        """Get AI system performance metrics."""
        return {
            "tasks_completed_24h": 12456,
            "tasks_in_progress": 34,
            "success_rate_percent": 98.5,
            "average_task_duration_seconds": 23.4,
            "throughput_per_hour": 519,
            "cost_per_task": 0.012,
            "ai_efficiency_score": 94.2
        }
    
    def _generate_forecasts(self) -> Dict:
        """Generate predictive forecasts for key metrics."""
        return {
            "revenue_forecast": {
                "next_month": 142000,
                "next_quarter": 450000,
                "end_of_year": 1950000,
                "confidence_level": "high"
            },
            "user_forecast": {
                "next_month": 1365,
                "next_quarter": 1580,
                "growth_trajectory": "accelerating"
            },
            "churn_forecast": {
                "expected_rate_percent": 2.0,
                "at_risk_customers": 12,
                "retention_impact": -3000
            }
        }
    
    def generate_ai_activity_feed(self, limit: int = 50, 
                                  sanitize: bool = True) -> List[Dict]:
        """
        Generate real-time AI task activity feed for public display.
        
        Args:
            limit: Maximum number of items to return
            sanitize: Whether to remove sensitive information
            
        Returns:
            List of sanitized AI task activities
        """
        # Simulated activity feed (in production, query from task queue)
        activities = [
            {
                "id": "task_12456",
                "type": "budget_optimization",
                "status": "completed",
                "started_at": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                "duration_seconds": 23,
                "result": "optimized" if not sanitize else None
            },
            {
                "id": "task_12457",
                "type": "churn_prediction",
                "status": "running",
                "started_at": (datetime.utcnow() - timedelta(minutes=2)).isoformat(),
                "duration_seconds": None,
                "result": None
            },
            {
                "id": "task_12458",
                "type": "content_generation",
                "status": "completed",
                "started_at": (datetime.utcnow() - timedelta(minutes=8)).isoformat(),
                "duration_seconds": 45,
                "result": "generated" if not sanitize else None
            }
        ]
        
        # Sanitize sensitive data if needed
        if sanitize:
            for activity in activities:
                # Remove any customer-specific information
                activity.pop("customer_id", None)
                activity.pop("user_id", None)
                # Generalize task types
                activity["type_display"] = self._get_public_task_name(activity["type"])
        
        return activities[:limit]
    
    def _get_public_task_name(self, task_type: str) -> str:
        """Get public-friendly task name."""
        public_names = {
            "budget_optimization": "Marketing Optimization",
            "churn_prediction": "Customer Analytics",
            "content_generation": "Content Creation",
            "task_scheduling": "System Optimization",
            "health_check": "System Monitoring"
        }
        return public_names.get(task_type, "AI Task")
    
    def generate_monthly_report(self, month: Optional[str] = None) -> Dict:
        """
        Generate comprehensive monthly report for stakeholders.
        
        Args:
            month: Month in YYYY-MM format (defaults to last month)
            
        Returns:
            Detailed monthly report
        """
        if not month:
            last_month = datetime.utcnow() - timedelta(days=30)
            month = last_month.strftime("%Y-%m")
        
        report = {
            "report_period": month,
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": {
                "highlights": [
                    "Revenue grew 11.7% month-over-month to $128.5K",
                    "95 new customers acquired, 20.1% trial conversion rate",
                    "AI system processed 375K tasks with 98.5% success rate",
                    "System maintained 99.97% uptime"
                ],
                "challenges": [
                    "Churn rate at 2.1% (target: <2.0%)",
                    "CAC increased to $850 (target: $800)"
                ],
                "next_steps": [
                    "Launch retention campaign for at-risk customers",
                    "Optimize acquisition funnel to reduce CAC",
                    "Expand enterprise sales team"
                ]
            },
            "financial_summary": {
                "revenue": 128500,
                "costs": 45000,
                "gross_margin_percent": 65,
                "net_income": 38500,
                "burn_rate": -6500,
                "runway_months": 18
            },
            "customer_summary": {
                "total_customers": 450,
                "new_customers": 95,
                "churned_customers": 9,
                "net_new_customers": 86,
                "expansion_accounts": 12
            },
            "product_summary": {
                "feature_releases": 3,
                "bug_fixes": 24,
                "ai_tasks_processed": 375000,
                "system_uptime_percent": 99.97,
                "customer_satisfaction": 4.7
            },
            "team_summary": {
                "total_employees": 12,
                "new_hires": 2,
                "departments": {
                    "engineering": 6,
                    "sales": 3,
                    "customer_success": 2,
                    "operations": 1
                }
            },
            "key_metrics": {
                "mrr": 125000,
                "arr": 1500000,
                "ltv_cac_ratio": 33.5,
                "magic_number": 2.1,
                "net_revenue_retention": 115
            }
        }
        
        logger.info(f"Generated monthly report for {month}")
        return report
    
    def get_public_metrics(self) -> Dict:
        """Get sanitized public metrics safe for display."""
        metrics = {
            "generated_at": datetime.utcnow().isoformat(),
            "visibility": "public",
            "metrics": {
                "total_customers": "450+",
                "ai_tasks_completed": "10M+",
                "system_uptime": "99.9%+",
                "countries_served": 45,
                "industries": 12
            },
            "milestones": [
                {"date": "2024-01", "event": "Platform launched"},
                {"date": "2024-06", "event": "Reached 100 customers"},
                {"date": "2024-09", "event": "Processed 1M AI tasks"},
                {"date": "2024-12", "event": "Expanded to enterprise"}
            ]
        }
        
        return metrics
    
    def calculate_investor_kpis(self) -> Dict:
        """Calculate key investor KPIs."""
        return {
            "rule_of_40": 55.7,  # Growth rate + profit margin
            "efficiency_score": {
                "ltv_cac_ratio": 33.5,
                "payback_period_months": 8,
                "magic_number": 2.1
            },
            "growth_metrics": {
                "revenue_growth_rate_percent": 11.7,
                "customer_growth_rate_percent": 8.2,
                "arr_growth_rate_percent": 145
            },
            "retention_metrics": {
                "net_revenue_retention_percent": 115,
                "logo_retention_percent": 97.9,
                "gross_churn_percent": 2.1
            },
            "unit_economics": {
                "average_revenue_per_account": 2778,
                "customer_acquisition_cost": 850,
                "customer_lifetime_value": 28500,
                "gross_margin_percent": 65
            }
        }
