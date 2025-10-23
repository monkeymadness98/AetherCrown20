"""Marketing budget allocation optimizer using AI."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MarketingBudgetOptimizer:
    """Auto-allocates marketing budget to highest ROI channels."""
    
    def __init__(self):
        self.historical_data = []
        self.channels = [
            "google_ads", "facebook_ads", "linkedin_ads", 
            "content_marketing", "email_campaigns", "seo"
        ]
    
    def calculate_roi(self, channel: str, spend: float, revenue: float) -> float:
        """Calculate ROI for a channel."""
        if spend == 0:
            return 0.0
        return (revenue - spend) / spend * 100
    
    def analyze_channel_performance(self, historical_data: List[Dict]) -> Dict[str, float]:
        """Analyze historical performance of each channel."""
        channel_roi = {}
        
        for channel in self.channels:
            channel_data = [d for d in historical_data if d.get("channel") == channel]
            if not channel_data:
                channel_roi[channel] = 0.0
                continue
            
            total_spend = sum(d.get("spend", 0) for d in channel_data)
            total_revenue = sum(d.get("revenue", 0) for d in channel_data)
            channel_roi[channel] = self.calculate_roi(channel, total_spend, total_revenue)
        
        return channel_roi
    
    def optimize_allocation(self, total_budget: float, historical_data: List[Dict]) -> Dict[str, float]:
        """
        Optimize budget allocation across channels based on historical ROI.
        
        Args:
            total_budget: Total marketing budget to allocate
            historical_data: Historical performance data for channels
            
        Returns:
            Dictionary mapping channel to allocated budget
        """
        logger.info(f"Optimizing budget allocation for total budget: ${total_budget}")
        
        # Analyze channel performance
        channel_roi = self.analyze_channel_performance(historical_data)
        
        # Sort channels by ROI
        sorted_channels = sorted(channel_roi.items(), key=lambda x: x[1], reverse=True)
        
        # Allocate budget proportionally to ROI with minimum threshold
        min_allocation = total_budget * 0.05  # 5% minimum per channel
        allocations = {}
        remaining_budget = total_budget
        
        # Give minimum to all channels first
        for channel in self.channels:
            allocations[channel] = min_allocation
            remaining_budget -= min_allocation
        
        # Distribute remaining budget based on ROI
        total_roi = sum(max(roi, 0) for _, roi in sorted_channels)
        
        if total_roi > 0:
            for channel, roi in sorted_channels:
                if roi > 0:
                    additional = (roi / total_roi) * remaining_budget
                    allocations[channel] += additional
        else:
            # If no positive ROI, distribute evenly
            equal_share = remaining_budget / len(self.channels)
            for channel in self.channels:
                allocations[channel] += equal_share
        
        logger.info(f"Budget allocation optimized: {allocations}")
        return allocations
    
    def get_recommendations(self, allocations: Dict[str, float], 
                           channel_roi: Dict[str, float]) -> List[Dict]:
        """Generate actionable recommendations based on allocations."""
        recommendations = []
        
        for channel, allocation in allocations.items():
            roi = channel_roi.get(channel, 0)
            
            if roi > 50:
                recommendations.append({
                    "channel": channel,
                    "action": "increase",
                    "reason": f"High ROI of {roi:.2f}%",
                    "suggested_allocation": allocation * 1.2
                })
            elif roi < 10:
                recommendations.append({
                    "channel": channel,
                    "action": "decrease",
                    "reason": f"Low ROI of {roi:.2f}%",
                    "suggested_allocation": allocation * 0.8
                })
            else:
                recommendations.append({
                    "channel": channel,
                    "action": "maintain",
                    "reason": f"Moderate ROI of {roi:.2f}%",
                    "suggested_allocation": allocation
                })
        
        return recommendations
