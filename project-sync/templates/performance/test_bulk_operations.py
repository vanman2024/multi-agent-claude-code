import asyncio
import time
import pytest

# Rate limit: 600 elements/minute = 10 elements/second
# This means each operation should take at least 0.1 seconds.
# We'll add a small buffer for network latency.
MIN_TIME_PER_OPERATION = 60 / 600.0  # 0.1 seconds

@pytest.mark.performance
@pytest.mark.slow
async def mock_operation(item_id: int):
    """Simulates a single async operation that takes some time."""
    # In a real test, this would be an API call or browser action.
    # We simulate the minimum time required by the rate limiter.
    await asyncio.sleep(MIN_TIME_PER_OPERATION)
    return f"Processed item {item_id}"

@pytest.mark.performance
@pytest.mark.slow
async def test_bulk_operations_stay_within_rate_limit():
    """
    Performance test for bulk operations.
    Ensures that the processing rate for a batch of operations
    does not exceed the 600 elements/minute limit.
    """
    num_operations = 100  # A reasonable batch size for a performance test
    
    start_time = time.monotonic()
    
    tasks = [mock_operation(i) for i in range(num_operations)]
    await asyncio.gather(*tasks)
    
    end_time = time.monotonic()
    
    total_time = end_time - start_time
    operations_per_second = num_operations / total_time
    operations_per_minute = operations_per_second * 60
    
    print(f"Processed {num_operations} operations in {total_time:.2f} seconds.")
    print(f"Rate: {operations_per_minute:.2f} operations/minute.")
    
    # Assert that the rate is below the limit.
    # We check for less than 610 to allow for minor timing fluctuations.
    assert operations_per_minute < 610, "Operation rate exceeded the 600/minute limit."
