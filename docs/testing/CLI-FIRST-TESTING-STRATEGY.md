# CLI-First Testing Strategy

## Overview

This document defines the testing strategy for CLI-first, agent-driven applications where frontend UIs are optional or non-existent. This approach prioritizes API testing through CLI commands and MCP server orchestration.

## Core Principles

1. **CLI is the Primary Interface** - All testing happens through CLI commands
2. **Agents Execute Tests** - AI agents run and validate tests
3. **MCP Orchestrates** - MCP servers coordinate test execution
4. **Frontend Optional** - UI testing only when UI exists
5. **No Conflicts** - Single test strategy that adapts to project type

## Project Type Detection

### Auto-Detection Logic
```javascript
detectProjectType() {
  return {
    hasBackend: exists('api/') || exists('src/services/'),
    hasFrontend: exists('public/') || exists('src/pages/'),
    hasCLI: exists('cli/') || exists('src/cli/'),
    hasMCP: exists('.claude/mcp-servers.json'),
    runtime: detectRuntime() // python, node, both
  }
}
```

### Project Classifications

| Project Type | Backend | Frontend | CLI | MCP | Example |
|-------------|---------|----------|-----|-----|---------|
| API-Only | ✅ | ❌ | ✅ | ✅ | Signal Hire |
| Full-Stack | ✅ | ✅ | ✅ | ✅ | E-commerce |
| CLI Tool | ⚠️ | ❌ | ✅ | ✅ | Dev Tools |
| Hybrid | ✅ | ⚠️ | ✅ | ✅ | Admin Panel |

## Unified Test Structure

```
tests/
├── cli/                    # CLI command testing
│   ├── commands/          # Individual command tests
│   │   ├── test_api.py
│   │   ├── test_agent.py
│   │   └── test_mcp.py
│   ├── workflows/         # Multi-command workflows
│   └── integration/       # CLI + API integration
│
├── api/                   # API endpoint testing
│   ├── unit/             # Isolated endpoint tests
│   ├── contract/         # API contract validation
│   └── integration/      # External service tests
│
├── mcp/                  # MCP server testing
│   ├── servers/          # Server protocol tests
│   ├── tools/            # Tool execution tests
│   └── coordination/     # Multi-server orchestration
│
├── agents/               # Agent-specific tests
│   ├── claude/          # Claude agent tests
│   ├── copilot/         # Copilot agent tests
│   └── qwen/            # Qwen agent tests
│
├── e2e/                 # End-to-end scenarios
│   └── scenarios/       # Complete user journeys
│
└── performance/         # Load and stress testing
```

## Testing Commands

### Universal Test Command
```bash
# Auto-detects project type and runs appropriate tests
./scripts/ops test

# With specific flags
./scripts/ops test --cli-only     # No browser testing
./scripts/ops test --api-only     # API endpoints only
./scripts/ops test --mcp-only     # MCP servers only
./scripts/ops test --quick        # Smoke tests only
```

### Project-Specific Commands

#### API-Only Projects (Signal Hire Pattern)
```bash
# Test API endpoints via CLI
cli test api --all
cli test api --endpoint users --method GET
cli test api --contract swagger.json

# Test MCP integration
cli test mcp --server signal-hire
cli test mcp --tool search_candidates

# Test complete workflows
cli test workflow --scenario hiring
cli test workflow --scenario screening
```

#### Full-Stack Projects (Optional UI)
```bash
# Backend testing (always available)
cli test backend --all
cli test backend --api
cli test backend --services

# Frontend testing (only if detected)
cli test frontend --detect  # Auto-detect UI
cli test frontend --skip    # Skip even if exists

# Integration testing
cli test integration --mode cli     # CLI only
cli test integration --mode hybrid  # CLI + UI
```

## Agent-Driven Testing

### Agent Test Delegation
```bash
# Claude handles complex integration tests
cli agent test --use claude --suite integration

# Copilot handles simple unit tests
cli agent test --use copilot --suite unit

# Qwen handles performance tests
cli agent test --use qwen --suite performance

# Gemini handles large codebase analysis
cli agent test --use gemini --suite analysis
```

### MCP Coordination
```python
# MCP server for test orchestration
@mcp.tool()
async def orchestrate_tests(
    agent: str,
    suite: str,
    parallel: bool = False
):
    """Coordinate multi-agent testing"""
    if parallel:
        return await run_parallel_tests(agent, suite)
    return await run_sequential_tests(agent, suite)
```

## CLI Testing Patterns

### Command Testing
```python
# tests/cli/commands/test_api.py
import pytest
from cli import CLI

def test_api_list_command():
    """Test CLI api list command"""
    cli = CLI()
    result = cli.execute(['api', 'list'])
    assert result.exit_code == 0
    assert 'Available endpoints' in result.output

def test_api_test_command():
    """Test CLI api test command"""
    cli = CLI()
    result = cli.execute(['api', 'test', '--endpoint', 'users'])
    assert result.exit_code == 0
    assert 'Test passed' in result.output
```

