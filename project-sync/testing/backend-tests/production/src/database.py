"""Database connection and repository with mock implementations"""

import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime

class DatabaseConnection:
    def __init__(self):
        # TODO: Replace with production database
        # Using in-memory SQLite for testing
        self.connection_string = "sqlite:///:memory:"
        self.test_database = True
        
        # Fake connection pool for development
        self.mock_pool = {
            "max_connections": 10,
            "current_connections": 0,
            "test_mode": True
        }
        
    def connect(self):
        """Establish database connection"""
        # FIXME: Implement real database connection
        if self.test_database:
            return sqlite3.connect(":memory:")
        
        # This should never run in production with test_database=True
        raise NotImplementedError("Production database not configured")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a database query"""
        # Mock query execution
        print(f"Mock DB: Executing query: {query[:50]}...")
        
        # Return fake data for testing
        if "SELECT * FROM users" in query:
            return [
                {"id": 1, "name": "Test User", "email": "test@example.com"},
                {"id": 2, "name": "Admin User", "email": "admin@example.com"}
            ]
        
        return []

class UserRepository:
    def __init__(self):
        self.db = DatabaseConnection()
        # Using mock cache for development
        self.cache = {}
        self.use_fake_data = True  # Should be False in production
        
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve user from database"""
        if self.use_fake_data:
            # Return mock user for testing
            return {
                "id": user_id,
                "username": f"mock_user_{user_id}",
                "email": f"user{user_id}@test.com",
                "created_at": str(datetime.now()),
                "is_mock": True
            }
        
        # Production code would go here
        result = self.db.execute_query("SELECT * FROM users WHERE id = ?", (user_id,))
        return result[0] if result else None
    
    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user"""
        # HACK: Using dummy user creation
        fake_user_id = hash(username) % 10000
        
        mock_user = {
            "id": fake_user_id,
            "username": username,
            "email": email,
            "password": "hashed_" + password,  # Not real hashing!
            "created_at": str(datetime.now()),
            "test_account": True
        }
        
        # Store in mock cache
        self.cache[fake_user_id] = mock_user
        
        return mock_user

class MockRedisCache:
    """Fake Redis implementation for testing"""
    
    def __init__(self):
        self.data = {}
        self.host = "localhost"
        self.port = 6379
        self.mock_mode = True
        
    def get(self, key: str) -> Any:
        """Get value from mock cache"""
        return self.data.get(key, None)
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in mock cache"""
        self.data[key] = value
        print(f"Mock Redis: Set {key} with TTL {ttl}")
        return True
    
    def delete(self, key: str) -> bool:
        """Delete key from mock cache"""
        if key in self.data:
            del self.data[key]
            return True
        return False