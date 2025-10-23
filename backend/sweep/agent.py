"""
Main Sweep Agent

Orchestrates all health checks and auto-fix operations.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any
from .report import SweepReport
from .checkers import (
    DeploymentChecker,
    EnvironmentChecker,
    DatabaseChecker,
    PaymentChecker,
    DependencyChecker,
    UIChecker
)
from .fixers import AutoFixer

logger = logging.getLogger(__name__)


class SweepAgent:
    """Main agent for running sweep operations."""
    
    def __init__(self, auto_fix: bool = False):
        """
        Initialize sweep agent.
        
        Args:
            auto_fix: If True, attempt to auto-fix issues when possible
        """
        self.auto_fix = auto_fix
        self.report = SweepReport()
        
        # Initialize checkers
        self.deployment_checker = DeploymentChecker()
        self.env_checker = EnvironmentChecker()
        self.db_checker = DatabaseChecker()
        self.payment_checker = PaymentChecker()
        self.dependency_checker = DependencyChecker()
        self.ui_checker = UIChecker()
        
        # Initialize fixer
        self.fixer = AutoFixer() if auto_fix else None
    
    async def run_full_sweep(self) -> SweepReport:
        """Run complete sweep of all systems."""
        logger.info("Starting full system sweep...")
        
        # Run all checks
        await self._check_deployments()
        await self._check_environment()
        await self._check_dependencies()
        await self._check_database()
        await self._check_payments()
        await self._check_ui()
        await self._check_ai_agents()
        
        logger.info("Sweep completed. Generating report...")
        return self.report
    
    async def _check_deployments(self):
        """Check deployment status."""
        logger.info("Checking deployment status...")
        
        # Check Render backend
        status, details = await self.deployment_checker.check_render_deployment()
        self.report.add_deployment_check('render_backend', status, details)
        
        if status != 'healthy':
            self.report.add_error(
                f"Render deployment issue: {details.get('error', 'Unknown error')}",
                can_auto_fix=False
            )
        
        # Check backend healthz endpoint
        backend_url = os.getenv('BACKEND_URL')
        if backend_url:
            status, details = await self.deployment_checker.check_backend_healthz(backend_url)
            self.report.add_deployment_check('backend_healthz', status, details)
            
            if status != 'healthy':
                self.report.add_error(
                    f"Backend health check failed: {details.get('error', 'Unknown error')}",
                    can_auto_fix=False
                )
        else:
            self.report.add_warning("BACKEND_URL not set, skipping health check")
        
        # Check Vercel frontend
        status, details = await self.deployment_checker.check_vercel_deployment()
        self.report.add_deployment_check('vercel_frontend', status, details)
        
        if status != 'healthy':
            self.report.add_error(
                f"Vercel deployment issue: {details.get('error', 'Unknown error')}",
                can_auto_fix=False
            )
    
    async def _check_environment(self):
        """Check environment variables."""
        logger.info("Checking environment variables...")
        
        env_status = self.env_checker.check_env_vars()
        
        self.report.add_connection_check(
            'environment_variables',
            env_status['all_required_present'],
            env_status
        )
        
        if env_status['missing_required']:
            for var in env_status['missing_required']:
                self.report.add_error(
                    f"Required environment variable missing: {var}",
                    can_auto_fix=False
                )
        
        if env_status['missing_optional']:
            for var in env_status['missing_optional']:
                self.report.add_warning(f"Optional environment variable missing: {var}")
    
    async def _check_dependencies(self):
        """Check dependencies."""
        logger.info("Checking dependencies...")
        
        # Check backend dependencies
        backend_req = os.path.join('backend', 'requirements.txt')
        if os.path.exists(backend_req):
            dep_status = self.dependency_checker.check_python_dependencies(backend_req)
            
            if dep_status.get('outdated_packages'):
                self.report.add_warning(
                    f"Found {len(dep_status['outdated_packages'])} outdated packages"
                )
                
                if self.auto_fix and self.fixer:
                    success = await self.fixer.update_dependencies(dep_status['outdated_packages'])
                    self.report.add_fix(
                        f"Attempted to update {len(dep_status['outdated_packages'])} packages",
                        success
                    )
        
        # Check root requirements.txt
        root_req = 'requirements.txt'
        if os.path.exists(root_req):
            dep_status = self.dependency_checker.check_python_dependencies(root_req)
            
            if dep_status.get('issues'):
                for issue in dep_status['issues']:
                    self.report.add_warning(f"Dependency issue: {issue}")
    
    async def _check_database(self):
        """Check database connectivity."""
        logger.info("Checking database...")
        
        status, details = await self.db_checker.check_database()
        self.report.add_database_check(status, details)
        
        if status != 'healthy':
            self.report.add_error(
                f"Database issue: {details.get('error', 'Unknown error')}",
                can_auto_fix=False
            )
        else:
            self.report.add_connection_check('database', True, details)
    
    async def _check_payments(self):
        """Check payment integrations."""
        logger.info("Checking payment integrations...")
        
        # Check PayPal
        status, details = await self.payment_checker.check_paypal()
        self.report.add_payment_check('paypal', status, details)
        
        if status == 'unconfigured':
            self.report.add_warning("PayPal not configured")
        elif status == 'warning':
            self.report.add_warning(f"PayPal configuration issue: {details.get('error', 'Unknown')}")
        
        # Check Stripe
        status, details = await self.payment_checker.check_stripe()
        self.report.add_payment_check('stripe', status, details)
        
        if status == 'unconfigured':
            self.report.add_warning("Stripe not configured")
    
    async def _check_ui(self):
        """Check frontend UI."""
        logger.info("Checking UI components...")
        
        frontend_url = os.getenv('FRONTEND_URL')
        if frontend_url:
            routes = await self.ui_checker.check_frontend_routes(frontend_url)
            
            for route, data in routes.items():
                if isinstance(data, dict):
                    accessible = data.get('accessible', False)
                    self.report.add_ui_check(
                        f"route_{route}",
                        'healthy' if accessible else 'error',
                        data
                    )
                    
                    if not accessible:
                        self.report.add_error(
                            f"Frontend route {route} not accessible",
                            can_auto_fix=False
                        )
        else:
            self.report.add_warning("FRONTEND_URL not set, skipping UI checks")
            
        # Check static files
        static_files = ['index.html', 'app.js', 'style.css']
        for file in static_files:
            exists = os.path.exists(file)
            self.report.add_ui_check(
                f"static_file_{file}",
                'healthy' if exists else 'missing',
                {'exists': exists, 'path': file}
            )
            
            if not exists:
                self.report.add_warning(f"Static file missing: {file}")
    
    async def _check_ai_agents(self):
        """Check AI agent tasks status."""
        logger.info("Checking AI agent tasks...")
        
        # Check if empire automation is configured
        empire_enabled = os.getenv('EMPIRE_AUTOMATION_ENABLED', 'false').lower() == 'true'
        
        self.report.add_ai_agent_check(
            'empire_automation',
            empire_enabled,
            {
                'enabled': empire_enabled,
                'lock_file': os.path.exists('/tmp/empire_automation.lock')
            }
        )
        
        if not empire_enabled:
            self.report.add_warning("Empire automation is not enabled")
        
        # Check for lock file (indicates running or stalled process)
        lock_file = '/tmp/empire_automation.lock'
        if os.path.exists(lock_file):
            try:
                with open(lock_file, 'r') as f:
                    pid = f.read().strip()
                    
                # Check if process is still running
                try:
                    os.kill(int(pid), 0)
                    self.report.add_ai_agent_check(
                        'empire_automation_process',
                        True,
                        {'pid': pid, 'status': 'running'}
                    )
                except OSError:
                    # Process not running but lock exists
                    self.report.add_error(
                        f"Stale lock file found for PID {pid}",
                        can_auto_fix=True
                    )
                    
                    if self.auto_fix and self.fixer:
                        success = await self.fixer.remove_stale_lock(lock_file)
                        self.report.add_fix(f"Remove stale lock file {lock_file}", success)
            except Exception as e:
                self.report.add_warning(f"Error checking lock file: {str(e)}")
    
    def get_report(self) -> SweepReport:
        """Get the current report."""
        return self.report
    
    def print_report(self, format: str = 'markdown'):
        """Print the report in specified format."""
        if format == 'json':
            print(self.report.to_json())
        elif format == 'markdown':
            print(self.report.to_markdown())
        else:
            print(self.report.to_json())
