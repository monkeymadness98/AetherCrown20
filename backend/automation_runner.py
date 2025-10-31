#!/usr/bin/env python3
"""
Autonomous Automation Runner for AetherCrown20.

This script runs periodic automated tasks for optimization, monitoring,
and decision-making across the platform.
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List

from backend.ai_optimization.budget_optimizer import MarketingBudgetOptimizer
from backend.ai_optimization.churn_predictor import ChurnPredictor
from backend.ai_optimization.task_scheduler import TaskScheduler
from backend.operational.health_checks import HealthCheckManager
from backend.security.key_rotation import KeyRotationManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


class AutomationRunner:
    """Run autonomous optimization and monitoring tasks."""
    
    def __init__(self):
        self.budget_optimizer = MarketingBudgetOptimizer()
        self.churn_predictor = ChurnPredictor()
        self.task_scheduler = TaskScheduler()
        self.health_check = HealthCheckManager()
        self.key_rotation = KeyRotationManager()
        
        self.tasks = {
            "health_check": {"interval_hours": 1, "last_run": None},
            "budget_optimization": {"interval_hours": 24, "last_run": None},
            "churn_prediction": {"interval_hours": 12, "last_run": None},
            "task_scheduling": {"interval_hours": 1, "last_run": None},
            "key_rotation_check": {"interval_hours": 24, "last_run": None},
        }
    
    async def run_health_checks(self):
        """Run system health checks."""
        logger.info("Running health checks...")
        try:
            report = await self.health_check.perform_all_checks()
            
            if report["overall_status"] != "healthy":
                logger.warning(f"System unhealthy: {report['summary']}")
                # In production, trigger alerts
            else:
                logger.info("System health: OK")
            
            return report
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return None
    
    def run_budget_optimization(self, total_budget: float = 10000):
        """Run marketing budget optimization."""
        logger.info("Running budget optimization...")
        try:
            # In production, load actual historical data
            historical_data = [
                {"channel": "google_ads", "spend": 3000, "revenue": 9000},
                {"channel": "facebook_ads", "spend": 2000, "revenue": 5000},
                {"channel": "linkedin_ads", "spend": 1500, "revenue": 4500},
                {"channel": "content_marketing", "spend": 1000, "revenue": 3500},
                {"channel": "email_campaigns", "spend": 800, "revenue": 3200},
                {"channel": "seo", "spend": 700, "revenue": 2800},
            ]
            
            allocations = self.budget_optimizer.optimize_allocation(
                total_budget, historical_data
            )
            
            logger.info(f"Budget optimized: {allocations}")
            return allocations
        except Exception as e:
            logger.error(f"Budget optimization failed: {e}")
            return None
    
    def run_churn_prediction(self):
        """Run churn prediction and trigger campaigns."""
        logger.info("Running churn prediction...")
        try:
            # In production, load actual user data
            sample_users = [
                {
                    "user_id": "user_001",
                    "user_email": "user1@example.com",
                    "days_since_last_login": 25,
                    "total_sessions": 8,
                    "avg_session_duration": 6,
                    "feature_usage_count": 3,
                    "support_tickets": 2,
                    "payment_issues": False
                },
                {
                    "user_id": "user_002",
                    "user_email": "user2@example.com",
                    "days_since_last_login": 45,
                    "total_sessions": 3,
                    "avg_session_duration": 4,
                    "feature_usage_count": 2,
                    "support_tickets": 5,
                    "payment_issues": True
                }
            ]
            
            predictions = self.churn_predictor.predict_churn(sample_users)
            campaigns = self.churn_predictor.trigger_campaigns(predictions)
            
            logger.info(f"Churn prediction: {len(predictions)} users analyzed, "
                       f"{len(campaigns)} campaigns triggered")
            return {"predictions": predictions, "campaigns": campaigns}
        except Exception as e:
            logger.error(f"Churn prediction failed: {e}")
            return None
    
    def run_task_scheduling(self):
        """Optimize AI task scheduling."""
        logger.info("Running task scheduler optimization...")
        try:
            assignments = self.task_scheduler.assign_tasks()
            metrics = self.task_scheduler.get_metrics()
            bottlenecks = self.task_scheduler.identify_bottlenecks()
            
            logger.info(f"Task scheduling: {len(assignments)} tasks assigned, "
                       f"{len(bottlenecks)} bottlenecks identified")
            
            return {
                "assignments": assignments,
                "metrics": metrics,
                "bottlenecks": bottlenecks
            }
        except Exception as e:
            logger.error(f"Task scheduling failed: {e}")
            return None
    
    def run_key_rotation_check(self):
        """Check for keys due for rotation."""
        logger.info("Checking key rotation status...")
        try:
            report = self.key_rotation.get_rotation_report()
            
            if report["overdue"] > 0:
                logger.warning(f"{report['overdue']} keys overdue for rotation")
                # Auto-rotate overdue keys
                rotations = self.key_rotation.schedule_auto_rotation()
                logger.info(f"Auto-rotated {len(rotations)} keys")
                return {"report": report, "rotations": rotations}
            else:
                logger.info("All keys rotation status: OK")
                return {"report": report, "rotations": []}
        except Exception as e:
            logger.error(f"Key rotation check failed: {e}")
            return None
    
    def should_run_task(self, task_name: str) -> bool:
        """Check if a task should run based on interval."""
        task_config = self.tasks[task_name]
        
        if task_config["last_run"] is None:
            return True
        
        hours_since_last = (
            datetime.utcnow() - task_config["last_run"]
        ).total_seconds() / 3600
        
        return hours_since_last >= task_config["interval_hours"]
    
    async def run_all_tasks(self):
        """Run all automation tasks based on their schedules."""
        logger.info("=" * 60)
        logger.info("Starting automation runner cycle")
        logger.info("=" * 60)
        
        results = {}
        
        # Health checks
        if self.should_run_task("health_check"):
            results["health_check"] = await self.run_health_checks()
            self.tasks["health_check"]["last_run"] = datetime.utcnow()
        
        # Budget optimization
        if self.should_run_task("budget_optimization"):
            results["budget_optimization"] = self.run_budget_optimization()
            self.tasks["budget_optimization"]["last_run"] = datetime.utcnow()
        
        # Churn prediction
        if self.should_run_task("churn_prediction"):
            results["churn_prediction"] = self.run_churn_prediction()
            self.tasks["churn_prediction"]["last_run"] = datetime.utcnow()
        
        # Task scheduling
        if self.should_run_task("task_scheduling"):
            results["task_scheduling"] = self.run_task_scheduling()
            self.tasks["task_scheduling"]["last_run"] = datetime.utcnow()
        
        # Key rotation
        if self.should_run_task("key_rotation_check"):
            results["key_rotation_check"] = self.run_key_rotation_check()
            self.tasks["key_rotation_check"]["last_run"] = datetime.utcnow()
        
        logger.info("=" * 60)
        logger.info(f"Automation cycle completed: {len(results)} tasks run")
        logger.info("=" * 60)
        
        return results
    
    async def run_continuous(self, check_interval_minutes: int = 30):
        """Run automation continuously with specified check interval."""
        logger.info(f"Starting continuous automation with {check_interval_minutes}min check interval")
        
        while True:
            try:
                await self.run_all_tasks()
            except Exception as e:
                logger.error(f"Error in automation cycle: {e}")
            
            # Wait before next cycle
            await asyncio.sleep(check_interval_minutes * 60)


async def main():
    """Main entry point for automation runner."""
    runner = AutomationRunner()
    
    # Run once
    logger.info("Running one-shot automation tasks...")
    results = await runner.run_all_tasks()
    
    # Print summary
    print("\n" + "=" * 60)
    print("AUTOMATION SUMMARY")
    print("=" * 60)
    for task_name, result in results.items():
        status = "✅ Success" if result else "❌ Failed"
        print(f"{task_name}: {status}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
