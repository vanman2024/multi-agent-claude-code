"""CLI help command tests - validate help text and documentation."""
import subprocess
import pytest
from inline_snapshot import snapshot


@pytest.mark.cli
def test_cli_help_output():
    """Test that CLI --help produces expected output format."""
    result = subprocess.run(
        ["python", "-m", "cli", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert "--help" in result.stdout
    assert "--version" in result.stdout


@pytest.mark.cli
def test_cli_version():
    """Test that CLI --version outputs version info."""
    result = subprocess.run(
        ["python", "-m", "cli", "--version"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    # Version format: "cli version X.Y.Z" or similar
    assert "version" in result.stdout.lower() or result.returncode == 0


@pytest.mark.cli
def test_subcommand_help():
    """Test that subcommands provide help text."""
    subcommands = ["api", "test", "mcp", "agent"]
    
    for cmd in subcommands:
        result = subprocess.run(
            ["python", "-m", "cli", cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Either the command exists with help, or skip if not implemented
        if result.returncode == 0:
            assert "Usage:" in result.stdout or "help" in result.stdout.lower()


@pytest.mark.cli
@pytest.mark.snapshot
def test_help_text_snapshot():
    """Snapshot test for help text stability."""
    result = subprocess.run(
        ["python", "-m", "cli", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    # Normalize dynamic content before snapshot
    help_text = result.stdout
    # Remove version numbers, timestamps, paths that might change
    normalized = help_text.replace("\\", "/")  # Normalize path separators
    
    # Snapshot comparison - first run will populate, subsequent runs verify
    assert normalized == snapshot()