"""A/B testing automation for campaigns and landing pages."""
from typing import Dict, List, Optional
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)


class ABTest:
    """Represents an A/B test experiment."""
    
    def __init__(self, test_id: str, name: str, variants: List[Dict]):
        self.test_id = test_id
        self.name = name
        self.variants = variants
        self.started_at = datetime.utcnow()
        self.status = "running"
        self.results = {v["id"]: {"impressions": 0, "conversions": 0} for v in variants}
    
    def record_impression(self, variant_id: str):
        """Record an impression for a variant."""
        if variant_id in self.results:
            self.results[variant_id]["impressions"] += 1
    
    def record_conversion(self, variant_id: str):
        """Record a conversion for a variant."""
        if variant_id in self.results:
            self.results[variant_id]["conversions"] += 1
    
    def get_conversion_rate(self, variant_id: str) -> float:
        """Calculate conversion rate for a variant."""
        if variant_id not in self.results:
            return 0.0
        
        impressions = self.results[variant_id]["impressions"]
        conversions = self.results[variant_id]["conversions"]
        
        return (conversions / impressions * 100) if impressions > 0 else 0.0
    
    def get_results(self) -> Dict:
        """Get test results with conversion rates."""
        results = {}
        
        for variant_id, data in self.results.items():
            results[variant_id] = {
                "impressions": data["impressions"],
                "conversions": data["conversions"],
                "conversion_rate": self.get_conversion_rate(variant_id)
            }
        
        return results


class ABTestingManager:
    """Manage A/B testing campaigns."""
    
    def __init__(self):
        self.active_tests = {}
        self.completed_tests = {}
        self.min_sample_size = 1000
        self.confidence_threshold = 0.95
    
    def create_test(self, name: str, variants: List[Dict], 
                   test_type: str = "conversion") -> ABTest:
        """
        Create a new A/B test.
        
        Args:
            name: Test name
            variants: List of variant configurations
            test_type: Type of test (conversion, engagement, revenue)
            
        Returns:
            ABTest instance
        """
        test_id = f"test_{datetime.utcnow().timestamp()}"
        
        # Validate variants
        if len(variants) < 2:
            raise ValueError("At least 2 variants required for A/B test")
        
        # Ensure variants have IDs
        for i, variant in enumerate(variants):
            if "id" not in variant:
                variant["id"] = f"variant_{chr(65 + i)}"  # A, B, C, etc.
        
        test = ABTest(test_id, name, variants)
        self.active_tests[test_id] = test
        
        logger.info(f"Created A/B test: {name} with {len(variants)} variants")
        return test
    
    def assign_variant(self, test_id: str, user_id: str) -> Optional[str]:
        """
        Assign a variant to a user for an A/B test.
        
        Uses random assignment for now. In production, use consistent hashing.
        """
        if test_id not in self.active_tests:
            logger.warning(f"Test {test_id} not found")
            return None
        
        test = self.active_tests[test_id]
        
        # Random assignment (in production, use consistent hashing by user_id)
        variant = random.choice(test.variants)
        variant_id = variant["id"]
        
        # Record impression
        test.record_impression(variant_id)
        
        return variant_id
    
    def track_conversion(self, test_id: str, variant_id: str):
        """Track a conversion for a test variant."""
        if test_id not in self.active_tests:
            logger.warning(f"Test {test_id} not found")
            return
        
        test = self.active_tests[test_id]
        test.record_conversion(variant_id)
        
        # Check if test should be auto-concluded
        self._check_test_conclusion(test_id)
    
    def _check_test_conclusion(self, test_id: str):
        """Check if test has enough data to conclude."""
        test = self.active_tests[test_id]
        
        # Check if minimum sample size reached
        total_impressions = sum(
            data["impressions"] 
            for data in test.results.values()
        )
        
        if total_impressions < self.min_sample_size:
            return
        
        # Check for statistical significance
        results = test.get_results()
        conversion_rates = [
            results[v_id]["conversion_rate"] 
            for v_id in results.keys()
        ]
        
        # Simple check: if one variant is clearly winning
        max_rate = max(conversion_rates)
        min_rate = min(conversion_rates)
        
        if max_rate > min_rate * 1.2:  # 20% improvement
            logger.info(f"Test {test_id} has significant results")
    
    def get_test_results(self, test_id: str) -> Optional[Dict]:
        """Get results for a specific test."""
        test = self.active_tests.get(test_id) or self.completed_tests.get(test_id)
        
        if not test:
            return None
        
        results = test.get_results()
        
        # Find winning variant
        winning_variant = max(
            results.items(),
            key=lambda x: x[1]["conversion_rate"]
        )
        
        # Calculate uplift
        conversion_rates = [r["conversion_rate"] for r in results.values()]
        baseline = min(conversion_rates)
        best = max(conversion_rates)
        uplift = ((best - baseline) / baseline * 100) if baseline > 0 else 0
        
        return {
            "test_id": test.test_id,
            "name": test.name,
            "status": test.status,
            "started_at": test.started_at.isoformat(),
            "variants": results,
            "winning_variant": {
                "id": winning_variant[0],
                "conversion_rate": winning_variant[1]["conversion_rate"]
            },
            "uplift_percent": uplift,
            "total_impressions": sum(r["impressions"] for r in results.values()),
            "total_conversions": sum(r["conversions"] for r in results.values())
        }
    
    def conclude_test(self, test_id: str, winning_variant_id: str) -> Dict:
        """
        Conclude an A/B test and select winner.
        
        Args:
            test_id: Test identifier
            winning_variant_id: ID of winning variant
            
        Returns:
            Final test results
        """
        if test_id not in self.active_tests:
            raise ValueError(f"Test {test_id} not found")
        
        test = self.active_tests[test_id]
        test.status = "completed"
        
        # Move to completed tests
        self.completed_tests[test_id] = test
        del self.active_tests[test_id]
        
        results = self.get_test_results(test_id)
        results["manually_selected_winner"] = winning_variant_id
        results["concluded_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Concluded test {test_id}, winner: {winning_variant_id}")
        return results
    
    def get_active_tests_summary(self) -> List[Dict]:
        """Get summary of all active tests."""
        summaries = []
        
        for test_id, test in self.active_tests.items():
            results = test.get_results()
            total_impressions = sum(r["impressions"] for r in results.values())
            
            summaries.append({
                "test_id": test_id,
                "name": test.name,
                "status": test.status,
                "variants_count": len(test.variants),
                "total_impressions": total_impressions,
                "progress_percent": min(
                    (total_impressions / self.min_sample_size * 100), 100
                ),
                "started_at": test.started_at.isoformat()
            })
        
        return summaries
    
    def generate_recommendations(self, test_id: str) -> List[str]:
        """Generate recommendations based on test results."""
        results = self.get_test_results(test_id)
        
        if not results:
            return ["Test not found"]
        
        recommendations = []
        
        # Check sample size
        if results["total_impressions"] < self.min_sample_size:
            recommendations.append(
                f"Continue test to reach minimum sample size of {self.min_sample_size}"
            )
        
        # Check uplift
        if results["uplift_percent"] > 20:
            recommendations.append(
                f"Strong positive result: {results['uplift_percent']:.1f}% uplift. "
                f"Consider concluding test and implementing winner."
            )
        elif results["uplift_percent"] < 5:
            recommendations.append(
                "Low uplift detected. Consider testing more different variants."
            )
        
        # Check individual variants
        for variant_id, variant_results in results["variants"].items():
            if variant_results["conversion_rate"] < 1:
                recommendations.append(
                    f"Variant {variant_id} has low conversion rate. "
                    "Consider removing or redesigning."
                )
        
        return recommendations
