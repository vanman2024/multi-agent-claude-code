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

import asyncio

import pytest

from tests.helpers.async_utils import patch_asyncio_sleep


@pytest.mark.unit
@pytest.mark.asyncio
async def test_patch_asyncio_sleep_fast_for_tests():
    elapsed = 0

    async def work():
        nonlocal elapsed
        start = asyncio.get_event_loop().time()
        await asyncio.sleep(1.0)
        end = asyncio.get_event_loop().time()
        elapsed = end - start

    async with patch_asyncio_sleep():
        await work()
    # Should be effectively instantaneous
    assert elapsed < 0.01

