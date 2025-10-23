"""Dynamic pricing engine based on usage, engagement, and enterprise size."""
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PricingTier:
    """Represents a pricing tier."""
    
    def __init__(self, name: str, base_price: float, features: List[str]):
        self.name = name
        self.base_price = base_price
        self.features = features


class DynamicPricingEngine:
    """Calculate optimized pricing based on multiple factors."""
    
    def __init__(self):
        self.base_tiers = {
            "starter": PricingTier("Starter", 29.0, ["basic_features", "email_support"]),
            "professional": PricingTier("Professional", 99.0, ["advanced_features", "priority_support", "api_access"]),
            "enterprise": PricingTier("Enterprise", 499.0, ["all_features", "dedicated_support", "sla", "custom_integration"])
        }
    
    def calculate_usage_multiplier(self, usage_data: Dict) -> float:
        """Calculate pricing multiplier based on usage patterns."""
        multiplier = 1.0
        
        # API calls factor
        api_calls = usage_data.get("api_calls", 0)
        if api_calls > 100000:
            multiplier *= 1.5
        elif api_calls > 50000:
            multiplier *= 1.3
        elif api_calls > 10000:
            multiplier *= 1.1
        
        # Storage factor
        storage_gb = usage_data.get("storage_gb", 0)
        if storage_gb > 1000:
            multiplier *= 1.4
        elif storage_gb > 500:
            multiplier *= 1.2
        elif storage_gb > 100:
            multiplier *= 1.1
        
        # User seats factor
        user_seats = usage_data.get("user_seats", 1)
        if user_seats > 100:
            multiplier *= 1.3
        elif user_seats > 50:
            multiplier *= 1.2
        elif user_seats > 10:
            multiplier *= 1.1
        
        return multiplier
    
    def calculate_engagement_discount(self, engagement_data: Dict) -> float:
        """Calculate discount based on engagement metrics."""
        discount = 0.0
        
        # High engagement gets discount to retain
        daily_active_rate = engagement_data.get("daily_active_rate", 0)
        if daily_active_rate > 0.8:
            discount += 0.05
        elif daily_active_rate > 0.6:
            discount += 0.03
        
        # Long-term commitment discount
        tenure_months = engagement_data.get("tenure_months", 0)
        if tenure_months > 24:
            discount += 0.10
        elif tenure_months > 12:
            discount += 0.05
        
        # Feature adoption discount
        feature_adoption_rate = engagement_data.get("feature_adoption_rate", 0)
        if feature_adoption_rate > 0.7:
            discount += 0.05
        
        return min(discount, 0.20)  # Max 20% discount
    
    def calculate_enterprise_multiplier(self, company_data: Dict) -> float:
        """Calculate multiplier based on enterprise size."""
        multiplier = 1.0
        
        # Company size
        employee_count = company_data.get("employee_count", 0)
        if employee_count > 10000:
            multiplier *= 2.0
        elif employee_count > 1000:
            multiplier *= 1.5
        elif employee_count > 100:
            multiplier *= 1.2
        
        # Revenue
        annual_revenue = company_data.get("annual_revenue", 0)
        if annual_revenue > 1000000000:  # $1B+
            multiplier *= 1.8
        elif annual_revenue > 100000000:  # $100M+
            multiplier *= 1.4
        elif annual_revenue > 10000000:  # $10M+
            multiplier *= 1.2
        
        return multiplier
    
    def calculate_dynamic_price(self, tier: str, usage_data: Dict,
                               engagement_data: Dict, company_data: Optional[Dict] = None) -> Dict:
        """
        Calculate dynamic price for a customer.
        
        Args:
            tier: Base pricing tier (starter, professional, enterprise)
            usage_data: Usage metrics
            engagement_data: Engagement metrics
            company_data: Company size data (optional)
            
        Returns:
            Dictionary with pricing breakdown
        """
        if tier not in self.base_tiers:
            raise ValueError(f"Invalid tier: {tier}")
        
        base_price = self.base_tiers[tier].base_price
        
        # Calculate multipliers and discounts
        usage_multiplier = self.calculate_usage_multiplier(usage_data)
        engagement_discount = self.calculate_engagement_discount(engagement_data)
        enterprise_multiplier = 1.0
        
        if company_data and tier == "enterprise":
            enterprise_multiplier = self.calculate_enterprise_multiplier(company_data)
        
        # Calculate final price
        adjusted_price = base_price * usage_multiplier * enterprise_multiplier
        discount_amount = adjusted_price * engagement_discount
        final_price = adjusted_price - discount_amount
        
        pricing = {
            "tier": tier,
            "base_price": base_price,
            "usage_multiplier": usage_multiplier,
            "enterprise_multiplier": enterprise_multiplier,
            "engagement_discount_percent": engagement_discount * 100,
            "adjusted_price": adjusted_price,
            "discount_amount": discount_amount,
            "final_price": final_price,
            "calculated_at": datetime.utcnow().isoformat(),
            "breakdown": {
                "base": base_price,
                "usage_adjustment": (usage_multiplier - 1) * base_price,
                "enterprise_adjustment": (enterprise_multiplier - 1) * adjusted_price / enterprise_multiplier if enterprise_multiplier > 1 else 0,
                "engagement_discount": -discount_amount
            }
        }
        
        logger.info(f"Calculated dynamic price for {tier}: ${final_price:.2f}")
        return pricing
    
    def recommend_tier(self, usage_data: Dict, company_data: Optional[Dict] = None) -> str:
        """Recommend appropriate pricing tier based on usage."""
        api_calls = usage_data.get("api_calls", 0)
        user_seats = usage_data.get("user_seats", 1)
        storage_gb = usage_data.get("storage_gb", 0)
        
        # Enterprise criteria
        if company_data:
            employee_count = company_data.get("employee_count", 0)
            if employee_count > 100 or user_seats > 50:
                return "enterprise"
        
        # Professional criteria
        if api_calls > 10000 or user_seats > 10 or storage_gb > 100:
            return "professional"
        
        # Default to starter
        return "starter"
    
    def calculate_upsell_opportunity(self, current_tier: str, usage_data: Dict) -> Optional[Dict]:
        """Identify upsell opportunities based on usage patterns."""
        recommended_tier = self.recommend_tier(usage_data)
        
        tier_order = ["starter", "professional", "enterprise"]
        current_index = tier_order.index(current_tier)
        recommended_index = tier_order.index(recommended_tier)
        
        if recommended_index > current_index:
            return {
                "current_tier": current_tier,
                "recommended_tier": recommended_tier,
                "reason": self._get_upsell_reason(usage_data),
                "potential_revenue_increase": (
                    self.base_tiers[recommended_tier].base_price - 
                    self.base_tiers[current_tier].base_price
                ),
                "confidence": "high" if recommended_index - current_index == 1 else "medium"
            }
        
        return None
    
    def _get_upsell_reason(self, usage_data: Dict) -> str:
        """Generate human-readable upsell reason."""
        reasons = []
        
        if usage_data.get("api_calls", 0) > 50000:
            reasons.append("high API usage")
        if usage_data.get("user_seats", 0) > 25:
            reasons.append("growing team size")
        if usage_data.get("storage_gb", 0) > 500:
            reasons.append("significant storage needs")
        
        return ", ".join(reasons) if reasons else "usage patterns suggest higher tier"
