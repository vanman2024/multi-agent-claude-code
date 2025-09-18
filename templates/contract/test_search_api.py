"""
Contract tests for SignalHire Search API

These tests MUST FAIL initially (RED phase) before implementing the search client.
Tests verify the contract with SignalHire's Search API as documented.
"""

import pytest
import httpx
from unittest.mock import patch, AsyncMock
from src.models.search_criteria import SearchCriteria
from src.models.prospect import Prospect
from src.services.signalhire_client import SignalHireClient


class TestSearchAPIContract:
    """Test contract compliance with SignalHire Search API"""

    @pytest.fixture
    def api_client(self):
        """Create SignalHire client for testing"""
        return SignalHireClient(api_key="test-api-key-12345")

    @pytest.fixture
    def basic_search_criteria(self):
        """Basic search criteria for testing"""
        return SearchCriteria(
            current_title="Software Engineer",
            location="San Francisco, California, United States",
            size=10
        )

    @pytest.fixture
    def mock_search_response(self):
        """Mock response from SignalHire Search API"""
        return {
            "scrollId": "abc123def456ghi789",
            "totalCount": 156,
            "data": [
                {
                    "uid": "prospect123456789012345678901234",
                    "fullName": "John Doe",
                    "location": "San Francisco, CA",
                    "currentTitle": "Senior Software Engineer",
                    "currentCompany": "TechCorp Inc",
                    "skills": ["Python", "JavaScript", "React"],
                    "experience": [
                        {
                            "company": "TechCorp Inc",
                            "title": "Senior Software Engineer",
                            "startDate": "2022-01-01",
                            "endDate": None,
                            "description": "Lead developer for web applications"
                        }
                    ],
                    "education": [
                        {
                            "institution": "UC Berkeley",
                            "degree": "Bachelor of Science",
                            "field": "Computer Science",
                            "startDate": "2018-09-01",
                            "endDate": "2022-05-01"
                        }
                    ],
                    "openToWork": True
                }
            ]
        }

    @pytest.mark.contract
    async def test_search_request_format(self, api_client, basic_search_criteria):
        """Test that search requests are formatted correctly for SignalHire API"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"scrollId": "test123", "totalCount": 0, "data": []}
            
            await api_client.search(basic_search_criteria)
            
            # Verify request was made with correct parameters
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Check endpoint
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/api/v1/search"
            
            # Check headers
            assert call_args[1]["headers"]["apikey"] == "test-api-key-12345"
            assert call_args[1]["headers"]["Content-Type"] == "application/json"
            
            # Check request body structure
            request_body = call_args[1]["json"]
            assert "currentTitle" in request_body
            assert "location" in request_body
            assert "size" in request_body
            assert request_body["currentTitle"] == "Software Engineer"
            assert request_body["location"] == "San Francisco, California, United States"
            assert request_body["size"] == 10

    @pytest.mark.contract
    async def test_search_response_parsing(self, api_client, basic_search_criteria, mock_search_response):
        """Test that search responses are parsed correctly"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_search_response
            
            result = await api_client.search(basic_search_criteria)
            
            # Verify response structure
            assert hasattr(result, 'scroll_id')
            assert hasattr(result, 'total_count')
            assert hasattr(result, 'prospects')
            
            # Verify data types
            assert isinstance(result.scroll_id, str)
            assert isinstance(result.total_count, int)
            assert isinstance(result.prospects, list)
            
            # Verify prospect data
            assert len(result.prospects) == 1
            prospect = result.prospects[0]
            assert isinstance(prospect, Prospect)
            assert prospect.uid == "prospect123456789012345678901234"
            assert prospect.full_name == "John Doe"
            assert prospect.current_title == "Senior Software Engineer"
            assert prospect.current_company == "TechCorp Inc"

    @pytest.mark.contract
    async def test_search_with_boolean_queries(self, api_client):
        """Test boolean query support in search criteria"""
        
        criteria = SearchCriteria(
            current_title="(Senior OR Lead) AND Engineer",
            current_company="NOT (Facebook OR Meta)",
            keywords="Python AND (Django OR Flask)",
            size=25
        )
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"scrollId": "test123", "totalCount": 0, "data": []}
            
            await api_client.search(criteria)
            
            request_body = mock_request.call_args[1]["json"]
            assert request_body["currentTitle"] == "(Senior OR Lead) AND Engineer"
            assert request_body["currentCompany"] == "NOT (Facebook OR Meta)"
            assert request_body["keywords"] == "Python AND (Django OR Flask)"

    @pytest.mark.contract
    async def test_search_with_experience_filters(self, api_client):
        """Test experience year filters in search"""
        
        criteria = SearchCriteria(
            current_title="Product Manager",
            years_experience_from=3,
            years_experience_to=10,
            size=15
        )
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"scrollId": "test123", "totalCount": 0, "data": []}
            
            await api_client.search(criteria)
            
            request_body = mock_request.call_args[1]["json"]
            assert request_body["yearsExperienceFrom"] == 3
            assert request_body["yearsExperienceTo"] == 10

    @pytest.mark.contract
    async def test_search_pagination_with_scroll_id(self, api_client):
        """Test pagination using scrollId parameter"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"scrollId": "next123", "totalCount": 156, "data": []}
            
            await api_client.continue_search(scroll_id="previous123")
            
            # Verify pagination request
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/api/v1/search"
            
            request_body = call_args[1]["json"]
            assert request_body["scrollId"] == "previous123"

    @pytest.mark.contract
    async def test_search_error_handling(self, api_client, basic_search_criteria):
        """Test error handling for various API response codes"""
        
        # Test 401 Unauthorized
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "Unauthorized", 
                request=httpx.Request("POST", "http://test.com"),
                response=httpx.Response(401)
            )
            
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.search(basic_search_criteria)
            assert exc_info.value.response.status_code == 401

        # Test 429 Rate Limit
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "Rate limit exceeded",
                request=httpx.Request("POST", "http://test.com"), 
                response=httpx.Response(429)
            )
            
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.search(basic_search_criteria)
            assert exc_info.value.response.status_code == 429

    @pytest.mark.contract
    async def test_search_validation_errors(self, api_client):
        """Test validation of search criteria before API call"""
        
        # Test empty search criteria (should fail validation)
        invalid_criteria = SearchCriteria(size=10)  # No search fields provided
        
        with pytest.raises(ValueError, match="At least one search field must be provided"):
            await api_client.search(invalid_criteria)

        # Test invalid size
        invalid_criteria = SearchCriteria(
            current_title="Engineer",
            size=150  # Exceeds maximum of 100
        )
        
        with pytest.raises(ValueError, match="size must be between 1 and 100"):
            await api_client.search(invalid_criteria)

    @pytest.mark.contract
    async def test_search_timeout_handling(self, api_client, basic_search_criteria):
        """Test timeout handling for search requests"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Request timeout")
            
            with pytest.raises(httpx.TimeoutException):
                await api_client.search(basic_search_criteria)

# This test file MUST initially fail with ImportError and other errors
# because the implementation doesn't exist yet. This is the RED phase of TDD.
