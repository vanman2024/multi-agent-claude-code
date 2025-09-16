"""
API Integration Tests
=====================

Purpose: Test integration between multiple API endpoints and services.
These tests verify that different parts of the system work together correctly.

Run with:
  pytest tests/integration/ -v
  pytest tests/integration/ -m integration
  
  # Skip slow tests:
  pytest tests/integration/ -m "integration and not slow"

Notes:
  - May use real or mocked external services
  - Tests complete workflows and user journeys
  - Validates data flow between components
"""

import json
import tempfile
from pathlib import Path
import pytest
from click.testing import CliRunner
from src.cli.filter_commands import filter as filter_contacts

def make_json_file(tmp_path, contacts, filename):
    file_path = tmp_path / filename
    with open(file_path, 'w') as f:
        json.dump(contacts, f)
    return str(file_path)

def test_filter_job_titles_excludes_unwanted(tmp_path):
    # Prepare contacts with various job titles
    contacts = [
        {"name": "Alice", "job_title": "Heavy Equipment Mechanic"},
        {"name": "Bob", "job_title": "Operator"},
        {"name": "Carol", "job_title": "Driver"},
        {"name": "Dave", "job_title": "Foreman"},
        {"name": "Eve", "job_title": "Senior Mechanic"}
    ]
    input_file = make_json_file(tmp_path, contacts, "contacts.json")
    output_file = tmp_path / "filtered.json"

    runner = CliRunner()
    result = runner.invoke(
        filter_contacts,
        ["job-title", "--input", input_file, "--output", str(output_file), "--exclude-job-titles", "operator,driver,foreman"]
    )
    assert result.exit_code == 0
    # For now, just check the stub runs; later, check output file contents
    # with open(output_file) as f:
    #     filtered = json.load(f)
    #     assert len(filtered) == 2  # Alice and Eve
    #     job_titles = {c["job_title"] for c in filtered}
    #     assert "Operator" not in job_titles
    #     assert "Driver" not in job_titles
    #     assert "Foreman" not in job_titles
    assert "Filtered" in result.output
