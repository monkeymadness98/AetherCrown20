#!/usr/bin/env python3
"""
Demo script showcasing AetherCrown20 API usage.

This script demonstrates key features of the autonomous optimization platform.
"""
import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def call_api(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Make API call and return response."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def demo_budget_optimization():
    """Demonstrate marketing budget optimization."""
    print_section("Marketing Budget Optimization")
    
    data = {
        "total_budget": 10000,
        "historical_data": [
            {"channel": "google_ads", "spend": 3000, "revenue": 9000},
            {"channel": "facebook_ads", "spend": 2000, "revenue": 5000},
            {"channel": "linkedin_ads", "spend": 1500, "revenue": 4500},
            {"channel": "content_marketing", "spend": 1000, "revenue": 3500},
            {"channel": "email_campaigns", "spend": 800, "revenue": 3200},
            {"channel": "seo", "spend": 700, "revenue": 2800},
        ]
    }
    
    result = call_api("POST", "/api/v1/optimization/budget/optimize", data)
    
    if "data" in result:
        allocations = result["data"]["allocations"]
        print("\n✅ Budget Allocation:")
        for channel, amount in allocations.items():
            print(f"   {channel}: ${amount:.2f}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_churn_prediction():
    """Demonstrate churn prediction."""
    print_section("Churn Prediction & Retention Campaigns")
    
    data = {
        "users_data": [
            {
                "user_id": "user_001",
                "user_email": "john@example.com",
                "days_since_last_login": 25,
                "total_sessions": 8,
                "avg_session_duration": 6,
                "feature_usage_count": 3,
                "support_tickets": 2,
                "payment_issues": False
            },
            {
                "user_id": "user_002",
                "user_email": "jane@example.com",
                "days_since_last_login": 45,
                "total_sessions": 3,
                "avg_session_duration": 4,
                "feature_usage_count": 2,
                "support_tickets": 5,
                "payment_issues": True
            }
        ]
    }
    
    result = call_api("POST", "/api/v1/optimization/churn/predict", data)
    
    if "data" in result:
        summary = result["data"]["summary"]
        print(f"\n✅ Analyzed {summary['total_users']} users")
        print(f"   At-risk users: {summary['at_risk_users']}")
        print(f"   Critical risk: {summary['critical_risk_users']}")
        print(f"   Campaigns triggered: {summary['campaigns_triggered']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_investor_dashboard():
    """Demonstrate investor dashboard."""
    print_section("Investor Dashboard - Live KPIs")
    
    result = call_api("GET", "/api/v1/investor/dashboard/live?include_forecasts=false")
    
    if "data" in result:
        dashboard = result["data"]["dashboard"]
        kpis = dashboard["real_time_kpis"]
        
        print("\n📊 Real-Time KPIs:")
        print(f"   MRR: ${kpis['current_mrr']:,}")
        print(f"   ARR: ${kpis['arr']:,}")
        print(f"   Total Customers: {kpis['total_customers']}")
        print(f"   Active Users Now: {kpis['active_users_now']}")
        print(f"   System Uptime: {kpis['uptime_percent']}%")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_public_metrics():
    """Demonstrate public metrics endpoint."""
    print_section("Public Metrics")
    
    result = call_api("GET", "/api/v1/investor/metrics/public")
    
    if "data" in result:
        metrics = result["data"]["metrics"]["metrics"]
        
        print("\n🌍 Platform Statistics:")
        print(f"   Customers: {metrics['total_customers']}")
        print(f"   AI Tasks: {metrics['ai_tasks_completed']}")
        print(f"   Uptime: {metrics['system_uptime']}")
        print(f"   Countries: {metrics['countries_served']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_health_check():
    """Demonstrate operational health check."""
    print_section("System Health Check")
    
    result = call_api("GET", "/api/v1/operational/health/check")
    
    if "data" in result:
        report = result["data"]["report"]
        summary = report["summary"]
        
        print(f"\n🏥 System Status: {report['overall_status'].upper()}")
        print(f"   Total Components: {summary['total_components']}")
        print(f"   Healthy: {summary['healthy']}")
        print(f"   Unhealthy: {summary['unhealthy']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_dynamic_pricing():
    """Demonstrate dynamic pricing."""
    print_section("Dynamic Pricing Engine")
    
    data = {
        "tier": "professional",
        "usage_data": {
            "api_calls": 50000,
            "storage_gb": 250,
            "user_seats": 15
        },
        "engagement_data": {
            "daily_active_rate": 0.75,
            "tenure_months": 18,
            "feature_adoption_rate": 0.65
        }
    }
    
    result = call_api("POST", "/api/v1/revenue/pricing/calculate", data)
    
    if "data" in result:
        pricing = result["data"]["pricing"]
        
        print(f"\n💰 Pricing Calculation:")
        print(f"   Base Price: ${pricing['base_price']:.2f}")
        print(f"   Usage Multiplier: {pricing['usage_multiplier']:.2f}x")
        print(f"   Engagement Discount: {pricing['engagement_discount_percent']:.1f}%")
        print(f"   Final Price: ${pricing['final_price']:.2f}/month")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("  AetherCrown20 API Demo")
    print("  Autonomous Optimization & Decision-Making Platform")
    print("=" * 60)
    print("\n⚠️  Make sure the server is running:")
    print("   uvicorn backend.main:app --reload")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/healthz", timeout=2)
        if response.status_code == 200:
            print("✅ Server is running!\n")
        else:
            print("❌ Server returned error")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Run demos
    demo_budget_optimization()
    demo_churn_prediction()
    demo_dynamic_pricing()
    demo_health_check()
    demo_investor_dashboard()
    demo_public_metrics()
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\n📚 For more information, see:")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Automation Guide: AUTOMATION_GUIDE.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
