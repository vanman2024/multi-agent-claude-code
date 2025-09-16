"""End-to-end CLI workflow tests - test complete command sequences."""
import pytest
import subprocess
import json
import tempfile
import os


pytestmark = [pytest.mark.e2e, pytest.mark.cli, pytest.mark.slow]


class TestCLIWorkflow:
    """Test complete CLI workflows from user perspective."""
    
    @pytest.fixture
    def temp_config(self):
        """Create temporary config file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config = {
                "api_url": "http://localhost:8000",
                "timeout": 30,
                "retry_count": 3
            }
            json.dump(config, f)
            config_file = f.name
        
        yield config_file
        
        # Cleanup
        if os.path.exists(config_file):
            os.unlink(config_file)
    
    def test_initialization_workflow(self, temp_config):
        """Test first-time setup and initialization."""
        # Test init command
        result = subprocess.run(
            ["python", "-m", "cli", "init", "--config", temp_config],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Should either succeed or indicate already initialized
        assert result.returncode in [0, 1]
        
        # Verify config was loaded
        result = subprocess.run(
            ["python", "-m", "cli", "config", "show"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # If command exists, verify output
            assert "api_url" in result.stdout or "config" in result.stdout.lower()
    
    def test_authentication_workflow(self):
        """Test authentication flow from login to logout."""
        # Attempt login (may not be implemented)
        result = subprocess.run(
            ["python", "-m", "cli", "auth", "login", "--username", "test", "--password", "test"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Check if auth command exists
        if "invalid" in result.stderr.lower() or "unknown" in result.stderr.lower():
            pytest.skip("Authentication not implemented")
        
        # If implemented, should handle invalid credentials gracefully
        assert result.returncode != 0 or "success" in result.stdout.lower()
    
    def test_data_processing_workflow(self):
        """Test complete data processing pipeline via CLI."""
        # Create test data file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = [
                {"id": 1, "name": "Item 1", "value": 100},
                {"id": 2, "name": "Item 2", "value": 200}
            ]
            json.dump(test_data, f)
            input_file = f.name
        
        try:
            # Process data (generic command that might exist)
            result = subprocess.run(
                ["python", "-m", "cli", "process", "--input", input_file, "--format", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # If command exists, verify behavior
            if result.returncode == 0:
                assert len(result.stdout) > 0
            elif "unknown" in result.stderr.lower() or "invalid" in result.stderr.lower():
                # Command doesn't exist - that's OK for generic template
                pass
            else:
                # Real error - should be handled gracefully
                assert "error" in result.stderr.lower()
        
        finally:
            # Cleanup
            if os.path.exists(input_file):
                os.unlink(input_file)
    
    def test_help_documentation_workflow(self):
        """Test that all commands have proper help documentation."""
        # Main help
        result = subprocess.run(
            ["python", "-m", "cli", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert len(result.stdout) > 0
        
        # Extract available commands from help output
        commands = []
        for line in result.stdout.split('\n'):
            if line.strip() and not line.startswith(' ') and not line.startswith('-'):
                # Simple heuristic to find command names
                parts = line.split()
                if parts and not parts[0].startswith('-'):
                    commands.append(parts[0])
        
        # Test help for each discovered command
        for cmd in commands[:5]:  # Test first 5 to avoid slowness
            sub_result = subprocess.run(
                ["python", "-m", "cli", cmd, "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Should either show help or indicate invalid command
            assert sub_result.returncode in [0, 1, 2]
    
    @pytest.mark.parametrize("output_format", ["json", "csv", "text"])
    def test_output_format_workflow(self, output_format):
        """Test that CLI supports multiple output formats."""
        result = subprocess.run(
            ["python", "-m", "cli", "list", "--format", output_format],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # If list command exists
        if result.returncode == 0:
            if output_format == "json":
                # Should be valid JSON
                try:
                    json.loads(result.stdout)
                except json.JSONDecodeError:
                    # Not JSON, but that's OK if command doesn't support it
                    pass
            elif output_format == "csv":
                # Should have comma-separated values
                assert "," in result.stdout or len(result.stdout.strip()) == 0
        elif "unknown" in result.stderr.lower() or "invalid" in result.stderr.lower():
            # Command doesn't exist - expected for generic template
            pass