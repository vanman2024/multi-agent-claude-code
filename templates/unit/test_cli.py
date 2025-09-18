import os
from click.testing import CliRunner
import pytest

from signalhire_agent.cli.main import cli


@pytest.mark.unit
def test_cli_help_shows_commands():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])  # nosec - help only
    assert result.exit_code == 0
    assert "SignalHire Agent CLI" in result.output
    assert "doctor" in result.output


@pytest.mark.unit
def test_cli_version_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])  # nosec - prints version
    assert result.exit_code == 0
    assert "signalhire-agent" in result.output


@pytest.mark.unit
def test_doctor_reports_env_vars_set(monkeypatch):
    monkeypatch.setenv("SIGNALHIRE_EMAIL", "you@example.com")
    monkeypatch.setenv("SIGNALHIRE_PASSWORD", "secret")
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])  # nosec - env check only
    assert result.exit_code == 0
    assert "SIGNALHIRE_EMAIL: set" in result.output
    assert "SIGNALHIRE_PASSWORD: set" in result.output


@pytest.mark.unit
def test_doctor_reports_env_vars_missing(monkeypatch):
    # Ensure vars are unset
    monkeypatch.delenv("SIGNALHIRE_EMAIL", raising=False)
    monkeypatch.delenv("SIGNALHIRE_PASSWORD", raising=False)
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])  # nosec - env check only
    assert result.exit_code == 0
    assert "SIGNALHIRE_EMAIL: missing" in result.output
    assert "SIGNALHIRE_PASSWORD: missing" in result.output

