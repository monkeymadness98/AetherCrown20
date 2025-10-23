"""Automated API key and secret rotation."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import secrets
import string

logger = logging.getLogger(__name__)


class KeyRotationManager:
    """Manage automated rotation of API keys and secrets."""
    
    def __init__(self):
        self.rotation_schedule = {
            "critical": 30,  # days
            "high": 60,
            "medium": 90,
            "low": 180
        }
        self.key_registry = {}
    
    def generate_secure_key(self, length: int = 32) -> str:
        """Generate a cryptographically secure random key."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def register_key(self, key_id: str, key_type: str, 
                    security_level: str = "medium") -> Dict:
        """
        Register a key for rotation tracking.
        
        Args:
            key_id: Unique identifier for the key
            key_type: Type of key (api_key, secret, token, etc.)
            security_level: Security level (critical, high, medium, low)
        """
        if security_level not in self.rotation_schedule:
            raise ValueError(f"Invalid security level: {security_level}")
        
        key_info = {
            "key_id": key_id,
            "key_type": key_type,
            "security_level": security_level,
            "created_at": datetime.utcnow(),
            "last_rotated": datetime.utcnow(),
            "rotation_interval_days": self.rotation_schedule[security_level],
            "next_rotation": datetime.utcnow() + timedelta(days=self.rotation_schedule[security_level])
        }
        
        self.key_registry[key_id] = key_info
        logger.info(f"Registered key {key_id} for rotation")
        return key_info
    
    def check_rotation_needed(self, key_id: str) -> bool:
        """Check if a key needs rotation."""
        if key_id not in self.key_registry:
            logger.warning(f"Key {key_id} not found in registry")
            return False
        
        key_info = self.key_registry[key_id]
        return datetime.utcnow() >= key_info["next_rotation"]
    
    def get_keys_due_for_rotation(self) -> List[Dict]:
        """Get all keys that are due for rotation."""
        due_keys = []
        
        for key_id, key_info in self.key_registry.items():
            if self.check_rotation_needed(key_id):
                due_keys.append(key_info)
        
        logger.info(f"Found {len(due_keys)} keys due for rotation")
        return due_keys
    
    def rotate_key(self, key_id: str, new_key: Optional[str] = None) -> Dict:
        """
        Rotate a key to a new value.
        
        Args:
            key_id: Key identifier to rotate
            new_key: New key value (generated if not provided)
            
        Returns:
            Dictionary with rotation details
        """
        if key_id not in self.key_registry:
            raise ValueError(f"Key {key_id} not registered")
        
        key_info = self.key_registry[key_id]
        
        # Generate new key if not provided
        if new_key is None:
            new_key = self.generate_secure_key()
        
        # Update registry
        old_rotation = key_info["last_rotated"]
        key_info["last_rotated"] = datetime.utcnow()
        key_info["next_rotation"] = (
            datetime.utcnow() + 
            timedelta(days=key_info["rotation_interval_days"])
        )
        
        rotation_record = {
            "key_id": key_id,
            "rotated_at": datetime.utcnow().isoformat(),
            "previous_rotation": old_rotation.isoformat(),
            "next_rotation": key_info["next_rotation"].isoformat(),
            "new_key": new_key,
            "action_required": "Update key in environment variables and affected services"
        }
        
        logger.info(f"Rotated key {key_id}")
        return rotation_record
    
    def schedule_auto_rotation(self) -> List[Dict]:
        """
        Schedule automatic rotation for all due keys.
        
        Returns list of rotation records.
        """
        due_keys = self.get_keys_due_for_rotation()
        rotations = []
        
        for key_info in due_keys:
            try:
                rotation = self.rotate_key(key_info["key_id"])
                rotations.append(rotation)
            except Exception as e:
                logger.error(f"Failed to rotate key {key_info['key_id']}: {e}")
        
        logger.info(f"Completed {len(rotations)} key rotations")
        return rotations
    
    def get_rotation_report(self) -> Dict:
        """Generate a rotation status report."""
        now = datetime.utcnow()
        
        # Categorize keys by rotation status
        overdue = []
        due_soon = []  # Within 7 days
        healthy = []
        
        for key_id, key_info in self.key_registry.items():
            next_rotation = key_info["next_rotation"]
            days_until = (next_rotation - now).days
            
            if days_until < 0:
                overdue.append(key_info)
            elif days_until <= 7:
                due_soon.append(key_info)
            else:
                healthy.append(key_info)
        
        report = {
            "generated_at": now.isoformat(),
            "total_keys": len(self.key_registry),
            "overdue": len(overdue),
            "due_soon": len(due_soon),
            "healthy": len(healthy),
            "overdue_keys": [k["key_id"] for k in overdue],
            "due_soon_keys": [k["key_id"] for k in due_soon],
            "recommendations": []
        }
        
        if overdue:
            report["recommendations"].append({
                "severity": "critical",
                "message": f"{len(overdue)} keys are overdue for rotation",
                "action": "Rotate immediately"
            })
        
        if due_soon:
            report["recommendations"].append({
                "severity": "medium",
                "message": f"{len(due_soon)} keys due for rotation within 7 days",
                "action": "Schedule rotation soon"
            })
        
        return report
