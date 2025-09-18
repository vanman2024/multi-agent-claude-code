"""
Live API smoke tests (skipped by default).

Run with:
  SIGNALHIRE_API_KEY=... python3 run.py -m pytest tests/live/test_live_api.py -m live -q

Notes:
- These tests make minimal requests and respect API limits.
- They skip if no SIGNALHIRE_API_KEY is present.
"""

import os
import pytest

from src.services.signalhire_client import SignalHireClient


pytestmark = pytest.mark.live


def _require_api_key() -> str:
    key = os.getenv("SIGNALHIRE_API_KEY")
    if not key:
        pytest.skip("SIGNALHIRE_API_KEY not set; skipping live API tests")
    return key


@pytest.mark.asyncio
async def test_live_credits_endpoint():
    key = _require_api_key()
    client = SignalHireClient(api_key=key)
    resp = await client.check_credits()
    # If unauthorized, xfail (validates live call path)
    if not resp.success and resp.status_code in (401, 403):
        pytest.xfail("Invalid API key or unauthorized; live path verified")
    assert resp.success is True
    assert isinstance(resp.data, dict)


@pytest.mark.asyncio
async def test_live_search_small_query():
    key = _require_api_key()
    client = SignalHireClient(api_key=key)
    # Use Search API documented keys (currentTitle)
    resp = await client.search_prospects({"currentTitle": "Engineer"}, size=1)
    if not resp.success and resp.status_code in (401, 403):
        pytest.xfail("Invalid API key or unauthorized; live path verified")
    assert resp.success is True
    assert isinstance(resp.data, dict)
    # SignalHire API returns 'profiles' not 'prospects'
    assert "profiles" in resp.data
