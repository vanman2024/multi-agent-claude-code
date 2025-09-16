"""
Unit Tests
==========

Purpose: Test individual functions and classes in isolation.
These tests verify that each component works correctly on its own.

Run with:
  pytest tests/unit/ -v
  pytest tests/unit/ -m unit

Notes:
  - All external dependencies are mocked
  - Tests are fast and deterministic
  - Focus on edge cases and error handling
"""

import pytest
pytest.skip("Skipped in API-only mode (legacy services package)", allow_module_level=True)

import asyncio
from typing import List

# from API Service_agent.lib.rate_limiter import AsyncTokenBucket
# from API Service_agent.lib.retry import async_retry


@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_token_bucket_respects_capacity_and_refill(monkeypatch):
    t = 0.0

    def fake_time():
        return t

    bucket = AsyncTokenBucket(capacity=2, refill_rate=1.0, time_fn=fake_time)

    # Consume 2 tokens immediately
    await bucket.acquire()
    await bucket.acquire()
    assert bucket.available == 0.0

    acquired = False

    async def try_acquire():
        nonlocal acquired
        await bucket.acquire()
        acquired = True

    task = asyncio.create_task(try_acquire())
    await asyncio.sleep(0)  # let task run and block
    assert not task.done()
    assert not acquired

    # Advance time by 1 second → 1 token refilled
    t += 1.0
    await asyncio.sleep(0)  # allow scheduler to proceed
    # Task should complete now
    await asyncio.wait_for(task, timeout=0.1)
    assert acquired


@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_retry_retries_and_succeeds(monkeypatch):
    calls: List[int] = []

    async def fake_sleep(_: float):
        # no real waiting in tests
        await asyncio.sleep(0)

    @async_retry(retries=2, base_delay=0.01, jitter=False, sleep=fake_sleep)
    async def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("boom")
        return "ok"

    result = await flaky()
    assert result == "ok"
    # Should have attempted 3 times total (2 retries + 1 initial)
    assert len(calls) == 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_token_bucket_rejects_more_than_capacity():
    bucket = AsyncTokenBucket(capacity=2, refill_rate=10.0)
    with pytest.raises(ValueError):
        await bucket.acquire(3)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_token_bucket_cancellation_does_not_deadlock():
    t = 0.0

    def fake_time():
        return t

    bucket = AsyncTokenBucket(capacity=1, refill_rate=1.0, time_fn=fake_time)

    # Consume initial token
    await bucket.acquire()

    # Start a waiter that will need to wait ~1s
    waiter = asyncio.create_task(bucket.acquire())
    await asyncio.sleep(0)  # ensure it blocks
    assert not waiter.done()

    # Cancel the waiter before refill and ensure cancellation propagates
    waiter.cancel()
    with pytest.raises(asyncio.CancelledError):
        await waiter

    # Advance time and ensure another task can still acquire (no deadlock)
    t += 1.0
    ok = asyncio.create_task(bucket.acquire())
    await asyncio.wait_for(ok, timeout=0.2)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_retry_non_retryable_exception_is_not_caught():
    calls = {"n": 0}

    @async_retry(retries=5, exceptions=(ValueError,))
    async def fn():
        calls["n"] += 1
        raise TypeError("no-retry")

    with pytest.raises(TypeError):
        await fn()
    assert calls["n"] == 1
import pytest
pytest.skip("Skipped in API-only mode (legacy services package)", allow_module_level=True)
