"""AI agent task scheduling optimizer."""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    QUEUED = "queued"


class AITask:
    """Represents an AI task to be scheduled."""
    
    def __init__(self, task_id: str, task_type: str, priority: TaskPriority,
                 estimated_duration: int, dependencies: List[str] = None):
        self.task_id = task_id
        self.task_type = task_type
        self.priority = priority
        self.estimated_duration = estimated_duration  # in seconds
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.created_at = datetime.utcnow()
        self.started_at = None
        self.completed_at = None
        self.assigned_worker = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "priority": self.priority.value,
            "estimated_duration": self.estimated_duration,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "assigned_worker": self.assigned_worker
        }


class TaskScheduler:
    """Optimize AI agent task scheduling for maximum throughput."""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.task_queue = []
        self.running_tasks = []
        self.completed_tasks = []
        self.failed_tasks = []
        self.workers = {f"worker_{i}": None for i in range(num_workers)}
    
    def add_task(self, task: AITask):
        """Add a task to the queue."""
        self.task_queue.append(task)
        logger.info(f"Added task {task.task_id} to queue")
    
    def _check_dependencies(self, task: AITask) -> bool:
        """Check if all dependencies are completed."""
        if not task.dependencies:
            return True
        
        completed_ids = {t.task_id for t in self.completed_tasks}
        return all(dep in completed_ids for dep in task.dependencies)
    
    def _calculate_task_score(self, task: AITask) -> float:
        """
        Calculate priority score for task scheduling.
        Higher score = higher priority for execution.
        """
        # Base score from priority
        priority_score = task.priority.value * 100
        
        # Age factor (older tasks get boost)
        age_minutes = (datetime.utcnow() - task.created_at).total_seconds() / 60
        age_score = min(age_minutes * 2, 100)  # Max 100 points from age
        
        # Duration factor (shorter tasks get slight boost for throughput)
        duration_score = max(0, 50 - (task.estimated_duration / 60))
        
        # Dependency factor (tasks with completed deps get boost)
        dep_score = 50 if self._check_dependencies(task) else 0
        
        total_score = priority_score + age_score + duration_score + dep_score
        return total_score
    
    def optimize_schedule(self) -> List[AITask]:
        """
        Optimize task execution order for maximum throughput.
        
        Returns sorted list of tasks ready for execution.
        """
        # Filter tasks that can run (dependencies met)
        ready_tasks = [t for t in self.task_queue 
                      if self._check_dependencies(t)]
        
        # Sort by calculated priority score
        ready_tasks.sort(key=lambda t: self._calculate_task_score(t), reverse=True)
        
        logger.info(f"Optimized schedule with {len(ready_tasks)} ready tasks")
        return ready_tasks
    
    def assign_tasks(self) -> List[Tuple[str, AITask]]:
        """
        Assign tasks to available workers.
        
        Returns list of (worker_id, task) tuples.
        """
        assignments = []
        optimized_tasks = self.optimize_schedule()
        
        # Find available workers
        available_workers = [w for w, t in self.workers.items() if t is None]
        
        # Assign tasks to workers
        for worker in available_workers:
            if not optimized_tasks:
                break
            
            task = optimized_tasks.pop(0)
            self.workers[worker] = task
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.utcnow()
            task.assigned_worker = worker
            
            self.task_queue.remove(task)
            self.running_tasks.append(task)
            
            assignments.append((worker, task))
            logger.info(f"Assigned task {task.task_id} to {worker}")
        
        return assignments
    
    def complete_task(self, task_id: str, success: bool = True):
        """Mark a task as completed or failed."""
        task = next((t for t in self.running_tasks if t.task_id == task_id), None)
        
        if not task:
            logger.warning(f"Task {task_id} not found in running tasks")
            return
        
        task.completed_at = datetime.utcnow()
        task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        
        # Free up the worker
        if task.assigned_worker:
            self.workers[task.assigned_worker] = None
        
        # Move to appropriate list
        self.running_tasks.remove(task)
        if success:
            self.completed_tasks.append(task)
        else:
            self.failed_tasks.append(task)
        
        logger.info(f"Task {task_id} marked as {task.status.value}")
    
    def get_metrics(self) -> Dict:
        """Get scheduler performance metrics."""
        total_tasks = (len(self.task_queue) + len(self.running_tasks) + 
                      len(self.completed_tasks) + len(self.failed_tasks))
        
        # Calculate average completion time
        completed_with_times = [t for t in self.completed_tasks 
                               if t.started_at and t.completed_at]
        
        avg_completion_time = 0
        if completed_with_times:
            total_time = sum((t.completed_at - t.started_at).total_seconds() 
                           for t in completed_with_times)
            avg_completion_time = total_time / len(completed_with_times)
        
        # Calculate throughput (tasks per hour)
        if self.completed_tasks:
            runtime = (datetime.utcnow() - 
                      min(t.created_at for t in self.completed_tasks)).total_seconds()
            throughput = len(self.completed_tasks) / (runtime / 3600) if runtime > 0 else 0
        else:
            throughput = 0
        
        # Worker utilization
        active_workers = sum(1 for t in self.workers.values() if t is not None)
        worker_utilization = (active_workers / self.num_workers) * 100
        
        return {
            "total_tasks": total_tasks,
            "queued": len(self.task_queue),
            "running": len(self.running_tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "avg_completion_time_seconds": avg_completion_time,
            "throughput_per_hour": throughput,
            "worker_utilization_percent": worker_utilization,
            "active_workers": active_workers,
            "total_workers": self.num_workers
        }
    
    def identify_bottlenecks(self) -> List[Dict]:
        """Identify scheduling bottlenecks and suggest improvements."""
        bottlenecks = []
        metrics = self.get_metrics()
        
        # High queue length
        if metrics["queued"] > self.num_workers * 5:
            bottlenecks.append({
                "type": "high_queue_length",
                "severity": "high",
                "description": f"{metrics['queued']} tasks queued",
                "suggestion": "Consider increasing worker count or optimizing task duration"
            })
        
        # Low worker utilization
        if metrics["worker_utilization_percent"] < 50:
            bottlenecks.append({
                "type": "low_worker_utilization",
                "severity": "medium",
                "description": f"Only {metrics['worker_utilization_percent']:.1f}% workers utilized",
                "suggestion": "Review task dependencies or increase task intake"
            })
        
        # High failure rate
        if total := metrics["completed"] + metrics["failed"]:
            failure_rate = (metrics["failed"] / total) * 100
            if failure_rate > 10:
                bottlenecks.append({
                    "type": "high_failure_rate",
                    "severity": "critical",
                    "description": f"{failure_rate:.1f}% task failure rate",
                    "suggestion": "Investigate task failures and improve error handling"
                })
        
        # Dependency blocking
        blocked_tasks = len([t for t in self.task_queue 
                           if not self._check_dependencies(t)])
        if blocked_tasks > metrics["queued"] * 0.3:
            bottlenecks.append({
                "type": "dependency_blocking",
                "severity": "medium",
                "description": f"{blocked_tasks} tasks blocked by dependencies",
                "suggestion": "Optimize task dependency graph or parallelize independent tasks"
            })
        
        logger.info(f"Identified {len(bottlenecks)} bottlenecks")
        return bottlenecks
