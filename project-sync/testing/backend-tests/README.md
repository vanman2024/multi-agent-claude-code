# SignalHire Agent Test Suite

## Test Organization

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── smoke/                   # Quick smoke tests for basic functionality
│   └── test_deps.py        # Dependency availability tests
├── unit/                    # Unit tests for individual components
│   └── test_export_comprehensive.py
├── integration/             # Integration tests with external services
│   └── browser/
│       └── test_stagehand.py  # Stagehand integration tests
├── browser/                 # Browser automation specific tests
│   ├── test_docker_browser.py      # Docker environment browser tests
│   ├── test_live_browser.py        # Live browser functionality tests
│   └── test_real_browser.py        # Real browser interaction tests
├── contract/               # API/UI contract tests
├── performance/            # Performance and load tests
└── helpers/               # Test helper utilities
```

## Test Categories

### 🏃 Smoke Tests (`tests/smoke/`)
**Purpose**: Quick validation that basic functionality works
**Runtime**: < 5 seconds
**Dependencies**: None (mocked)
```bash
pytest tests/smoke/ -v
```

### 🔬 Unit Tests (`tests/unit/`)
**Purpose**: Test individual components in isolation
**Runtime**: < 30 seconds total
**Dependencies**: Mocked external services
```bash
pytest tests/unit/ -v
```

### 🔌 Integration Tests (`tests/integration/`)
**Purpose**: Test integration with external services
**Runtime**: 30 seconds - 2 minutes
**Dependencies**: Real external services (limited calls)
```bash
pytest tests/integration/ -v -m "not slow"
```

### 🌐 Browser Tests (`tests/browser/`)
**Purpose**: Browser automation functionality
**Runtime**: 1-5 minutes
**Dependencies**: Browser, internet connection
```bash
pytest tests/browser/ -v -m "not credentials"
```

### 📋 Contract Tests (`tests/contract/`)
**Purpose**: Verify external API/UI contracts haven't changed
**Runtime**: 10-60 seconds
**Dependencies**: Internet connection
```bash
pytest tests/contract/ -v
```

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Quick tests only
pytest -m "smoke or unit" -v

# Skip slow tests
pytest -m "not slow" -v

# Skip tests requiring credentials
pytest -m "not credentials" -v

# Browser tests only
pytest -m "browser" -v

# Integration tests only  
pytest -m "integration" -v
```

## Environment Variables

Set these for comprehensive testing:

```bash
# SignalHire credentials (for integration/browser tests)
export SIGNALHIRE_EMAIL="your-test-account@example.com"
export SIGNALHIRE_PASSWORD="your-test-password"

# Browserbase credentials (optional, for cloud browser testing)
export BROWSERBASE_API_KEY="your-browserbase-key"
export BROWSERBASE_PROJECT_ID="your-project-id"
export MODEL_API_KEY="your-openai-key"
```

## Running Tests

### Local Development
```bash
# Quick feedback loop
python3 run.py -m pytest tests/smoke/ tests/unit/ -v

# Full test suite (no credentials needed)
python3 run.py -m pytest -m "not credentials and not slow" -v

# Browser automation tests  
python3 run.py -m pytest tests/browser/ -v --tb=short
```

### Docker Environment
```bash
# Start test environment
docker-compose up -d signalhire-agent

# Run tests in container
docker-compose exec signalhire-agent pytest tests/smoke/ tests/unit/ -v

# Run browser tests with display
docker-compose exec signalhire-agent pytest tests/browser/ -v -s
```

### CI/CD Pipeline
```bash
# Automated testing (no manual interaction)
pytest tests/smoke/ tests/unit/ tests/contract/ -v --tb=line
```

## Test Development Guidelines

### Writing New Tests

1. **Choose the right category** based on what you're testing
2. **Use appropriate markers** (`@pytest.mark.unit`, `@pytest.mark.slow`, etc.)
3. **Use fixtures** from `conftest.py` for common setup
4. **Mock external services** in unit tests
5. **Keep tests isolated** - each test should be independent

### Example Test Structure

```python
import pytest
from src.services.example_service import ExampleService

@pytest.mark.unit
async def test_example_functionality(sample_data, mock_browser_session):
    \"\"\"Test example service functionality.\"\"\"
    service = ExampleService()
    result = await service.process(sample_data)
    assert result.success is True
    assert len(result.data) > 0

@pytest.mark.integration
@pytest.mark.slow
async def test_real_api_integration(signalhire_credentials):
    \"\"\"Test real API integration - requires credentials.\"\"\"
    # This test will be skipped if credentials not available
    pytest.skip("Requires real credentials")
```

### Debugging Failed Tests

```bash
# Verbose output with full traceback
pytest tests/failing_test.py -v -s --tb=long

# Drop into debugger on failure
pytest tests/failing_test.py --pdb

# Run only failed tests from last run
pytest --lf -v
```

## Test Data

- **Fixtures**: Use fixtures from `conftest.py` for consistent test data
- **Sample Data**: Keep sample data realistic but minimal
- **Secrets**: Never commit real credentials or API keys
- **Cleanup**: Tests should clean up any created files/data

## Browser Test Considerations

- **Headless Mode**: Use `headless=True` for CI/CD, `headless=False` for debugging
- **Screenshots**: Browser tests automatically capture screenshots on failure
- **Timeouts**: Set appropriate timeouts for network operations
- **Rate Limits**: Be mindful of API rate limits in integration tests
- **Isolation**: Each browser test should start with a clean session

This test structure follows the testing pyramid: many unit tests, fewer integration tests, minimal end-to-end tests.