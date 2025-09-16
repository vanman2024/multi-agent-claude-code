"""
API Contract Tests
==================

Purpose: Verify that API endpoints adhere to their documented contracts.
These tests validate request/response formats, data types, and business rules.

Test Strategy:
  - RED phase: Tests should fail initially before implementation
  - GREEN phase: Implement API client to make tests pass
  - REFACTOR phase: Optimize implementation while keeping tests green

Run with:
  pytest tests/contract/ -v
  pytest tests/contract/ -m contract

Notes:
  - Uses mocked responses to avoid external API calls
  - Validates both successful and error scenarios
  - Ensures backward compatibility when API changes
"""

import pytest
import httpx
from unittest.mock import patch, AsyncMock
from src.services.api_client import APIClient
from src.models.credit_usage import CreditUsage, CreditBalance


class TestUsageAPIContract:
    """Test contract compliance with API Service Usage API"""

    @pytest.fixture
    def api_client(self):
        """Create API Service client for testing"""
        return APIClient(api_key="test-api-key-12345")

    @pytest.fixture
    def mock_credits_response(self):
        """Mock response from Usage API"""
        return {
            "credits": 1247,
            "creditsUsed": 153,
            "creditsTotal": 1400,
            "resetDate": "2025-10-01T00:00:00Z",
            "planType": "Professional",
            "usageDetails": {
                "personReveals": 145,
                "searches": 8,
                "exports": 12
            }
        }

    @pytest.fixture
    def mock_usage_history_response(self):
        """Mock response from Credits usage history API"""
        return {
            "period": "last30days",
            "totalCreditsUsed": 423,
            "dailyUsage": [
                {
                    "date": "2025-09-11",
                    "credits": 25,
                    "operations": {
                        "searches": 2,
                        "reveals": 20,
                        "exports": 3
                    }
                },
                {
                    "date": "2025-09-10", 
                    "credits": 18,
                    "operations": {
                        "searches": 1,
                        "reveals": 15,
                        "exports": 2
                    }
                }
            ]
        }

    @pytest.mark.contract
    async def test_usage_balance_request_format(self, api_client):
        """Test that credits balance requests are formatted correctly"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "credits": 1000,
                "creditsUsed": 100,
                "creditsTotal": 1100
            }
            
            await api_client.get_credits_balance()
            
            # Verify request format
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/api/v1/credits"
            
            # Check headers
            assert call_args[1]["headers"]["apikey"] == "test-api-key-12345"
            assert call_args[1]["headers"]["Content-Type"] == "application/json"

    @pytest.mark.contract
    async def test_usage_balance_response_parsing(self, api_client, mock_credits_response):
        """Test parsing of credits balance response"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_credits_response
            
            result = await api_client.get_credits_balance()
            
            # Verify response structure
            assert isinstance(result, CreditBalance)
            assert result.available_credits == 1247
            assert result.used_credits == 153
            assert result.total_credits == 1400
            assert result.plan_type == "Professional"
            assert result.reset_date == "2025-10-01T00:00:00Z"
            
            # Verify usage breakdown
            assert result.person_reveals == 145
            assert result.searches == 8
            assert result.exports == 12

    @pytest.mark.contract
    async def test_usage_usage_history_request(self, api_client):
        """Test credits usage history request format"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"period": "last30days", "totalCreditsUsed": 0, "dailyUsage": []}
            
            await api_client.get_credits_usage(period="last30days")
            
            # Verify request format
            call_args = mock_request.call_args
            assert call_args[0][0] == "GET"
            assert call_args[0][1] == "/api/v1/credits/usage"
            
            # Check query parameters
            assert call_args[1]["params"]["period"] == "last30days"

    @pytest.mark.contract
    async def test_usage_usage_history_response_parsing(self, api_client, mock_usage_history_response):
        """Test parsing of credits usage history response"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_usage_history_response
            
            result = await api_client.get_credits_usage(period="last30days")
            
            # Verify response structure
            assert isinstance(result, CreditUsage)
            assert result.period == "last30days"
            assert result.total_credits_used == 423
            assert len(result.daily_usage) == 2
            
            # Verify daily usage data
            day1 = result.daily_usage[0]
            assert day1.date == "2025-09-11"
            assert day1.credits_used == 25
            assert day1.searches == 2
            assert day1.reveals == 20
            assert day1.exports == 3

    @pytest.mark.contract
    async def test_usage_low_balance_warning(self, api_client):
        """Test detection of low usage balance"""
        
        low_credits_response = {
            "credits": 25,  # Low balance
            "creditsUsed": 975,
            "creditsTotal": 1000,
            "resetDate": "2025-10-01T00:00:00Z",
            "planType": "Basic"
        }
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = low_credits_response
            
            result = await api_client.get_credits_balance()
            
            # Verify low balance detection
            assert result.is_low_balance(threshold=50) is True
            assert result.is_low_balance(threshold=20) is False

    @pytest.mark.contract
    async def test_usage_exhausted_detection(self, api_client):
        """Test detection of exhausted credits"""
        
        no_credits_response = {
            "credits": 0,
            "creditsUsed": 1000,
            "creditsTotal": 1000,
            "resetDate": "2025-10-01T00:00:00Z",
            "planType": "Basic"
        }
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = no_credits_response
            
            result = await api_client.get_credits_balance()
            
            # Verify exhaustion detection
            assert result.is_exhausted() is True
            assert result.available_credits == 0

    @pytest.mark.contract
    async def test_usage_usage_estimation(self, api_client):
        """Test estimation of credit usage for operations"""
        
        # Test search operation estimation
        search_estimate = api_client.estimate_search_credits(
            title="Software Engineer",
            location="San Francisco",
            size=50
        )
        assert search_estimate == 1  # Searches typically cost 1 credit
        
        # Test reveal operation estimation
        reveal_estimate = api_client.estimate_reveal_credits(Result_count=25)
        assert reveal_estimate == 25  # 1 credit per Result reveal
        
        # Test batch reveal estimation  
        batch_estimate = api_client.estimate_batch_reveal_credits(Result_count=150)
        assert batch_estimate == 150

    @pytest.mark.contract
    async def test_usage_insufficient_error(self, api_client):
        """Test handling of insufficient credits error"""
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "Insufficient credits",
                request=httpx.Request("POST", "http://test.com"),
                response=httpx.Response(402)  # Payment Required
            )
            
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.get_credits_balance()
            assert exc_info.value.response.status_code == 402

    @pytest.mark.contract
    async def test_usage_rate_limit_tracking(self, api_client):
        """Test tracking of credits against rate limits"""
        
        # Mock current usage
        with patch.object(api_client, 'get_credits_usage') as mock_usage:
            mock_usage.return_value = CreditUsage(
                period="today",
                total_credits_used=580,  # Close to 600/minute limit
                daily_usage=[]
            )
            
            # Check if near rate limit
            can_proceed = await api_client.check_rate_limit_headroom(requested_credits=25)
            assert can_proceed is False  # Would exceed 600/minute
            
            can_proceed = await api_client.check_rate_limit_headroom(requested_credits=15)
            assert can_proceed is True  # Within limit

    @pytest.mark.contract
    async def test_usage_plan_limits(self, api_client):
        """Test plan-specific credit limits and features"""
        
        # Test different plan types
        plan_configs = [
            {"planType": "Free", "creditsTotal": 100},
            {"planType": "Basic", "creditsTotal": 500}, 
            {"planType": "Professional", "creditsTotal": 2000},
            {"planType": "Enterprise", "creditsTotal": 10000}
        ]
        
        for config in plan_configs:
            with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = {
                    "credits": config["creditsTotal"],
                    "creditsUsed": 0,
                    "creditsTotal": config["creditsTotal"],
                    "planType": config["planType"],
                    "resetDate": "2025-10-01T00:00:00Z"
                }
                
                result = await api_client.get_credits_balance()
                assert result.total_credits == config["creditsTotal"]
                assert result.plan_type == config["planType"]

    @pytest.mark.contract
    async def test_usage_reset_cycle_tracking(self, api_client):
        """Test tracking of credit reset cycles"""
        
        reset_response = {
            "credits": 1500,
            "creditsUsed": 0,  # Just reset
            "creditsTotal": 1500,
            "resetDate": "2025-10-01T00:00:00Z",
            "planType": "Professional",
            "lastResetDate": "2025-09-01T00:00:00Z"
        }
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = reset_response
            
            result = await api_client.get_credits_balance()
            
            # Verify reset cycle information
            assert result.reset_date == "2025-10-01T00:00:00Z"
            assert result.used_credits == 0  # Fresh reset
            days_until_reset = result.days_until_reset()
            assert isinstance(days_until_reset, int)
            assert days_until_reset >= 0

    @pytest.mark.contract
    async def test_usage_api_error_handling(self, api_client):
        """Test error handling for credits API"""
        
        # Test network timeout
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Request timeout")
            
            with pytest.raises(httpx.TimeoutException):
                await api_client.get_credits_balance()

        # Test server error
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "Internal server error",
                request=httpx.Request("GET", "http://test.com"),
                response=httpx.Response(500)
            )
            
            with pytest.raises(httpx.HTTPStatusError):
                await api_client.get_credits_balance()

# This test file MUST initially fail because the implementation doesn't exist yet.
# This is the RED phase of TDD - tests fail first, then we implement to make them pass.
