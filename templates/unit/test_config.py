import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.lib.config import (
    Config, 
    Environment, 
    LogLevel,
    SignalHireConfig,
    CallbackServerConfig, 
    BrowserConfig,
    RateLimitConfig,
    ExportConfig,
    load_config,
    get_config,
    create_test_config,
    get_signalhire_credentials,
)


@pytest.fixture
def clean_env():
    """Clean environment fixture that restores env vars after test."""
    original_env = dict(os.environ)
    # Clear relevant env vars
    env_vars_to_clear = [
        'SIGNALHIRE_EMAIL', 'SIGNALHIRE_PASSWORD', 'SIGNALHIRE_API_KEY',
        'OPENAI_API_KEY', 'GEMINI_API_KEY', 'ENVIRONMENT'
    ]
    for var in env_vars_to_clear:
        os.environ.pop(var, None)
    
    yield
    
    # Restore environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    content = """
SIGNALHIRE_EMAIL=test@example.com
SIGNALHIRE_PASSWORD=testpass123
OPENAI_API_KEY=sk-test123
GEMINI_API_KEY=ai-test456
ENVIRONMENT=development
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    
    os.unlink(f.name)


class TestEnvironmentEnums:
    """Test environment and log level enums."""
    
    def test_environment_enum(self):
        """Test Environment enum values."""
        assert Environment.DEVELOPMENT == "development"
        assert Environment.TEST == "test"
        assert Environment.PRODUCTION == "production"
    
    def test_log_level_enum(self):
        """Test LogLevel enum values."""
        assert LogLevel.DEBUG == "DEBUG"
        assert LogLevel.INFO == "INFO"
        assert LogLevel.WARNING == "WARNING"
        assert LogLevel.ERROR == "ERROR"
        assert LogLevel.CRITICAL == "CRITICAL"


class TestConfigModels:
    """Test individual configuration models."""
    
    def test_signalhire_config_validation(self):
        """Test SignalHire config validation."""
        # Valid config
        config = SignalHireConfig(
            email="test@example.com",
            password="password123"
        )
        assert config.email == "test@example.com"
        assert config.password == "password123"
        assert config.base_url == "https://www.signalhire.com"
        
        # Invalid email
        with pytest.raises(ValueError, match="Invalid email format"):
            SignalHireConfig(email="invalid-email")
    
    def test_callback_server_config_validation(self):
        """Test callback server config validation."""
        # Valid config
        config = CallbackServerConfig(host="localhost", port=8080)
        assert config.host == "localhost"
        assert config.port == 8080
        
        # Invalid port
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            CallbackServerConfig(port=0)
        
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            CallbackServerConfig(port=70000)
    
    def test_browser_config_defaults(self):
        """Test browser config default values."""
        config = BrowserConfig()
        assert config.headless is True
        assert config.timeout == 30
        assert config.viewport_width == 1920
        assert config.viewport_height == 1080
        assert config.user_agent is None
    
    def test_rate_limit_config_defaults(self):
        """Test rate limit config default values."""
        config = RateLimitConfig()
        assert config.requests_per_minute == 600
        assert config.burst_limit == 100
        assert config.retry_attempts == 3
        assert config.retry_delay == 1.0
    
    def test_export_config_defaults(self, tmp_path):
        """Test export config defaults."""
        with patch.object(Path, 'mkdir') as mock_mkdir:
            config = ExportConfig()
            assert config.default_format == "csv"
            assert config.include_headers is True
            assert config.date_format == "%Y-%m-%d"
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestMainConfig:
    """Test main Config class."""
    
    def test_config_defaults(self, clean_env):
        """Test config default values."""
        config = Config()
        assert config.environment == Environment.DEVELOPMENT
        assert config.debug is False
        assert config.log_level == LogLevel.INFO
        assert isinstance(config.signalhire, SignalHireConfig)
        assert isinstance(config.callback_server, CallbackServerConfig)
        assert isinstance(config.browser, BrowserConfig)
        assert isinstance(config.rate_limit, RateLimitConfig)
        assert isinstance(config.export, ExportConfig)
    
    def test_environment_parsing(self, clean_env):
        """Test environment string parsing."""
        os.environ['ENVIRONMENT'] = 'PRODUCTION'
        config = Config()
        assert config.environment == Environment.PRODUCTION
    
    def test_signalhire_credentials_loading(self, clean_env):
        """Test SignalHire credentials loading from env."""
        os.environ['SIGNALHIRE_EMAIL'] = 'test@example.com'
        os.environ['SIGNALHIRE_PASSWORD'] = 'testpass'
        os.environ['SIGNALHIRE_API_KEY'] = 'api-key-123'
        
        config = Config()
        assert config.signalhire.email == 'test@example.com'
        assert config.signalhire.password == 'testpass'
        assert config.signalhire.api_key == 'api-key-123'
    
    def test_api_keys_loading(self, clean_env):
        """Test external API keys loading."""
        os.environ['OPENAI_API_KEY'] = 'sk-openai123'
        os.environ['GEMINI_API_KEY'] = 'ai-gemini456'
        
        config = Config()
        assert config.openai_api_key == 'sk-openai123'
        assert config.gemini_api_key == 'ai-gemini456'
    
    def test_validate_required_credentials(self, clean_env):
        """Test credential validation."""
        config = Config()
        
        # No credentials set
        missing = config.validate_required_credentials()
        assert 'SIGNALHIRE_EMAIL' in missing
        assert 'SIGNALHIRE_PASSWORD' in missing
        
        # Set credentials
        config.signalhire.email = 'test@example.com'
        config.signalhire.password = 'testpass'
        missing = config.validate_required_credentials()
        assert len(missing) == 0
        
        # Don't require SignalHire
        config.signalhire.email = None
        missing = config.validate_required_credentials(require_signalhire=False)
        assert len(missing) == 0
    
    def test_get_callback_url(self, clean_env):
        """Test callback URL generation."""
        config = Config()
        
        # Default host
        url = config.get_callback_url()
        assert url == "http://localhost:8000/signalhire/callback"
        
        # External host set
        config.callback_server.external_host = "example.com"
        url = config.get_callback_url()
        assert url == "http://example.com:8000/signalhire/callback"
        
        # Custom port
        config.callback_server.port = 9000
        url = config.get_callback_url()
        assert url == "http://example.com:9000/signalhire/callback"
    
    def test_environment_checks(self, clean_env):
        """Test environment check methods."""
        config = Config()
        
        config.environment = Environment.DEVELOPMENT
        assert config.is_development() is True
        assert config.is_production() is False
        assert config.is_test() is False
        
        config.environment = Environment.PRODUCTION
        assert config.is_development() is False
        assert config.is_production() is True
        assert config.is_test() is False
        
        config.environment = Environment.TEST
        assert config.is_development() is False
        assert config.is_production() is False
        assert config.is_test() is True
    
    def test_get_log_config(self, clean_env):
        """Test logging configuration generation."""
        config = Config()
        log_config = config.get_log_config()
        
        assert "version" in log_config
        assert "handlers" in log_config
        assert "loggers" in log_config
        assert log_config["loggers"][""]["level"] == "INFO"
        
        # Test with different log level
        config.log_level = LogLevel.DEBUG
        log_config = config.get_log_config()
        assert log_config["loggers"][""]["level"] == "DEBUG"


