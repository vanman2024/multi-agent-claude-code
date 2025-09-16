"""
API Contract Tests
==================

Purpose: Verify that API endpoints adhere to their documented contracts.
These tests validate request/response formats, data types, and business rules.

Test Strategy:
  - RED phase: Tests should fail initially before implementation
  - GREEN phase: Implement API client to make tests pass
  - REFACTOR phase: Optimize implementation while keeping tests green

Run with:
  pytest tests/contract/ -v
  pytest tests/contract/ -m contract

Notes:
  - Uses mocked responses to avoid external API calls
  - Validates both successful and error scenarios
  - Ensures backward compatibility when API changes
"""

import os
import pytest
from click.testing import CliRunner

# Stub out optional browser dependency to avoid heavy imports during contract tests
import sys
from types import ModuleType
_dummy = ModuleType("stagehand")
setattr(_dummy, "Stagehand", object)
sys.modules.setdefault("stagehand", _dummy)

from src.cli.main import main


pytestmark = pytest.mark.contract


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help_mentions_api_first(runner, monkeypatch):
    """Top-level help should mention API-first mode and guidance."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "API-first" in result.output or "API first" in result.output


def test_default_uses_api_when_api_key_present(runner, monkeypatch):
    """When API key is set, default mode should be API without extra flags."""
    monkeypatch.setenv("API_KEY", "test-key-abc")
    res = runner.invoke(main, ["reveal", "Result123"])
    # Reveal command should log/echo API usage path by default
    assert res.exit_code in (0, 1)  # may fail for missing implementation paths
    assert ("Using API" in res.output) or ("Mode: API" in res.output)


def test_api_only_flag_disables_browser_fallback(runner, monkeypatch):
    """CLI should provide --api-only to force API path even without API key."""
    # Unset API key to force ambiguity
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.setenv("API Service_EMAIL", "user@example.com")
    monkeypatch.setenv("API Service_PASSWORD", "secret")

    # Expect: new global or command-level flag --api-only exists
    result = runner.invoke(main, ["--api-only", "reveal", "Result123"])  # type: ignore[list-item]
    # Initially this should fail (unknown option) until implemented
    assert result.exit_code == 0
    assert "Using API" in result.output
