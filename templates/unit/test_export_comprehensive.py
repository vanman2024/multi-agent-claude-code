#!/usr/bin/env python3
"""
Test script for ExportService functionality.
"""

import asyncio
import json
from pathlib import Path
from src.services.export_service import ExportService, ExportServiceConfig

async def test_comprehensive_export():
    """Test comprehensive export functionality."""
    
    # Sample prospect data with various fields
    prospects = [
        {
            "uid": "prospect_001",
            "full_name": "John Doe",
            "first_name": "John",
            "last_name": "Doe",
            "current_title": "Senior Software Engineer",
            "current_company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "profile_url": "https://signalhire.com/profiles/johndoe"
        },
        {
            "uid": "prospect_002", 
            "full_name": "Jane Smith",
            "first_name": "Jane",
            "last_name": "Smith",
            "current_title": "Product Manager",
            "current_company": "StartupXYZ",
            "location": "New York, NY",
            "linkedin_url": "https://linkedin.com/in/janesmith",
            "profile_url": "https://signalhire.com/profiles/janesmith"
        },
        {
            "uid": "prospect_003",
            "full_name": "Bob Johnson",
            "first_name": "Bob", 
            "last_name": "Johnson",
            "current_title": "Data Scientist",
            "current_company": "DataCorp",
            "location": "Austin, TX",
            "linkedin_url": "https://linkedin.com/in/bobjohnson",
            "profile_url": "https://signalhire.com/profiles/bobjohnson"
        }
    ]
    
    # Sample contact information
    contacts = {
        "prospect_001": {
            "contacts": [
                {"type": "email", "value": "john.doe@techcorp.com", "primary": True},
                {"type": "email", "value": "john@gmail.com", "primary": False},
                {"type": "phone", "value": "+1-415-555-1234", "primary": True}
            ],
            "credits_used": 2,
            "reveal_timestamp": "2025-09-11T14:00:00Z"
        },
        "prospect_002": {
            "contacts": [
                {"type": "email", "value": "jane.smith@startupxyz.com", "primary": True},
                {"type": "phone", "value": "+1-212-555-5678", "primary": True}
            ],
            "credits_used": 2,
            "reveal_timestamp": "2025-09-11T14:01:00Z"
        }
    }
    
    # Sample experience data
    experiences = {
        "prospect_001": [
            {
                "company": "TechCorp Inc",
                "title": "Senior Software Engineer",
                "start_date": "2022-01-01",
                "end_date": None,
                "duration": "3+ years",
                "current": True
            },
            {
                "company": "Previous Corp",
                "title": "Software Engineer",
                "start_date": "2020-01-01", 
                "end_date": "2021-12-31",
                "duration": "2 years",
                "current": False
            }
        ]
    }
    
    # Sample education data
    education = {
        "prospect_001": [
            {
                "university": "Stanford University",
                "degree": "Master of Science",
                "field_of_study": "Computer Science",
                "graduation_year": 2020
            },
            {
                "university": "UC Berkeley",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science", 
                "graduation_year": 2018
            }
        ]
    }
    
    # Test 1: Basic export
    print("=== Test 1: Basic Export ===")
    config = ExportServiceConfig(validate_data=True, sanitize_data=True)
    service = ExportService(config)
    
    result = await service.export_to_csv(
        prospects=prospects,
        contacts=contacts,
        experiences=experiences,
        education=education,
        output_file="comprehensive_export.csv",
        include_contacts=True
    )
    
    print(f"✅ Export successful: {result.success}")
    print(f"✅ Records processed: {result.records_processed}")
    print(f"✅ Valid records: {result.valid_records}")
    print(f"✅ Records exported: {result.records_exported}")
    print(f"✅ File size: {result.file_size_bytes} bytes")
    print(f"✅ Duration: {result.export_duration_seconds:.2f} seconds")
    print(f"✅ Output file: {result.file_path}")
    
    # Test 2: Export with invalid data (should handle gracefully)
    print("\n=== Test 2: Export with Invalid Data ===")
    invalid_prospects = [
        {"uid": "", "full_name": ""},  # Invalid: empty fields
        {"uid": "valid_001", "full_name": "Valid Person"},  # Valid
        {"uid": None, "full_name": None}  # Invalid: null fields
    ]
    
    result2 = await service.export_to_csv(
        prospects=invalid_prospects,
        output_file="invalid_data_export.csv"
    )
    
    print(f"✅ Export with invalid data: {result2.success}")
    print(f"✅ Records processed: {result2.records_processed}")
    print(f"✅ Valid records: {result2.valid_records}")
    print(f"✅ Invalid records: {result2.invalid_records}")
    
    # Test 3: Export operations
    print("\n=== Test 3: Export Operations ===")
    operations = [
        {
            "operation_id": "search_001",
            "operation_type": "search",
            "status": "completed",
            "created_at": "2025-09-11T14:00:00Z",
            "completed_at": "2025-09-11T14:00:30Z",
            "total_results": 150,
            "credits_used": 0
        },
        {
            "operation_id": "reveal_001", 
            "operation_type": "reveal",
            "status": "completed",
            "created_at": "2025-09-11T14:01:00Z",
            "completed_at": "2025-09-11T14:01:45Z",
            "prospects_revealed": 25,
            "credits_used": 50
        }
    ]
    
    result3 = await service.export_operations_to_csv(
        operations=operations,
        output_file="operations_export.csv"
    )
    
    print(f"✅ Operations export: {result3.success}")
    print(f"✅ Operations exported: {result3.records_exported}")
    
    # Test 4: Process from JSON file
    print("\n=== Test 4: Export from JSON File ===")
    json_data = {"prospects": prospects[:2]}  # First 2 prospects
    json_file = "test_input.json"
    
    with open(json_file, 'w') as f:
        json.dump(json_data, f)
    
    result4 = await service.export_to_csv(
        input_file=json_file,
        output_file="from_json_export.csv"
    )
    
    print(f"✅ JSON file export: {result4.success}")
    print(f"✅ Records from JSON: {result4.records_exported}")
    
    # Show generated files
    print("\n=== Generated Files ===")
    files = ["comprehensive_export.csv", "invalid_data_export.csv", "operations_export.csv", "from_json_export.csv"]
    for file in files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"✅ {file}: {size} bytes")

if __name__ == "__main__":
    asyncio.run(test_comprehensive_export())
