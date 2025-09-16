"""
Pytest configuration and shared fixtures for SignalHire Agent tests.
Includes opt-in handling for live API tests via RUN_LIVE=1.
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
    """Skip live tests unless RUN_LIVE=1 and SIGNALHIRE_API_KEY is present."""
    run_live = os.getenv("RUN_LIVE") == "1"
    has_key = bool(os.getenv("SIGNALHIRE_API_KEY"))
    if run_live and has_key:
        return
    import pytest
    skip_live = pytest.mark.skip(reason="Set RUN_LIVE=1 and SIGNALHIRE_API_KEY to run live tests")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)



@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# BrowserConfig fixture removed (API-only)
@pytest.fixture
def signalhire_credentials():
    """Provide SignalHire test credentials from environment."""
    return {
        'email': os.getenv('SIGNALHIRE_EMAIL', 'test@example.com'),
        'password': os.getenv('SIGNALHIRE_PASSWORD', 'testpassword')
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
def sample_prospects():
    """Provide sample prospect data for testing."""
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
        "markers", "credentials: Tests that require real SignalHire credentials"
    )
