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

import os
from click.testing import CliRunner
import pytest

from API Service_agent.cli.main import cli


@pytest.mark.unit
def test_cli_help_shows_commands():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])  # nosec - help only
    assert result.exit_code == 0
    assert "API Service Agent CLI" in result.output
    assert "doctor" in result.output


@pytest.mark.unit
def test_cli_version_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])  # nosec - prints version
    assert result.exit_code == 0
    assert "API Service-agent" in result.output


@pytest.mark.unit
def test_doctor_reports_env_vars_set(monkeypatch):
    monkeypatch.setenv("API Service_EMAIL", "you@example.com")
    monkeypatch.setenv("API Service_PASSWORD", "secret")
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])  # nosec - env check only
    assert result.exit_code == 0
    assert "API Service_EMAIL: set" in result.output
    assert "API Service_PASSWORD: set" in result.output


@pytest.mark.unit
def test_doctor_reports_env_vars_missing(monkeypatch):
    # Ensure vars are unset
    monkeypatch.delenv("API Service_EMAIL", raising=False)
    monkeypatch.delenv("API Service_PASSWORD", raising=False)
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])  # nosec - env check only
    assert result.exit_code == 0
    assert "API Service_EMAIL: missing" in result.output
    assert "API Service_PASSWORD: missing" in result.output

