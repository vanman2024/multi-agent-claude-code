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
import asyncio
import json
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from src.lib.callback_server import CallbackServer, get_server, start_server
from src.models.person_callback import PersonCallbackData, PersonCallbackItem, PersonCandidate


@pytest.fixture
def callback_server():
    """Create a fresh callback server for testing."""
    return CallbackServer(host="127.0.0.1", port=8899)


@pytest.fixture
def test_client(callback_server):
    """Create a test client for the callback server."""
    app = callback_server.create_app()
    return TestClient(app)


@pytest.fixture
def sample_callback_data():
    """Sample callback data matching API Service Resource API format."""
    return [
        {
            "status": "success",
            "item": "john.doe@example.com",
            "candidate": {
                "uid": "10000000000000000000000000001006",
                "fullName": "John Doe",
                "gender": "male",
                "photo": {
                    "url": "https://example.com/photo.jpg"
                },
                "locations": [
                    {
                        "name": "New York, NY, United States"
                    }
                ],
                "skills": ["Python", "JavaScript"],
                "education": [],
                "experience": [],
                "contacts": [
                    {
                        "type": "email",
                        "value": "john.doe@company.com",
                        "rating": "100",
                        "subType": "work",
                        "info": None
                    }
                ],
                "social": [],
                "headLine": "Software Engineer",
                "summary": "Experienced developer",
                "language": []
            }
        },
        {
            "status": "failed",
            "item": "invalid@email",
            "candidate": None
        }
    ]


class TestCallbackServer:
    """Test cases for CallbackServer class."""

    def test_init(self):
        """Test server initialization."""
        server = CallbackServer(host="localhost", port=9000)
        assert server.host == "localhost"
        assert server.port == 9000
        assert not server.is_running
        assert server.app is None

    def test_create_app(self, callback_server):
        """Test FastAPI app creation."""
        app = callback_server.create_app()
        assert app is not None
        assert callback_server.app is app

    def test_get_callback_url(self, callback_server):
        """Test callback URL generation."""
        url = callback_server.get_callback_url()
        assert url == "http://127.0.0.1:8899/API Service/callback"
        
        # Test with external host
        external_url = callback_server.get_callback_url("example.com")
        assert external_url == "http://example.com:8899/API Service/callback"

    def test_handler_registration(self, callback_server):
        """Test handler registration and unregistration."""
        def dummy_handler(data):
            pass

        # Register handler
        callback_server.register_handler("test", dummy_handler)
        assert "test" in callback_server._callback_handlers

        # Unregister handler
        result = callback_server.unregister_handler("test")
        assert result is True
        assert "test" not in callback_server._callback_handlers

        # Unregister non-existent handler
        result = callback_server.unregister_handler("nonexistent")
        assert result is False

    def test_request_handler_registration(self, callback_server):
        """Test request-specific handler registration."""
        def dummy_handler(request_id, data):
            pass

        callback_server.register_request_handler("req123", dummy_handler)
        assert "req123" in callback_server._request_handlers

    def test_status_property(self, callback_server):
        """Test status property."""
        status = callback_server.status
        assert "running" in status
        assert "host" in status
        assert "port" in status
        assert "callback_url" in status
        assert "handlers" in status
        assert "pending_requests" in status


class TestCallbackEndpoints:
    """Test cases for FastAPI endpoints."""

    def test_root_endpoint(self, test_client):
        """Test root endpoint."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "API Service Callback Server"
        assert "endpoints" in data

    def test_health_endpoint(self, test_client):
        """Test health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_callback_endpoint_success(self, test_client, sample_callback_data):
        """Test successful callback processing."""
        headers = {"Request-Id": "test123", "Content-Type": "application/json"}
        response = test_client.post("/API Service/callback", json=sample_callback_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["request_id"] == "test123"

    def test_callback_endpoint_missing_request_id(self, test_client, sample_callback_data):
        """Test callback without Request-Id header."""
        response = test_client.post("/API Service/callback", json=sample_callback_data)
        assert response.status_code == 400

    def test_callback_endpoint_invalid_data(self, test_client):
        """Test callback with invalid data."""
        headers = {"Request-Id": "test123", "Content-Type": "application/json"}
        invalid_data = [{"invalid": "data"}]
        response = test_client.post("/API Service/callback", json=invalid_data, headers=headers)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_callback_processing(self, callback_server, sample_callback_data):
        """Test callback data processing."""
        handler_called = asyncio.Event()
        received_data = []

        def test_handler(data):
            received_data.append(data)
            handler_called.set()

        callback_server.register_handler("test", test_handler)
        
        # Process callback
        callback_data = [PersonCallbackItem.model_validate(item) for item in sample_callback_data]
        await callback_server._process_callback("test123", callback_data)
        
        # Wait for handler to be called
        await asyncio.wait_for(handler_called.wait(), timeout=1.0)
        
        assert len(received_data) == 1
        assert len(received_data[0]) == 2  # Two items in sample data

    @pytest.mark.asyncio
    async def test_request_specific_handler(self, callback_server, sample_callback_data):
        """Test request-specific handler processing."""
        handler_called = asyncio.Event()
        received_request_id = []

        def test_handler(request_id, data):
            received_request_id.append(request_id)
            handler_called.set()

        callback_server.register_request_handler("test123", test_handler)
        
        # Process callback
        callback_data = [PersonCallbackItem.model_validate(item) for item in sample_callback_data]
        await callback_server._process_callback("test123", callback_data)
        
        # Wait for handler to be called
        await asyncio.wait_for(handler_called.wait(), timeout=1.0)
        
        assert received_request_id[0] == "test123"
        # Handler should be removed after use
        assert "test123" not in callback_server._request_handlers


class TestModuleFunctions:
    """Test module-level functions."""

    def test_get_server(self):
        """Test get_server function."""
        server1 = get_server()
        server2 = get_server()
        assert server1 is server2  # Should return same instance

    @patch('src.lib.callback_server.CallbackServer.start')
    def test_start_server(self, mock_start):
        """Test start_server function."""
        server = start_server(port=8001)
        assert server is not None
        mock_start.assert_called_once_with(background=True)

    def test_callback_data_validation(self, sample_callback_data):
        """Test PersonCallbackData validation."""
        # Valid data
        data = [PersonCallbackItem.model_validate(item) for item in sample_callback_data]
        assert len(data) == 2
        assert data[0].status == "success"
        assert data[0].candidate is not None
        assert data[1].status == "failed"
        assert data[1].candidate is None

    def test_callback_item_validation(self):
        """Test individual callback item validation."""
        # Success item
        success_item = PersonCallbackItem.model_validate({
            "status": "success",
            "item": "test@example.com",
            "candidate": {
                "uid": "123",
                "fullName": "Test User",
                "locations": [],
                "skills": [],
                "education": [],
                "experience": [],
                "contacts": [],
                "social": [],
                "language": []
            }
        })
        assert success_item.status == "success"
        assert success_item.candidate.fullName == "Test User"

        # Failed item
        failed_item = PersonCallbackItem.model_validate({
            "status": "failed",
            "item": "invalid@email"
        })
        assert failed_item.status == "failed"
        assert failed_item.candidate is None