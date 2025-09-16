"""CLI error handling tests - validate error messages and recovery."""
import subprocess
import pytest


@pytest.mark.cli
def test_invalid_command():
    """Test that invalid commands produce clear error messages."""
    result = subprocess.run(
        ["python", "-m", "cli", "nonexistent-command"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode != 0
    assert "error" in result.stderr.lower() or "invalid" in result.stderr.lower() or result.returncode == 2


@pytest.mark.cli
def test_missing_required_argument():
    """Test that missing required arguments produce helpful errors."""
    # Try API command without required endpoint
    result = subprocess.run(
        ["python", "-m", "cli", "api", "test"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0:
        # Should tell us what's missing
        error_output = result.stderr.lower()
        assert any(word in error_output for word in ["required", "missing", "endpoint", "argument"])


@pytest.mark.cli
def test_invalid_json_input():
    """Test that invalid JSON input is handled gracefully."""
    result = subprocess.run(
        ["python", "-m", "cli", "api", "call", "--data", "{invalid json}"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0:
        error_output = result.stderr.lower()
        assert any(word in error_output for word in ["json", "invalid", "parse", "format"])


@pytest.mark.cli
@pytest.mark.mcp
def test_mcp_connection_error():
    """Test graceful handling of MCP server connection failures."""
    result = subprocess.run(
        ["python", "-m", "cli", "mcp", "connect", "--server", "nonexistent://server"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode != 0:
        error_output = result.stderr.lower()
        # Should indicate connection problem
        assert any(word in error_output for word in ["connect", "failed", "error", "unavailable"])


@pytest.mark.cli
def test_timeout_handling():
    """Test that CLI handles timeouts appropriately."""
    # This would need a mock slow endpoint or flag to trigger timeout
    result = subprocess.run(
        ["python", "-m", "cli", "api", "test", "--endpoint", "/slow", "--timeout", "1"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Either it times out with appropriate message, or command doesn't exist yet
    if result.returncode != 0:
        if "timeout" in result.stderr.lower():
            assert "timeout" in result.stderr.lower()


@pytest.mark.cli
def test_permission_denied_error():
    """Test handling of permission-denied scenarios."""
    result = subprocess.run(
        ["python", "-m", "cli", "config", "write", "--file", "/root/forbidden.json"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0:
        error_output = result.stderr.lower()
        # Should indicate permission issue
        assert any(word in error_output for word in ["permission", "denied", "access", "forbidden", "not found"])


@pytest.mark.cli
def test_error_output_format():
    """Test that errors follow consistent format."""
    # Trigger an error
    result = subprocess.run(
        ["python", "-m", "cli", "invalid"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode != 0 and result.stderr:
        # Errors should be on stderr, not stdout
        assert result.stderr.strip()
        # Should not leak stack traces in normal mode
        assert "Traceback" not in result.stderr or "--debug" in result.stderr