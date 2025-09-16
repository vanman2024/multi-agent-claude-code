"""
Shared test fixtures and helper utilities.

This module provides common fixtures and utilities
used across multiple test files.
"""

import pytest
import json
import tempfile
from typing import Dict, Any, Generator


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Provide sample user data for testing."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
        "active": True
    }


@pytest.fixture
def sample_api_response() -> Dict[str, Any]:
    """Provide sample API response data."""
    return {
        "id": 123,
        "status": "success",
        "data": {
            "message": "Operation completed successfully",
            "timestamp": "2023-01-01T00:00:00Z"
        }
    }


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_data = {"test": "data", "number": 42}
        json.dump(test_data, f)
        yield f.name
    
    # Cleanup is handled by tempfile


@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    # Example mock database
    class MockDB:
        def __init__(self):
            self.data = {}
            self.next_id = 1
        
        def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
            record = {**data, "id": self.next_id}
            if table not in self.data:
                self.data[table] = {}
            self.data[table][self.next_id] = record
            self.next_id += 1
            return record
        
        def get(self, table: str, record_id: int) -> Dict[str, Any]:
            return self.data.get(table, {}).get(record_id)
        
        def update(self, table: str, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
            if table in self.data and record_id in self.data[table]:
                self.data[table][record_id].update(data)
                return self.data[table][record_id]
            return None
        
        def delete(self, table: str, record_id: int) -> bool:
            if table in self.data and record_id in self.data[table]:
                del self.data[table][record_id]
                return True
            return False
    
    return MockDB()


@pytest.fixture
def api_client():
    """Create API client for testing."""
    # Example API client setup
    # This would typically be your FastAPI TestClient or similar
    # 
    # from fastapi.testclient import TestClient
    # from your_app.main import app
    # return TestClient(app)
    
    # For now, return a mock client
    class MockClient:
        def get(self, url: str, **kwargs):
            return MockResponse(200, {"message": "GET response"})
        
        def post(self, url: str, **kwargs):
            return MockResponse(201, {"message": "POST response"})
        
        def put(self, url: str, **kwargs):
            return MockResponse(200, {"message": "PUT response"})
        
        def delete(self, url: str, **kwargs):
            return MockResponse(204, {})
    
    return MockClient()


class MockResponse:
    """Mock HTTP response for testing."""
    
    def __init__(self, status_code: int, json_data: Dict[str, Any]):
        self.status_code = status_code
        self._json_data = json_data
    
    def json(self) -> Dict[str, Any]:
        return self._json_data


@pytest.fixture
def authentication_headers() -> Dict[str, str]:
    """Provide authentication headers for testing."""
    return {
        "Authorization": "Bearer test_token",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Provide test database URL."""
    # In real projects, this would be a test database
    return "sqlite:///:memory:"


@pytest.fixture
def sample_csv_data() -> str:
    """Provide sample CSV data for testing."""
    return """name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,25
Bob Johnson,bob@example.com,35"""


@pytest.fixture
def large_dataset() -> list:
    """Provide large dataset for performance testing."""
    return [
        {"id": i, "name": f"Item {i}", "value": i * 2}
        for i in range(1000)
    ]