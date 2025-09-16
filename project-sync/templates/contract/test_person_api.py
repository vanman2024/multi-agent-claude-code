"""
Contract tests for SignalHire Person API with callback handling

These tests MUST FAIL initially (RED phase) before implementing the person API client.
Tests verify the contract with SignalHire's Person API including asynchronous callbacks.
"""

import pytest
import httpx
from unittest.mock import patch, AsyncMock, MagicMock
from src.models.prospect import Prospect
from src.models.contact_info import ContactInfo
from src.services.signalhire_client import SignalHireClient
from src.lib.callback_server import CallbackServer


class TestPersonAPIContract:
    """Test contract compliance with SignalHire Person API"""

    @pytest.fixture
    def api_client(self):
        """Create SignalHire client for testing"""
        return SignalHireClient(api_key="test-api-key-12345")

    @pytest.fixture
    def callback_server(self):
        """Create callback server for testing"""
        return CallbackServer(host="localhost", port=8080)

    @pytest.fixture
    def sample_prospects(self):
        """Sample prospects for reveal testing"""
        return [
            Prospect(
                uid="prospect123456789012345678901234",
                full_name="John Doe",
                current_title="Senior Software Engineer",
                current_company="TechCorp Inc"
            ),
            Prospect(
                uid="prospect567890123456789012345678",
                full_name="Jane Smith", 
                current_title="Product Manager",
                current_company="InnovateCorp"
            )
        ]

    @pytest.fixture
    def mock_person_api_response(self):
        """Mock response from Person API request"""
        return {
            "operationId": "reveal_op_abc123def456ghi789",
            "status": "ACCEPTED",
            "message": "Person reveal request accepted. Results will be sent to callback URL."
        }

    @pytest.fixture
    def mock_callback_data(self):
        """Mock callback data received from SignalHire"""
        return {
            "operationId": "reveal_op_abc123def456ghi789",
            "status": "COMPLETED",
            "results": [
                {
                    "uid": "prospect123456789012345678901234",
                    "status": "SUCCESS",
                    "credits": 1,
                    "contacts": [
                        {
                            "type": "EMAIL_WORK",
                            "value": "john.doe@techcorp.com",
                            "confirmed": True
                        },
                        {
                            "type": "PHONE_WORK", 
                            "value": "+1-555-123-4567",
                            "confirmed": False
                        }
                    ]
                },
                {
                    "uid": "prospect567890123456789012345678",
                    "status": "FAILED",
                    "credits": 0,
                    "error": "Contact information not available"
                }
            ]
        }

    @pytest.mark.contract
    async def test_person_reveal_request_format(self, api_client, sample_prospects):
        """Test that person reveal requests are formatted correctly"""
        
        callback_url = "http://localhost:8080/callback"
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "operationId": "test_op_123",
                "status": "ACCEPTED",
                "message": "Request accepted"
            }
            
            await api_client.reveal_contacts(sample_prospects, callback_url)
            
            # Verify request format
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert call_args[0][1] == "/api/v1/person"
            
            # Check headers
            assert call_args[1]["headers"]["apikey"] == "test-api-key-12345"
            assert call_args[1]["headers"]["Content-Type"] == "application/json"
            
            # Check request body
            request_body = call_args[1]["json"]
            assert "uids" in request_body
            assert "callbackUrl" in request_body
            assert request_body["callbackUrl"] == callback_url
            assert len(request_body["uids"]) == 2
            assert "prospect123456789012345678901234" in request_body["uids"]
            assert "prospect567890123456789012345678" in request_body["uids"]

    @pytest.mark.contract
    async def test_person_api_batch_size_limit(self, api_client):
        """Test that Person API respects 100 element batch size limit"""
        
        # Create 101 prospects (exceeds limit)
        prospects = [
            Prospect(
                uid=f"prospect{i:032d}",
                full_name=f"Person {i}",
                current_title="Engineer"
            )
            for i in range(101)
        ]
        
        callback_url = "http://localhost:8080/callback"
        
        with pytest.raises(ValueError, match="Maximum 100 prospects per reveal request"):
            await api_client.reveal_contacts(prospects, callback_url)

    @pytest.mark.contract
    async def test_person_api_response_parsing(self, api_client, sample_prospects, mock_person_api_response):
        """Test parsing of Person API response"""
        
        callback_url = "http://localhost:8080/callback"
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_person_api_response
            
            result = await api_client.reveal_contacts(sample_prospects, callback_url)
            
            # Verify response structure
            assert hasattr(result, 'operation_id')
            assert hasattr(result, 'status')
            assert hasattr(result, 'message')
            
            assert result.operation_id == "reveal_op_abc123def456ghi789"
            assert result.status == "ACCEPTED"
            assert "callback URL" in result.message

    @pytest.mark.contract
    async def test_callback_server_setup(self, callback_server):
        """Test callback server initialization and endpoint setup"""
        
        # Verify server configuration
        assert callback_server.host == "localhost"
        assert callback_server.port == 8080
        assert hasattr(callback_server, 'app')
        assert hasattr(callback_server, 'start')
        assert hasattr(callback_server, 'stop')
        
        # Verify callback endpoint exists
        assert hasattr(callback_server, 'handle_callback')

    @pytest.mark.contract
    async def test_callback_data_processing(self, callback_server, mock_callback_data):
        """Test processing of callback data from SignalHire"""
        
        # Mock the callback handler
        with patch.object(callback_server, 'process_callback_data') as mock_process:
            mock_process.return_value = True
            
            # Simulate receiving callback data
            result = await callback_server.handle_callback(mock_callback_data)
            
            # Verify callback was processed
            mock_process.assert_called_once_with(mock_callback_data)
            assert result is True

    @pytest.mark.contract
    async def test_callback_data_validation(self, callback_server):
        """Test validation of callback data structure"""
        
        # Test valid callback data
        valid_data = {
            "operationId": "test_op_123",
            "status": "COMPLETED",
            "results": []
        }
        
        assert callback_server.validate_callback_data(valid_data) is True
        
        # Test invalid callback data
        invalid_data = {
            "operationId": "test_op_123"
            # Missing required fields
        }
        
        assert callback_server.validate_callback_data(invalid_data) is False

    @pytest.mark.contract
    async def test_contact_info_extraction(self, api_client, mock_callback_data):
        """Test extraction of contact information from callback results"""
        
        contacts = api_client.extract_contacts_from_callback(mock_callback_data)
        
        # Verify contact data structure
        assert len(contacts) == 1  # Only successful result
        
        contact = contacts[0]
        assert isinstance(contact, ContactInfo)
        assert contact.prospect_uid == "prospect123456789012345678901234"
        assert contact.email_work == "john.doe@techcorp.com"
        assert contact.phone_work == "+1-555-123-4567"
        assert contact.email_confirmed is True
        assert contact.phone_confirmed is False

    @pytest.mark.contract
    async def test_callback_timeout_handling(self, api_client, callback_server):
        """Test handling of callback timeouts"""
        
        operation_id = "test_op_timeout_123"
        timeout_seconds = 300  # 5 minutes
        
        # Start waiting for callback
        with patch.object(callback_server, 'wait_for_callback') as mock_wait:
            mock_wait.return_value = None  # Timeout
            
            result = await callback_server.wait_for_operation(operation_id, timeout_seconds)
            
            # Verify timeout handling
            assert result is None
            mock_wait.assert_called_once_with(operation_id, timeout_seconds)

    @pytest.mark.contract
    async def test_callback_error_handling(self, callback_server):
        """Test handling of error callbacks from SignalHire"""
        
        error_callback_data = {
            "operationId": "test_op_error_123",
            "status": "FAILED",
            "error": "Insufficient credits",
            "results": []
        }
        
        with patch.object(callback_server, 'handle_error_callback') as mock_error:
            mock_error.return_value = True
            
            result = await callback_server.handle_callback(error_callback_data)
            
            # Verify error handling
            mock_error.assert_called_once()
            assert result is True

    @pytest.mark.contract
    async def test_concurrent_callback_handling(self, callback_server):
        """Test handling of multiple concurrent callbacks"""
        
        # Simulate multiple operations running concurrently
        operation_ids = ["op_1", "op_2", "op_3"]
        
        for op_id in operation_ids:
            callback_data = {
                "operationId": op_id,
                "status": "COMPLETED", 
                "results": []
            }
            
            with patch.object(callback_server, 'store_callback_result') as mock_store:
                mock_store.return_value = True
                
                await callback_server.handle_callback(callback_data)
                mock_store.assert_called_once_with(op_id, callback_data)

    @pytest.mark.contract
    async def test_person_api_rate_limiting(self, api_client, sample_prospects):
        """Test rate limiting compliance (600 elements per minute)"""
        
        callback_url = "http://localhost:8080/callback"
        
        # Mock rate limiter
        with patch.object(api_client, 'rate_limiter') as mock_limiter:
            mock_limiter.check_rate_limit.return_value = True
            
            with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
                mock_request.return_value = {"operationId": "test", "status": "ACCEPTED"}
                
                await api_client.reveal_contacts(sample_prospects, callback_url)
                
                # Verify rate limiting was checked
                mock_limiter.check_rate_limit.assert_called_once()

    @pytest.mark.contract
    async def test_person_api_authentication_error(self, api_client, sample_prospects):
        """Test authentication error handling"""
        
        callback_url = "http://localhost:8080/callback"
        
        with patch.object(api_client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.HTTPStatusError(
                "Unauthorized",
                request=httpx.Request("POST", "http://test.com"),
                response=httpx.Response(401)
            )
            
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.reveal_contacts(sample_prospects, callback_url)
            assert exc_info.value.response.status_code == 401

# This test file MUST initially fail because the implementation doesn't exist yet.
# This is the RED phase of TDD - tests fail first, then we implement to make them pass.
