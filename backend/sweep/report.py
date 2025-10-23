"""
Sweep Report Generator

Generates comprehensive reports summarizing all sweep operations.
"""

from datetime import datetime, timezone
from typing import Dict, List, Any
import json


class SweepReport:
    """Generate and format sweep operation reports."""
    
    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.deployment_status = {}
        self.connection_health = {}
        self.ai_agent_status = {}
        self.database_status = {}
        self.payment_status = {}
        self.ui_status = {}
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        
    def add_deployment_check(self, service: str, status: str, details: Dict[str, Any]):
        """Add deployment check results."""
        self.deployment_status[service] = {
            'status': status,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_connection_check(self, connection: str, healthy: bool, details: Dict[str, Any]):
        """Add connection health check results."""
        self.connection_health[connection] = {
            'healthy': healthy,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_ai_agent_check(self, agent: str, running: bool, details: Dict[str, Any]):
        """Add AI agent status check results."""
        self.ai_agent_status[agent] = {
            'running': running,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_database_check(self, status: str, details: Dict[str, Any]):
        """Add database check results."""
        self.database_status = {
            'status': status,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_payment_check(self, provider: str, status: str, details: Dict[str, Any]):
        """Add payment integration check results."""
        self.payment_status[provider] = {
            'status': status,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_ui_check(self, component: str, status: str, details: Dict[str, Any]):
        """Add UI component check results."""
        self.ui_status[component] = {
            'status': status,
            'details': details,
            'checked_at': datetime.now(timezone.utc).isoformat()
        }
    
    def add_error(self, error: str, can_auto_fix: bool = False):
        """Add an error to the report."""
        self.errors.append({
            'message': error,
            'can_auto_fix': can_auto_fix,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    def add_warning(self, warning: str):
        """Add a warning to the report."""
        self.warnings.append({
            'message': warning,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    def add_fix(self, fix_description: str, success: bool):
        """Add a fix that was applied."""
        self.fixes_applied.append({
            'description': fix_description,
            'success': success,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            'timestamp': self.timestamp,
            'summary': {
                'total_errors': len(self.errors),
                'auto_fixable_errors': len([e for e in self.errors if e['can_auto_fix']]),
                'warnings': len(self.warnings),
                'fixes_applied': len(self.fixes_applied),
                'successful_fixes': len([f for f in self.fixes_applied if f['success']])
            },
            'deployment_status': self.deployment_status,
            'connection_health': self.connection_health,
            'ai_agent_status': self.ai_agent_status,
            'database_status': self.database_status,
            'payment_status': self.payment_status,
            'ui_status': self.ui_status,
            'errors': self.errors,
            'warnings': self.warnings,
            'fixes_applied': self.fixes_applied
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_markdown(self) -> str:
        """Convert report to markdown format."""
        lines = [
            "# AI Agent Sweep Report",
            f"\n**Generated:** {self.timestamp}\n",
            "## Summary",
            f"- **Total Errors:** {len(self.errors)}",
            f"- **Auto-fixable Errors:** {len([e for e in self.errors if e['can_auto_fix']])}",
            f"- **Warnings:** {len(self.warnings)}",
            f"- **Fixes Applied:** {len(self.fixes_applied)}",
            f"- **Successful Fixes:** {len([f for f in self.fixes_applied if f['success']])}",
        ]
        
        # Deployment Status
        if self.deployment_status:
            lines.append("\n## Deployment Status")
            for service, data in self.deployment_status.items():
                status_icon = "✅" if data['status'] == 'healthy' else "❌"
                lines.append(f"\n### {status_icon} {service}")
                lines.append(f"- **Status:** {data['status']}")
                lines.append(f"- **Checked:** {data['checked_at']}")
        
        # Connection Health
        if self.connection_health:
            lines.append("\n## Connection Health")
            for conn, data in self.connection_health.items():
                health_icon = "✅" if data['healthy'] else "❌"
                lines.append(f"\n### {health_icon} {conn}")
                lines.append(f"- **Healthy:** {data['healthy']}")
                lines.append(f"- **Checked:** {data['checked_at']}")
        
        # AI Agent Status
        if self.ai_agent_status:
            lines.append("\n## AI Agent Status")
            for agent, data in self.ai_agent_status.items():
                status_icon = "✅" if data['running'] else "❌"
                lines.append(f"\n### {status_icon} {agent}")
                lines.append(f"- **Running:** {data['running']}")
                lines.append(f"- **Checked:** {data['checked_at']}")
        
        # Database Status
        if self.database_status:
            lines.append("\n## Database Status")
            status = self.database_status.get('status', 'unknown')
            status_icon = "✅" if status == 'healthy' else "❌"
            lines.append(f"{status_icon} **Status:** {status}")
        
        # Payment Status
        if self.payment_status:
            lines.append("\n## Payment Integration Status")
            for provider, data in self.payment_status.items():
                status_icon = "✅" if data['status'] == 'healthy' else "❌"
                lines.append(f"\n### {status_icon} {provider}")
                lines.append(f"- **Status:** {data['status']}")
        
        # UI Status
        if self.ui_status:
            lines.append("\n## Frontend & UI Status")
            for component, data in self.ui_status.items():
                status_icon = "✅" if data['status'] == 'healthy' else "❌"
                lines.append(f"\n### {status_icon} {component}")
                lines.append(f"- **Status:** {data['status']}")
        
        # Errors
        if self.errors:
            lines.append("\n## Errors")
            for i, error in enumerate(self.errors, 1):
                fix_status = "🔧 Auto-fixable" if error['can_auto_fix'] else "⚠️ Manual review required"
                lines.append(f"\n{i}. **{fix_status}**")
                lines.append(f"   - {error['message']}")
                lines.append(f"   - Time: {error['timestamp']}")
        
        # Warnings
        if self.warnings:
            lines.append("\n## Warnings")
            for i, warning in enumerate(self.warnings, 1):
                lines.append(f"{i}. {warning['message']}")
        
        # Fixes Applied
        if self.fixes_applied:
            lines.append("\n## Fixes Applied")
            for i, fix in enumerate(self.fixes_applied, 1):
                success_icon = "✅" if fix['success'] else "❌"
                lines.append(f"\n{i}. {success_icon} {fix['description']}")
                lines.append(f"   - Time: {fix['timestamp']}")
        
        return "\n".join(lines)
