# Generic Backend Test Suite

## Test Organization

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── smoke/                   # Quick smoke tests for basic functionality
│   └── test_deps.py        # Dependency availability tests
├── unit/                    # Unit tests for individual components
│   └── test_export_comprehensive.py
├── integration/             # Integration tests with external services
│   └── browser/            # Browser integration if needed
├── browser/                 # Browser automation specific tests (optional)
│   ├── test_docker_browser.py      # Docker environment browser tests
│   ├── test_live_browser.py        # Live browser functionality tests
│   └── test_real_browser.py        # Real browser interaction tests
├── contract/               # API/UI contract tests
├── mcp/                    # MCP server/client tests
│   ├── test_mcp_server.py  # MCP server protocol tests
│   ├── test_mcp_client.py  # MCP client integration tests
│   └── test_mcp_tools.py   # MCP tool execution tests
├── performance/            # Performance and load tests
└── helpers/               # Test helper utilities
```

## Test Categories

### 🏃 Smoke Tests (`tests/smoke/`)
**Purpose**: Quick validation that basic functionality works
**Runtime**: < 5 seconds
**Dependencies**: None (mocked)
```bash
pytest tests/smoke/ -v
```

### 🔬 Unit Tests (`tests/unit/`)
**Purpose**: Test individual components in isolation
**Runtime**: < 30 seconds total
**Dependencies**: Mocked external services
```bash
pytest tests/unit/ -v
```

### 🔌 Integration Tests (`tests/integration/`)
**Purpose**: Test integration with external services
**Runtime**: 30 seconds - 2 minutes
**Dependencies**: Real external services (limited calls)
```bash
pytest tests/integration/ -v -m "not slow"
```

### 🌐 Browser Tests (`tests/browser/`)
**Purpose**: Browser automation functionality
**Runtime**: 1-5 minutes
**Dependencies**: Browser, internet connection
```bash
pytest tests/browser/ -v -m "not credentials"
```

### 📋 Contract Tests (`tests/contract/`)
**Purpose**: Verify external API/UI contracts haven't changed
**Runtime**: 10-60 seconds
**Dependencies**: Internet connection
```bash
pytest tests/contract/ -v
```

### 🔗 MCP Tests (`tests/mcp/`)
**Purpose**: Validate MCP servers/clients and tools using FastMCP CLI patterns
**Runtime**: milliseconds (in-memory) to seconds
**Dependencies**: `fastmcp` installed for Python tests

The MCP tests follow FastMCP CLI patterns for running servers:

#### FastMCP CLI Pattern Support
```python
# Inferred server instance (looks for mcp, server, or app)
runner = FastMCPRunner()
server = runner.load_server("server.py")

# Explicit server entrypoint
server = runner.load_server("server.py:custom_name")

# Factory function (sync or async)
server = runner.load_server("server.py:create_server")

# FastMCP configuration file
server = runner.load_server("fastmcp.json")

# Remote server proxy
server = runner.load_server("https://example.com/mcp")
```

#### Running Tests
```bash
# Run MCP-only tests
pytest tests/mcp -v -m mcp

# Skip tests that spawn separate processes
pytest tests/mcp -v -m "mcp and not client_process"

# Install dependency if missing
pip install fastmcp

# Run FastMCP pattern tests
pytest tests/mcp/test_fastmcp_patterns.py -v

# Run FastMCP server tests
pytest tests/mcp/test_fastmcp_server.py -v
```

#### Test Context Manager
```python
# Use in tests like fastmcp run
async with fastmcp_test_server("server.py") as server:
    # Test server functionality
    tools = server.list_tools()
    assert len(tools) > 0
```

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Quick tests only
pytest -m "smoke or unit" -v

# Skip slow tests
pytest -m "not slow" -v

# Skip tests requiring credentials
pytest -m "not credentials" -v

# Browser tests only
pytest -m "browser" -v

# Integration tests only  
pytest -m "integration" -v
```

## API Testing Strategy: CLI-First Approach

### Why CLI Over Postman
Since we're building a CLI for local agent management, we get API testing "for free":
- **Single tool** for both management and testing
- **Version controlled** test scripts alongside code
- **Agent integration** - agents can run tests automatically
- **CI/CD friendly** - no external dependencies
- **Programmable** - complex test scenarios in code

