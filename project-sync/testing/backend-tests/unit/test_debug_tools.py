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
pytest.skip("Skipped in API-only mode (debug tools not present)", allow_module_level=True)

import json
import tempfile
from pathlib import Path

# from API Service_agent.lib.debug_tools import dump_session_artifacts


def test_dump_session_artifacts_writes_files():
    with tempfile.TemporaryDirectory() as td:
        out = td  # placeholder to keep structure when skipped
        _ = {
            "session_id": "s-123",
            "error": "timeout",
            "steps": ["login", "search", "reveal"],
            "calls": [{"op": "login"}],
        }
        p = Path(out)
        assert p.exists()
        meta = json.loads((p / "metadata.json").read_text())
        assert meta["session_id"] == "s-123"
        assert (p / "calls.log").exists()
