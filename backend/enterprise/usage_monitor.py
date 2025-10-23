"""Monitor enterprise usage and trigger upsell opportunities."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class UsageMonitor:
    """Monitor enterprise client usage and identify upsell opportunities."""
    
    def __init__(self):
        self.usage_thresholds = {
            "api_calls": {"warning": 0.8, "critical": 0.95},
            "storage": {"warning": 0.75, "critical": 0.90},
            "compute_units": {"warning": 0.80, "critical": 0.95},
            "user_seats": {"warning": 0.90, "critical": 0.98}
        }
    
    def track_usage(self, client_id: str, usage_data: Dict) -> Dict:
        """
        Track client usage metrics.
        
        Args:
            client_id: Enterprise client identifier
            usage_data: Current usage metrics
            
        Returns:
            Usage summary with alerts
        """
        limits = usage_data.get("limits", {})
        current = usage_data.get("current", {})
        
        usage_percentages = {}
        alerts = []
        
        for metric, values in self.usage_thresholds.items():
            if metric not in limits or metric not in current:
                continue
            
            limit = limits[metric]
            used = current[metric]
            
            if limit > 0:
                percentage = (used / limit) * 100
                usage_percentages[metric] = percentage
                
                # Generate alerts
                if percentage >= values["critical"] * 100:
                    alerts.append({
                        "severity": "critical",
                        "metric": metric,
                        "usage_percent": percentage,
                        "message": f"{metric} at {percentage:.1f}% capacity"
                    })
                elif percentage >= values["warning"] * 100:
                    alerts.append({
                        "severity": "warning",
                        "metric": metric,
                        "usage_percent": percentage,
                        "message": f"{metric} approaching limit at {percentage:.1f}%"
                    })
        
        summary = {
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat(),
            "usage_percentages": usage_percentages,
            "alerts": alerts,
            "requires_attention": len(alerts) > 0
        }
        
        logger.info(f"Tracked usage for {client_id}: {len(alerts)} alerts")
        return summary
    
    def identify_upsell_opportunities(self, client_id: str, 
                                     usage_history: List[Dict],
                                     current_tier: str) -> List[Dict]:
        """
        Identify upsell opportunities based on usage patterns.
        
        Args:
            client_id: Enterprise client identifier
            usage_history: Historical usage data
            current_tier: Current pricing tier
            
        Returns:
            List of upsell opportunities
        """
        opportunities = []
        
        # Analyze usage trends
        if len(usage_history) < 2:
            return opportunities
        
        # Calculate growth rates
        recent = usage_history[-1]["current"]
        previous = usage_history[0]["current"]
        
        growth_rates = {}
        for metric in ["api_calls", "storage", "user_seats"]:
            if metric in recent and metric in previous and previous[metric] > 0:
                growth = ((recent[metric] - previous[metric]) / previous[metric]) * 100
                growth_rates[metric] = growth
        
        # High API usage growth
        if growth_rates.get("api_calls", 0) > 50:
            opportunities.append({
                "type": "api_tier_upgrade",
                "confidence": "high",
                "reason": f"API usage growing at {growth_rates['api_calls']:.1f}%",
                "suggested_action": "Upgrade to higher API rate limit tier",
                "estimated_value": 500,  # Monthly additional revenue
                "priority": "high"
            })
        
        # Storage expansion needed
        if growth_rates.get("storage", 0) > 30:
            opportunities.append({
                "type": "storage_expansion",
                "confidence": "high",
                "reason": f"Storage usage growing at {growth_rates['storage']:.1f}%",
                "suggested_action": "Add storage expansion package",
                "estimated_value": 200,
                "priority": "medium"
            })
        
        # Team growth
        if growth_rates.get("user_seats", 0) > 20:
            opportunities.append({
                "type": "user_seat_expansion",
                "confidence": "medium",
                "reason": f"Team size growing at {growth_rates['user_seats']:.1f}%",
                "suggested_action": "Offer team expansion package",
                "estimated_value": 300,
                "priority": "medium"
            })
        
        # Check for consistent high usage
        avg_api_usage = sum(h["current"].get("api_calls", 0) 
                           for h in usage_history) / len(usage_history)
        avg_limit = sum(h["limits"].get("api_calls", 1) 
                       for h in usage_history) / len(usage_history)
        
        if avg_limit > 0 and (avg_api_usage / avg_limit) > 0.85:
            opportunities.append({
                "type": "tier_upgrade",
                "confidence": "high",
                "reason": "Consistently using over 85% of allocated resources",
                "suggested_action": f"Upgrade from {current_tier} to next tier",
                "estimated_value": 1000,
                "priority": "high"
            })
        
        logger.info(f"Identified {len(opportunities)} upsell opportunities for {client_id}")
        return opportunities
    
    def generate_usage_report(self, client_id: str, 
                             period_days: int = 30) -> Dict:
        """
        Generate comprehensive usage report for enterprise client.
        
        Args:
            client_id: Enterprise client identifier
            period_days: Reporting period in days
        """
        # In production, aggregate from database
        report = {
            "client_id": client_id,
            "report_period": f"{period_days} days",
            "generated_at": datetime.utcnow().isoformat(),
            "usage_summary": {
                "api_calls": {
                    "total": 487234,
                    "daily_average": 16241,
                    "peak_day": 23456,
                    "limit": 500000,
                    "usage_percent": 97.4
                },
                "storage": {
                    "total_gb": 847,
                    "limit_gb": 1000,
                    "usage_percent": 84.7,
                    "growth_gb": 123
                },
                "compute_units": {
                    "total": 4567,
                    "daily_average": 152,
                    "limit": 5000,
                    "usage_percent": 91.3
                },
                "user_seats": {
                    "active": 47,
                    "limit": 50,
                    "usage_percent": 94.0
                }
            },
            "cost_analysis": {
                "current_monthly_cost": 2499,
                "projected_next_month": 2850,
                "overage_charges": 0
            },
            "recommendations": [
                "Consider upgrading to next tier to avoid hitting limits",
                "Current growth rate suggests 100% capacity in 15 days",
                "Add 500GB storage expansion to accommodate growth"
            ],
            "health_score": 78,  # Out of 100
            "risk_level": "medium"
        }
        
        return report
    
    def trigger_upsell_campaign(self, client_id: str, 
                               opportunity: Dict) -> Dict:
        """
        Trigger automated upsell campaign for identified opportunity.
        
        Args:
            client_id: Enterprise client identifier
            opportunity: Upsell opportunity details
            
        Returns:
            Campaign configuration
        """
        campaign = {
            "campaign_id": f"upsell_{datetime.utcnow().timestamp()}",
            "client_id": client_id,
            "opportunity_type": opportunity["type"],
            "priority": opportunity["priority"],
            "created_at": datetime.utcnow().isoformat(),
            "actions": []
        }
        
        # Define campaign actions based on priority
        if opportunity["priority"] == "high":
            campaign["actions"] = [
                {
                    "type": "email",
                    "template": "enterprise_upsell_urgent",
                    "recipient": "account_owner",
                    "schedule": "immediate"
                },
                {
                    "type": "account_manager_notification",
                    "template": "high_value_upsell_opportunity",
                    "schedule": "immediate"
                },
                {
                    "type": "in_app_notification",
                    "template": "capacity_warning_upsell",
                    "schedule": "immediate"
                }
            ]
        else:
            campaign["actions"] = [
                {
                    "type": "email",
                    "template": "enterprise_upsell_standard",
                    "recipient": "account_owner",
                    "schedule": "next_business_day"
                },
                {
                    "type": "in_app_notification",
                    "template": "growth_opportunity",
                    "schedule": "immediate"
                }
            ]
        
        # Add follow-up sequence
        campaign["follow_up_sequence"] = [
            {"delay_days": 3, "action": "reminder_email"},
            {"delay_days": 7, "action": "account_manager_call"},
            {"delay_days": 14, "action": "final_reminder"}
        ]
        
        logger.info(f"Triggered upsell campaign for {client_id}: {campaign['campaign_id']}")
        return campaign
    
    def calculate_renewal_probability(self, client_id: str, 
                                     usage_data: Dict) -> Dict:
        """
        Calculate probability of contract renewal based on usage patterns.
        
        Args:
            client_id: Enterprise client identifier
            usage_data: Usage metrics and engagement data
        """
        score = 100.0
        factors = []
        
        # Usage activity score
        usage_percent = usage_data.get("average_usage_percent", 0)
        if usage_percent < 30:
            score -= 30
            factors.append("Low usage indicates potential churn risk")
        elif usage_percent > 80:
            score += 10
            factors.append("High usage indicates strong product-market fit")
        
        # Engagement score
        last_login_days = usage_data.get("days_since_last_login", 0)
        if last_login_days > 14:
            score -= 20
            factors.append("Inactive account - engagement required")
        
        # Support interaction score
        support_tickets = usage_data.get("support_tickets_30d", 0)
        if support_tickets > 10:
            score -= 15
            factors.append("High support volume may indicate issues")
        
        # Feature adoption score
        feature_adoption = usage_data.get("feature_adoption_rate", 0)
        if feature_adoption < 0.3:
            score -= 10
            factors.append("Low feature adoption")
        elif feature_adoption > 0.7:
            score += 10
            factors.append("Strong feature adoption")
        
        probability = max(min(score, 100), 0)
        
        return {
            "client_id": client_id,
            "renewal_probability": probability,
            "risk_level": "high" if probability < 50 else "medium" if probability < 75 else "low",
            "factors": factors,
            "recommended_actions": self._get_renewal_actions(probability),
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def _get_renewal_actions(self, probability: float) -> List[str]:
        """Get recommended actions based on renewal probability."""
        if probability < 50:
            return [
                "Schedule immediate executive review call",
                "Offer custom onboarding or training",
                "Consider contract incentives or discounts"
            ]
        elif probability < 75:
            return [
                "Schedule account review meeting",
                "Share success stories and best practices",
                "Highlight underutilized features"
            ]
        else:
            return [
                "Maintain regular check-ins",
                "Explore upsell opportunities",
                "Request testimonial or case study"
            ]