class TestConfigLoading:
    """Test configuration loading functions."""
    
    def test_load_config_from_env_file(self, temp_env_file, clean_env):
        """Test loading config from .env file."""
        config = load_config(env_file=temp_env_file, validate_credentials=False)
        
        assert config.signalhire.email == "test@example.com"
        assert config.signalhire.password == "testpass123"
        assert config.openai_api_key == "sk-test123"
        assert config.gemini_api_key == "ai-test456"
        assert config.environment == Environment.DEVELOPMENT
    
    @patch('src.lib.config.load_dotenv')
    @patch('os.path.exists')
    def test_load_config_searches_env_files(self, mock_exists, mock_load_dotenv, clean_env):
        """Test that load_config searches for .env files."""
        mock_exists.side_effect = lambda path: path == "../.env"
        
        load_config(validate_credentials=False)
        
        mock_load_dotenv.assert_called_with("../.env")
    
    def test_get_config_singleton(self, clean_env):
        """Test that get_config returns singleton instance."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2
    
    def test_create_test_config(self, clean_env):
        """Test test configuration creation."""
        config = create_test_config(
            signalhire__email="custom@test.com",
            callback_server__port=9999
        )
        
        assert config.environment == Environment.TEST
        assert config.debug is True
        assert config.log_level == LogLevel.DEBUG
        assert config.signalhire.email == "custom@test.com"
        assert config.callback_server.port == 9999


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_get_signalhire_credentials(self, clean_env):
        """Test get_signalhire_credentials function."""
        os.environ['SIGNALHIRE_EMAIL'] = 'test@example.com'
        os.environ['SIGNALHIRE_PASSWORD'] = 'testpass'
        
        email, password = get_signalhire_credentials()
        assert email == 'test@example.com'
        assert password == 'testpass'
    
    def test_get_config_accessors(self, clean_env):
        """Test config accessor functions."""
        from src.lib.config import (
            get_callback_server_config,
            get_browser_config,
            get_rate_limit_config,
            get_export_config
        )
        
        callback_config = get_callback_server_config()
        assert isinstance(callback_config, CallbackServerConfig)
        
        browser_config = get_browser_config()
        assert isinstance(browser_config, BrowserConfig)
        
        rate_config = get_rate_limit_config()
        assert isinstance(rate_config, RateLimitConfig)
        
        export_config = get_export_config()
        assert isinstance(export_config, ExportConfig)


class TestConfigValidation:
    """Test configuration validation scenarios."""
    
    def test_config_with_missing_credentials_warning(self, clean_env):
        """Test that missing credentials generate warnings."""
        with pytest.warns(UserWarning, match="Missing required credentials"):
            load_config(validate_credentials=True)
    
    def test_config_with_all_credentials(self, temp_env_file, clean_env):
        """Test config loading with all credentials present."""
        # Should not raise warnings
        config = load_config(env_file=temp_env_file, validate_credentials=True)
        assert config.signalhire.email == "test@example.com"
        assert config.signalhire.password == "testpass123"