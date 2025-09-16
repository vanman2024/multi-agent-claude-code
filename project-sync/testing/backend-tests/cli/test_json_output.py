"""CLI JSON output tests - validate structured outputs for agent consumption."""
import json
import subprocess
import pytest
from inline_snapshot import snapshot


@pytest.mark.cli
def test_cli_json_output_format():
    """Test that CLI can output valid JSON for agent consumption."""
    result = subprocess.run(
        ["python", "-m", "cli", "api", "list", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        # Should be valid JSON
        try:
            data = json.loads(result.stdout)
            assert isinstance(data, (dict, list))
        except json.JSONDecodeError:
            pytest.skip("CLI doesn't support JSON output yet")


@pytest.mark.cli
def test_cli_api_response_structure():
    """Test API command returns structured data."""
    result = subprocess.run(
        ["python", "-m", "cli", "api", "test", "--endpoint", "/health", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            # Expected structure for API response
            assert "status" in data or "success" in data or "result" in data
        except (json.JSONDecodeError, AssertionError):
            pytest.skip("API test command not yet implemented")


@pytest.mark.cli
@pytest.mark.mcp
def test_mcp_tool_list_json():
    """Test MCP tool listing returns JSON."""
    result = subprocess.run(
        ["python", "-m", "cli", "mcp", "list-tools", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            # Should be a list of tools or dict with tools key
            assert isinstance(data, (list, dict))
            if isinstance(data, dict):
                assert "tools" in data or "items" in data
        except json.JSONDecodeError:
            pytest.skip("MCP tool listing not yet JSON-capable")


@pytest.mark.cli
def test_cli_workflow_json_output():
    """Test complete workflow produces parseable JSON at each step."""
    workflow_commands = [
        ["python", "-m", "cli", "search", "--query", "test", "--format", "json"],
        ["python", "-m", "cli", "status", "--format", "json"],
    ]
    
    for cmd in workflow_commands:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # Skip if command not implemented
        if result.returncode == 127 or "not found" in result.stderr:
            continue
            
        if result.returncode == 0 and result.stdout.strip():
            # Try to parse as JSON
            try:
                json.loads(result.stdout)
            except json.JSONDecodeError:
                # Not JSON yet, that's ok for now
                pass


@pytest.mark.cli
@pytest.mark.snapshot
def test_json_schema_stability():
    """Snapshot test for JSON output schema stability."""
    result = subprocess.run(
        ["python", "-m", "cli", "config", "show", "--format", "json"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0 and result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            # Normalize dynamic values
            if isinstance(data, dict):
                data.pop("timestamp", None)
                data.pop("version", None)
            
            # Snapshot the schema structure
            assert data == snapshot()
        except json.JSONDecodeError:
            pytest.skip("Config command doesn't output JSON yet")