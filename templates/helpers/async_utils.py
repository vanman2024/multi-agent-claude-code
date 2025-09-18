from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable


@asynccontextmanager
async def patch_asyncio_sleep(fake: Callable[[float], float] | None = None) -> AsyncIterator[None]:
    """Patch asyncio.sleep to run nearly instantly for tests.

    By default, replaces asyncio.sleep with a coroutine that sleeps 0 seconds.
    A custom mapping function can be provided to translate requested seconds.
    """
    orig_sleep = asyncio.sleep

    async def fast_sleep(secs: float) -> None:  # type: ignore[override]
        mapped = fake(secs) if fake else 0.0
        await orig_sleep(0.0 if mapped < 0 else mapped)

    asyncio.sleep = fast_sleep  # type: ignore[assignment]
    try:
        yield
    finally:
        asyncio.sleep = orig_sleep  # type: ignore[assignment]

