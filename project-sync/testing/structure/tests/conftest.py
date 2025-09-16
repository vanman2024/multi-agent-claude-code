"""
Pytest configuration and shared fixtures for PROJECT_NAME tests.

This file configures pytest settings and provides common fixtures
used across all test categories.
"""

import pytest
import os
from typing import Generator, Any

# Test markers for categorizing tests
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "contract: Contract tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Tests that take > 5 seconds")
    config.addinivalue_line("markers", "credentials: Tests requiring real credentials")


@pytest.fixture(scope="session")
def test_config() -> dict[str, Any]:
    """Provide test configuration settings."""
    return {
        "environment": os.getenv("TEST_ENV", "test"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "timeout": int(os.getenv("TEST_TIMEOUT", "30")),
    }


@pytest.fixture
def mock_env_vars(monkeypatch) -> Generator[None, None, None]:
    """Mock environment variables for testing."""
    test_vars = {
        "NODE_ENV": "test",
        "PYTHON_ENV": "test", 
        "CI": "true",
    }
    
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
    
    yield


@pytest.fixture
def temp_directory(tmp_path) -> str:
    """Provide a temporary directory for tests."""
    return str(tmp_path)


# Add project-specific fixtures below
# Example:
# @pytest.fixture
# def mock_database():
#     """Mock database connection for tests."""
#     pass