#!/usr/bin/env python3
"""Test script to verify all dependencies are working."""

def test_imports():
    """Test importing all required packages."""
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import httpx
        print("✅ httpx imported successfully")
        
        import pydantic
        print("✅ pydantic imported successfully")
        
        import fastapi
        print("✅ fastapi imported successfully")
        
        print("\n🎉 All dependencies are working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