### CLI Testing Architecture
```bash
# CLI manages both application and tests
cli test api --endpoint users --method GET
cli test mcp --server filesystem --method list
cli test integration --suite full
cli test performance --concurrent 10

# Agent-driven testing
cli agent test --agent claude --suite contract
cli agent test --agent qwen --suite performance
```

## Environment Variables

Set these for comprehensive testing:

```bash
# API credentials (for integration/live tests)
export API_BASE_URL="http://localhost:3000"
export API_KEY="your-api-key"
export API_SECRET="your-api-secret"

# MCP Server Configuration
export MCP_SERVER_URL="stdio://./mcp-server"
export MCP_AUTH_TOKEN="your-mcp-token"

# Browser testing (optional)
export BROWSER_EXECUTABLE="/usr/bin/chromium"
export HEADLESS_MODE="true"
```

## Running Tests

### Local Development
```bash
# Quick feedback loop
python3 run.py -m pytest tests/smoke/ tests/unit/ -v

# Full test suite (no credentials needed)
python3 run.py -m pytest -m "not credentials and not slow" -v

# Browser automation tests  
python3 run.py -m pytest tests/browser/ -v --tb=short
```

### Docker Environment
```bash
# Start test environment
docker-compose up -d test-runner

# Run Python tests in container
docker-compose exec test-runner pytest tests/smoke/ tests/unit/ -v

# Run Node.js tests in container
docker-compose exec test-runner npm test

# Run browser tests with display
docker-compose exec test-runner pytest tests/browser/ -v -s
```

### CI/CD Pipeline
```bash
# Automated testing (no manual interaction)
pytest tests/smoke/ tests/unit/ tests/contract/ -v --tb=line
```

## Test Development Guidelines

### Writing New Tests

1. **Choose the right category** based on what you're testing
2. **Use appropriate markers** (`@pytest.mark.unit`, `@pytest.mark.slow`, etc.)
3. **Use fixtures** from `conftest.py` for common setup
4. **Mock external services** in unit tests
5. **Keep tests isolated** - each test should be independent

### Example Test Structure

```python
import pytest
import os
from src.services.api_client import APIClient
from src.mcp.server import MCPServer

@pytest.mark.unit
async def test_api_functionality(sample_data, mock_api):
    \"\"\"Test API client functionality.\"\"\"
    client = APIClient(base_url="http://localhost:3000")
    result = await client.process(sample_data)
    assert result.success is True
    assert len(result.data) > 0

@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("API_KEY"), reason="No API credentials")
async def test_real_api_integration():
    \"\"\"Test real API integration - requires credentials.\"\"\"
    client = APIClient(api_key=os.getenv("API_KEY"))
    response = await client.search("test query")
    assert response.status_code == 200

@pytest.mark.mcp
async def test_mcp_server_initialization():
    \"\"\"Test MCP server starts and responds correctly.\"\"\"
    server = MCPServer(transport="stdio")
    response = await server.handle_request({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    })
    assert response["result"]["tools"] is not None
    
@pytest.mark.mcp
async def test_mcp_tool_execution():
    \"\"\"Test MCP tool execution through server.\"\"\"
    server = MCPServer()
    result = await server.execute_tool("search", {"query": "test"})
    assert result["success"] == True
```

### Debugging Failed Tests

```bash
# Verbose output with full traceback
pytest tests/failing_test.py -v -s --tb=long

# Drop into debugger on failure
pytest tests/failing_test.py --pdb

# Run only failed tests from last run
pytest --lf -v
```

## Test Data

- **Fixtures**: Use fixtures from `conftest.py` for consistent test data
- **Sample Data**: Keep sample data realistic but minimal
- **Secrets**: Never commit real credentials or API keys
- **Cleanup**: Tests should clean up any created files/data

## Browser Test Considerations

- **Headless Mode**: Use `headless=True` for CI/CD, `headless=False` for debugging
- **Screenshots**: Browser tests automatically capture screenshots on failure
- **Timeouts**: Set appropriate timeouts for network operations
- **Rate Limits**: Be mindful of API rate limits in integration tests
- **Isolation**: Each browser test should start with a clean session

This test structure follows the testing pyramid: many unit tests, fewer integration tests, minimal end-to-end tests.
