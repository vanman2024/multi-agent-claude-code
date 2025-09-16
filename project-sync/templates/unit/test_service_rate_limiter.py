import pytest
pytest.skip("Skipped in API-only mode (legacy service rate limiter)", allow_module_level=True)

import asyncio

# from signalhire_agent.services.rate_limiter import RateLimiterService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_rate_limiter_respects_capacity_and_refill():
    t = 0.0

    def fake_time():
        return t

    svc = RateLimiterService(capacity=2, refill_rate=1.0, time_fn=fake_time)
    await svc.acquire()
    await svc.acquire()
    assert svc.available == 0.0

    task = asyncio.create_task(svc.acquire())
    await asyncio.sleep(0)
    assert not task.done()
    t += 1.0
    await asyncio.wait_for(task, timeout=0.2)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_rate_limiter_rejects_excess_request():
    svc = RateLimiterService(capacity=2, refill_rate=10.0)
    with pytest.raises(ValueError):
        await svc.acquire(3)
