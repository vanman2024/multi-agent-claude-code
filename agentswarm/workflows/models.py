"""Multi-Agent Workflow Definitions and Models."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union
from uuid import uuid4

from ..core.models import AgentProcess


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStepStatus(Enum):
    """Individual workflow step status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowType(Enum):
    """Types of multi-agent workflows."""
    SEQUENTIAL = "sequential"  # Steps execute one after another
    PARALLEL = "parallel"      # Steps execute simultaneously
    CONDITIONAL = "conditional"  # Steps based on conditions
    LOOP = "loop"             # Repeating workflow
    PIPELINE = "pipeline"     # Data flows between steps


@dataclass
class WorkflowStep:
    """Individual step in a workflow."""
    id: str
    name: str
    description: str
    agent_type: str
    task: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)  # Step IDs this depends on
    timeout: Optional[int] = None  # seconds
    retry_count: int = 0
    retry_delay: int = 1  # seconds
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    id: str
    name: str
    description: str
    type: WorkflowType
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    version: str = "1.0.0"


@dataclass
class WorkflowExecution:
    """Runtime execution of a workflow."""
    id: str
    definition_id: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    current_step: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)  # Shared data between steps
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None


class WorkflowExecutor(Protocol):
    """Protocol for workflow execution engines."""

    async def execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Any:
        """Execute a single workflow step."""
        ...

    async def validate_step(self, step: WorkflowStep) -> bool:
        """Validate that a step can be executed."""
        ...


@dataclass
class AgentWorkflowExecutor:
    """Workflow executor that uses agent processes."""

    agent_processes: Dict[str, List[AgentProcess]]

    async def execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Any:
        """Execute step using available agent processes."""
        if step.agent_type not in self.agent_processes:
            raise ValueError(f"No agents available for type: {step.agent_type}")

        # Find available agent process
        available_agents = [
            proc for proc in self.agent_processes[step.agent_type]
            if proc.status == "running"
        ]

        if not available_agents:
            raise RuntimeError(f"No running agents available for type: {step.agent_type}")

        # Use first available agent (could implement load balancing)
        agent = available_agents[0]

        # Simulate task execution (in real implementation, this would communicate with the agent)
        await asyncio.sleep(0.1)  # Simulate processing time

        # Mock result based on task type
        if "search" in step.task.lower():
            result = {"type": "search_results", "count": 10, "data": []}
        elif "analyze" in step.task.lower():
            result = {"type": "analysis", "insights": [], "metrics": {}}
        elif "generate" in step.task.lower():
            result = {"type": "generation", "content": "", "quality_score": 0.8}
        else:
            result = {"type": "generic", "output": f"Executed {step.task}"}

        return result

    async def validate_step(self, step: WorkflowStep) -> bool:
        """Validate step can be executed."""
        return step.agent_type in self.agent_processes


# Predefined workflow templates
LEAD_GENERATION_WORKFLOW = WorkflowDefinition(
    id="lead-generation-v1",
    name="Lead Generation Pipeline",
    description="Multi-agent workflow for comprehensive lead generation",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="search",
            name="Initial Search",
            description="Search for potential leads using multiple criteria",
            agent_type="search_agent",
            task="search_leads",
            parameters={"sources": ["linkedin", "company_websites", "news"]},
        ),
        WorkflowStep(
            id="enrich",
            name="Data Enrichment",
            description="Enrich lead data with additional information",
            agent_type="enrichment_agent",
            task="enrich_profiles",
            dependencies=["search"],
            parameters={"fields": ["company_size", "industry", "social_profiles"]},
        ),
        WorkflowStep(
            id="score",
            name="Lead Scoring",
            description="Score leads based on engagement and fit criteria",
            agent_type="analysis_agent",
            task="score_leads",
            dependencies=["enrich"],
            parameters={"criteria": ["job_title_match", "company_size", "engagement"]},
        ),
        WorkflowStep(
            id="validate",
            name="Contact Validation",
            description="Validate contact information and reachability",
            agent_type="validation_agent",
            task="validate_contacts",
            dependencies=["score"],
            parameters={"validation_types": ["email", "phone", "social"]},
        ),
    ],
)

CONTENT_GENERATION_WORKFLOW = WorkflowDefinition(
    id="content-generation-v1",
    name="Content Generation Pipeline",
    description="Multi-agent workflow for content creation and optimization",
    type=WorkflowType.SEQUENTIAL,
    steps=[
        WorkflowStep(
            id="research",
            name="Topic Research",
            description="Research trending topics and audience interests",
            agent_type="research_agent",
            task="research_topic",
            parameters={"depth": "comprehensive"},
        ),
        WorkflowStep(
            id="outline",
            name="Content Outline",
            description="Create detailed content outline and structure",
            agent_type="planning_agent",
            task="create_outline",
            dependencies=["research"],
        ),
        WorkflowStep(
            id="write",
            name="Content Writing",
            description="Write the main content based on outline",
            agent_type="writing_agent",
            task="write_content",
            dependencies=["outline"],
            parameters={"tone": "professional", "length": "medium"},
        ),
        WorkflowStep(
            id="edit",
            name="Content Editing",
            description="Edit and polish the written content",
            agent_type="editing_agent",
            task="edit_content",
            dependencies=["write"],
        ),
        WorkflowStep(
            id="optimize",
            name="SEO Optimization",
            description="Optimize content for search engines",
            agent_type="seo_agent",
            task="optimize_seo",
            dependencies=["edit"],
        ),
    ],
)

# Registry of available workflows
WORKFLOW_REGISTRY: Dict[str, WorkflowDefinition] = {}

# Import templates to populate registry
from . import templates  # noqa: F401
