import logging
import json
from io import StringIO
import pytest
import structlog

from src.lib.logger import setup_logging

def test_setup_logging_produces_json_output():
    """
    Tests that the configured logger produces JSON-formatted logs.
    """
    log_stream = StringIO()
    
    # Configure logging to use our stream
    setup_logging(log_stream=log_stream)
    
    # Get the logger and bind some context
    logger = structlog.get_logger("test_logger")
    logger = logger.bind(user_id=123, request_id="abc-xyz")
    
    # Log a message
    message = "This is a test message."
    logger.info(message)
    
    # Retrieve the log output
    log_output = log_stream.getvalue()
    
    # Parse the JSON log record
    log_record = json.loads(log_output)
    
    # Assert that the log record has the expected structure and content
    assert log_record["event"] == message
    assert log_record["level"] == "info"
    assert log_record["user_id"] == 123
    assert log_record["request_id"] == "abc-xyz"
    assert "timestamp" in log_record
