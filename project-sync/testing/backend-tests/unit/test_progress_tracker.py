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
from src.services.progress_service import ProgressTracker
import tempfile
import json

def test_progress_tracker_init():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tracker = ProgressTracker(f.name)
        assert tracker.progress == {"revealed": [], "remaining": []}

def test_mark_revealed():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tracker = ProgressTracker(f.name)
        tracker.mark_revealed("1")
        assert "1" in tracker.progress["revealed"]

def test_get_remaining():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tracker = ProgressTracker(f.name)
        tracker.mark_revealed("1")
        remaining = tracker.get_remaining(["1", "2", "3"])
        assert remaining == ["2", "3"]
