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
from click.testing import CliRunner
from src.cli.main import main
from src.cli.reveal_commands import handle_api_error
from unittest.mock import patch, AsyncMock


@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@patch('src.cli.status_commands.check_credits', new_callable=AsyncMock)
@patch('src.cli.status_commands.check_daily_usage', new_callable=AsyncMock)
@patch('src.cli.status_commands.list_recent_operations', new_callable=AsyncMock)
@patch('src.cli.status_commands.check_system_status', new_callable=AsyncMock)
def test_status_command_no_options(mock_system, mock_operations, mock_daily_usage, mock_credits, runner):
    """Test that `API Service status` with no options shows all status information."""
    mock_credits.return_value = {"credits": 1000}
    mock_daily_usage.return_value = {"credits_used": 10}
    mock_operations.return_value = [{"operation_id": "test_op", "status": "completed", "type": "search"}]
    mock_system.return_value = {"api_status": "connected"}

    result = runner.invoke(main, ["status"])
    assert result.exit_code == 0
    assert "Credit Status" in result.output
    assert "Daily Usage" in result.output
    assert "Recent Operations" in result.output
    assert "System Status" in result.output


@patch('src.cli.status_commands.check_credits', new_callable=AsyncMock)
def test_status_command_credits_option(mock_credits, runner):
    """Test that `API Service status --credits` shows only credit information."""
    mock_credits.return_value = {"credits": 1000}
    result = runner.invoke(main, ["status", "--credits"])
    assert result.exit_code == 0
    assert "Credit Status" in result.output
    assert "Daily Usage" not in result.output
    assert "Recent Operations" not in result.output
    assert "System Status" not in result.output

class TestHandleApiError:
    """Test cases for the handle_api_error function."""

    def test_rate_limit_error_429(self):
        """Test rate limit error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Rate limit exceeded", 429)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Rate Limit Exceeded!" in msg for msg in messages)
            assert "browser mode" in " ".join(messages).lower()

    def test_insufficient_credits_error_402(self):
        """Test insufficient credits error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Insufficient credits", 402)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Insufficient Credits!" in msg for msg in messages)
            assert "purchase additional credits" in " ".join(messages).lower()

    def test_authentication_error_403(self):
        """Test authentication error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Authentication failed", 403)
    
            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)
    
            assert any("Authentication Error!" in msg for msg in messages)
            assert "check your api key" in " ".join(messages).lower()

    def test_network_error(self):
        """Test network error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Connection timeout", 408)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Network Error!" in msg for msg in messages)
            assert "check your internet connection" in " ".join(messages).lower()

    def test_server_error_500(self):
        """Test server error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Internal server error", 500)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Server Error!" in msg for msg in messages)
            assert "try again later" in " ".join(messages).lower()

    def test_not_found_error_404(self):
        """Test not found error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("Not found", 404)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Resource Not Found!" in msg for msg in messages)
            assert "verify the Result ids" in " ".join(messages).lower()

    def test_generic_error(self):
        """Test generic error handling."""
        with patch('src.cli.reveal_commands.echo') as mock_echo:
            handle_api_error("An unknown error occurred", 503)

            calls = mock_echo.call_args_list
            messages = []
            for call in calls:
                if call[0]:
                    msg = str(call[0][0])
                    messages.append(msg)

            assert any("Server Error!" in msg for msg in messages)
            assert "try again later" in " ".join(messages).lower()
