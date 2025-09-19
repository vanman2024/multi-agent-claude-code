# AgentSwarm Multi-Agent Workflows

A comprehensive multi-agent workflow orchestration system for coordinating complex agent interactions and task pipelines.

## Overview

The workflow system enables you to define, execute, and monitor sophisticated multi-agent workflows that coordinate multiple AI agents working together on complex tasks. Workflows can be sequential, parallel, conditional, or pipeline-based.

## Key Features

- **Multiple Workflow Types**: Sequential, parallel, conditional, and pipeline workflows
- **Agent Coordination**: Automatic coordination between different agent types
- **Real-time Monitoring**: Live dashboards and execution tracking
- **State Persistence**: Workflow state survives restarts
- **Error Handling**: Retry logic and failure recovery
- **Resource Management**: Prevent resource conflicts between workflows

## Available Workflows

### Business Workflows
- **Lead Generation**: Multi-agent lead research, enrichment, scoring, and validation
- **Customer Support**: Automated issue classification, diagnosis, and resolution

### Content Workflows
- **Content Generation**: Research, writing, editing, and SEO optimization pipeline

### Data Workflows
- **Data Analysis**: Collection, cleaning, analysis, visualization, and insights

### Research Workflows
- **Research & Development**: Hypothesis generation, literature review, experimentation, and conclusions

## Quick Start

### 1. Deploy Agent Swarm
```bash
# Initialize project
agentswarm init my-project
cd my-project

# Deploy agents
agentswarm deploy --instances codex:2,claude:1,research_agent:1
```

### 2. Run a Workflow
```bash
# List available workflows
agentswarm workflow list

# Run a lead generation workflow
agentswarm workflow run lead-generation

# Run with custom context
agentswarm workflow run lead-generation --context '{"target_company": "TechCorp", "industry": "SaaS"}'
```

### 3. Monitor Execution
```bash
# Monitor specific execution
agentswarm workflow monitor <execution-id>

# View live dashboard
agentswarm workflow dashboard

# Check execution metrics
agentswarm workflow metrics <execution-id>

# View system statistics
agentswarm workflow stats
```

## Workflow Types

### Sequential Workflows
Steps execute one after another, each waiting for the previous to complete.

```yaml
type: sequential
steps:
  - id: research
    agent_type: research_agent
    task: research_topic
  - id: write
    agent_type: writing_agent
    task: write_content
    dependencies: [research]
```

### Parallel Workflows
Independent steps execute simultaneously, with dependencies respected.

```yaml
type: parallel
steps:
  - id: search_linkedin
    agent_type: search_agent
    task: search_linkedin
  - id: search_website
    agent_type: search_agent
    task: search_website
  - id: enrich
    agent_type: enrichment_agent
    task: enrich_data
    dependencies: [search_linkedin, search_website]
```

### Pipeline Workflows
Data flows between steps, with each step processing the output of the previous.

```yaml
type: pipeline
steps:
  - id: collect
    agent_type: data_agent
    task: collect_data
  - id: clean
    agent_type: cleaning_agent
    task: clean_data
  - id: analyze
    agent_type: analysis_agent
    task: analyze_data
```

## Custom Workflows

### Creating Custom Workflows

1. **Define Workflow Structure**
```python
from agentswarm.workflows.models import WorkflowDefinition, WorkflowStep, WorkflowType

custom_workflow = WorkflowDefinition(
    id="my-custom-workflow",
    name="My Custom Workflow",
    description="Description of my workflow",
    type=WorkflowType.SEQUENTIAL,
    steps=[
        WorkflowStep(
            id="step1",
            name="First Step",
            description="Description of first step",
            agent_type="my_agent",
            task="my_task",
            parameters={"param1": "value1"}
        ),
        # Add more steps...
    ]
)
```

2. **Register Workflow**
```python
from agentswarm.workflows.models import WORKFLOW_REGISTRY

WORKFLOW_REGISTRY["my-workflow"] = custom_workflow
```

3. **Execute Workflow**
```bash
agentswarm workflow run my-workflow
```

## Monitoring & Debugging

### Real-time Monitoring
```bash
# Live dashboard for all executions
agentswarm workflow dashboard

# Monitor specific execution
agentswarm workflow monitor <execution-id>
```

### Execution History
```bash
# View execution status
agentswarm workflow status <execution-id>

# Get detailed metrics
agentswarm workflow metrics <execution-id>

# View system statistics
agentswarm workflow stats
```

### Logs and Debugging
Workflow executions are logged with detailed information about each step, timing, and any errors. Check the project logs directory for comprehensive execution logs.

## Configuration

### Workflow Parameters
- **timeout**: Maximum execution time per step (seconds)
- **retry_count**: Number of retry attempts on failure
- **retry_delay**: Delay between retry attempts (seconds)
- **dependencies**: List of step IDs that must complete first

### Agent Requirements
Each workflow step specifies the `agent_type` required. Ensure your agent swarm deployment includes the necessary agent types:

```bash
# Deploy with required agents
agentswarm deploy --instances search_agent:2,enrichment_agent:1,analysis_agent:1
```

## Advanced Features

### Conditional Logic
Workflows can include conditional branching based on step results:

```python
# Conditional step execution based on previous results
if execution.context.get("lead_score", 0) > 7:
    # High-value lead processing
    await self._execute_step(high_value_step, execution)
else:
    # Standard lead processing
    await self._execute_step(standard_step, execution)
```

### Resource Coordination
The system automatically coordinates resource usage to prevent conflicts between concurrent workflows.

### Error Recovery
- Automatic retry with configurable backoff
- Step-level error handling
- Workflow-level failure recovery
- Detailed error reporting and logging

## API Reference

### WorkflowOrchestrator
Main orchestration engine for executing workflows.

### WorkflowManager
High-level interface for managing workflow definitions and executions.

### WorkflowMonitor
Real-time monitoring and event handling for workflow executions.

### WorkflowStateStore
Persistent storage for workflow execution state and history.

## Troubleshooting

### Common Issues

1. **"No agents available for type"**
   - Ensure your agent swarm includes the required agent types
   - Check agent deployment status: `agentswarm monitor`

2. **Workflow stuck in pending**
   - Check agent availability and resource locks
   - Review workflow dependencies and step requirements

3. **Execution failures**
   - Check workflow logs for detailed error information
   - Verify agent configurations and API access
   - Review step parameters and context data

### Performance Tuning

- **Parallel Execution**: Use parallel workflows for independent tasks
- **Resource Pooling**: Deploy multiple instances of bottleneck agent types
- **Caching**: Implement result caching for expensive operations
- **Monitoring**: Use live dashboards to identify performance bottlenecks

## Contributing

To add new workflow types or agent integrations:

1. Extend the `WorkflowType` enum for new workflow patterns
2. Implement custom `WorkflowExecutor` subclasses for specialized execution
3. Add workflow templates to `templates.py`
4. Update CLI commands for new functionality
5. Add comprehensive tests and documentation

## License

This workflow system is part of the AgentSwarm project and follows the same licensing terms.
