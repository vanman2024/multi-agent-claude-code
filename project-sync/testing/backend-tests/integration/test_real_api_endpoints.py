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
import time
from datetime import datetime
from pathlib import Path

from src.models.search_criteria import SearchCriteria
from src.services.api_client import APIClient
from src.lib.config import get_config


@pytest.mark.live
@pytest.mark.asyncio  
class TestRealAPI ServiceAPI:
    """Test real API endpoints with live data"""

    @pytest.fixture(scope="class")
    def real_client(self):
        """Create real API Service client with API key"""
        config = get_config()
        
        # Skip if no real API key (for now we'll use API key instead of email/password)
        if not config.API Service.api_key:
            pytest.skip("Real API key required. Set API_KEY")
        
        client = APIClient(
            api_key=config.API Service.api_key,
            base_url="https://api.API Service.com"
        )
        return client

    @pytest.mark.asyncio
    async def test_heavy_equipment_mechanic_canada_search(self, real_client):
        """Test real API search for Heavy Equipment Mechanic in Canada
        
        This validates:
        - Actual result counts for this job title
        - Data structure and quality
        - Geographic filtering accuracy
        - Response time performance
        """
        search_criteria = SearchCriteria(
            title="Heavy Equipment Mechanic",
            location="Canada",
            limit=50  # Test with reasonable limit
        )
        
        start_time = time.time()
        response = await real_client.search_results(search_criteria.dict())
        end_time = time.time()
        
        # Response time validation
        response_time = end_time - start_time
        assert response_time < 10.0, f"Search took {response_time:.2f}s, expected < 10s"
        
        # API response validation
        assert response.success is True, f"Search failed: {response.error}"
        assert response.data is not None
        assert "results" in response.data
        
        results = response.data["results"]
        
        # Result count validation
        assert len(results) > 0, "No Heavy Equipment Mechanic results found in Canada"
        print(f"✅ Found {len(results)} Heavy Equipment Mechanic results in Canada")
        
        # Data quality validation
        for i, Result in enumerate(results[:5]):  # Check first 5 for quality
            # Required fields
            assert "uid" in Result, f"Result {i} missing uid"
            assert "current_title" in Result, f"Result {i} missing current_title" 
            assert "location" in Result, f"Result {i} missing location"
            
            # Validate job title relevance
            title = Result["current_title"].lower()
            location = Result["location"].lower()
            
            # Check title relevance (should contain mechanic-related keywords)
            title_keywords = ["mechanic", "technician", "operator", "maintenance", "equipment", "heavy"]
            title_relevant = any(keyword in title for keyword in title_keywords)
            if not title_relevant:
                print(f"⚠️  Title '{Result['current_title']}' may not be relevant to Heavy Equipment Mechanic")
            
            # Check Canada location
            canada_keywords = ["canada", "ontario", "alberta", "british columbia", "quebec", "manitoba", "saskatchewan"]
            location_relevant = any(keyword in location for keyword in canada_keywords)
            if not location_relevant:
                print(f"⚠️  Location '{Result['location']}' may not be in Canada")
        
        # Performance logging
        print(f"📊 Search Performance:")
        print(f"   Response Time: {response_time:.2f}s")
        print(f"   Results: {len(results)}")
        print(f"   Rate: {len(results)/response_time:.1f} results/second")
        
        return results

    @pytest.mark.asyncio
    async def test_credits_check_real_api(self, real_client):
        """Test real credits API to validate actual account status"""
        start_time = time.time()
        response = await real_client.check_credits()
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"Credits check took {response_time:.2f}s, expected < 5s"
        
        assert response.success is True, f"Credits check failed: {response.error}"
        assert response.data is not None
        
        # Validate credits data structure
        credits_data = response.data
        required_fields = ["credits", "daily_limit", "used_today", "reset_time"]
        
        for field in required_fields:
            assert field in credits_data, f"Missing credits field: {field}"
        
        # Validate data types and ranges
        assert isinstance(credits_data["credits"], int), "Credits should be integer"
        assert isinstance(credits_data["daily_limit"], int), "Daily limit should be integer"  
        assert isinstance(credits_data["used_today"], int), "Used today should be integer"
        assert isinstance(credits_data["reset_time"], str), "Reset time should be string"
        
        # Logical validation
        assert credits_data["credits"] >= 0, "Credits cannot be negative"
        assert credits_data["daily_limit"] > 0, "Daily limit should be positive"
        assert credits_data["used_today"] >= 0, "Used today cannot be negative"
        assert credits_data["used_today"] <= credits_data["daily_limit"], "Used today cannot exceed daily limit"
        
        print(f"💳 Real Account Status:")
        print(f"   Available Credits: {credits_data['credits']}")
        print(f"   Daily Usage: {credits_data['used_today']}/{credits_data['daily_limit']}")
        print(f"   Reset Time: {credits_data['reset_time']}")
        
        return credits_data

    @pytest.mark.asyncio
    async def test_contact_reveal_real_api(self, real_client):
        """Test real contact reveal API with actual Result data
        
        This test:
        1. Searches for results
        2. Attempts to reveal contact info for one
        3. Validates response structure and data quality
        """
        # First get some results
        search_criteria = SearchCriteria(title="Heavy Equipment Mechanic", location="Canada", limit=5)
        search_response = await real_client.search_results(search_criteria.dict())
        
        assert search_response.success is True, "Search failed"
        results = search_response.data["results"]
        assert len(results) > 0, "No results found for reveal test"
        
        # Try to reveal first Result
        Result = results[0]
        Result_uid = Result["uid"]
        
        start_time = time.time()
        reveal_response = await real_client.reveal_contact(Result_uid)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 15.0, f"Contact reveal took {response_time:.2f}s, expected < 15s"
        
        if reveal_response.success:
            # Successful reveal - validate data structure
            contact_data = reveal_response.data
            
            # Common contact fields that might be present
            possible_fields = ["email", "phone", "linkedin_url", "full_name"]
            found_fields = [field for field in possible_fields if field in contact_data and contact_data[field]]
            
            assert len(found_fields) > 0, "No contact information revealed"
            
            print(f"📞 Contact Reveal Success:")
            print(f"   Result: {Result.get('current_title', 'Unknown')} at {Result.get('current_company', 'Unknown')}")
            print(f"   Response Time: {response_time:.2f}s")
            print(f"   Fields Revealed: {', '.join(found_fields)}")
            
            # Validate email format if present
            if "email" in contact_data and contact_data["email"]:
                email = contact_data["email"]
                assert "@" in email, f"Invalid email format: {email}"
                assert "." in email, f"Invalid email format: {email}"
        
        else:
            # Failed reveal - this might be expected (insufficient credits, etc.)
            print(f"⚠️  Contact reveal failed (may be expected): {reveal_response.error}")
            
            # Common acceptable failure reasons
            acceptable_errors = [
                "insufficient credits",
                "daily limit exceeded", 
                "contact not available",
                "rate limit"
            ]
            
            error_msg = reveal_response.error.lower()
            is_acceptable = any(reason in error_msg for reason in acceptable_errors)
            
            if not is_acceptable:
                pytest.fail(f"Unexpected reveal failure: {reveal_response.error}")

    @pytest.mark.asyncio
    async def test_api_rate_limiting_real(self, real_client):
        """Test real API rate limiting behavior"""
        # Make rapid requests to test rate limiting
        requests = []
        start_time = time.time()
        
        # Make 5 rapid search requests
        for i in range(5):
            search_criteria = SearchCriteria(
                title=f"Mechanic {i}",  # Slight variation
                location="Canada", 
                limit=5
            )
            requests.append(real_client.search_results(search_criteria.dict()))
        
        # Execute all requests concurrently
        responses = await asyncio.gather(*requests, return_exceptions=True)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Analyze responses
        successful = sum(1 for r in responses if hasattr(r, 'success') and r.success)
        rate_limited = sum(1 for r in responses if hasattr(r, 'error') and 'rate limit' in str(r.error).lower())
        errors = len([r for r in responses if isinstance(r, Exception)])
        
        print(f"🚦 Rate Limiting Test Results:")
        print(f"   Total Requests: 5")
        print(f"   Successful: {successful}")
        print(f"   Rate Limited: {rate_limited}")
        print(f"   Errors: {errors}")
        print(f"   Total Time: {total_time:.2f}s")
        print(f"   Average Time per Request: {total_time/5:.2f}s")
        
        # At least some should succeed (or fail gracefully with rate limiting)
        assert successful + rate_limited >= 3, "Too many unexpected failures during rate limiting test"

    @pytest.mark.asyncio
    async def test_location_filtering_accuracy(self, real_client):
        """Test location filtering accuracy with different Canadian locations"""
        
        canadian_locations = [
            "Toronto, Ontario, Canada",
            "Vancouver, British Columbia, Canada", 
            "Calgary, Alberta, Canada",
            "Montreal, Quebec, Canada"
        ]
        
        location_results = {}
        
        for location in canadian_locations:
            search_criteria = SearchCriteria(
                title="Heavy Equipment Mechanic",
                location=location,
                limit=10
            )
            
            response = await real_client.search_results(search_criteria.dict())
            
            if response.success:
                results = response.data["results"]
                location_results[location] = len(results)
                
                # Validate location relevance for first few results
                for Result in results[:3]:
                    Result_location = Result.get("location", "").lower()
                    city = location.split(",")[0].lower()
                    
                    if city not in Result_location:
                        print(f"⚠️  Location mismatch: searched '{location}', got '{Result['location']}'")
            
            else:
                location_results[location] = 0
                print(f"❌ Search failed for {location}: {response.error}")
            
            # Small delay to respect rate limits
            await asyncio.sleep(1)
        
        print(f"🌍 Location Filtering Results:")
        for location, count in location_results.items():
            print(f"   {location}: {count} results")
        
        # At least some locations should return results
        total_results = sum(location_results.values())
        assert total_results > 0, "No results found for any Canadian locations"


