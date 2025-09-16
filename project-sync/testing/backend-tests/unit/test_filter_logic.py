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
from src.services.filter_service import load_contacts_from_file, filter_contacts_by_job_title, save_contacts_to_file
import tempfile
import json

def test_load_contacts_from_file():
    contacts = [{"name": "Alice", "job_title": "Mechanic"}]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(contacts, f)
        f.flush()
        loaded = load_contacts_from_file(f.name)
        assert loaded == contacts

def test_filter_contacts_by_job_title():
    contacts = [
        {"name": "Alice", "job_title": "Heavy Equipment Mechanic"},
        {"name": "Bob", "job_title": "Operator"},
        {"name": "Carol", "job_title": "Driver"}
    ]
    filtered = filter_contacts_by_job_title(contacts, ["operator", "driver"])
    assert len(filtered) == 1
    assert filtered[0]["name"] == "Alice"
