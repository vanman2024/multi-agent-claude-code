"""
Real SignalHire API Endpoint Tests

Tests actual API endpoints with real credentials to validate:
- Data quality and structure
- Result counts and accuracy
- Response times and performance
- Rate limiting behavior
- Error handling

These tests require real SignalHire credentials and hit live endpoints.
Mark with @pytest.mark.live to distinguish from mocked tests.
"""

import pytest
import asyncio
import time
from datetime import datetime
from pathlib import Path

from src.models.search_criteria import SearchCriteria
from src.services.signalhire_client import SignalHireClient
from src.lib.config import get_config


@pytest.mark.live
@pytest.mark.asyncio  
class TestRealSignalHireAPI:
    """Test real SignalHire API endpoints with live data"""

    @pytest.fixture(scope="class")
    def real_client(self):
        """Create real SignalHire client with API key"""
        config = get_config()
        
        # Skip if no real API key (for now we'll use API key instead of email/password)
        if not config.signalhire.api_key:
            pytest.skip("Real SignalHire API key required. Set SIGNALHIRE_API_KEY")
        
        client = SignalHireClient(
            api_key=config.signalhire.api_key,
            base_url="https://api.signalhire.com"
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
        response = await real_client.search_prospects(search_criteria.dict())
        end_time = time.time()
        
        # Response time validation
        response_time = end_time - start_time
        assert response_time < 10.0, f"Search took {response_time:.2f}s, expected < 10s"
        
        # API response validation
        assert response.success is True, f"Search failed: {response.error}"
        assert response.data is not None
        assert "prospects" in response.data
        
        prospects = response.data["prospects"]
        
        # Result count validation
        assert len(prospects) > 0, "No Heavy Equipment Mechanic prospects found in Canada"
        print(f"✅ Found {len(prospects)} Heavy Equipment Mechanic prospects in Canada")
        
        # Data quality validation
        for i, prospect in enumerate(prospects[:5]):  # Check first 5 for quality
            # Required fields
            assert "uid" in prospect, f"Prospect {i} missing uid"
            assert "current_title" in prospect, f"Prospect {i} missing current_title" 
            assert "location" in prospect, f"Prospect {i} missing location"
            
            # Validate job title relevance
            title = prospect["current_title"].lower()
            location = prospect["location"].lower()
            
            # Check title relevance (should contain mechanic-related keywords)
            title_keywords = ["mechanic", "technician", "operator", "maintenance", "equipment", "heavy"]
            title_relevant = any(keyword in title for keyword in title_keywords)
            if not title_relevant:
                print(f"⚠️  Title '{prospect['current_title']}' may not be relevant to Heavy Equipment Mechanic")
            
            # Check Canada location
            canada_keywords = ["canada", "ontario", "alberta", "british columbia", "quebec", "manitoba", "saskatchewan"]
            location_relevant = any(keyword in location for keyword in canada_keywords)
            if not location_relevant:
                print(f"⚠️  Location '{prospect['location']}' may not be in Canada")
        
        # Performance logging
        print(f"📊 Search Performance:")
        print(f"   Response Time: {response_time:.2f}s")
        print(f"   Results: {len(prospects)}")
        print(f"   Rate: {len(prospects)/response_time:.1f} results/second")
        
        return prospects

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
        """Test real contact reveal API with actual prospect data
        
        This test:
        1. Searches for prospects
        2. Attempts to reveal contact info for one
        3. Validates response structure and data quality
        """
        # First get some prospects
        search_criteria = SearchCriteria(title="Heavy Equipment Mechanic", location="Canada", limit=5)
        search_response = await real_client.search_prospects(search_criteria.dict())
        
        assert search_response.success is True, "Search failed"
        prospects = search_response.data["prospects"]
        assert len(prospects) > 0, "No prospects found for reveal test"
        
        # Try to reveal first prospect
        prospect = prospects[0]
        prospect_uid = prospect["uid"]
        
        start_time = time.time()
        reveal_response = await real_client.reveal_contact(prospect_uid)
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
            print(f"   Prospect: {prospect.get('current_title', 'Unknown')} at {prospect.get('current_company', 'Unknown')}")
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
            requests.append(real_client.search_prospects(search_criteria.dict()))
        
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
            
            response = await real_client.search_prospects(search_criteria.dict())
            
            if response.success:
                prospects = response.data["prospects"]
                location_results[location] = len(prospects)
                
                # Validate location relevance for first few results
                for prospect in prospects[:3]:
                    prospect_location = prospect.get("location", "").lower()
                    city = location.split(",")[0].lower()
                    
                    if city not in prospect_location:
                        print(f"⚠️  Location mismatch: searched '{location}', got '{prospect['location']}'")
            
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
            
            response = await real_client.search_prospects(search_criteria.dict())
            
            if not response.success:
                print(f"❌ Search failed for '{search_title}': {response.error}")
                continue
            
            prospects = response.data["prospects"]
            if len(prospects) == 0:
                print(f"⚠️  No results for '{search_title}'")
                continue
            
            # Analyze title relevance
            relevant_count = 0
            for prospect in prospects:
                actual_title = prospect.get("current_title", "").lower()
                
                # Check if any expected keywords are in the actual title
                matches = [kw for kw in expected_keywords if kw in actual_title]
                if matches:
                    relevant_count += 1
                else:
                    print(f"   Less relevant: '{prospect['current_title']}'")
            
            relevance_score = (relevant_count / len(prospects)) * 100
            print(f"🎯 Title Relevance for '{search_title}':")
            print(f"   Results: {len(prospects)}")
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