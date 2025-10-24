"""
Health Check Components

Individual checker modules for different aspects of the system.
"""

import os
import logging
from typing import Dict, Any, Optional, Tuple
import httpx
import asyncio

logger = logging.getLogger(__name__)


class DeploymentChecker:
    """Check deployment health on Render and Vercel."""
    
    def __init__(self):
        self.render_api_key = os.getenv('RENDER_API_KEY')
        self.render_service_id = os.getenv('RENDER_SERVICE_ID')
        self.vercel_token = os.getenv('VERCEL_TOKEN')
        self.vercel_project_id = os.getenv('VERCEL_PROJECT_ID')
        
    async def check_render_deployment(self) -> Tuple[str, Dict[str, Any]]:
        """Check Render backend deployment status."""
        details = {'configured': False, 'api_accessible': False}
        
        if not self.render_api_key or not self.render_service_id:
            return 'unconfigured', {'error': 'Missing RENDER_API_KEY or RENDER_SERVICE_ID'}
        
        details['configured'] = True
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f'https://api.render.com/v1/services/{self.render_service_id}',
                    headers={'Authorization': f'Bearer {self.render_api_key}'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    details['api_accessible'] = True
                    details['service_name'] = data.get('service', {}).get('name')
                    details['service_type'] = data.get('service', {}).get('type')
                    details['suspended'] = data.get('service', {}).get('suspended')
                    return 'healthy' if not details.get('suspended') else 'suspended', details
                else:
                    details['error'] = f'API returned {response.status_code}'
                    return 'unhealthy', details
                    
        except Exception as e:
            details['error'] = str(e)
            return 'error', details
    
    async def check_backend_healthz(self, base_url: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Check backend /healthz endpoint."""
        if not base_url:
            base_url = os.getenv('BACKEND_URL', 'http://localhost:8000')
        
        details = {'url': f'{base_url}/healthz'}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f'{base_url}/healthz')
                
                if response.status_code == 200:
                    data = response.json()
                    details['response'] = data
                    details['ok'] = data.get('ok', False)
                    return 'healthy' if details['ok'] else 'unhealthy', details
                else:
                    details['status_code'] = response.status_code
                    return 'unhealthy', details
                    
        except Exception as e:
            details['error'] = str(e)
            return 'error', details
    
    async def check_vercel_deployment(self) -> Tuple[str, Dict[str, Any]]:
        """Check Vercel frontend deployment status."""
        details = {'configured': False}
        
        if not self.vercel_token or not self.vercel_project_id:
            return 'unconfigured', {'error': 'Missing VERCEL_TOKEN or VERCEL_PROJECT_ID'}
        
        details['configured'] = True
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f'https://api.vercel.com/v9/projects/{self.vercel_project_id}',
                    headers={'Authorization': f'Bearer {self.vercel_token}'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    details['project_name'] = data.get('name')
                    details['framework'] = data.get('framework')
                    return 'healthy', details
                else:
                    details['error'] = f'API returned {response.status_code}'
                    return 'unhealthy', details
                    
        except Exception as e:
            details['error'] = str(e)
            return 'error', details


class EnvironmentChecker:
    """Check and validate environment variables."""
    
    REQUIRED_VARS = [
        'DATABASE_URL',
        'PAYPAL_CLIENT_ID',
        'PAYPAL_SECRET',
        'RENDER_API_KEY',
        'RENDER_SERVICE_ID',
    ]
    
    OPTIONAL_VARS = [
        'VERCEL_TOKEN',
        'VERCEL_PROJECT_ID',
        'REDIS_URL',
        'SECRET_KEY',
    ]
    
    def check_env_vars(self) -> Dict[str, Any]:
        """Check if all required environment variables are set."""
        missing = []
        present = []
        optional_missing = []
        
        for var in self.REQUIRED_VARS:
            value = os.getenv(var)
            if value:
                present.append(var)
            else:
                missing.append(var)
        
        for var in self.OPTIONAL_VARS:
            if not os.getenv(var):
                optional_missing.append(var)
        
        return {
            'missing_required': missing,
            'present': present,
            'missing_optional': optional_missing,
            'all_required_present': len(missing) == 0
        }


class DatabaseChecker:
    """Check database connectivity and health."""
    
    async def check_database(self) -> Tuple[str, Dict[str, Any]]:
        """Check database connectivity."""
        db_url = os.getenv('DATABASE_URL')
        details = {'configured': False}
        
        if not db_url:
            return 'unconfigured', {'error': 'DATABASE_URL not set'}
        
        details['configured'] = True
        details['url_pattern'] = self._mask_url(db_url)
        
        try:
            # Try to import SQLAlchemy
            try:
                from sqlalchemy import create_engine, text
                from sqlalchemy.pool import NullPool
            except ImportError:
                details['error'] = 'SQLAlchemy not installed'
                return 'error', details
            
            # Create engine with minimal pooling for test
            engine = create_engine(db_url, poolclass=NullPool, connect_args={'connect_timeout': 5})
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text('SELECT 1'))
                result.fetchone()
                details['connection_successful'] = True
                return 'healthy', details
                
        except Exception as e:
            details['error'] = str(e)
            details['error_type'] = type(e).__name__
            return 'error', details
    
    @staticmethod
    def _mask_url(url: str) -> str:
        """Mask sensitive parts of database URL."""
        if '@' in url:
            parts = url.split('@')
            protocol_user = parts[0].split('://')
            if len(protocol_user) == 2:
                protocol = protocol_user[0]
                return f"{protocol}://***:***@{parts[1]}"
        return "***"


class PaymentChecker:
    """Check payment integration status."""
    
    async def check_paypal(self) -> Tuple[str, Dict[str, Any]]:
        """Check PayPal integration."""
        client_id = os.getenv('PAYPAL_CLIENT_ID')
        secret = os.getenv('PAYPAL_SECRET')
        mode = os.getenv('PAYPAL_MODE', 'sandbox')
        
        details = {
            'configured': False,
            'mode': mode
        }
        
        if not client_id or not secret:
            return 'unconfigured', {'error': 'Missing PAYPAL_CLIENT_ID or PAYPAL_SECRET'}
        
        details['configured'] = True
        details['client_id_present'] = bool(client_id)
        
        # Check if credentials format looks valid (basic validation)
        if len(client_id) > 10 and len(secret) > 10:
            details['credentials_format'] = 'valid'
            return 'configured', details
        else:
            details['credentials_format'] = 'invalid'
            return 'warning', details
    
    async def check_stripe(self) -> Tuple[str, Dict[str, Any]]:
        """Check Stripe integration."""
        api_key = os.getenv('STRIPE_API_KEY')
        
        details = {'configured': False}
        
        if not api_key:
            return 'unconfigured', {'error': 'STRIPE_API_KEY not set'}
        
        details['configured'] = True
        details['key_format'] = 'valid' if api_key.startswith('sk_') else 'invalid'
        
        return 'configured', details


class DependencyChecker:
    """Check and validate dependencies."""
    
    def check_python_dependencies(self, requirements_file: str = 'requirements.txt') -> Dict[str, Any]:
        """Check if Python dependencies are properly installed."""
        import subprocess
        
        results = {
            'file_exists': False,
            'outdated_packages': [],
            'issues': []
        }
        
        # Check if requirements file exists
        if not os.path.exists(requirements_file):
            results['issues'].append(f'{requirements_file} not found')
            return results
        
        results['file_exists'] = True
        
        try:
            # Check for outdated packages
            result = subprocess.run(
                ['pip', 'list', '--outdated', '--format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                import json
                outdated = json.loads(result.stdout)
                results['outdated_packages'] = [
                    {
                        'name': pkg['name'],
                        'current': pkg['version'],
                        'latest': pkg['latest_version']
                    }
                    for pkg in outdated
                ]
        except Exception as e:
            results['issues'].append(f'Error checking outdated packages: {str(e)}')
        
        return results


class UIChecker:
    """Check frontend UI components."""
    
    async def check_frontend_routes(self, base_url: Optional[str] = None) -> Dict[str, Any]:
        """Check if frontend routes are accessible."""
        if not base_url:
            base_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        
        routes = {
            '/': 'Home',
            '/dev': 'Dev Dashboard',
            '/live': 'Live Dashboard'
        }
        
        results = {}
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                for route, name in routes.items():
                    try:
                        response = await client.get(f'{base_url}{route}')
                        results[route] = {
                            'name': name,
                            'status_code': response.status_code,
                            'accessible': response.status_code == 200
                        }
                    except Exception as e:
                        results[route] = {
                            'name': name,
                            'error': str(e),
                            'accessible': False
                        }
        except Exception as e:
            return {'error': str(e)}
        
        return results
