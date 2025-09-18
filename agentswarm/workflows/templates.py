"""Predefined Multi-Agent Workflow Templates."""

from ..workflows.models import (
    WorkflowDefinition,
    WorkflowStep,
    WorkflowType,
    WORKFLOW_REGISTRY,
)

# Codebase Analysis Workflow
CODEBASE_ANALYSIS_WORKFLOW = WorkflowDefinition(
    id="codebase-analysis-v1",
    name="Codebase Analysis Pipeline",
    description="Multi-agent workflow for comprehensive codebase analysis and insights",
    type=WorkflowType.PIPELINE,
    steps=[
        WorkflowStep(
            id="discover",
            name="Project Discovery",
            description="Scan project structure and identify key components",
            agent_type="claude",
            task="analyze_project_structure",
            parameters={
                "scan_depth": "comprehensive",
                "focus_areas": ["architecture", "dependencies", "configurations", "patterns"]
            },
        ),
        WorkflowStep(
            id="document",
            name="Documentation Analysis",
            description="Analyze existing documentation and identify gaps",
            agent_type="gemini",
            task="analyze_documentation",
            dependencies=["discover"],
            parameters={
                "scope": "full_codebase",
                "context_window": "2M",
                "output_format": "detailed_report"
            },
        ),
        WorkflowStep(
            id="optimize",
            name="Performance Analysis",
            description="Identify performance bottlenecks and optimization opportunities",
            agent_type="qwen",
            task="analyze_performance",
            dependencies=["discover"],
            parameters={
                "analysis_types": ["memory", "cpu", "network", "database"],
                "benchmarking": True
            },
        ),
        WorkflowStep(
            id="test",
            name="Testing Analysis",
            description="Review testing coverage and strategies",
            agent_type="codex",
            task="analyze_testing",
            dependencies=["discover"],
            parameters={
                "coverage_types": ["unit", "integration", "e2e"],
                "framework_review": True
            },
        ),
        WorkflowStep(
            id="synthesize",
            name="Synthesis Report",
            description="Combine all agent analyses into comprehensive recommendations",
            agent_type="claude",
            task="synthesize_analysis",
            dependencies=["document", "optimize", "test"],
            parameters={
                "report_format": "executive_summary",
                "include_roadmap": True
            },
        ),
    ],
)

# Future: Additional workflows can be added here as needed

# Register all workflows
WORKFLOW_REGISTRY.update({
    "codebase-analysis": CODEBASE_ANALYSIS_WORKFLOW,
})

# Workflow categories for organization
WORKFLOW_CATEGORIES = {
    "Development": ["codebase-analysis"],
}
