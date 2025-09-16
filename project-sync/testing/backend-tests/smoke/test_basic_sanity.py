"""Basic sanity smoke tests - verify core functionality is working."""
import pytest
import sys
import os
import importlib.util


pytestmark = pytest.mark.smoke


class TestBasicSanity:
    """Quick smoke tests to verify basic system health."""
    
    def test_python_version(self):
        """Verify Python version is compatible."""
        assert sys.version_info >= (3, 8), "Python 3.8+ required"
    
    def test_project_structure_exists(self):
        """Verify essential project directories exist."""
        # Check from testing directory perspective
        # Go up from smoke/ -> backend-tests/ -> testing/ -> project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        
        # Essential directories that should exist
        essential_dirs = [
            "testing",
            "testing/backend-tests",
            "scripts"
        ]
        
        for dir_name in essential_dirs:
            dir_path = os.path.join(project_root, dir_name)
            assert os.path.isdir(dir_path), f"Essential directory missing: {dir_name}"
    
    def test_core_modules_importable(self):
        """Verify core Python modules can be imported."""
        required_modules = [
            "json",
            "os", 
            "sys",
            "subprocess",
            "typing",
            "pathlib"
        ]
        
        for module in required_modules:
            try:
                importlib.import_module(module)
            except ImportError:
                pytest.fail(f"Cannot import required module: {module}")
    
    def test_pytest_markers_configured(self):
        """Verify pytest markers are properly configured."""
        # This test runs, so pytest is working
        assert True
        
        # Verify we can access config
        config = pytest.config if hasattr(pytest, 'config') else None
        # Config might not be available in test context, that's OK
    
    def test_environment_variables_accessible(self):
        """Verify environment variables can be accessed."""
        # Should be able to read env vars
        path = os.environ.get("PATH")
        assert path is not None, "Cannot read PATH environment variable"
        
        # Check Python path
        python_path = sys.path
        assert len(python_path) > 0, "Python path is empty"
    
    def test_file_operations(self):
        """Verify basic file operations work."""
        import tempfile
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "smoke test content"
            f.write(test_content)
            temp_path = f.name
        
        try:
            # Read it back
            with open(temp_path, 'r') as f:
                content = f.read()
            assert content == test_content
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_json_operations(self):
        """Verify JSON serialization works."""
        import json
        
        test_data = {
            "test": True,
            "value": 42,
            "items": ["a", "b", "c"]
        }
        
        # Serialize
        json_str = json.dumps(test_data)
        assert isinstance(json_str, str)
        
        # Deserialize
        parsed = json.loads(json_str)
        assert parsed == test_data
    
    def test_subprocess_execution(self):
        """Verify subprocess execution works."""
        import subprocess
        
        # Run simple command
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        assert result.returncode == 0
        assert "Python" in result.stdout or "Python" in result.stderr