"""
Live API Integration Tests - PLACEHOLDER
=========================================

NOTE: When src/ is implemented and you have real APIs:
- These tests will make actual external API calls
- Controlled by environment variables (API_KEY, etc.)
- Skipped by default to avoid rate limits

Currently using placeholder tests.
"""

import pytest
import os


@pytest.mark.live
@pytest.mark.skipif(not os.getenv("API_KEY"), reason="No API key provided")
def test_live_api_connection():
    """Test connection to live API."""
    # PLACEHOLDER: Will test actual API when credentials available
    # from src.clients.api_client import APIClient
    # client = APIClient(api_key=os.getenv("API_KEY"))
    # response = await client.health_check()
    # assert response.status_code == 200
    assert True  # Placeholder
