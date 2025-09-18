import pytest
import pandas as pd
from pathlib import Path

from src.models.prospect import Prospect
from src.models.contact_info import ContactInfo
from src.services.csv_exporter import CSVExporter

@pytest.fixture
def sample_prospects():
    """Provides a list of sample Prospect objects for testing."""
    return [
        Prospect(
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
        Prospect(
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

def test_export_to_csv_creates_file_with_correct_headers(sample_prospects, tmp_path):
    """
    Tests that export_to_csv creates a file with the expected headers.
    """
    exporter = CSVExporter()
    output_file = tmp_path / "prospects.csv"
    
    exporter.export_to_csv(sample_prospects, output_file)
    
    assert output_file.exists()
    
    df = pd.read_csv(output_file)
    expected_headers = [
        "name", "title", "company", "location", 
        "email", "phone", "linkedin"
    ]
    assert list(df.columns) == expected_headers

def test_export_to_csv_writes_correct_data(sample_prospects, tmp_path):
    """
    Tests that export_to_csv writes the correct prospect data to the file.
    """
    exporter = CSVExporter()
    output_file = tmp_path / "prospects.csv"
    
    exporter.export_to_csv(sample_prospects, output_file)
    
    df = pd.read_csv(output_file)
    
    assert len(df) == 2
    assert df.iloc[0]["name"] == "John Doe"
    assert df.iloc[1]["company"] == "Innovate Inc."
    assert df.iloc[0]["email"] == "john.doe@techcorp.com"
