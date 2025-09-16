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
from src.services.deduplication_service import load_contacts_from_files, deduplicate_contacts, save_contacts_to_file
import tempfile
import json
from pathlib import Path

def test_load_contacts_from_files():
    # Test loading from single file
    contacts = [{"uid": "1", "name": "Alice"}]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(contacts, f)
        f.flush()
        loaded = load_contacts_from_files([f.name])
        assert loaded == contacts

def test_deduplicate_contacts_by_uid():
    contacts = [
        {"uid": "1", "name": "Alice"},
        {"uid": "1", "name": "Alice"},  # Duplicate
        {"uid": "2", "name": "Bob"}
    ]
    deduped = deduplicate_contacts(contacts)
    assert len(deduped) == 2
    uids = {c["uid"] for c in deduped}
    assert uids == {"1", "2"}

def test_deduplicate_contacts_by_linkedin():
    contacts = [
        {"linkedin_url": "https://linkedin.com/in/alice", "name": "Alice"},
        {"linkedin_url": "https://linkedin.com/in/alice", "name": "Alice"},  # Duplicate
        {"linkedin_url": "https://linkedin.com/in/bob", "name": "Bob"}
    ]
    deduped = deduplicate_contacts(contacts)
    assert len(deduped) == 2
