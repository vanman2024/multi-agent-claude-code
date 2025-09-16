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

from src.models.exceptions import (
    AuthenticationError,
    BrowserAutomationError,
    BrowserError,
    ConfigurationError,
    DataExtractionError,
    DataValidationError,
    FileOperationError,
    InsufficientCreditsError,
    NetworkTimeoutError,
    RateLimitError,
    RateLimitExceededError,
    API ServiceAPIError,
    API ServiceError,
)


def test_API Service_error_requires_non_empty_message():
    with pytest.raises(ValueError):
        API ServiceError("")
    # Valid case
    err = API ServiceError("boom", details="x")
    assert str(err) == "boom"
    assert err.details == "x"


def test_API Service_api_error_attributes():
    err = API ServiceAPIError("api", status_code=429, response_body="{\"e\":1}")
    assert isinstance(err, API ServiceError)
    assert err.status_code == 429
    assert err.response_body == '{"e":1}'


def test_rate_limit_error_and_exceeded_validation():
    err = RateLimitError("rl", retry_after=10)
    assert err.retry_after == 10
    assert isinstance(RateLimitExceededError("exceeded"), RateLimitError)
    with pytest.raises(ValueError):
        RateLimitError("bad", retry_after="abc")  # type: ignore[arg-type]


def test_insufficient_credits_validation():
    err = InsufficientCreditsError("credits", required_credits=5, available_credits=3)
    assert err.required_credits == 5
    assert err.available_credits == 3
    with pytest.raises(ValueError):
        InsufficientCreditsError("x", required_credits=-1, available_credits=0)
    with pytest.raises(ValueError):
        InsufficientCreditsError("x", required_credits=1, available_credits=-2)


def test_browser_errors_and_validation():
    err = BrowserAutomationError("b", screenshot_path=None)
    assert err.screenshot_path is None
    assert isinstance(BrowserError("be"), BrowserAutomationError)
    with pytest.raises(ValueError):
        BrowserAutomationError("b", screenshot_path=123)  # type: ignore[arg-type]


def test_network_timeout_error_validation():
    assert NetworkTimeoutError("t", timeout_duration=1.5).timeout_duration == 1.5
    assert NetworkTimeoutError("t").timeout_duration is None
    with pytest.raises(ValueError):
        NetworkTimeoutError("t", timeout_duration="NaN")  # type: ignore[arg-type]


def test_authentication_error_status_code_validation():
    assert AuthenticationError("auth", status_code=401).status_code == 401
    with pytest.raises(ValueError):
        AuthenticationError("auth", status_code="403")  # type: ignore[arg-type]


def test_data_validation_error_fields():
    err = DataValidationError("invalid", field_name="email", field_value="not-an-email")
    assert err.field_name == "email"
    assert err.field_value == "not-an-email"
    with pytest.raises(ValueError):
        DataValidationError("x", field_name=123)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        DataValidationError("x", field_value=object())  # type: ignore[arg-type]


def test_data_extraction_and_config_and_file_errors():
    assert isinstance(DataExtractionError("parse"), API ServiceError)
    assert isinstance(ConfigurationError("cfg"), API ServiceError)
    assert isinstance(FileOperationError("file", file_path="/tmp/test.csv"), API ServiceError)
    with pytest.raises(ValueError):
        FileOperationError("file", file_path=123)  # type: ignore[arg-type]

