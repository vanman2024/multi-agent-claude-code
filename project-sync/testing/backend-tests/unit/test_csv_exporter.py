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
import pandas as pd
from pathlib import Path

from src.models.Result import Result
from src.models.contact_info import ContactInfo
from src.services.csv_exporter import CSVExporter

@pytest.fixture
def sample_results():
    """Provides a list of sample Result objects for testing."""
    return [
        Result(
            name="John Doe",
            title="Software Engineer",
            company="Tech Corp",
            location="San Francisco, CA",
            contact=ContactInfo(
                email="john.doe@techcorp.com",
                phone="123-456-7890",
                linkedin="https://linkedin.com/in/johndoe"
            )
        ),
        Result(
            name="Jane Smith",
            title="Product Manager",
            company="Innovate Inc.",
            location="New York, NY",
            contact=ContactInfo(
                email="jane.smith@innovate.com",
                phone="098-765-4321",
                linkedin="https://linkedin.com/in/janesmith"
            )
        ),
    ]

def test_export_to_csv_creates_file_with_correct_headers(sample_results, tmp_path):
    """
    Tests that export_to_csv creates a file with the expected headers.
    """
    exporter = CSVExporter()
    output_file = tmp_path / "results.csv"
    
    exporter.export_to_csv(sample_results, output_file)
    
    assert output_file.exists()
    
    df = pd.read_csv(output_file)
    expected_headers = [
        "name", "title", "company", "location", 
        "email", "phone", "linkedin"
    ]
    assert list(df.columns) == expected_headers

def test_export_to_csv_writes_correct_data(sample_results, tmp_path):
    """
    Tests that export_to_csv writes the correct Result data to the file.
    """
    exporter = CSVExporter()
    output_file = tmp_path / "results.csv"
    
    exporter.export_to_csv(sample_results, output_file)
    
    df = pd.read_csv(output_file)
    
    assert len(df) == 2
    assert df.iloc[0]["name"] == "John Doe"
    assert df.iloc[1]["company"] == "Innovate Inc."
    assert df.iloc[0]["email"] == "john.doe@techcorp.com"
