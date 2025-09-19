"""Workflow State Management and Persistence."""

import json
import logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import WorkflowExecution, WorkflowStatus


class WorkflowStateStore:
    """Persistent storage for workflow execution state."""

    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.executions_file = self.state_dir / "workflow_executions.json"
        self.logger = logging.getLogger(__name__)

        # In-memory cache
        self._executions: Dict[str, WorkflowExecution] = {}
        self._load_state()

    def _load_state(self) -> None:
        """Load workflow executions from disk."""
        if not self.executions_file.exists():
            return

        try:
            with open(self.executions_file, 'r') as f:
                data = json.load(f)

            for exec_data in data.get("executions", []):
                execution = self._deserialize_execution(exec_data)
                self._executions[execution.id] = execution

            self.logger.info(f"Loaded {len(self._executions)} workflow executions from state")
        except Exception as e:
            self.logger.error(f"Failed to load workflow state: {e}")

    def _save_state(self) -> None:
        """Save workflow executions to disk."""
        try:
            data = {
                "last_updated": datetime.now(UTC).isoformat(),
                "executions": [self._serialize_execution(exec) for exec in self._executions.values()]
            }

            with open(self.executions_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)

        except Exception as e:
            self.logger.error(f"Failed to save workflow state: {e}")

    def _serialize_execution(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Serialize workflow execution to dictionary."""
        return {
            "id": execution.id,
            "definition_id": execution.definition_id,
            "status": execution.status.value,
            "current_step": execution.current_step,
            "step_results": execution.step_results,
            "context": execution.context,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
            "execution_time": execution.execution_time,
            "error": execution.error,
        }

    def _deserialize_execution(self, data: Dict[str, Any]) -> WorkflowExecution:
        """Deserialize dictionary to workflow execution."""
        return WorkflowExecution(
            id=data["id"],
            definition_id=data["definition_id"],
            status=WorkflowStatus(data["status"]),
            current_step=data.get("current_step"),
            step_results=data.get("step_results", {}),
            context=data.get("context", {}),
            start_time=datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None,
            end_time=datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None,
            execution_time=data.get("execution_time"),
            error=data.get("error"),
        )

    def save_execution(self, execution: WorkflowExecution) -> None:
        """Save a workflow execution."""
        self._executions[execution.id] = execution
        self._save_state()
        self.logger.debug(f"Saved workflow execution: {execution.id}")

    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get a workflow execution by ID."""
        return self._executions.get(execution_id)

    def list_executions(
        self,
        status: Optional[WorkflowStatus] = None,
        definition_id: Optional[str] = None,
        limit: int = 50
    ) -> List[WorkflowExecution]:
        """List workflow executions with optional filtering."""
        executions = list(self._executions.values())

        if status:
            executions = [e for e in executions if e.status == status]

        if definition_id:
            executions = [e for e in executions if e.definition_id == definition_id]

        # Sort by start time (most recent first)
        executions.sort(key=lambda e: e.start_time or datetime.min.replace(tzinfo=UTC), reverse=True)

        return executions[:limit]

    def delete_execution(self, execution_id: str) -> bool:
        """Delete a workflow execution."""
        if execution_id in self._executions:
            del self._executions[execution_id]
            self._save_state()
            self.logger.info(f"Deleted workflow execution: {execution_id}")
            return True
        return False

    def get_active_executions(self) -> List[WorkflowExecution]:
        """Get all currently active (running) workflow executions."""
        return [
            execution for execution in self._executions.values()
            if execution.status == WorkflowStatus.RUNNING
        ]

    def get_completed_executions(self, limit: int = 20) -> List[WorkflowExecution]:
        """Get recently completed workflow executions."""
        completed = [
            execution for execution in self._executions.values()
            if execution.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]
        ]

        # Sort by end time (most recent first)
        completed.sort(key=lambda e: e.end_time or datetime.min.replace(tzinfo=UTC), reverse=True)

        return completed[:limit]

    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about workflow executions."""
        total = len(self._executions)
        if total == 0:
            return {"total": 0, "completed": 0, "failed": 0, "running": 0, "success_rate": 0.0}

        completed = sum(1 for e in self._executions.values() if e.status == WorkflowStatus.COMPLETED)
        failed = sum(1 for e in self._executions.values() if e.status == WorkflowStatus.FAILED)
        running = sum(1 for e in self._executions.values() if e.status == WorkflowStatus.RUNNING)

        success_rate = (completed / (completed + failed)) * 100 if (completed + failed) > 0 else 0.0

        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "running": running,
            "cancelled": sum(1 for e in self._executions.values() if e.status == WorkflowStatus.CANCELLED),
            "success_rate": round(success_rate, 2),
        }

    def cleanup_old_executions(self, days: int = 30) -> int:
        """Clean up executions older than specified days."""
        from datetime import timedelta

        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        to_delete = []

        for execution_id, execution in self._executions.items():
            if execution.end_time and execution.end_time < cutoff_date:
                to_delete.append(execution_id)

        for execution_id in to_delete:
            del self._executions[execution_id]

        if to_delete:
            self._save_state()
            self.logger.info(f"Cleaned up {len(to_delete)} old workflow executions")

        return len(to_delete)
