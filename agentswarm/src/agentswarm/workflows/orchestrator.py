"""Multi-Agent Workflow Orchestrator.

Orchestrates multi-agent workflows.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from .models import (
    WorkflowDefinition,
    WorkflowExecution,
    WorkflowExecutor,
    WorkflowStatus,
    WorkflowStep,
    WorkflowStepStatus,
    WorkflowType,
    WORKFLOW_REGISTRY,
)
from .state import WorkflowStateStore


class WorkflowOrchestrator:
    """Orchestrates multi-agent workflows."""

    def __init__(
        self,
        executor: WorkflowExecutor,
        state_dir: Optional[Path] = None,
    ):
        self.executor = executor
        self.state_dir = state_dir or Path.cwd() / "workflow_state"
        self.state_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Initialize state store
        self.state_store = WorkflowStateStore(self.state_dir)

        # In-memory state (could be persisted to disk/database)
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.completed_executions: Dict[str, WorkflowExecution] = {}

    async def execute_workflow(
        self,
        definition: WorkflowDefinition,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """Execute a workflow definition."""
        execution = WorkflowExecution(
            id=str(uuid4()),
            definition_id=definition.id,
            context=initial_context or {},
        )

        self.active_executions[execution.id] = execution
        self.state_store.save_execution(execution)
        self.logger.info(f"Starting workflow execution: {execution.id}")

        try:
            execution.start_time = datetime.now(UTC)
            execution.status = WorkflowStatus.RUNNING
            self.state_store.save_execution(execution)

            if definition.type in (WorkflowType.SEQUENTIAL, WorkflowType.VALIDATION):
                await self._execute_sequential(definition, execution)
            elif definition.type == WorkflowType.PARALLEL:
                await self._execute_parallel(definition, execution)
            elif definition.type == WorkflowType.PIPELINE:
                await self._execute_pipeline(definition, execution)
            else:
                raise ValueError(f"Unsupported workflow type: {definition.type}")

            execution.status = WorkflowStatus.COMPLETED
            self.logger.info(f"Workflow completed: {execution.id}")

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error = str(e)
            self.logger.error(f"Workflow failed: {execution.id} - {e}")

        finally:
            execution.end_time = datetime.now(UTC)
            if execution.start_time and execution.end_time:
                execution.execution_time = (
                    execution.end_time - execution.start_time
                ).total_seconds()

            # Move to completed and save final state
            self.completed_executions[execution.id] = execution
            self.active_executions.pop(execution.id, None)
            self.state_store.save_execution(execution)

        return execution

    async def _execute_sequential(
        self,
        definition: WorkflowDefinition,
        execution: WorkflowExecution,
    ) -> None:
        """Execute steps sequentially."""
        for step in definition.steps:
            await self._execute_step(step, execution)

    async def _execute_parallel(
        self,
        definition: WorkflowDefinition,
        execution: WorkflowExecution,
    ) -> None:
        """Execute independent steps in parallel."""
        # Group steps by dependencies
        independent_steps = [
            step for step in definition.steps
            if not step.dependencies
        ]

        # Execute independent steps in parallel
        tasks = [
            self._execute_step(step, execution)
            for step in independent_steps
        ]
        await asyncio.gather(*tasks)

        # Execute dependent steps (simplified - could be more sophisticated)
        dependent_steps = [
            step for step in definition.steps
            if step.dependencies
        ]

        for step in dependent_steps:
            if self._dependencies_satisfied(step, execution):
                await self._execute_step(step, execution)

    async def _execute_pipeline(
        self,
        definition: WorkflowDefinition,
        execution: WorkflowExecution,
    ) -> None:
        """Execute steps as a pipeline (data flows between steps)."""
        for step in definition.steps:
            # Wait for dependencies
            while not self._dependencies_satisfied(step, execution):
                await asyncio.sleep(0.1)

            await self._execute_step(step, execution)

    async def _execute_step(
        self,
        step: WorkflowStep,
        execution: WorkflowExecution,
    ) -> None:
        """Execute a single workflow step."""
        execution.current_step = step.id
        step.status = WorkflowStepStatus.RUNNING
        step.start_time = datetime.now(UTC)

        try:
            # Validate step can be executed
            if not await self.executor.validate_step(step):
                raise RuntimeError(f"Step validation failed: {step.name}")

            # Execute step with retry logic
            result = await self._execute_with_retry(step, execution.context)

            step.result = result
            step.status = WorkflowStepStatus.COMPLETED

            # Update execution context with step result
            execution.step_results[step.id] = result
            execution.context[f"step_{step.id}_result"] = result

            self.logger.info(f"Step completed: {step.name}")

        except Exception as e:
            step.status = WorkflowStepStatus.FAILED
            step.error = str(e)
            self.logger.error(f"Step failed: {step.name} - {e}")
            raise

        finally:
            step.end_time = datetime.now(UTC)
            if step.start_time and step.end_time:
                step.execution_time = (
                    step.end_time - step.start_time
                ).total_seconds()

    async def _execute_with_retry(
        self,
        step: WorkflowStep,
        context: Dict[str, Any],
    ) -> Any:
        """Execute step with retry logic."""
        last_error = None

        for attempt in range(step.retry_count + 1):
            try:
                return await self.executor.execute_step(step, context)
            except Exception as e:
                last_error = e
                if attempt < step.retry_count:
                    self.logger.warning(
                        f"Step {step.name} attempt {attempt + 1} failed, retrying in {step.retry_delay}s"
                    )
                    await asyncio.sleep(step.retry_delay)
                else:
                    self.logger.error(f"Step {step.name} failed after {step.retry_count + 1} attempts")
                    raise e

        raise last_error

    def _dependencies_satisfied(
        self,
        step: WorkflowStep,
        execution: WorkflowExecution,
    ) -> bool:
        """Check if all dependencies for a step are satisfied."""
        for dep_id in step.dependencies:
            if dep_id not in execution.step_results:
                return False

        return True

    def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get status of a workflow execution."""
        # Check active executions first
        if execution_id in self.active_executions:
            return self.active_executions[execution_id]
        # Then check state store
        return self.state_store.get_execution(execution_id)

    def list_executions(self) -> List[WorkflowExecution]:
        """List all workflow executions."""
        # Combine active and stored executions
        active = list(self.active_executions.values())
        stored = self.state_store.list_executions()
        return active + stored

    def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running workflow execution."""
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
            execution.status = WorkflowStatus.CANCELLED
            self.state_store.save_execution(execution)
            self.completed_executions[execution_id] = execution
            self.active_executions.pop(execution_id)
            return True
        return False


class WorkflowManager:
    """High-level workflow management interface."""

    def __init__(self, orchestrator: WorkflowOrchestrator):
        self.orchestrator = orchestrator

    async def run_workflow_by_name(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """Run a workflow by name from the registry."""
        if name not in WORKFLOW_REGISTRY:
            raise ValueError(f"Workflow '{name}' not found in registry")

        definition = WORKFLOW_REGISTRY[name]
        return await self.orchestrator.execute_workflow(definition, context)

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflow names."""
        return list(WORKFLOW_REGISTRY.keys())

    def get_workflow_definition(self, name: str) -> Optional[WorkflowDefinition]:
        """Get workflow definition by name."""
        return WORKFLOW_REGISTRY.get(name)
