"""
Integration tests for SignalHire Agent Credit Management workflow

These tests MUST FAIL initially (RED phase) before implementing the enhanced API-first services.
Tests verify comprehensive credit management, usage tracking, and daily limit handling.
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch, call

from src.services.signalhire_client import SignalHireClient, APIResponse


class TestCreditManagementWorkflow:
    """Test credit management and daily usage tracking integration"""

    @pytest.fixture
    def mock_client_with_credits(self):
        """Mock SignalHire client with detailed credit management"""
        client = AsyncMock(spec=SignalHireClient)
        
        # Track credits internally for realistic simulation
        self._credits_remaining = 100
        self._daily_used = 0
        self._daily_limit = 100
        self._last_reset = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        async def mock_check_credits():
            return APIResponse(
                success=True,
                data={
                    "credits": self._credits_remaining,
                    "daily_limit": self._daily_limit,
                    "used_today": self._daily_used,
                    "reset_time": (self._last_reset + timedelta(days=1)).isoformat(),
                    "reset_in_seconds": int((self._last_reset + timedelta(days=1) - datetime.now(timezone.utc)).total_seconds())
                },
                credits_remaining=self._credits_remaining
            )
        
        async def mock_reveal_contact(uid):
            if self._daily_used >= self._daily_limit:
                return APIResponse(
                    success=False,
                    error="Daily reveal limit exceeded",
                    status_code=429,
                    credits_used=0,
                    credits_remaining=self._credits_remaining
                )
            
            # Consume credit
            self._daily_used += 1
            if self._credits_remaining > 0:
                self._credits_remaining -= 1
            
            return APIResponse(
                success=True,
                data={
                    "prospect_uid": uid,
                    "email": f"contact{self._daily_used}@example.com",
                    "phone": f"+1-555-{self._daily_used:04d}",
                    "linkedin_url": f"https://linkedin.com/in/contact{self._daily_used}"
                },
                credits_used=1,
                credits_remaining=self._credits_remaining
            )
        
        async def mock_batch_reveal_contacts(uids):
            responses = []
            for uid in uids:
                response = await mock_reveal_contact(uid)
                responses.append(response)
                if not response.success:
                    break  # Stop on first failure (rate limit)
            return responses
        
        client.check_credits = mock_check_credits
        client.reveal_contact = mock_reveal_contact
        client.batch_reveal_contacts = mock_batch_reveal_contacts
        
        # Store test state for assertions
        client._test_credits_remaining = lambda: self._credits_remaining
        client._test_daily_used = lambda: self._daily_used
        client._test_daily_limit = lambda: self._daily_limit
        
        return client

    @pytest.mark.asyncio
    async def test_initial_credit_check(self, mock_client_with_credits):
        """Test initial credit status check and data structure
        
        Verifies:
        - Credit check API response structure
        - Daily usage tracking
        - Reset time calculation
        """
        response = await mock_client_with_credits.check_credits()
        
        # Verify response structure
        assert response.success is True
        assert response.data is not None
        assert "credits" in response.data
        assert "daily_limit" in response.data
        assert "used_today" in response.data
        assert "reset_time" in response.data
        assert "reset_in_seconds" in response.data
        
        # Verify initial values
        assert response.data["credits"] == 100
        assert response.data["daily_limit"] == 100
        assert response.data["used_today"] == 0
        assert response.data["reset_in_seconds"] > 0
        
        # Verify reset time format
        reset_time = response.data["reset_time"]
        assert reset_time.endswith("T00:00:00+00:00") or reset_time.endswith("Z")

    @pytest.mark.asyncio
    async def test_credit_consumption_tracking(self, mock_client_with_credits):
        """Test that credit consumption is properly tracked
        
        Verifies:
        - Credits decrease with each reveal
        - Daily usage increases correctly
        - Remaining credits are accurate
        """
        # Initial state
        initial_response = await mock_client_with_credits.check_credits()
        initial_credits = initial_response.data["credits"]
        initial_used = initial_response.data["used_today"]
        
        # Perform single reveal
        reveal_response = await mock_client_with_credits.reveal_contact("test_uid_1")
        
        assert reveal_response.success is True
        assert reveal_response.credits_used == 1
        assert reveal_response.credits_remaining == initial_credits - 1
        
        # Check updated credit status
        updated_response = await mock_client_with_credits.check_credits()
        assert updated_response.data["credits"] == initial_credits - 1
        assert updated_response.data["used_today"] == initial_used + 1
        
        # Verify internal tracking matches API responses
        assert mock_client_with_credits._test_credits_remaining() == initial_credits - 1
        assert mock_client_with_credits._test_daily_used() == initial_used + 1

    @pytest.mark.asyncio
    async def test_batch_credit_consumption(self, mock_client_with_credits):
        """Test credit consumption in batch operations
        
        Verifies:
        - Batch operations consume correct number of credits
        - Individual reveal tracking within batch
        - Accurate credit counting for mixed success/failure
        """
        initial_response = await mock_client_with_credits.check_credits()
        initial_credits = initial_response.data["credits"]
        
        # Perform batch reveal of 5 contacts
        uids = [f"batch_uid_{i}" for i in range(5)]
        batch_responses = await mock_client_with_credits.batch_reveal_contacts(uids)
        
        # Verify all succeeded
        assert len(batch_responses) == 5
        assert all(r.success for r in batch_responses)
        
        # Verify credit consumption
        total_credits_used = sum(r.credits_used for r in batch_responses)
        assert total_credits_used == 5
        
        # Verify final credits remaining
        last_response = batch_responses[-1]
        assert last_response.credits_remaining == initial_credits - 5
        
        # Verify credit status
        final_response = await mock_client_with_credits.check_credits()
        assert final_response.data["credits"] == initial_credits - 5
        assert final_response.data["used_today"] == 5

    @pytest.mark.asyncio
    async def test_daily_limit_enforcement(self, mock_client_with_credits):
        """Test daily limit enforcement and rate limiting
        
        Verifies:
        - Daily limit is enforced
        - Proper error response when limit exceeded
        - No credit consumption on failed attempts due to limits
        """
        # Set up scenario where we're near the daily limit
        # Use internal test methods to simulate this state
        client = mock_client_with_credits
        
        # Manually set daily usage to near limit for testing
        client._daily_used = 98
        
        # Should succeed - 2 reveals remaining
        reveal_response_1 = await client.reveal_contact("near_limit_1")
        assert reveal_response_1.success is True
        assert client._test_daily_used() == 99
        
        reveal_response_2 = await client.reveal_contact("near_limit_2") 
        assert reveal_response_2.success is True
        assert client._test_daily_used() == 100
        
        # Should fail - daily limit reached
        reveal_response_3 = await client.reveal_contact("over_limit")
        assert reveal_response_3.success is False
        assert "Daily reveal limit exceeded" in reveal_response_3.error
        assert reveal_response_3.status_code == 429
        assert reveal_response_3.credits_used == 0  # No credits consumed on limit failure
        assert client._test_daily_used() == 100  # Usage doesn't increase beyond limit

    @pytest.mark.asyncio
    async def test_batch_operation_limit_enforcement(self, mock_client_with_credits):
        """Test daily limit enforcement in batch operations
        
        Verifies:
        - Batch operations stop at daily limit
        - Partial batch completion when limit reached
        - Correct credit accounting for partial batches
        """
        client = mock_client_with_credits
        
        # Set daily usage to 97 (3 remaining)
        client._daily_used = 97
        
        # Attempt batch reveal of 5 (should only complete 3)
        uids = [f"batch_limit_uid_{i}" for i in range(5)]
        batch_responses = await client.batch_reveal_contacts(uids)
        
        # Should have 4 responses: 3 successes, 1 failure
        assert len(batch_responses) == 4
        
        successful_responses = [r for r in batch_responses if r.success]
        failed_responses = [r for r in batch_responses if not r.success]
        
        assert len(successful_responses) == 3
        assert len(failed_responses) == 1
        
        # Verify failure response
        failed_response = failed_responses[0]
        assert "Daily reveal limit exceeded" in failed_response.error
        assert failed_response.status_code == 429
        assert failed_response.credits_used == 0
        
        # Verify final state
        assert client._test_daily_used() == 100
        total_credits_used = sum(r.credits_used for r in batch_responses)
        assert total_credits_used == 3

    @pytest.mark.asyncio
    async def test_credit_warnings_and_thresholds(self, mock_client_with_credits):
        """Test credit warning thresholds and user notifications
        
        Verifies:
        - Warning logic at different usage levels
        - Appropriate messaging for different scenarios
        """
        client = mock_client_with_credits
        
        # Test various usage levels and expected warnings
        test_scenarios = [
            (10, False, "Low usage - no warning"),
            (50, False, "Moderate usage - no warning"), 
            (75, True, "75% usage - should warn"),
            (90, True, "90% usage - should warn"),
            (95, True, "95% usage - critical warning"),
            (100, True, "100% usage - limit reached")
        ]
        
        for daily_used, should_warn, scenario_description in test_scenarios:
            client._daily_used = daily_used
            client._credits_remaining = 100 - daily_used
            
            response = await client.check_credits()
            usage_percentage = (daily_used / client._test_daily_limit()) * 100
            
            # Warning logic simulation
            needs_warning = usage_percentage >= 75
            assert needs_warning == should_warn, f"Warning logic failed for {scenario_description}"
            
            # Verify data for warning display
            assert response.data["used_today"] == daily_used
            assert response.data["daily_limit"] == 100
            
            # Calculate remaining
            remaining = response.data["daily_limit"] - response.data["used_today"]
            assert remaining == (100 - daily_used)

    @pytest.mark.asyncio
    async def test_credit_pre_check_validation(self, mock_client_with_credits):
        """Test credit pre-check before batch operations
        
        Verifies:
        - Pre-check prevents unnecessary API calls
        - Accurate credit estimation
        - User guidance for batch size adjustment
        """
        client = mock_client_with_credits
        
        # Test scenario: 10 credits remaining, want to reveal 15
        client._daily_used = 90
        client._credits_remaining = 90
        
        credits_response = await client.check_credits()
        remaining_today = credits_response.data["daily_limit"] - credits_response.data["used_today"]
        
        # Pre-check logic
        requested_reveals = 15
        can_complete_all = remaining_today >= requested_reveals
        
        assert remaining_today == 10
        assert can_complete_all is False
        
        # Should suggest batch size adjustment
        recommended_batch_size = min(requested_reveals, remaining_today)
        assert recommended_batch_size == 10
        
        # Test successful pre-check scenario
        client._daily_used = 5  # 95 remaining
        credits_response = await client.check_credits()
        remaining_today = credits_response.data["daily_limit"] - credits_response.data["used_today"]
        
        requested_reveals = 50
        can_complete_all = remaining_today >= requested_reveals
        
        assert remaining_today == 95
        assert can_complete_all is True

    @pytest.mark.asyncio
    async def test_usage_tracking_display_format(self, mock_client_with_credits):
        """Test usage tracking display formatting and user presentation
        
        Verifies:
        - Proper formatting for CLI display
        - Progress indication
        - Time until reset
        """
        client = mock_client_with_credits
        client._daily_used = 65
        
        response = await client.check_credits()
        data = response.data
        
        # Test CLI display formatting
        used_today = data["used_today"]
        daily_limit = data["daily_limit"]
        usage_percentage = (used_today / daily_limit) * 100
        remaining = daily_limit - used_today
        
        # Format tests
        usage_display = f"{used_today}/{daily_limit}"
        percentage_display = f"{usage_percentage:.0f}%"
        remaining_display = f"{remaining} remaining"
        
        assert usage_display == "65/100"
        assert percentage_display == "65%"
        assert remaining_display == "35 remaining"
        
        # Progress bar simulation (10 segments)
        progress_segments = int((usage_percentage / 100) * 10)
        progress_bar = "█" * progress_segments + "░" * (10 - progress_segments)
        
        assert len(progress_bar) == 10
        assert progress_segments == 6  # 65% = 6.5, rounded to 6
        assert progress_bar == "██████░░░░"
        
        # Time until reset
        reset_seconds = data["reset_in_seconds"]
        hours_until_reset = reset_seconds // 3600
        minutes_until_reset = (reset_seconds % 3600) // 60
        
        assert hours_until_reset >= 0
        assert minutes_until_reset >= 0
        
        if hours_until_reset > 0:
            time_display = f"{hours_until_reset}h {minutes_until_reset}m"
        else:
            time_display = f"{minutes_until_reset}m"
        
        assert isinstance(time_display, str)
        assert ("h" in time_display or "m" in time_display)

    @pytest.mark.asyncio
    async def test_credit_error_handling(self, mock_client_with_credits):
        """Test error handling in credit management scenarios
        
        Verifies:
        - Authentication failures
        - Network errors
        - API service unavailability
        """
        client = mock_client_with_credits
        
        # Test authentication error
        async def mock_auth_error():
            return APIResponse(
                success=False,
                error="Authentication failed - invalid credentials",
                status_code=401
            )
        
        client.check_credits = mock_auth_error
        
        response = await client.check_credits()
        assert response.success is False
        assert response.status_code == 401
        assert "Authentication failed" in response.error
        
        # Test network/service error
        async def mock_service_error():
            return APIResponse(
                success=False,
                error="Service temporarily unavailable",
                status_code=503
            )
        
        client.check_credits = mock_service_error
        
        response = await client.check_credits()
        assert response.success is False
        assert response.status_code == 503
        assert "Service temporarily unavailable" in response.error

    @pytest.mark.asyncio
    async def test_concurrent_credit_operations(self, mock_client_with_credits):
        """Test concurrent credit operations and consistency
        
        Verifies:
        - Concurrent reveal operations
        - Credit consistency under concurrent load
        - Race condition handling
        """
        client = mock_client_with_credits
        
        # Set initial state
        client._daily_used = 95  # Near limit for testing
        
        # Create concurrent reveal tasks
        async def reveal_with_id(task_id):
            return await client.reveal_contact(f"concurrent_uid_{task_id}")
        
        # Launch 10 concurrent reveals (should only allow 5)
        tasks = [reveal_with_id(i) for i in range(10)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and check responses
        valid_responses = [r for r in responses if isinstance(r, APIResponse)]
        successful = [r for r in valid_responses if r.success]
        failed = [r for r in valid_responses if not r.success]
        
        # Should have stopped at daily limit
        assert len(successful) <= 5  # At most 5 (from 95 to 100)
        assert len(failed) >= 0  # Failed attempts when limit reached
        
        # Verify final state doesn't exceed limit
        assert client._test_daily_used() == 100
        
        # Verify credit consistency
        final_response = await client.check_credits()
        assert final_response.data["used_today"] == 100

    @pytest.mark.asyncio
    async def test_credit_reset_simulation(self, mock_client_with_credits):
        """Test daily credit reset behavior simulation
        
        Verifies:
        - Reset time calculation
        - Usage reset logic
        - Next day preparation
        """
        client = mock_client_with_credits
        
        # Set to end of day scenario
        client._daily_used = 100
        
        response = await client.check_credits()
        reset_seconds = response.data["reset_in_seconds"]
        
        # Should be less than 24 hours
        assert 0 <= reset_seconds <= 86400
        
        # Simulate reset (would happen in real system)
        # This is testing the reset logic, not implementing actual time-based reset
        def simulate_daily_reset():
            client._daily_used = 0
            client._last_reset = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        simulate_daily_reset()
        
        # After reset, should be able to reveal again
        reset_response = await client.reveal_contact("post_reset_uid")
        assert reset_response.success is True
        assert client._test_daily_used() == 1
        
        # Check status after reset
        post_reset_status = await client.check_credits()
        assert post_reset_status.data["used_today"] == 1
        assert post_reset_status.data["daily_limit"] == 100