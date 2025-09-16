"""
Pytest configuration and shared fixtures for backend tests.
Includes opt-in handling for live API tests and MCP server testing.
"""

import pytest
import asyncio
import os
from pathlib import Path
import os
from typing import Dict, Any

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def pytest_collection_modifyitems(config, items):
    """Skip live tests unless RUN_LIVE=1 and API_KEY is present."""
    run_live = os.getenv("RUN_LIVE") == "1"
    has_key = bool(os.getenv("API_KEY"))
    if run_live and has_key:
        return
    import pytest
    skip_live = pytest.mark.skip(reason="Set RUN_LIVE=1 and API_KEY to run live tests")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)



@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def api_credentials():
    """Provide API test credentials from environment."""
    return {
        'api_key': os.getenv('API_KEY'),
        'api_secret': os.getenv('API_SECRET'),
        'base_url': os.getenv('API_BASE_URL', 'http://localhost:3000')
    }


@pytest.fixture
def sample_search_criteria():
    """Provide sample search criteria for testing."""
    return {
        'title': 'Software Engineer',
        'location': 'San Francisco',
        'company': 'Tech Corp'
    }


@pytest.fixture
def sample_results():
    """Provide sample Result data for testing."""
    return [
        {
            "uid": "test_001",
            "full_name": "Test Engineer",
            "title": "Software Engineer",
            "company": "Test Corp",
            "location": "San Francisco, CA",
            "email": "test@testcorp.com",
            "linkedin_url": "https://linkedin.com/in/test-engineer"
        },
        {
            "uid": "test_002", 
            "full_name": "Jane Developer",
            "title": "Senior Developer",
            "company": "Dev Inc",
            "location": "New York, NY",
            "email": "jane@devinc.com",
            "linkedin_url": "https://linkedin.com/in/jane-developer"
        }
    ]


@pytest.fixture
def test_output_dir(tmp_path):
    """Provide a temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir()
    return output_dir


# ============= FastMCP Testing Fixtures =============

@pytest.fixture
def mock_mcp_server():
    """Create a mock MCP server for testing."""
    class MockMCPServer:
        async def handle_request(self, request):
            """Handle JSON-RPC request."""
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {"name": "search", "description": "Search for content"},
                            {"name": "calculate", "description": "Perform calculations"}
                        ]
                    }
                }
            elif method == "resources/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "resources": []
                    }
                }
            elif method == "tools/call":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": "Tool executed"}]
                    }
                }
            elif method == "log":
                # Notifications don't get responses
                return None
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                }
        
        def is_running(self):
            return True
            
        async def initialize(self):
            return True
    
    return MockMCPServer()


@pytest.fixture
def mcp_server_config():
    """Provide MCP server configuration for testing."""
    return {
        'transport': 'stdio',
        'server_url': os.getenv('MCP_SERVER_URL', 'stdio://./mcp-server'),
        'auth_token': os.getenv('MCP_AUTH_TOKEN')
    }


@pytest.fixture  
def sample_tool_schema():
    """Provide sample tool schema for FastMCP testing."""
    return {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "default": 10}
        },
        "required": ["query"]
    }


@pytest.fixture
def sample_mcp_request():
    """Provide sample MCP JSON-RPC request."""
    return {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "search",
            "arguments": {"query": "test query", "limit": 5}
        },
        "id": 1
    }


@pytest.fixture
def fastmcp_test_server():
    """Create a FastMCP test server with common tools."""
    try:
        from fastmcp import FastMCP
    except ImportError:
        pytest.skip("FastMCP not installed")
        
    server = FastMCP("TestServer")
    
    @server.tool
    def echo(message: str) -> str:
        """Echo the message back."""
        return message
        
    @server.tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
        
    @server.resource("config://test")
    def get_config() -> dict:
        """Get test configuration."""
        return {"env": "test", "debug": True}
        
    return server


# Mock browser session fixture removed (API-only)
# Test markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "smoke: Smoke tests for basic functionality"
    )
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components" 
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests with external services"
    )
    config.addinivalue_line(
        "markers", "browser: Browser automation tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests that take >30 seconds"
    )
    config.addinivalue_line(
        "markers", "credentials: Tests that require real API credentials"
    )
    config.addinivalue_line(
        "markers", "mcp: Tests for Model Context Protocol (MCP) servers/clients"
    )
    config.addinivalue_line(
        "markers", "client_process: Tests that spawn a separate client/server process"
    )
    config.addinivalue_line(
        "markers", "cli: Tests for CLI commands and interactions"
    )
    config.addinivalue_line(
        "markers", "asyncio: Async tests requiring event loop"
    )
    config.addinivalue_line(
        "markers", "contract: API contract validation tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance and benchmarking tests"
    )
