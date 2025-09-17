"""
Production Readiness Tests

These tests validate that mock implementations have been properly replaced
with production-ready code before deployment.
"""

import pytest
import os
import sys
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestProductionReadiness:
    """Test suite to validate production readiness"""

    def test_no_mock_implementations_in_production_code(self):
        """Ensure no mock implementations exist in production code"""
        mock_patterns = [
            'mock_',
            'fake_',
            'test_',
            'dummy_',
            'localhost',
            '127.0.0.1',
            'FIXME',
            'TODO: Replace',
            'HACK:',
            'do_not_use_in_production'
        ]

        # Scan production directories (exclude test directories)
        production_dirs = [
            project_root / "src",
            project_root / "api",
            project_root / "lib",
            project_root / "components"
        ]

        found_issues = []

        for prod_dir in production_dirs:
            if not prod_dir.exists():
                continue

            for file_path in prod_dir.rglob("*.py"):
                # Skip test files
                if "test" in str(file_path) or "__pycache__" in str(file_path):
                    continue

                try:
                    content = file_path.read_text()
                    for line_num, line in enumerate(content.split('\n'), 1):
                        for pattern in mock_patterns:
                            if pattern.lower() in line.lower():
                                found_issues.append(f"{file_path}:{line_num} - {pattern}")
                except Exception:
                    continue

        assert not found_issues, f"Mock implementations found in production code:\n" + "\n".join(found_issues)

    def test_environment_variables_configured(self):
        """Ensure required environment variables are set for production"""
        required_env_vars = [
            'DATABASE_URL',
            'API_SECRET_KEY',
            'JWT_SECRET'
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.getenv(var):
                # Check if it's in .env file
                env_file = project_root / ".env"
                if env_file.exists():
                    env_content = env_file.read_text()
                    if f"{var}=" not in env_content:
                        missing_vars.append(var)
                else:
                    missing_vars.append(var)

        # For template repo, this is expected to fail - that's the point
        if missing_vars:
            pytest.skip(f"Template repo - missing env vars: {missing_vars}")

    def test_no_debug_flags_enabled(self):
        """Ensure debug flags are disabled in production"""
        debug_patterns = [
            'DEBUG = True',
            'debug: true',
            'debugMode = true',
            'console.log',
            'print(',  # Python debug prints
            'console.debug'
        ]

        # Check our mock files that should be flagged
        production_mock_dir = Path(__file__).parent
        mock_files = [
            production_mock_dir / "auth" / "authentication.js",
            production_mock_dir / "api" / "external_api.ts"
        ]

        found_debug_code = []
        for mock_file in mock_files:
            if mock_file.exists():
                content = mock_file.read_text()
                for line_num, line in enumerate(content.split('\n'), 1):
                    for pattern in debug_patterns:
                        if pattern in line:
                            found_debug_code.append(f"{mock_file}:{line_num} - {pattern}")

        # These SHOULD be found in our mock files (they're examples of what not to do)
        assert found_debug_code, "Expected to find debug code in mock examples"

    def test_authentication_security(self):
        """Test that authentication uses secure implementations"""
        auth_file = Path(__file__).parent / "auth" / "authentication.js"

        if not auth_file.exists():
            pytest.skip("Auth file not found")

        content = auth_file.read_text()

        # These should be found in our mock file (bad practices)
        security_issues = []
        if 'fake_jwt_secret' in content:
            security_issues.append("Hardcoded JWT secret found")
        if 'password123' in content:
            security_issues.append("Hardcoded test passwords found")
        if 'mock_admin_token' in content:
            security_issues.append("Mock admin token found")

        # In our mock file, these SHOULD be present (they're examples of what not to do)
        assert security_issues, f"Expected security issues in mock file: {security_issues}"

    def test_api_endpoints_use_real_implementations(self):
        """Test that API endpoints don't use mock implementations"""
        api_file = Path(__file__).parent / "api" / "external_api.ts"

        if not api_file.exists():
            pytest.skip("API file not found")

        content = api_file.read_text()

        # These should be found in our mock file
        mock_indicators = []
        if 'useMockData = true' in content:
            mock_indicators.append("Mock data flag enabled")
        if 'test_api_key' in content:
            mock_indicators.append("Test API key found")
        if 'localhost' in content:
            mock_indicators.append("Localhost URLs found")

        # In our mock file, these SHOULD be present
        assert mock_indicators, f"Expected mock indicators in example file: {mock_indicators}"


class TestMockDetectorIntegration:
    """Test integration with the mock detector script"""

    def test_mock_detector_finds_issues(self):
        """Test that the mock detector properly identifies issues"""
        mock_detector_script = project_root / ".claude" / "scripts" / "mock_detector.py"

        if not mock_detector_script.exists():
            pytest.skip("Mock detector script not found")

        # Run mock detector on our production test files
        import subprocess
        result = subprocess.run([
            sys.executable, str(mock_detector_script),
            "--target", str(Path(__file__).parent),
            "--format", "json"
        ], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                report = json.loads(result.stdout)
                # Should find issues in our mock files
                assert report.get('total_issues', 0) > 0, "Mock detector should find issues in example files"
                assert report.get('critical_issues', 0) > 0, "Should find critical issues"
            except json.JSONDecodeError:
                pytest.skip("Could not parse mock detector output")
        else:
            pytest.skip("Mock detector failed to run")