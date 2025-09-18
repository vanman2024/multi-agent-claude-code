"""Workflow Monitoring and Coordination."""

import asyncio
import logging
import threading
import time
from datetime import datetime, UTC
from typing import Any, Callable, Dict, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

from .models import WorkflowExecution, WorkflowStatus, WorkflowStepStatus
from .orchestrator import WorkflowOrchestrator
from .state import WorkflowStateStore


console = Console()


class WorkflowMonitor:
    """Real-time monitoring and coordination for workflow executions."""

    def __init__(
        self,
        orchestrator: WorkflowOrchestrator,
        state_store: WorkflowStateStore,
        update_interval: float = 1.0,
    ):
        self.orchestrator = orchestrator
        self.state_store = state_store
        self.update_interval = update_interval
        self.logger = logging.getLogger(__name__)

        # Monitoring state
        self.active_monitors: Dict[str, asyncio.Task] = {}
        self.event_listeners: Dict[str, List[Callable]] = {}
        self.monitoring_active = False

        # Thread pool for background tasks
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="workflow-monitor")

    async def start_monitoring(self) -> None:
        """Start the workflow monitoring system."""
        self.monitoring_active = True
        self.logger.info("Workflow monitoring started")

        # Start background monitoring task
        asyncio.create_task(self._background_monitor())

    async def stop_monitoring(self) -> None:
        """Stop the workflow monitoring system."""
        self.monitoring_active = False

        # Cancel all active monitors
        for task in self.active_monitors.values():
            task.cancel()

        self.active_monitors.clear()
        self.executor.shutdown(wait=True)
        self.logger.info("Workflow monitoring stopped")

    def monitor_execution(self, execution_id: str) -> None:
        """Start monitoring a specific workflow execution."""
        if execution_id in self.active_monitors:
            self.logger.warning(f"Already monitoring execution: {execution_id}")
            return

        task = asyncio.create_task(self._monitor_single_execution(execution_id))
        self.active_monitors[execution_id] = task
        self.logger.info(f"Started monitoring execution: {execution_id}")

    def stop_monitoring_execution(self, execution_id: str) -> None:
        """Stop monitoring a specific workflow execution."""
        if execution_id in self.active_monitors:
            self.active_monitors[execution_id].cancel()
            del self.active_monitors[execution_id]
            self.logger.info(f"Stopped monitoring execution: {execution_id}")

    async def _monitor_single_execution(self, execution_id: str) -> None:
        """Monitor a single workflow execution."""
        try:
            while self.monitoring_active:
                execution = self.orchestrator.get_execution(execution_id)
                if not execution:
                    # Check state store
                    execution = self.state_store.get_execution(execution_id)

                if execution:
                    # Notify listeners of status changes
                    await self._notify_listeners(execution_id, "status_update", execution)

                    # If execution is complete, stop monitoring
                    if execution.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
                        self.logger.info(f"Execution {execution_id} completed with status: {execution.status.value}")
                        break

                await asyncio.sleep(self.update_interval)

        except asyncio.CancelledError:
            self.logger.info(f"Monitoring cancelled for execution: {execution_id}")
        except Exception as e:
            self.logger.error(f"Error monitoring execution {execution_id}: {e}")

    async def _background_monitor(self) -> None:
        """Background monitoring task."""
        while self.monitoring_active:
            try:
                # Check for new executions to monitor
                active_executions = self.orchestrator.list_executions()
                active_executions.extend(self.state_store.get_active_executions())

                for execution in active_executions:
                    if execution.id not in self.active_monitors and execution.status == WorkflowStatus.RUNNING:
                        self.monitor_execution(execution.id)

                # Clean up completed monitors
                completed = [
                    exec_id for exec_id, task in self.active_monitors.items()
                    if task.done()
                ]
                for exec_id in completed:
                    del self.active_monitors[exec_id]

                await asyncio.sleep(self.update_interval * 5)  # Less frequent background checks

            except Exception as e:
                self.logger.error(f"Error in background monitoring: {e}")
                await asyncio.sleep(self.update_interval)

    def add_event_listener(
        self,
        event_type: str,
        callback: Callable[[str, str, Any], None]
    ) -> None:
        """Add an event listener for workflow events."""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(callback)

    def remove_event_listener(
        self,
        event_type: str,
        callback: Callable[[str, str, Any], None]
    ) -> None:
        """Remove an event listener."""
        if event_type in self.event_listeners:
            self.event_listeners[event_type] = [
                cb for cb in self.event_listeners[event_type] if cb != callback
            ]

    async def _notify_listeners(self, execution_id: str, event_type: str, data: Any) -> None:
        """Notify all listeners of an event."""
        if event_type not in self.event_listeners:
            return

        for callback in self.event_listeners[event_type]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(execution_id, event_type, data)
                else:
                    # Run sync callbacks in thread pool
                    await asyncio.get_event_loop().run_in_executor(
                        self.executor, callback, execution_id, event_type, data
                    )
            except Exception as e:
                self.logger.error(f"Error in event listener: {e}")

    def display_live_dashboard(self, execution_id: Optional[str] = None) -> None:
        """Display a live monitoring dashboard."""
        def generate_table() -> Table:
            if execution_id:
                # Single execution view
                execution = self.orchestrator.get_execution(execution_id)
                if not execution:
                    execution = self.state_store.get_execution(execution_id)

                if not execution:
                    return Table(title=f"Execution {execution_id} - Not Found")

                table = Table(title=f"Workflow Execution: {execution_id}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="white")

                table.add_row("Status", execution.status.value)
                table.add_row("Current Step", execution.current_step or "None")
                table.add_row("Start Time", str(execution.start_time))
                table.add_row("Execution Time", f"{execution.execution_time:.2f}s" if execution.execution_time else "N/A")
                if execution.error:
                    table.add_row("Error", execution.error)

                return table
            else:
                # Multi-execution view
                executions = self.orchestrator.list_executions()
                executions.extend(self.state_store.list_executions(limit=10))

                table = Table(title="Active Workflow Executions")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Definition", style="white")
                table.add_column("Status", style="green")
                table.add_column("Current Step", style="yellow")
                table.add_column("Execution Time", style="magenta", justify="right")

                for execution in executions[:10]:  # Show top 10
                    exec_time = f"{execution.execution_time:.1f}s" if execution.execution_time else "-"
                    table.add_row(
                        execution.id[:8] + "...",
                        execution.definition_id,
                        execution.status.value,
                        execution.current_step or "-",
                        exec_time
                    )

                return table

        console.print("Starting live workflow dashboard. Press Ctrl+C to exit.", style="cyan")
        try:
            with Live(generate_table(), refresh_per_second=1) as live:
                while True:
                    live.update(generate_table())
                    time.sleep(1)
        except KeyboardInterrupt:
            console.print("Dashboard stopped", style="yellow")

    def get_execution_metrics(self, execution_id: str) -> Dict[str, Any]:
        """Get detailed metrics for a workflow execution."""
        execution = self.orchestrator.get_execution(execution_id)
        if not execution:
            execution = self.state_store.get_execution(execution_id)

        if not execution:
            return {"error": "Execution not found"}

        return {
            "id": execution.id,
            "definition_id": execution.definition_id,
            "status": execution.status.value,
            "current_step": execution.current_step,
            "total_steps": len(execution.step_results),
            "completed_steps": sum(1 for result in execution.step_results.values() if result),
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
            "execution_time": execution.execution_time,
            "success_rate": len([r for r in execution.step_results.values() if r]) / len(execution.step_results) if execution.step_results else 0,
            "error": execution.error,
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide workflow metrics."""
        stats = self.state_store.get_execution_stats()

        return {
            **stats,
            "active_monitors": len(self.active_monitors),
            "total_listeners": sum(len(listeners) for listeners in self.event_listeners.values()),
        }


class WorkflowCoordinator:
    """Coordinates between multiple workflow executions and agents."""

    def __init__(self, monitor: WorkflowMonitor):
        self.monitor = monitor
        self.logger = logging.getLogger(__name__)

        # Coordination state
        self.resource_locks: Dict[str, asyncio.Lock] = {}
        self.execution_dependencies: Dict[str, Set[str]] = {}

    async def coordinate_executions(self, executions: List[WorkflowExecution]) -> None:
        """Coordinate multiple workflow executions to avoid conflicts."""
        # Group executions by resource requirements
        resource_groups = self._group_by_resources(executions)

        # Execute groups sequentially, executions within groups in parallel
        for resource_group in resource_groups.values():
            await asyncio.gather(*[
                self._execute_with_coordination(execution)
                for execution in resource_group
            ])

    def _group_by_resources(self, executions: List[WorkflowExecution]) -> Dict[str, List[WorkflowExecution]]:
        """Group executions by required resources."""
        groups = {}

        for execution in executions:
            # Simple resource detection based on definition ID
            # In a real implementation, this would analyze the workflow definition
            resource_key = execution.definition_id.split('-')[0]  # e.g., "lead" from "lead-generation"

            if resource_key not in groups:
                groups[resource_key] = []
            groups[resource_key].append(execution)

        return groups

    async def _execute_with_coordination(self, execution: WorkflowExecution) -> None:
        """Execute a workflow with resource coordination."""
        # Acquire resource locks if needed
        locks_to_acquire = []

        # Determine required locks based on execution type
        if "search" in execution.definition_id:
            locks_to_acquire.append("search_api")
        if "analysis" in execution.definition_id:
            locks_to_acquire.append("analysis_engine")

        # Acquire locks
        acquired_locks = []
        try:
            for lock_name in locks_to_acquire:
                if lock_name not in self.resource_locks:
                    self.resource_locks[lock_name] = asyncio.Lock()
                await self.resource_locks[lock_name].acquire()
                acquired_locks.append(lock_name)

            # Execute the workflow (this would normally be handled by the orchestrator)
            self.logger.info(f"Executing coordinated workflow: {execution.id}")

        finally:
            # Release locks
            for lock_name in reversed(acquired_locks):
                self.resource_locks[lock_name].release()

    def add_execution_dependency(self, execution_id: str, depends_on: str) -> None:
        """Add a dependency between executions."""
        if execution_id not in self.execution_dependencies:
            self.execution_dependencies[execution_id] = set()
        self.execution_dependencies[execution_id].add(depends_on)

    def check_execution_dependencies(self, execution_id: str) -> bool:
        """Check if all dependencies for an execution are satisfied."""
        if execution_id not in self.execution_dependencies:
            return True

        for dep_id in self.execution_dependencies[execution_id]:
            dep_execution = self.monitor.orchestrator.get_execution(dep_id)
            if not dep_execution or dep_execution.status != WorkflowStatus.COMPLETED:
                return False

        return True
