"""Churn prediction and automated retention campaigns."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Predict user churn and trigger retention campaigns."""
    
    def __init__(self):
        self.churn_threshold = 0.7  # 70% probability threshold
        self.features = [
            "days_since_last_login",
            "total_sessions",
            "avg_session_duration",
            "feature_usage_count",
            "support_tickets",
            "payment_issues"
        ]
    
    def calculate_churn_score(self, user_data: Dict) -> float:
        """
        Calculate churn probability for a user.
        
        Simple scoring model based on engagement metrics.
        In production, this would use a trained ML model.
        """
        score = 0.0
        
        # Days since last login (higher = more likely to churn)
        days_inactive = user_data.get("days_since_last_login", 0)
        if days_inactive > 30:
            score += 0.3
        elif days_inactive > 14:
            score += 0.2
        elif days_inactive > 7:
            score += 0.1
        
        # Session frequency (lower = more likely to churn)
        total_sessions = user_data.get("total_sessions", 0)
        if total_sessions < 5:
            score += 0.2
        elif total_sessions < 10:
            score += 0.1
        
        # Average session duration (lower = more likely to churn)
        avg_duration = user_data.get("avg_session_duration", 0)  # in minutes
        if avg_duration < 5:
            score += 0.2
        elif avg_duration < 10:
            score += 0.1
        
        # Feature usage (lower = more likely to churn)
        feature_usage = user_data.get("feature_usage_count", 0)
        if feature_usage < 3:
            score += 0.15
        
        # Support tickets (higher = more likely to churn)
        support_tickets = user_data.get("support_tickets", 0)
        if support_tickets > 5:
            score += 0.15
        elif support_tickets > 2:
            score += 0.05
        
        # Payment issues (any = likely to churn)
        if user_data.get("payment_issues", False):
            score += 0.2
        
        return min(score, 1.0)
    
    def predict_churn(self, users_data: List[Dict]) -> List[Dict]:
        """
        Predict churn for multiple users.
        
        Returns list of users with churn probability and risk level.
        """
        predictions = []
        
        for user in users_data:
            churn_score = self.calculate_churn_score(user)
            
            risk_level = "low"
            if churn_score >= 0.7:
                risk_level = "critical"
            elif churn_score >= 0.5:
                risk_level = "high"
            elif churn_score >= 0.3:
                risk_level = "medium"
            
            predictions.append({
                "user_id": user.get("user_id"),
                "user_email": user.get("user_email"),
                "churn_probability": churn_score,
                "risk_level": risk_level,
                "predicted_at": datetime.utcnow().isoformat(),
                "factors": self._identify_churn_factors(user, churn_score)
            })
        
        logger.info(f"Predicted churn for {len(predictions)} users")
        return predictions
    
    def _identify_churn_factors(self, user_data: Dict, score: float) -> List[str]:
        """Identify key factors contributing to churn risk."""
        factors = []
        
        if user_data.get("days_since_last_login", 0) > 14:
            factors.append("inactive_user")
        if user_data.get("total_sessions", 0) < 10:
            factors.append("low_engagement")
        if user_data.get("support_tickets", 0) > 2:
            factors.append("support_issues")
        if user_data.get("payment_issues", False):
            factors.append("payment_problems")
        if user_data.get("feature_usage_count", 0) < 3:
            factors.append("limited_feature_adoption")
        
        return factors
    
    def generate_retention_campaign(self, churn_prediction: Dict) -> Dict:
        """
        Generate automated retention campaign based on churn prediction.
        
        Returns campaign configuration for the at-risk user.
        """
        risk_level = churn_prediction["risk_level"]
        factors = churn_prediction["factors"]
        
        campaign = {
            "user_id": churn_prediction["user_id"],
            "campaign_type": "retention",
            "priority": risk_level,
            "created_at": datetime.utcnow().isoformat(),
            "actions": []
        }
        
        # Critical risk: aggressive intervention
        if risk_level == "critical":
            campaign["actions"].extend([
                {"type": "email", "template": "critical_retention_offer", "discount": 30},
                {"type": "sms", "template": "urgent_check_in"},
                {"type": "personal_outreach", "assign_to": "customer_success_manager"}
            ])
        
        # High risk: moderate intervention
        elif risk_level == "high":
            campaign["actions"].extend([
                {"type": "email", "template": "re_engagement_offer", "discount": 20},
                {"type": "in_app_message", "template": "feature_highlights"}
            ])
        
        # Medium risk: gentle nudge
        elif risk_level == "medium":
            campaign["actions"].extend([
                {"type": "email", "template": "gentle_reminder"},
                {"type": "in_app_notification", "template": "new_features"}
            ])
        
        # Add factor-specific actions
        if "payment_problems" in factors:
            campaign["actions"].append({
                "type": "email",
                "template": "payment_assistance",
                "priority": "high"
            })
        
        if "support_issues" in factors:
            campaign["actions"].append({
                "type": "support_ticket",
                "template": "proactive_support_outreach"
            })
        
        if "limited_feature_adoption" in factors:
            campaign["actions"].append({
                "type": "onboarding_email",
                "template": "feature_education_series"
            })
        
        logger.info(f"Generated retention campaign for user {campaign['user_id']}")
        return campaign
    
    def trigger_campaigns(self, predictions: List[Dict]) -> List[Dict]:
        """Trigger retention campaigns for at-risk users."""
        campaigns = []
        
        for prediction in predictions:
            # Only trigger for medium risk and above
            if prediction["risk_level"] in ["medium", "high", "critical"]:
                campaign = self.generate_retention_campaign(prediction)
                campaigns.append(campaign)
        
        logger.info(f"Triggered {len(campaigns)} retention campaigns")
        return campaigns
