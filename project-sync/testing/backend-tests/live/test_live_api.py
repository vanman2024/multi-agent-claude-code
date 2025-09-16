"""
Live API Integration Tests
==========================

Purpose: Validate real API endpoints with actual external service calls.
These tests are skipped by default to avoid API rate limits and costs.

Run with:
  API_KEY=your_key pytest tests/live/ -m live -v
  
Configuration:
  - API_BASE_URL: Base URL of the API service
  - API_KEY: Authentication key for the API
  - API_SECRET: Optional secret for additional auth

Notes:
  - These tests make minimal requests to respect API rate limits
  - Tests are automatically skipped if required credentials are not present
  - Use sparingly in CI/CD - prefer contract tests for regular validation
"""

import os
import pytest
from typing import Optional

# Import your actual API client here
# from src.services.api_client import APIClient


pytestmark = pytest.mark.live


def _require_api_credentials() -> tuple[str, Optional[str]]:
    """Get API credentials from environment or skip test."""
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")  # Optional
    
    if not api_key:
        pytest.skip("API_KEY not set; skipping live API tests")
    
    return api_key, api_secret


def _get_api_base_url() -> str:
    """Get API base URL from environment."""
    return os.getenv("API_BASE_URL", "http://localhost:3000")


@pytest.mark.asyncio
async def test_live_health_check():
    """Test that the API health endpoint is responsive."""
    base_url = _get_api_base_url()
    # Uncomment and adapt when API client is available:
    # client = APIClient(base_url=base_url)
    # resp = await client.health_check()
    # assert resp.status_code in (200, 204)
    pytest.skip("API client not yet implemented")


@pytest.mark.asyncio
async def test_live_authentication():
    """Test authentication with real credentials."""
    api_key, api_secret = _require_api_credentials()
    base_url = _get_api_base_url()
    
    # Uncomment and adapt when API client is available:
    # client = APIClient(
    #     base_url=base_url,
    #     api_key=api_key,
    #     api_secret=api_secret
    # )
    # resp = await client.authenticate()
    # 
    # # If unauthorized, xfail (validates live call path)
    # if resp.status_code in (401, 403):
    #     pytest.xfail("Invalid API key or unauthorized; live path verified")
    # 
    # assert resp.success is True
    # assert "token" in resp.data or "session" in resp.data
    pytest.skip("API client not yet implemented")


@pytest.mark.asyncio
async def test_live_basic_query():
    """Test a basic API query with minimal data."""
    api_key, _ = _require_api_credentials()
    base_url = _get_api_base_url()
    
    # Uncomment and adapt when API client is available:
    # client = APIClient(base_url=base_url, api_key=api_key)
    # 
    # # Make a minimal query to avoid rate limits
    # resp = await client.search(
    #     query="test",
    #     limit=1
    # )
    # 
    # if resp.status_code in (401, 403):
    #     pytest.xfail("Invalid API key or unauthorized; live path verified")
    # 
    # assert resp.success is True
    # assert isinstance(resp.data, (dict, list))
    pytest.skip("API client not yet implemented")


@pytest.mark.asyncio  
@pytest.mark.slow
async def test_live_rate_limiting():
    """Test that rate limiting is properly enforced."""
    api_key, _ = _require_api_credentials()
    base_url = _get_api_base_url()
    
    # Uncomment and adapt when API client is available:
    # client = APIClient(base_url=base_url, api_key=api_key)
    # 
    # # Make multiple requests to test rate limiting
    # responses = []
    # for _ in range(3):
    #     resp = await client.search(query="test", limit=1)
    #     responses.append(resp)
    #     
    #     # Check for rate limit headers
    #     if "X-RateLimit-Remaining" in resp.headers:
    #         assert int(resp.headers["X-RateLimit-Remaining"]) >= 0
    # 
    # # At least one should succeed
    # assert any(r.success for r in responses)
    pytest.skip("API client not yet implemented")
