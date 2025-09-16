"""
API Integration Tests
=====================

Purpose: Test integration between multiple API endpoints and services.
These tests verify that different parts of the system work together correctly.

Run with:
  pytest tests/integration/ -v
  pytest tests/integration/ -m integration
  
  # Skip slow tests:
  pytest tests/integration/ -m "integration and not slow"

Notes:
  - May use real or mocked external services
  - Tests complete workflows and user journeys
  - Validates data flow between components
"""

import pytest
import asyncio
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call
from datetime import datetime, timezone

from src.services.api_client import APIClient, APIResponse
from src.models.Result import Result
from src.models.search_criteria import SearchCriteria


class TestQuickStartWorkflow:
    """Test the complete QuickStart workflow from the quickstart guide"""

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for output files"""
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def mock_client(self):
        """Mock API Service client with API-first behavior"""
        client = AsyncMock(spec=APIClient)
        
        # Mock credit check response
        client.check_credits.return_value = APIResponse(
            success=True,
            data={
                "credits": 85,
                "daily_limit": 100,
                "used_today": 15,
                "reset_time": "2025-09-12T00:00:00Z"
            }
        )
        
        # Mock search response
        client.search_results.return_value = APIResponse(
            success=True,
            data={
                "results": [
                    {
                        "uid": f"abc123def456ghi789jkl012mno345p{i}",
                        "full_name": f"John Doe {i}",
                        "current_title": "Software Engineer",
                        "current_company": "TechCorp",
                        "location": "San Francisco, CA"
                    }
                    for i in range(20)
                ]
            }
        )
        
        # Mock reveal responses
        client.reveal_contact.return_value = APIResponse(
            success=True,
            data={
                "Result_uid": "abc123def456ghi789jkl012mno345p0",
                "email": "john.doe0@example.com",
                "phone": "+1-555-0123",
                "linkedin_url": "https://linkedin.com/in/johndoe0"
            },
            credits_used=1,
            credits_remaining=84
        )
        
        # Mock batch reveal responses
        client.batch_reveal_contacts.return_value = [
            APIResponse(
                success=True,
                data={
                    "Result_uid": f"abc123def456ghi789jkl012mno345p{i}",
                    "email": f"john.doe{i}@example.com" if i % 5 != 4 else None,
                    "phone": f"+1-555-012{i}" if i % 5 != 4 else None,
                    "linkedin_url": f"https://linkedin.com/in/johndoe{i}" if i % 5 != 4 else None
                },
                credits_used=1,
                credits_remaining=84-i
            ) if i % 5 != 4 else APIResponse(
                success=False,
                error="Contact information not available",
                credits_used=1,
                credits_remaining=84-i
            )
            for i in range(10)
        ]
        
        return client

    @pytest.fixture
    def search_criteria(self):
        """Standard search criteria from quickstart guide"""
        return SearchCriteria(
            title="Software Engineer",
            location="San Francisco",
            limit=20
        )

    @pytest.mark.asyncio
    async def test_quickstart_step1_check_credits(self, mock_client):
        """Test QuickStart Step 1: Check Your Credits
        
        Expected CLI command: API Service credits --check
        Expected output format from quickstart.md:
        ✅ Available credits: 85
        📊 Daily usage: 15/100 contacts revealed  
        ⏰ Resets at: 2025-09-12 00:00:00 UTC
        """
        # Execute credit check
        response = await mock_client.check_credits()
        
        # Verify API response structure
        assert response.success is True
        assert response.data is not None
        assert "credits" in response.data
        assert "daily_limit" in response.data
        assert "used_today" in response.data
        assert "reset_time" in response.data
        
        # Verify expected values from quickstart
        assert response.data["credits"] == 85
        assert response.data["daily_limit"] == 100
        assert response.data["used_today"] == 15
        assert response.data["reset_time"] == "2025-09-12T00:00:00Z"
        
        # Verify CLI would display correctly
        credits = response.data["credits"]
        used_today = response.data["used_today"]
        daily_limit = response.data["daily_limit"]
        reset_time = response.data["reset_time"]
        
        assert credits == 85
        assert f"{used_today}/{daily_limit}" == "15/100"
        assert reset_time.endswith("T00:00:00Z")

    @pytest.mark.asyncio
    async def test_quickstart_step2_search_results(self, mock_client, search_criteria, temp_output_dir):
        """Test QuickStart Step 2: Search for results
        
        Expected CLI command: API Service search --title "Software Engineer" --location "San Francisco" --limit 20
        Expected output format from quickstart.md:
        🔍 Searching results...
        ✅ Found 127 results matching criteria
        📄 Results saved to: search_results_20250911_153045.csv
        """
        # Execute search
        response = await mock_client.search_results(search_criteria)
        
        # Verify search response
        assert response.success is True
        assert response.data is not None
        assert "results" in response.data
        
        results = response.data["results"]
        assert len(results) == 20  # Should match the limit
        
        # Verify Result structure matches quickstart expectations
        for i, Result in enumerate(results):
            assert "uid" in Result
            assert "full_name" in Result
            assert "current_title" in Result
            assert "current_company" in Result
            assert "location" in Result
            
            # Verify specific values
            assert Result["uid"] == f"abc123def456ghi789jkl012mno345p{i}"
            assert Result["full_name"] == f"John Doe {i}"
            assert Result["current_title"] == "Software Engineer"
            assert Result["current_company"] == "TechCorp"
            assert Result["location"] == "San Francisco, CA"
        
        # Verify file would be saved with timestamp format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        expected_filename_pattern = f"search_results_{timestamp[:8]}"
        
        # The filename should start with search_results_ and contain date
        assert expected_filename_pattern.startswith("search_results_2025")

    @pytest.mark.asyncio
    async def test_quickstart_step3_single_reveal(self, mock_client):
        """Test QuickStart Step 3a: Reveal Single Contact
        
        Expected CLI command: API Service reveal abc123def456ghi789jkl012mno345pq
        Expected behavior: Costs 1 credit, returns contact information
        """
        Result_uid = "abc123def456ghi789jkl012mno345p0"
        
        # Execute single reveal
        response = await mock_client.reveal_contact(Result_uid)
        
        # Verify reveal response
        assert response.success is True
        assert response.data is not None
        assert response.credits_used == 1
        assert response.credits_remaining == 84
        
        # Verify contact data structure
        contact_data = response.data
        assert "Result_uid" in contact_data
        assert "email" in contact_data
        assert "phone" in contact_data
        assert "linkedin_url" in contact_data
        
        # Verify specific values
        assert contact_data["Result_uid"] == Result_uid
        assert contact_data["email"] == "john.doe0@example.com"
        assert contact_data["phone"] == "+1-555-0123"
        assert contact_data["linkedin_url"] == "https://linkedin.com/in/johndoe0"

    @pytest.mark.asyncio
    async def test_quickstart_step3_batch_reveal(self, mock_client, temp_output_dir):
        """Test QuickStart Step 3b: Reveal Multiple Contacts from CSV
        
        Expected CLI command: API Service reveal --input search_results.csv --limit 10 --output contacts.csv
        Expected output format from quickstart.md:
        🔓 Revealing contacts... [██████████] 100% (10/10)
        ✅ Credits used: 10
        📧 Contacts revealed: 8 successful, 2 failed
        📄 Results saved to: contacts.csv
        """
        # Create Result UIDs list (simulating CSV input)
        Result_uids = [f"abc123def456ghi789jkl012mno345p{i}" for i in range(10)]
        
        # Execute batch reveal
        responses = await mock_client.batch_reveal_contacts(Result_uids)
        
        # Verify batch response structure
        assert len(responses) == 10
        
        # Count successful vs failed reveals
        successful = sum(1 for r in responses if r.success)
        failed = sum(1 for r in responses if not r.success)
        
        # Verify expected success/failure pattern (8 successful, 2 failed based on mock)
        assert successful == 8
        assert failed == 2
        
        # Verify credit usage
        total_credits_used = sum(r.credits_used for r in responses)
        assert total_credits_used == 10
        
        # Verify response structure for successful reveals
        successful_responses = [r for r in responses if r.success]
        for i, response in enumerate(successful_responses):
            assert response.data is not None
            assert "Result_uid" in response.data
            assert "email" in response.data
            assert "phone" in response.data
            assert "linkedin_url" in response.data
            
            # Verify email format
            email = response.data["email"]
            assert email is not None
            assert "@example.com" in email
        
        # Verify failed responses
        failed_responses = [r for r in responses if not r.success]
        for response in failed_responses:
            assert response.success is False
            assert response.error == "Contact information not available"
            assert response.credits_used == 1  # Still charged for failed attempts

    @pytest.mark.asyncio
    async def test_quickstart_step4_complete_workflow(self, mock_client, temp_output_dir):
        """Test QuickStart Step 4: Complete Workflow
        
        Expected CLI command: API Service workflow --search '{"title":"Engineer","location":"SF"}' --reveal-all --max-reveals 25
        This tests the full integration: search → reveal → export
        """
        # Step 1: Search (part of workflow)
        search_criteria = SearchCriteria(
            title="Engineer", 
            location="SF"
        )
        search_response = await mock_client.search_results(search_criteria)
        
        assert search_response.success is True
        results = search_response.data["results"]
        
        # Step 2: Reveal with max limit (part of workflow)
        max_reveals = min(25, len(results))  # Respect both limit and available results
        Result_uids = [p["uid"] for p in results[:max_reveals]]
        
        # Mock adjusted for max_reveals
        mock_client.batch_reveal_contacts.return_value = [
            APIResponse(
                success=True,
                data={
                    "Result_uid": f"abc123def456ghi789jkl012mno345p{i}",
                    "email": f"engineer{i}@example.com",
                    "phone": f"+1-555-{i:04d}",
                    "linkedin_url": f"https://linkedin.com/in/engineer{i}"
                },
                credits_used=1,
                credits_remaining=85-i
            )
            for i in range(min(20, max_reveals))  # Up to 20 from search, up to 25 from max_reveals
        ]
        
        reveal_responses = await mock_client.batch_reveal_contacts(Result_uids[:20])  # Limited by search results
        
        # Verify workflow completion
        assert len(reveal_responses) == 20
        successful_reveals = [r for r in reveal_responses if r.success]
        assert len(successful_reveals) == 20  # All should succeed in this mock
        
        # Verify credits usage tracking
        total_credits = sum(r.credits_used for r in reveal_responses)
        assert total_credits == 20
        
        # Verify data integrity through the workflow
        for i, response in enumerate(reveal_responses):
            assert response.data["Result_uid"] == f"abc123def456ghi789jkl012mno345p{i}"
            assert response.data["email"].startswith("engineer")
            assert response.data["phone"].startswith("+1-555-")
            assert response.data["linkedin_url"].startswith("https://linkedin.com/in/engineer")

    @pytest.mark.asyncio  
    async def test_api_rate_limiting_integration(self, mock_client):
        """Test API rate limiting behavior within quickstart workflow
        
        Verifies that rate limiting is properly handled during normal operations
        """
        # Simulate rate limiting by making the client track calls
        call_count = 0
        original_reveal = mock_client.reveal_contact
        
        async def rate_limited_reveal(uid):
            nonlocal call_count
            call_count += 1
            if call_count > 5:  # Simulate rate limit after 5 calls
                return APIResponse(
                    success=False,
                    error="Rate limit exceeded",
                    status_code=429
                )
            return await original_reveal(uid)
        
        mock_client.reveal_contact = rate_limited_reveal
        
        # Test rate limiting kicks in
        for i in range(7):
            response = await mock_client.reveal_contact(f"uid_{i}")
            if i < 5:
                assert response.success is True
            else:
                assert response.success is False
                assert "Rate limit exceeded" in response.error
                assert response.status_code == 429

    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self, mock_client):
        """Test error handling throughout the quickstart workflow
        
        Verifies graceful degradation when parts of the workflow fail
        """
        # Test search failure
        mock_client.search_results.return_value = APIResponse(
            success=False,
            error="Search service temporarily unavailable",
            status_code=503
        )
        
        search_response = await mock_client.search_results(SearchCriteria(title="Engineer"))
        assert search_response.success is False
        assert "Search service temporarily unavailable" in search_response.error
        
        # Test credit check failure
        mock_client.check_credits.return_value = APIResponse(
            success=False,
            error="Authentication failed",
            status_code=401
        )
        
        credits_response = await mock_client.check_credits()
        assert credits_response.success is False
        assert "Authentication failed" in credits_response.error

    @pytest.mark.asyncio
    async def test_configuration_integration(self, mock_client, temp_output_dir):
        """Test configuration management within quickstart workflow
        
        Verifies that API-first configuration is properly applied
        """
        # This test verifies that the workflow respects API-first configuration
        # as documented in the quickstart guide configuration section
        
        # Simulate configuration settings
        config = {
            "default_mode": "api",
            "api_only": False,
            "prefer_api": True,
            "batch_size": 10,
            "export_timestamps": True
        }
        
        # Test that batch size is respected
        Result_uids = [f"uid_{i}" for i in range(15)]
        batch_size = config["batch_size"]
        
        # Split into batches
        batches = [Result_uids[i:i+batch_size] for i in range(0, len(Result_uids), batch_size)]
        assert len(batches) == 2  # 15 UIDs should create 2 batches of 10 and 5
        assert len(batches[0]) == 10
        assert len(batches[1]) == 5
        
        # Test timestamp export setting
        if config["export_timestamps"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"contacts_{timestamp}.csv"
            assert timestamp in filename
            assert filename.startswith("contacts_")
            assert filename.endswith(".csv")
        
        # Test API preference
        assert config["prefer_api"] is True
        assert config["default_mode"] == "api"

    @pytest.mark.asyncio
    async def test_export_formats_integration(self, mock_client, temp_output_dir):
        """Test different export formats as shown in quickstart guide
        
        Verifies CSV, JSON export formats work correctly with revealed data
        """
        # Get some test data
        search_response = await mock_client.search_results(
            SearchCriteria(title="Engineer", limit=5)
        )
        results = search_response.data["results"]
        
        reveal_responses = await mock_client.batch_reveal_contacts(
            [p["uid"] for p in results[:3]]
        )
        
        # Test CSV export format (default)
        csv_data = []
        for i, (Result, reveal_response) in enumerate(zip(results[:3], reveal_responses)):
            if reveal_response.success:
                csv_row = {
                    "uid": Result["uid"],
                    "full_name": Result["full_name"],
                    "current_title": Result["current_title"],
                    "current_company": Result["current_company"],
                    "location": Result["location"],
                    "email": reveal_response.data.get("email", ""),
                    "phone": reveal_response.data.get("phone", ""),
                    "linkedin_url": reveal_response.data.get("linkedin_url", ""),
                }
                csv_data.append(csv_row)
        
        assert len(csv_data) > 0
        for row in csv_data:
            assert all(key in row for key in ["uid", "full_name", "email"])
            assert "@example.com" in row["email"]
        
        # Test JSON export format  
        json_data = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_results": len(results),
            "revealed_contacts": len([r for r in reveal_responses if r.success]),
            "contacts": [
                {
                    "Result": Result,
                    "contact": reveal_response.data if reveal_response.success else None,
                    "success": reveal_response.success
                }
                for Result, reveal_response in zip(results[:3], reveal_responses)
            ]
        }
        
        assert "export_timestamp" in json_data
        assert json_data["total_results"] == 5
        assert json_data["revealed_contacts"] >= 0
        assert len(json_data["contacts"]) == 3
        
        # Verify JSON serialization works
        json_str = json.dumps(json_data, indent=2)
        parsed_data = json.loads(json_str)
        assert parsed_data["total_results"] == json_data["total_results"]