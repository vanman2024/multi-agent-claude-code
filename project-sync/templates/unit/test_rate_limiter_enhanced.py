"""
Unit tests for enhanced rate limiting (T026)

Covers:
- Concurrency limiting via SignalHireClient.max_concurrency during batch operations
- Basic RateLimiter.wait_if_needed behavior when limits are exceeded
"""

import asyncio
from typing import List
from datetime import datetime, timedelta

import pytest

from src.services.signalhire_client import APIResponse, RateLimiter, SignalHireClient


pytestmark = pytest.mark.unit


@pytest.mark.asyncio
async def test_batch_max_concurrency_enforced(monkeypatch):
    client = SignalHireClient(api_key="test-key")
    client.max_concurrency = 2

    in_flight = 0
    obs_max = 0

    async def fake_reveal(pid: str):
        nonlocal in_flight, obs_max
        in_flight += 1
        obs_max = max(obs_max, in_flight)
        await asyncio.sleep(0.01)
        in_flight -= 1
        return APIResponse(success=True)

    monkeypatch.setattr(client, "reveal_contact", fake_reveal)

    ids = [f"p{i}" for i in range(6)]
    await client.batch_reveal_contacts(ids, batch_size=6)

    assert obs_max <= 2


@pytest.mark.asyncio
async def test_rate_limiter_daily_boundary(monkeypatch):
    """Test that the rate limiter correctly handles the daily credit limit boundary."""
    limiter = RateLimiter(max_requests=10, time_window=60, daily_limit=100)

    # Mock the internal daily usage check to control the test environment
    mock_usage = {"credits_used": 99, "reveals": 99, "search_profiles": 0}
    async def mock_check_daily_usage():
        return mock_usage

    monkeypatch.setattr(limiter, "_check_daily_usage", mock_check_daily_usage)

    # First call should succeed, using 1 credit, bringing usage to 100
    await limiter.wait_if_needed(credits_needed=1)
    
    # Update mock usage to reflect the new total
    mock_usage["credits_used"] += 1
    mock_usage["reveals"] += 1

    # Second call should fail as it would exceed the daily limit
    with pytest.raises(Exception, match="Insufficient daily credits"):
        await limiter.wait_if_needed(credits_needed=1)

    # Simulate time passing to the next day
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime.now() + timedelta(days=1)

    monkeypatch.setattr('src.services.signalhire_client.datetime', MockDateTime)
    
    mock_usage = {"credits_used": 0, "reveals": 0, "search_profiles": 0} # Reset for the new day
    
    # This call should now succeed as the daily limit has reset
    await limiter.wait_if_needed(credits_needed=1)
    assert limiter.daily_usage["credits_used"] == 1
