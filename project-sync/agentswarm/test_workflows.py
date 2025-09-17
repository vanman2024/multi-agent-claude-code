#!/usr/bin/env python3
"""Test script for AgentSwarm Multi-Agent Workflow System."""

import asyncio
import sys
from pathlib import Path

# Add agentswarm to path
agentswarm_dir = Path(__file__).parent
if str(agentswarm_dir) not in sys.path:
    sys.path.insert(0, str(agentswarm_dir))

from workflows.models import AgentWorkflowExecutor, WORKFLOW_REGISTRY
from workflows.orchestrator import WorkflowOrchestrator, WorkflowManager
from workflows.state import WorkflowStateStore
from workflows.monitor import WorkflowMonitor
from core.models import AgentProcess


async def test_workflow_system():
    """Test the complete workflow system."""
    print("🧪 Testing AgentSwarm Multi-Agent Workflow System")
    print("=" * 50)

    # Create mock agent processes
    mock_agents = {
        "search_agent": [
            AgentProcess("search-1", "search_agent", 1234, "running"),
            AgentProcess("search-2", "search_agent", 1235, "running"),
        ],
        "enrichment_agent": [
            AgentProcess("enrich-1", "enrichment_agent", 1236, "running"),
        ],
        "analysis_agent": [
            AgentProcess("analysis-1", "analysis_agent", 1237, "running"),
        ],
        "validation_agent": [
            AgentProcess("validation-1", "validation_agent", 1238, "running"),
        ],
        "segmentation_agent": [
            AgentProcess("segment-1", "segmentation_agent", 1239, "running"),
        ],
    }

    # Setup components
    executor = AgentWorkflowExecutor(mock_agents)
    orchestrator = WorkflowOrchestrator(executor)
    manager = WorkflowManager(orchestrator)

    # Test workflow listing
    print("📋 Available workflows:")
    workflows = manager.get_available_workflows()
    for workflow in workflows:
        definition = manager.get_workflow_definition(workflow)
        if definition:
            print(f"  • {workflow}: {definition.description} ({len(definition.steps)} steps)")

    print(f"\n✅ Found {len(workflows)} workflows")

    # Test workflow execution
    print("\n🚀 Testing workflow execution...")
    test_workflow = "lead-generation"

    if test_workflow in workflows:
        print(f"Executing workflow: {test_workflow}")

        try:
            execution = await manager.run_workflow_by_name(test_workflow)

            print("✅ Workflow execution completed!"            print(f"   Status: {execution.status.value}")
            print(".2f"            print(f"   Steps completed: {len(execution.step_results)}")

            # Show step results
            print("\n📊 Step Results:")
            for step_id, result in execution.step_results.items():
                status = "✅" if result else "❌"
                print(f"   {status} {step_id}: {result}")

        except Exception as e:
            print(f"❌ Workflow execution failed: {e}")
            return False
    else:
        print(f"❌ Test workflow '{test_workflow}' not found")
        return False

    # Test state persistence
    print("\n💾 Testing state persistence...")
    state_dir = Path("test_workflow_state")
    state_store = WorkflowStateStore(state_dir)

    # Save execution
    if 'execution' in locals():
        state_store.save_execution(execution)
        print("✅ Execution saved to state store")

        # Retrieve execution
        retrieved = state_store.get_execution(execution.id)
        if retrieved:
            print("✅ Execution retrieved from state store")
        else:
            print("❌ Failed to retrieve execution from state store")
            return False

    # Test monitoring
    print("\n📊 Testing monitoring system...")
    monitor = WorkflowMonitor(orchestrator, state_store)

    metrics = monitor.get_execution_metrics(execution.id)
    if metrics and "error" not in metrics:
        print("✅ Monitoring system working")
        print(f"   Success rate: {metrics.get('success_rate', 0) * 100:.1f}%")
    else:
        print("❌ Monitoring system failed")
        return False

    # Cleanup
    import shutil
    if state_dir.exists():
        shutil.rmtree(state_dir)
        print("🧹 Cleaned up test state directory")

    print("\n🎉 All tests passed! Multi-agent workflow system is working correctly.")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_workflow_system())
    sys.exit(0 if success else 1)
