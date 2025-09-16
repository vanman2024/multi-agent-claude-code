"""Quick health check smoke tests - 30 second validation."""
import pytest
import time
import asyncio
from typing import Optional


pytestmark = pytest.mark.smoke


class TestQuickHealth:
    """Ultra-fast health checks that should complete in seconds."""
    
    def test_basic_arithmetic(self):
        """Verify basic operations work (canary test)."""
        assert 2 + 2 == 4
        assert 10 / 2 == 5
        assert 3 * 3 == 9
    
    def test_string_operations(self):
        """Verify string operations work correctly."""
        test_str = "hello world"
        assert test_str.upper() == "HELLO WORLD"
        assert test_str.replace("world", "python") == "hello python"
        assert len(test_str) == 11
    
    def test_list_operations(self):
        """Verify list operations work correctly."""
        test_list = [1, 2, 3, 4, 5]
        assert len(test_list) == 5
        assert sum(test_list) == 15
        assert max(test_list) == 5
        assert min(test_list) == 1
    
    def test_dict_operations(self):
        """Verify dictionary operations work correctly."""
        test_dict = {"a": 1, "b": 2, "c": 3}
        assert len(test_dict) == 3
        assert test_dict.get("a") == 1
        assert test_dict.get("d", "default") == "default"
        assert list(test_dict.keys()) == ["a", "b", "c"]
    
    def test_exception_handling(self):
        """Verify exception handling works correctly."""
        with pytest.raises(ZeroDivisionError):
            _ = 1 / 0
        
        with pytest.raises(KeyError):
            _ = {}["nonexistent"]
        
        with pytest.raises(IndexError):
            _ = [][0]
    
    @pytest.mark.asyncio
    async def test_async_operations(self):
        """Verify async operations work correctly."""
        async def async_add(a: int, b: int) -> int:
            await asyncio.sleep(0.01)  # Tiny delay
            return a + b
        
        result = await async_add(5, 3)
        assert result == 8
    
    def test_class_instantiation(self):
        """Verify classes can be created and used."""
        class TestClass:
            def __init__(self, value: int):
                self.value = value
            
            def double(self) -> int:
                return self.value * 2
        
        obj = TestClass(21)
        assert obj.value == 21
        assert obj.double() == 42
    
    def test_comprehensions(self):
        """Verify list/dict comprehensions work."""
        # List comprehension
        squares = [x**2 for x in range(5)]
        assert squares == [0, 1, 4, 9, 16]
        
        # Dict comprehension
        square_dict = {x: x**2 for x in range(3)}
        assert square_dict == {0: 0, 1: 1, 2: 4}
        
        # Set comprehension
        unique = {x % 3 for x in range(10)}
        assert unique == {0, 1, 2}
    
    def test_context_managers(self):
        """Verify context managers work correctly."""
        class TestContext:
            def __init__(self):
                self.entered = False
                self.exited = False
            
            def __enter__(self):
                self.entered = True
                return self
            
            def __exit__(self, *args):
                self.exited = True
        
        ctx = TestContext()
        assert not ctx.entered
        assert not ctx.exited
        
        with ctx:
            assert ctx.entered
            assert not ctx.exited
        
        assert ctx.entered
        assert ctx.exited
    
    def test_performance_baseline(self):
        """Verify basic operations complete in reasonable time."""
        start = time.time()
        
        # Do some work
        total = sum(range(1000000))
        
        elapsed = time.time() - start
        
        # Should complete in under 1 second
        assert elapsed < 1.0, f"Performance issue: took {elapsed:.2f} seconds"
        assert total == 499999500000  # Verify result is correct