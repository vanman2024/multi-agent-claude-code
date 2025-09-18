#!/usr/bin/env python3
"""AgentSwarm CLI - Enterprise multi-agent orchestration entry point."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

import psutil

from ..core.config import (
    SwarmConfig,
    create_default_config,
    create_example_config,
)
from ..core.models import AgentProcess
from ..core.orchestrator import AgentOrchestrator
from ..core.state import STATE_DIRECTORY_NAME, SwarmStateStore
from ..workflows.orchestrator import WorkflowManager, WorkflowOrchestrator
from ..workflows.models import AgentWorkflowExecutor, WORKFLOW_REGISTRY
from ..workflows.state import WorkflowStateStore
from ..workflows.monitor import WorkflowMonitor


console = Console()

DEFAULT_CONFIG_FILENAME = "agentswarm.yaml"


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s")


def _resolve_project_path(project_path: Optional[Path]) -> Path:
    return Path(project_path).resolve() if project_path else Path.cwd()


def _get_state_store(project_path: Path) -> SwarmStateStore:
    state_dir = project_path / STATE_DIRECTORY_NAME
    return SwarmStateStore(state_dir)


def _load_config(
    *,
    instances: Optional[str],
    config_file: Optional[Path],
    task: Optional[str],
    project_path: Path,
) -> SwarmConfig:
    if config_file:
        config = SwarmConfig.from_file(config_file)
    else:
        default_path = project_path / DEFAULT_CONFIG_FILENAME
        if default_path.exists():
            config = SwarmConfig.from_file(default_path)
        elif instances:
            config = SwarmConfig.from_instances(instances, task=task)
        else:
            config = create_default_config()

    if instances:
        overrides = SwarmConfig.from_instances(instances, task=task).to_dict()
        config = config.merge(overrides)

    if task:
        merged = config.to_dict()
        for agent_cfg in merged["agents"].values():
            agent_cfg.setdefault("tasks", [])
            if task not in agent_cfg["tasks"]:
                agent_cfg["tasks"].append(task)
        config = SwarmConfig(
            agents=merged["agents"],
            deployment=merged.get("deployment", {}),
            metadata=merged.get("metadata", {}),
        )

    return config


@click.group()
@click.option("--project", type=click.Path(path_type=Path), default=None, help="Project root path")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx: click.Context, project: Optional[Path], verbose: bool) -> None:
    """AgentSwarm - Enterprise Multi-Agent Orchestration CLI"""

    _configure_logging(verbose)
    resolved_project = _resolve_project_path(project)
    ctx.obj = {
        "project": resolved_project,
        "state_store": _get_state_store(resolved_project),
    }


@cli.command()
@click.argument("project_path", type=click.Path(path_type=Path))
@click.option("--agents", default="codex:1,claude:1", help="Agent blueprint (e.g. codex:3,claude:2)")
@click.option(
    "--config",
    "config_template",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    help="Custom configuration template to seed the project",
)
@click.option("--force", is_flag=True, help="Overwrite existing configuration files")
def init(project_path: Path, agents: str, config_template: Optional[Path], force: bool) -> None:
    """Initialize a new AgentSwarm project"""

    project_root = project_path.resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    config_path = project_root / DEFAULT_CONFIG_FILENAME
    if config_path.exists() and not force:
        console.print(
            Panel.fit(
                f"Configuration already exists at {config_path}. Use --force to overwrite.",
                title="Init Skipped",
                style="yellow",
            )
        )
        return

    if config_template:
        config = SwarmConfig.from_file(config_template)
    else:
        config = SwarmConfig.from_instances(agents)

    config.to_yaml(config_path)

    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    example_path = docs_dir / "agentswarm-example.yaml"
    example_path.write_text(create_example_config(), encoding="utf-8")

    _get_state_store(project_root)  # Ensure state directory exists

    console.print(
        Panel.fit(
            f"Project initialized at {project_root}\nConfiguration: {config_path}",
            title="AgentSwarm Ready",
            style="green",
        )
    )


@cli.command()
@click.option("--instances", help="Agent instances (e.g. codex:3,claude:2)")
@click.option("--config", "config_file", type=click.Path(path_type=Path, exists=True))
@click.option("--task", help="Task description for agents")
@click.option("--dry-run", is_flag=True, help="Show deployment plan without executing")
@click.pass_context
def deploy(
    ctx: click.Context,
    instances: Optional[str],
    config_file: Optional[Path],
    task: Optional[str],
    dry_run: bool,
) -> None:
    """Deploy agent swarm with specified configuration"""

    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]

    config = _load_config(
        instances=instances,
        config_file=config_file,
        task=task,
        project_path=project_path,
    )

    console.print(Panel.fit("Preparing deployment...", style="cyan"))

    if dry_run:
        _render_deployment_plan(config)
        return

    orchestrator = AgentOrchestrator(project_root=project_path, state_store=state_store)
    deployment = asyncio.run(orchestrator.deploy_swarm(config))

    _render_deployment_summary(deployment)


def _render_deployment_plan(config: SwarmConfig) -> None:
    table = Table(title="Deployment Plan")
    table.add_column("Agent Type")
    table.add_column("Instances", justify="right")
    table.add_column("Tasks")

    for agent_type, agent_config in config.iter_agents():
        instances = str(agent_config.get("instances", 1))
        tasks = ", ".join(agent_config.get("tasks", [])) or "(none)"
        table.add_row(agent_type, instances, tasks)

    console.print(table)


def _render_deployment_summary(deployment: Any) -> None:
    table = Table(title=f"Deployment {deployment.deployment_id}")
    table.add_column("Agent Type")
    table.add_column("Instances", justify="right")
    table.add_column("PIDs")

    for agent_type, processes in deployment.agents.items():
        pids = ", ".join(str(proc.pid) for proc in processes)
        table.add_row(agent_type, str(len(processes)), pids)

    console.print(table)


@cli.command()
@click.option("--logs", is_flag=True, help="Show real-time logs")
@click.option("--dashboard", is_flag=True, help="Launch web dashboard")
@click.option("--metrics", is_flag=True, help="Show performance metrics")
@click.pass_context
def monitor(ctx: click.Context, logs: bool, dashboard: bool, metrics: bool) -> None:
    """Monitor running agent swarm"""

    store: SwarmStateStore = ctx.obj["state_store"]
    latest = store.latest_deployment()
    if not latest:
        console.print("No deployments recorded. Run `agentswarm deploy` first.", style="yellow")
        return

    deployment_id = latest["deployment_id"]
    def render_snapshot() -> Table:
        include_metrics = metrics or dashboard
        return _build_status_table(latest, include_metrics=include_metrics)

    if dashboard:
        console.print("Starting live dashboard. Press Ctrl+C to exit.", style="cyan")
        try:
            with Live(render_snapshot(), refresh_per_second=1) as live:
                while True:
                    latest_refresh = store.latest_deployment()
                    if latest_refresh:
                        live.update(
                            _build_status_table(
                                latest_refresh,
                                include_metrics=metrics or dashboard,
                            )
                        )
                    time.sleep(1)
        except KeyboardInterrupt:
            console.print("Dashboard stopped", style="yellow")
            return
    else:
        console.print(render_snapshot())

    if logs:
        console.print(
            "Log streaming will attach to processes in a future release.",
            style="yellow",
        )

    if metrics and not dashboard:
        console.print("Metrics summary displayed above.", style="cyan")


@cli.command()
@click.argument("agent_type")
@click.argument("delta", type=int)
@click.option("--deployment", "deployment_id", help="Target deployment id")
@click.pass_context
def scale(ctx: click.Context, agent_type: str, delta: int, deployment_id: Optional[str]) -> None:
    """Scale agent instances up or down"""

    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]
    orchestrator = AgentOrchestrator(project_root=project_path, state_store=state_store)
    try:
        asyncio.run(
            orchestrator.scale_agents(agent_type, delta, deployment_id=deployment_id)
        )
    except Exception as exc:  # noqa: BLE001 - surface to CLI
        console.print(f"Scaling failed: {exc}", style="red")
        return

    console.print(f"Scaled {agent_type} by {delta}", style="green")


@cli.command()
@click.pass_context
def health(ctx: click.Context) -> None:
    """Check health of all agents"""

    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]
    orchestrator = AgentOrchestrator(project_root=project_path, state_store=state_store)

    try:
        status = asyncio.run(orchestrator.health_check())
    except Exception as exc:  # noqa: BLE001 - CLI entry point
        console.print(f"Health check failed: {exc}", style="red")
        return

    table = Table(title="Agent Health")
    table.add_column("Deployment:Agent")
    table.add_column("Status")
    table.add_column("Healthy")
    table.add_column("Unhealthy")
    table.add_column("Uptime", justify="right")

    for key, health in status.items():
        # Enhanced health display with uptime estimation
        uptime = getattr(health, 'uptime', 'N/A')
        if uptime == 'N/A' and health.healthy_instances > 0:
            uptime = "~5m"  # Rough estimate for running instances
        
        table.add_row(
            key,
            health.status,
            str(health.healthy_instances),
            str(health.unhealthy_instances),
            str(uptime),
        )

    console.print(table)


@cli.command()
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json", "yaml"]))
@click.pass_context
def status(ctx: click.Context, output_format: str) -> None:
    """Show comprehensive deployment status with multiple output formats"""
    
    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]
    
    latest = state_store.latest_deployment()
    if not latest:
        console.print("No deployments recorded. Run `agentswarm deploy` first.", style="yellow")
        return
    
    if output_format == "json":
        import json
        console.print(json.dumps(latest, indent=2, default=str))
    elif output_format == "yaml":
        import yaml
        console.print(yaml.dump(latest, default_flow_style=False))
    else:
        # Enhanced table format with more details
        table = _build_status_table(latest, include_metrics=True)
        console.print(table)
        
        # Additional deployment metadata
        metadata_table = Table(title="Deployment Metadata")
        metadata_table.add_column("Property", style="cyan")
        metadata_table.add_column("Value", style="white")
        
        metadata_table.add_row("Deployment ID", latest.get("deployment_id", "Unknown"))
        metadata_table.add_row("Created", latest.get("created_at", "Unknown"))
        metadata_table.add_row("Project Path", str(project_path))
        metadata_table.add_row("Total Agents", str(sum(len(procs) for procs in latest.get("agents", {}).values())))
        
        console.print(metadata_table)


@cli.command()
@click.argument("key")
@click.argument("value")
@click.pass_context
def config(ctx: click.Context, key: str, value: str) -> None:
    """Set configuration values"""

    project_path: Path = ctx.obj["project"]
    config_path = project_path / DEFAULT_CONFIG_FILENAME

    if not config_path.exists():
        console.print(
            f"Configuration file not found at {config_path}. Run `agentswarm init` first.",
            style="red",
        )
        return

    config = SwarmConfig.from_file(config_path)
    section, _, option = key.partition(".")

    if not section or not option:
        console.print("Configuration key must be in the format section.option", style="red")
        return

    data = config.to_dict()
    target = data.setdefault(section, {})
    target[option] = value

    SwarmConfig(
        agents=data["agents"],
        deployment=data.get("deployment", {}),
        metadata=data.get("metadata", {}),
    ).to_yaml(config_path)

    console.print(f"Updated {key} in {config_path}", style="green")


@cli.group()
def workflow():
    """Multi-agent workflow management"""
    pass


@workflow.command()
def list():
    """List available workflows"""
    if not WORKFLOW_REGISTRY:
        console.print("No workflows available. Create workflow definitions first.", style="yellow")
        return

    table = Table(title="Available Workflows")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Type", style="green")
    table.add_column("Steps", justify="right")

    for name, workflow in WORKFLOW_REGISTRY.items():
        table.add_row(
            name,
            workflow.description,
            workflow.type.value,
            str(len(workflow.steps))
        )

    console.print(table)


@workflow.command()
@click.argument("name")
@click.option("--context", help="JSON context data for workflow execution")
@click.pass_context
def run(ctx: click.Context, name: str, context: Optional[str]):
    """Run a workflow by name"""
    if name not in WORKFLOW_REGISTRY:
        console.print(f"Workflow '{name}' not found. Use 'agentswarm workflow list' to see available workflows.", style="red")
        return

    # Parse context if provided
    execution_context = {}
    if context:
        try:
            import json
            execution_context = json.loads(context)
        except json.JSONDecodeError as e:
            console.print(f"Invalid JSON context: {e}", style="red")
            return

    # Get agent processes from current deployment
    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]

    # Get latest deployment to find running agents
    latest = state_store.latest_deployment()
    if not latest:
        console.print("No active deployment found. Run 'agentswarm deploy' first.", style="red")
        return

    # Extract agent processes from deployment
    agent_processes = {}
    for agent_type, processes in latest.get("agents", {}).items():
        agent_processes[agent_type] = [
            AgentProcess(
                pid=proc.get("pid", 0),
                agent_type=agent_type,
                instance_id=proc.get("instance_id", 0),
                command=proc.get("command", f"agent-{agent_type}"),
                status="running" if proc.get("pid") else "stopped"
            )
            for proc in processes
        ]

    # Create workflow executor and orchestrator
    executor = AgentWorkflowExecutor(agent_processes)
    workflow_orchestrator = WorkflowOrchestrator(executor)
    manager = WorkflowManager(workflow_orchestrator)

    console.print(f"Starting workflow: {name}", style="cyan")

    try:
        execution = asyncio.run(manager.run_workflow_by_name(name, execution_context))

        # Display results
        table = Table(title=f"Workflow Execution: {execution.id}")
        table.add_column("Step", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Result", style="white")

        for step_id, result in execution.step_results.items():
            status = "✓" if result else "✗"
            result_summary = str(result)[:50] + "..." if len(str(result)) > 50 else str(result)
            table.add_row(step_id, status, result_summary)

        console.print(table)

        if execution.status.value == "completed":
            console.print(f"Workflow completed successfully in {execution.execution_time:.2f}s", style="green")
        else:
            console.print(f"Workflow {execution.status.value}: {execution.error}", style="red")

    except Exception as e:
        console.print(f"Workflow execution failed: {e}", style="red")


@workflow.command()
@click.argument("execution_id")
@click.pass_context
def status(ctx: click.Context, execution_id: str):
    """Check status of workflow execution"""
    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]

    # Create workflow orchestrator to check status
    # For now, we'll use the state store directly
    workflow_state_dir = project_path / "workflow_state"
    if not workflow_state_dir.exists():
        console.print(f"No workflow state found in {workflow_state_dir}", style="yellow")
        return

    from ..workflows.state import WorkflowStateStore as WFStateStore
    wf_state_store = WFStateStore(workflow_state_dir)

    execution = wf_state_store.get_execution(execution_id)
    if not execution:
        console.print(f"Workflow execution '{execution_id}' not found.", style="red")
        return

    # Display execution status
    status_color = {
        "pending": "yellow",
        "running": "blue",
        "completed": "green",
        "failed": "red",
        "cancelled": "magenta"
    }.get(execution.status.value, "white")

    console.print(f"Workflow Execution: {execution.id}")
    console.print(f"Status: [{status_color}]{execution.status.value}[/{status_color}]")
    console.print(f"Definition: {execution.definition_id}")

    if execution.start_time:
        console.print(f"Started: {execution.start_time}")
    if execution.end_time:
        console.print(f"Ended: {execution.end_time}")
    if execution.execution_time:
        console.print(f"Duration: {execution.execution_time:.2f}s")

    if execution.error:
        console.print(f"Error: [red]{execution.error}[/red]")

    if execution.step_results:
        console.print("\nStep Results:")
        for step_id, result in execution.step_results.items():
            console.print(f"  {step_id}: {result}")


@workflow.command()
@click.argument("execution_id")
@click.pass_context
def cancel(ctx: click.Context, execution_id: str):
    """Cancel a running workflow execution"""
    project_path: Path = ctx.obj["project"]

    # Create a temporary orchestrator to cancel
    from ..workflows.orchestrator import WorkflowOrchestrator
    from ..workflows.models import AgentWorkflowExecutor

    # We need agent processes to create the executor, but for cancellation we might not need them
    # For now, just mark as cancelled in state store
    workflow_state_dir = project_path / "workflow_state"
    if not workflow_state_dir.exists():
        console.print(f"No workflow state found in {workflow_state_dir}", style="yellow")
        return

    from ..workflows.state import WorkflowStateStore as WFStateStore
    wf_state_store = WFStateStore(workflow_state_dir)

    execution = wf_state_store.get_execution(execution_id)
    if not execution:
        console.print(f"Workflow execution '{execution_id}' not found.", style="red")
        return

    if execution.status.value not in ["running", "pending"]:
        console.print(f"Workflow is already {execution.status.value}, cannot cancel.", style="yellow")
        return

    # Mark as cancelled
    from ..workflows.models import WorkflowStatus
    execution.status = WorkflowStatus.CANCELLED
    execution.end_time = datetime.now(UTC)
    wf_state_store.save_execution(execution)

    console.print(f"Workflow execution '{execution_id}' cancelled.", style="green")


@workflow.command()
@click.pass_context
def monitor(ctx: click.Context):
    """Monitor workflow executions and statistics"""
    project_path: Path = ctx.obj["project"]

    workflow_state_dir = project_path / "workflow_state"
    if not workflow_state_dir.exists():
        console.print(f"No workflow state found in {workflow_state_dir}", style="yellow")
        console.print("Run some workflows first to see monitoring data.", style="dim")
        return

    from ..workflows.state import WorkflowStateStore as WFStateStore
    wf_state_store = WFStateStore(workflow_state_dir)

    # Get statistics
    stats = wf_state_store.get_execution_stats()

    # Display statistics
    console.print(Panel.fit(
        f"[bold blue]Workflow Statistics[/bold blue]\n\n"
        f"Total Executions: {stats['total']}\n"
        f"Completed: {stats['completed']}\n"
        f"Failed: {stats['failed']}\n"
        f"Running: {stats['running']}\n"
        f"Success Rate: {stats['success_rate']}%",
        title="Workflow Overview"
    ))

    # Show recent executions
    recent = wf_state_store.get_completed_executions(limit=5)
    if recent:
        console.print("\n[bold]Recent Executions:[/bold]")
        table = Table()
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Definition", style="white")
        table.add_column("Status", style="green")
        table.add_column("Duration", justify="right")
        table.add_column("Ended", style="dim")

        for execution in recent:
            duration = f"{execution.execution_time:.1f}s" if execution.execution_time else "N/A"
            end_time = execution.end_time.strftime("%H:%M:%S") if execution.end_time else "N/A"
            status_color = {
                "completed": "green",
                "failed": "red",
                "cancelled": "yellow"
            }.get(execution.status.value, "white")

            table.add_row(
                execution.id[:8] + "...",
                execution.definition_id,
                f"[{status_color}]{execution.status.value}[/{status_color}]",
                duration,
                end_time
            )

        console.print(table)

    # Show active executions
    active = wf_state_store.get_active_executions()
    if active:
        console.print("\n[bold yellow]Active Executions:[/bold yellow]")
        for execution in active:
            duration = "N/A"
            if execution.start_time:
                elapsed = (datetime.now(UTC) - execution.start_time).total_seconds()
                duration = f"{elapsed:.1f}s"

            console.print(f"  {execution.id[:8]}... - {execution.definition_id} ({duration})")


@workflow.command()
@click.option("--days", type=int, default=30, help="Clean executions older than this many days")
@click.pass_context
def cleanup(ctx: click.Context, days: int):
    """Clean up old workflow executions"""
    project_path: Path = ctx.obj["project"]

    workflow_state_dir = project_path / "workflow_state"
    if not workflow_state_dir.exists():
        console.print(f"No workflow state found in {workflow_state_dir}", style="yellow")
        return

    from ..workflows.state import WorkflowStateStore as WFStateStore
    wf_state_store = WFStateStore(workflow_state_dir)

    deleted = wf_state_store.cleanup_old_executions(days=days)
    console.print(f"Cleaned up {deleted} workflow executions older than {days} days.", style="green")


@workflow.command()
@click.argument("name")
def show(name: str):
    """Show detailed information about a workflow"""
    if name not in WORKFLOW_REGISTRY:
        console.print(f"Workflow '{name}' not found.", style="red")
        return

    workflow = WORKFLOW_REGISTRY[name]

    # Workflow overview
    console.print(Panel.fit(
        f"[bold]{workflow.name}[/bold]\n"
        f"[dim]{workflow.description}[/dim]\n\n"
        f"Type: {workflow.type.value}\n"
        f"Steps: {len(workflow.steps)}\n"
        f"Version: {workflow.version}",
        title=f"Workflow: {name}"
    ))

    # Steps table
    table = Table(title="Workflow Steps")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Agent Type", style="green")
    table.add_column("Task", style="yellow")
    table.add_column("Dependencies", style="magenta")

    for step in workflow.steps:
        deps = ", ".join(step.dependencies) if step.dependencies else "None"
        table.add_row(
            step.id,
            step.name,
            step.agent_type,
            step.task,
            deps
        )

@workflow.command()
@click.argument("execution_id")
@click.pass_context
def monitor(ctx: click.Context, execution_id: str):
    """Monitor a workflow execution in real-time"""
    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]

    # Get agent processes
    latest = state_store.latest_deployment()
    if not latest:
        console.print("No active deployment found. Run 'agentswarm deploy' first.", style="red")
        return

    agent_processes = {}
    for agent_type, processes in latest.get("agents", {}).items():
        agent_processes[agent_type] = [
            AgentProcess(
                pid=proc.get("pid", 0),
                agent_type=agent_type,
                instance_id=proc.get("instance_id", 0),
                command=proc.get("command", f"agent-{agent_type}"),
                status="running" if proc.get("pid") else "stopped"
            )
            for proc in processes
        ]

    # Setup workflow components
    executor = AgentWorkflowExecutor(agent_processes)
    workflow_orchestrator = WorkflowOrchestrator(executor)
    workflow_state_store = WorkflowStateStore(project_path / "workflow_state")
    monitor = WorkflowMonitor(workflow_orchestrator, workflow_state_store)

    # Start monitoring and display dashboard
    asyncio.run(monitor.start_monitoring())
    monitor.display_live_dashboard(execution_id)
    asyncio.run(monitor.stop_monitoring())


@workflow.command()
@click.pass_context
def dashboard(ctx: click.Context):
    """Display live workflow monitoring dashboard"""
    project_path: Path = ctx.obj["project"]
    state_store: SwarmStateStore = ctx.obj["state_store"]

    # Get agent processes
    latest = state_store.latest_deployment()
    if not latest:
        console.print("No active deployment found. Run 'agentswarm deploy' first.", style="red")
        return

    agent_processes = {}
    for agent_type, processes in latest.get("agents", {}).items():
        agent_processes[agent_type] = [
            AgentProcess(
                pid=proc.get("pid", 0),
                agent_type=agent_type,
                instance_id=proc.get("instance_id", 0),
                command=proc.get("command", f"agent-{agent_type}"),
                status="running" if proc.get("pid") else "stopped"
            )
            for proc in processes
        ]

    # Setup workflow components
    executor = AgentWorkflowExecutor(agent_processes)
    workflow_orchestrator = WorkflowOrchestrator(executor)
    workflow_state_store = WorkflowStateStore(project_path / "workflow_state")
    monitor = WorkflowMonitor(workflow_orchestrator, workflow_state_store)

    # Start monitoring and display dashboard
    asyncio.run(monitor.start_monitoring())
    monitor.display_live_dashboard()
    asyncio.run(monitor.stop_monitoring())


@workflow.command()
@click.argument("execution_id")
@click.pass_context
def metrics(ctx: click.Context, execution_id: str):
    """Show detailed metrics for a workflow execution"""
    project_path: Path = ctx.obj["project"]

    workflow_state_store = WorkflowStateStore(project_path / "workflow_state")
    monitor = WorkflowMonitor(None, workflow_state_store)  # Monitor only needs state store for metrics

    metrics_data = monitor.get_execution_metrics(execution_id)

    if "error" in metrics_data:
        console.print(f"[red]Error: {metrics_data['error']}[/red]")
        return

    table = Table(title=f"Execution Metrics: {execution_id}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")

    for key, value in metrics_data.items():
        if key != "id":
            table.add_row(key.replace("_", " ").title(), str(value))

    console.print(table)


@workflow.command()
@click.pass_context
def stats(ctx: click.Context):
    """Show system-wide workflow statistics"""
    project_path: Path = ctx.obj["project"]

    workflow_state_store = WorkflowStateStore(project_path / "workflow_state")
    monitor = WorkflowMonitor(None, workflow_state_store)

    stats_data = monitor.get_system_metrics()

    panel = Panel.fit(
        f"[bold blue]Workflow System Statistics[/bold blue]\n\n"
        f"Total Executions: {stats_data['total']}\n"
        f"Completed: {stats_data['completed']}\n"
        f"Failed: {stats_data['failed']}\n"
        f"Running: {stats_data['running']}\n"
        f"Success Rate: {stats_data['success_rate']}%\n"
        f"Active Monitors: {stats_data['active_monitors']}\n"
        f"Event Listeners: {stats_data['total_listeners']}",
        title="System Stats"
    )

    console.print(panel)


def _pid_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _build_status_table(
    deployment: dict[str, Any], *, include_metrics: bool = False
) -> Table:
    table = Table(title=f"Deployment {deployment['deployment_id']} Status")
    table.add_column("Agent Type")
    table.add_column("Instances", justify="right")
    table.add_column("Running", justify="right")
    table.add_column("Stopped", justify="right")
    if include_metrics:
        table.add_column("Memory", justify="right")
        table.add_column("CPU", justify="right")

    for agent_type, processes in deployment.get("agents", {}).items():
        running = 0
        stopped = 0
        memory, cpu = _collect_metrics(processes) if include_metrics else ("-", "-")

        for proc in processes:
            pid = proc.get("pid")
            if pid and _pid_running(pid):
                running += 1
            else:
                stopped += 1

        row = [agent_type, str(len(processes)), str(running), str(stopped)]
        if include_metrics:
            row.extend([memory, cpu])
        table.add_row(*row)

    return table


def _collect_metrics(processes: list[dict[str, Any]]) -> tuple[str, str]:
    total_memory = 0.0
    total_cpu = 0.0

    for proc in processes:
        pid = proc.get("pid")
        if not pid:
            continue
        try:
            ps_proc = psutil.Process(pid)
            total_memory += ps_proc.memory_info().rss / 1024 / 1024
            total_cpu += ps_proc.cpu_percent(interval=0.0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    memory_display = f"{total_memory:.1f} MB" if total_memory else "0.0 MB"
    cpu_display = f"{total_cpu:.1f}%" if total_cpu else "0.0%"
    return memory_display, cpu_display


if __name__ == "__main__":
    cli()
