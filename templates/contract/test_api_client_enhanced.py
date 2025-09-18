"""
Enhanced API client contract tests (Phase 3.2)

These tests define the enhanced behavior expected from the SignalHire API
client for professional, API-first workflows. They MUST be written first
and are expected to FAIL initially until the implementation (T014–T017)
adds the required capabilities.
"""

import asyncio
from typing import Any, Dict, List

import pytest
from unittest.mock import AsyncMock, patch

from src.services.signalhire_client import SignalHireClient, APIResponse, SignalHireAPIError


pytestmark = pytest.mark.contract


@pytest.mark.asyncio
async def test_batch_reveal_supports_progress_callback():
    """Batch reveal should accept a progress callback and call it periodically."""
    client = SignalHireClient(api_key="test-key")

    progress_events: List[Dict[str, Any]] = []

    async def progress_cb(event: Dict[str, Any]):
        progress_events.append(event)

    # Expect: new kwarg progress_callback is supported and invoked
    # Current implementation does not accept this kwarg, so this should fail initially
    prospect_ids = [f"prospect{i:02d}" for i in range(1, 6)]
    with patch.object(client, "reveal_contact", return_value=APIResponse(success=True)):
        await client.batch_reveal_contacts(prospect_ids, batch_size=2, progress_callback=progress_cb)  # type: ignore[arg-type]

    # At least one progress event should be emitted
    assert any("current" in e and "total" in e for e in progress_events)


@pytest.mark.asyncio
async def test_queue_management_limits_concurrency(monkeypatch):
    """Batch operations must obey a configurable max_concurrency (queueing beyond limit)."""
    client = SignalHireClient(api_key="test-key")

    # Expect: client exposes max_concurrency and batch method enforces it
    client.max_concurrency = 3  # type: ignore[attr-defined]

    in_flight = 0
    observed_max = 0

    async def fake_reveal(prospect_id: str):
        nonlocal in_flight, observed_max
        in_flight += 1
        observed_max = max(observed_max, in_flight)
        await asyncio.sleep(0.05)
        in_flight -= 1
        return APIResponse(success=True, data={"prospect_id": prospect_id})

    monkeypatch.setattr(client, "reveal_contact", fake_reveal)

    ids = [f"p{i}" for i in range(10)]
    _ = await client.batch_reveal_contacts(ids, batch_size=10)  # type: ignore[arg-type]

    # Should never exceed configured concurrency
    assert observed_max <= 3


@pytest.mark.asyncio
async def test_retry_logic_on_transient_failures(monkeypatch):
    """Transient HTTP failures (timeouts/5xx) should be retried before failing."""
    client = SignalHireClient(api_key="test-key")

    attempts = {"count": 0}

    async def flaky_request(method, endpoint, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            # Simulate transient error responses
            return APIResponse(success=False, status_code=503, error="Service Unavailable")
        return APIResponse(success=True, data={"ok": True})

    monkeypatch.setattr(client, "_make_request", flaky_request)

    # Expect: reveal_contact performs internal retry and succeeds after transient errors
    resp = await client.reveal_contact("prospect123")
    assert resp.success is True
    assert attempts["count"] >= 3


@pytest.mark.asyncio
async def test_credit_precheck_before_batch_operations(monkeypatch):
    """Client should pre-check available credits and block batches if insufficient."""
    client = SignalHireClient(api_key="test-key")

    async def fake_credits():
        return APIResponse(success=True, data={"credits_remaining": 2})

    monkeypatch.setattr(client, "check_credits", fake_credits)
    monkeypatch.setattr(client, "reveal_contact", AsyncMock(return_value=APIResponse(success=True)))

    # Need 5 credits but only 2 remain → expect error
    ids = [f"p{i}" for i in range(5)]

    with pytest.raises(SignalHireAPIError):
        await client.batch_reveal_contacts(ids, batch_size=2)

