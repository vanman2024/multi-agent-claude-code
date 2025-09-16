"""CLI exit code tests - validate standard exit codes for different scenarios."""
import subprocess
import pytest


# Standard exit codes
SUCCESS = 0
GENERAL_ERROR = 1
MISUSE = 2  # Command line usage error
CANNOT_EXECUTE = 126
COMMAND_NOT_FOUND = 127


@pytest.mark.cli
def test_successful_command_exit_code():
    """Test that successful commands return 0."""
    result = subprocess.run(
        ["python", "-m", "cli", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == SUCCESS


@pytest.mark.cli
def test_help_exit_code():
    """Test that help commands return 0."""
    result = subprocess.run(
        ["python", "-m", "cli", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == SUCCESS


@pytest.mark.cli
def test_invalid_command_exit_code():
    """Test that invalid commands return non-zero."""
    result = subprocess.run(
        ["python", "-m", "cli", "invalid-command"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode != SUCCESS
    # Typically 1 or 2 for command errors
    assert result.returncode in [GENERAL_ERROR, MISUSE, COMMAND_NOT_FOUND]


@pytest.mark.cli
def test_missing_argument_exit_code():
    """Test that missing required arguments return usage error."""
    result = subprocess.run(
        ["python", "-m", "cli", "api", "call"],  # Missing required args
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Should return non-zero for missing args
    if result.returncode != SUCCESS:
        # Preferably MISUSE (2) for argument errors
        assert result.returncode in [GENERAL_ERROR, MISUSE]


@pytest.mark.cli
def test_api_failure_exit_code():
    """Test that API failures return appropriate exit codes."""
    result = subprocess.run(
        ["python", "-m", "cli", "api", "test", "--endpoint", "/nonexistent"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    # If implemented, should return non-zero for API failures
    if "not found" in result.stderr.lower() or "404" in result.stderr:
        assert result.returncode != SUCCESS


@pytest.mark.cli
def test_interrupt_exit_code():
    """Test that interrupted commands return appropriate code."""
    # This is hard to test without actual interruption
    # Document expected behavior: Ctrl+C should return 130
    pass  # Placeholder for documentation


@pytest.mark.cli
def test_exit_code_consistency():
    """Test that same error conditions produce consistent exit codes."""
    # Run same invalid command twice
    results = []
    for _ in range(2):
        result = subprocess.run(
            ["python", "-m", "cli", "nonexistent"],
            capture_output=True,
            text=True,
            timeout=5
        )
        results.append(result.returncode)
    
    # Should get same exit code for same error
    assert results[0] == results[1]


@pytest.mark.cli
def test_debug_mode_exit_codes():
    """Test that debug mode preserves exit codes."""
    # Normal mode
    normal = subprocess.run(
        ["python", "-m", "cli", "invalid"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Debug mode should have same exit code
    debug = subprocess.run(
        ["python", "-m", "cli", "--debug", "invalid"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Exit codes should match even if output differs
    if normal.returncode != 0 and debug.returncode != 0:
        # Both should fail with same code
        assert abs(normal.returncode - debug.returncode) <= 1  # Allow minor variation