### Workflow Testing
```python
# tests/cli/workflows/test_hiring.py
async def test_complete_hiring_workflow():
    """Test complete hiring workflow via CLI"""
    cli = CLI()
    
    # Step 1: Search candidates
    result = await cli.execute(['search', '--skill', 'python'])
    assert result.success
    candidate_id = result.data['candidates'][0]['id']
    
    # Step 2: Screen candidate
    result = await cli.execute(['screen', '--id', candidate_id])
    assert result.success
    
    # Step 3: Schedule interview
    result = await cli.execute(['schedule', '--id', candidate_id])
    assert result.success
```

## MCP Testing Integration

### MCP Server Tests
```python
# tests/mcp/servers/test_signal_hire.py
from fastmcp.testing import MCPTestClient

async def test_mcp_server_initialization():
    """Test MCP server starts correctly"""
    async with MCPTestClient("signal-hire") as client:
        # Test server responds
        response = await client.list_tools()
        assert len(response.tools) > 0
        
        # Test specific tool
        result = await client.call_tool(
            "search_candidates",
            {"skills": ["python"]}
        )
        assert result.success
```

### MCP Tool Tests
```python
# tests/mcp/tools/test_search.py
async def test_search_tool_execution():
    """Test MCP search tool"""
    server = SignalHireMCP()
    result = await server.execute_tool(
        "search",
        {"query": "python developer"}
    )
    assert result["success"] == True
    assert len(result["candidates"]) > 0
```

## Performance Testing

### CLI Performance
```bash
# Measure CLI response times
cli perf test --command "api list" --iterations 100
cli perf test --command "search --skill python" --concurrent 10
```

### API Performance
```python
# tests/performance/test_api_load.py
import asyncio
from locust import HttpUser, task

class APIUser(HttpUser):
    @task
    def search_candidates(self):
        self.client.get("/api/candidates?skill=python")
    
    @task
    def get_candidate(self):
        self.client.get("/api/candidates/123")
```

## Environment Configuration

### Test Environment Variables
```bash
# .env.test
TEST_MODE=cli-only
API_BASE_URL=http://localhost:3000
MCP_TEST_SERVERS=signal-hire,filesystem,memory
AGENT_TEST_MODE=mock  # or live
SKIP_FRONTEND_TESTS=true  # for API-only projects
```

### CI/CD Configuration
```yaml
# .github/workflows/test.yml
jobs:
  test:
    steps:
      - name: Detect Project Type
        run: |
          PROJECT_TYPE=$(./scripts/ops detect-type)
          echo "PROJECT_TYPE=$PROJECT_TYPE" >> $GITHUB_ENV
      
      - name: Run Appropriate Tests
        run: |
          if [ "$PROJECT_TYPE" = "api-only" ]; then
            ./scripts/ops test --cli-only
          else
            ./scripts/ops test --all
          fi
```

## Migration Path

### From Current Structure
1. Keep `backend-tests/` for Python projects
2. Keep `frontend-tests-template/` for full-stack
3. Add `tests/cli/` for CLI testing
4. Add `tests/mcp/` for MCP testing
5. Update `ops` script to detect and route

### Progressive Enhancement
```bash
# Start with CLI tests only
./scripts/ops test --cli-only

# Add API tests when ready
./scripts/ops test --cli-only --api

# Add frontend tests if needed
./scripts/ops test --all
```

## Best Practices

1. **Always Test Through CLI First** - Even if UI exists
2. **Mock External Services** - Use MCP mocking capabilities
3. **Parallel Agent Testing** - Run different suites simultaneously
4. **Contract-First API Testing** - Validate against OpenAPI/GraphQL schemas
5. **Environment Isolation** - Separate test environments per agent

## Example: Signal Hire Testing

```bash
# Complete test suite for API-only project
./scripts/ops test --project signal-hire

# What it runs:
# 1. CLI command tests (all commands work)
# 2. API endpoint tests (all endpoints respond)
# 3. MCP server tests (server protocol works)
# 4. Integration tests (external services)
# 5. Workflow tests (complete scenarios)
# 6. Performance tests (load handling)

# No frontend tests - project has no UI
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Frontend tests run for API project | Add `SKIP_FRONTEND_TESTS=true` to .env |
| MCP server tests fail | Ensure MCP servers are installed |
| CLI tests timeout | Increase timeout in test config |
| Agent tests conflict | Run agents in separate processes |

### Debug Commands
```bash
# Debug test detection
./scripts/ops test --detect --verbose

# Debug specific test suite
./scripts/ops test --suite cli --debug

# Run single test
./scripts/ops test --file tests/cli/test_api.py
```

## Summary

This CLI-first testing strategy ensures:
- No conflicts between frontend/backend testing
- Seamless testing for API-only projects
- Agent-driven test execution
- MCP server integration
- Adaptive testing based on project type

The key is that **testing adapts to your project**, not the other way around.