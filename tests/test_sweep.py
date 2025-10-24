"""
Tests for Sweep Agent functionality
"""

import os
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.sweep import SweepAgent, SweepReport
from backend.sweep.checkers import (
    EnvironmentChecker,
    DeploymentChecker,
    DatabaseChecker,
    PaymentChecker
)


class TestSweepReport:
    """Test SweepReport functionality."""
    
    def test_report_initialization(self):
        """Test report initializes correctly."""
        report = SweepReport()
        assert report.timestamp is not None
        assert len(report.errors) == 0
        assert len(report.warnings) == 0
    
    def test_add_error(self):
        """Test adding errors to report."""
        report = SweepReport()
        report.add_error("Test error", can_auto_fix=True)
        
        assert len(report.errors) == 1
        assert report.errors[0]['message'] == "Test error"
        assert report.errors[0]['can_auto_fix'] is True
    
    def test_add_warning(self):
        """Test adding warnings to report."""
        report = SweepReport()
        report.add_warning("Test warning")
        
        assert len(report.warnings) == 1
        assert report.warnings[0]['message'] == "Test warning"
    
    def test_add_deployment_check(self):
        """Test adding deployment check results."""
        report = SweepReport()
        report.add_deployment_check('test_service', 'healthy', {'status': 'ok'})
        
        assert 'test_service' in report.deployment_status
        assert report.deployment_status['test_service']['status'] == 'healthy'
    
    def test_to_dict(self):
        """Test converting report to dictionary."""
        report = SweepReport()
        report.add_error("Error 1", can_auto_fix=True)
        report.add_warning("Warning 1")
        
        data = report.to_dict()
        
        assert 'timestamp' in data
        assert 'summary' in data
        assert data['summary']['total_errors'] == 1
        assert data['summary']['warnings'] == 1
    
    def test_to_json(self):
        """Test converting report to JSON."""
        report = SweepReport()
        report.add_error("Error 1")
        
        json_str = report.to_json()
        
        assert isinstance(json_str, str)
        assert 'Error 1' in json_str
    
    def test_to_markdown(self):
        """Test converting report to markdown."""
        report = SweepReport()
        report.add_error("Test error", can_auto_fix=False)
        report.add_warning("Test warning")
        
        markdown = report.to_markdown()
        
        assert '# AI Agent Sweep Report' in markdown
        assert 'Test error' in markdown
        assert 'Test warning' in markdown


class TestEnvironmentChecker:
    """Test EnvironmentChecker functionality."""
    
    def test_check_env_vars_missing(self):
        """Test checking missing environment variables."""
        # Clear environment variables for test
        for var in EnvironmentChecker.REQUIRED_VARS:
            os.environ.pop(var, None)
        
        checker = EnvironmentChecker()
        result = checker.check_env_vars()
        
        assert len(result['missing_required']) > 0
        assert result['all_required_present'] is False
    
    def test_check_env_vars_present(self):
        """Test checking present environment variables."""
        # Set required variables
        for var in EnvironmentChecker.REQUIRED_VARS:
            os.environ[var] = 'test_value'
        
        checker = EnvironmentChecker()
        result = checker.check_env_vars()
        
        assert len(result['present']) == len(EnvironmentChecker.REQUIRED_VARS)
        assert result['all_required_present'] is True
        
        # Clean up
        for var in EnvironmentChecker.REQUIRED_VARS:
            os.environ.pop(var, None)


class TestDeploymentChecker:
    """Test DeploymentChecker functionality."""
    
    @pytest.mark.asyncio
    async def test_check_render_unconfigured(self):
        """Test checking Render when not configured."""
        # Clear environment variables
        os.environ.pop('RENDER_API_KEY', None)
        os.environ.pop('RENDER_SERVICE_ID', None)
        
        checker = DeploymentChecker()
        status, details = await checker.check_render_deployment()
        
        assert status == 'unconfigured'
        assert 'error' in details
    
    @pytest.mark.asyncio
    async def test_check_vercel_unconfigured(self):
        """Test checking Vercel when not configured."""
        os.environ.pop('VERCEL_TOKEN', None)
        os.environ.pop('VERCEL_PROJECT_ID', None)
        
        checker = DeploymentChecker()
        status, details = await checker.check_vercel_deployment()
        
        assert status == 'unconfigured'
        assert 'error' in details


class TestDatabaseChecker:
    """Test DatabaseChecker functionality."""
    
    @pytest.mark.asyncio
    async def test_check_database_unconfigured(self):
        """Test checking database when not configured."""
        os.environ.pop('DATABASE_URL', None)
        
        checker = DatabaseChecker()
        status, details = await checker.check_database()
        
        assert status == 'unconfigured'
        assert 'error' in details
    
    def test_mask_url(self):
        """Test URL masking functionality."""
        url = "postgresql://user:password@localhost:5432/db"
        masked = DatabaseChecker._mask_url(url)
        
        assert 'password' not in masked
        assert '***' in masked


class TestPaymentChecker:
    """Test PaymentChecker functionality."""
    
    @pytest.mark.asyncio
    async def test_check_paypal_unconfigured(self):
        """Test checking PayPal when not configured."""
        os.environ.pop('PAYPAL_CLIENT_ID', None)
        os.environ.pop('PAYPAL_SECRET', None)
        
        checker = PaymentChecker()
        status, details = await checker.check_paypal()
        
        assert status == 'unconfigured'
        assert 'error' in details
    
    @pytest.mark.asyncio
    async def test_check_stripe_unconfigured(self):
        """Test checking Stripe when not configured."""
        os.environ.pop('STRIPE_API_KEY', None)
        
        checker = PaymentChecker()
        status, details = await checker.check_stripe()
        
        assert status == 'unconfigured'
        assert 'error' in details


class TestSweepAgent:
    """Test SweepAgent functionality."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test agent initializes correctly."""
        agent = SweepAgent(auto_fix=False)
        
        assert agent.auto_fix is False
        assert agent.report is not None
        assert agent.deployment_checker is not None
    
    @pytest.mark.asyncio
    async def test_run_full_sweep(self):
        """Test running full sweep."""
        agent = SweepAgent(auto_fix=False)
        report = await agent.run_full_sweep()
        
        assert report is not None
        assert isinstance(report, SweepReport)
        
        # Should have at least attempted some checks
        report_dict = report.to_dict()
        assert 'summary' in report_dict


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