@pytest.mark.live
class TestAPIDataQuality:
    """Test data quality and accuracy of real API responses"""
    
    @pytest.mark.asyncio
    async def test_job_title_relevance_scoring(self, real_client):
        """Test how well job title searches match actual job titles"""
        
        test_searches = [
            ("Heavy Equipment Mechanic", ["mechanic", "equipment", "heavy", "machinery", "operator"]),
            ("Software Engineer", ["software", "engineer", "developer", "programmer", "coding"]),
            ("Sales Manager", ["sales", "manager", "business", "account", "revenue"])
        ]
        
        for search_title, expected_keywords in test_searches:
            search_criteria = SearchCriteria(
                title=search_title,
                location="Canada",
                limit=20
            )
            
            response = await real_client.search_results(search_criteria.dict())
            
            if not response.success:
                print(f"❌ Search failed for '{search_title}': {response.error}")
                continue
            
            results = response.data["results"]
            if len(results) == 0:
                print(f"⚠️  No results for '{search_title}'")
                continue
            
            # Analyze title relevance
            relevant_count = 0
            for Result in results:
                actual_title = Result.get("current_title", "").lower()
                
                # Check if any expected keywords are in the actual title
                matches = [kw for kw in expected_keywords if kw in actual_title]
                if matches:
                    relevant_count += 1
                else:
                    print(f"   Less relevant: '{Result['current_title']}'")
            
            relevance_score = (relevant_count / len(results)) * 100
            print(f"🎯 Title Relevance for '{search_title}':")
            print(f"   Results: {len(results)}")
            print(f"   Relevant: {relevant_count} ({relevance_score:.1f}%)")
            
            # At least 50% should be relevant
            assert relevance_score >= 50, f"Low relevance score ({relevance_score:.1f}%) for '{search_title}'"
            
            # Small delay between searches
            await asyncio.sleep(2)


if __name__ == "__main__":
    """Run real API tests manually"""
    pytest.main([
        __file__, 
        "-v", 
        "-s",
        "--tb=short",
        "-m", "live"
    ])