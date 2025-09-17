"""
Pytest Configuration
====================

Central configuration for all backend tests.
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests (fast, isolated)")
    config.addinivalue_line("markers", "integration: Integration tests") 
    config.addinivalue_line("markers", "contract: Contract/API tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "cli: CLI tests")
    config.addinivalue_line("markers", "mcp: MCP server tests")
    config.addinivalue_line("markers", "live: Live API tests (requires credentials)")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "skip_ci: Skip in CI environment")


@pytest.fixture
def api_client():
    """Mock API client for testing."""
    class MockAPIClient:
        def __init__(self, base_url="http://localhost:8000"):
            self.base_url = base_url
            
        async def get(self, endpoint):
            return {"status": "success", "data": []}
            
        async def post(self, endpoint, data):
            return {"status": "created", "id": "123"}
    
    return MockAPIClient()


@pytest.fixture
def sample_data():
    """Generic sample data for tests."""
    return [
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200},
        {"id": 3, "name": "Item 3", "value": 300},
    ]