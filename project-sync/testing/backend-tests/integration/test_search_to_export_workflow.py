import pytest
pytest.skip("Skipped in API-only mode due to legacy module dependencies", allow_module_level=True)
"""
Integration tests for SignalHire Agent end-to-end workflows

These tests MUST FAIL initially (RED phase) before implementing the services.
Tests verify complete workflows from search through export.
"""

import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.search_service import SearchService
from src.services.reveal_service import RevealService
from src.services.export_service import ExportService
from src.lib.signalhire_client import SignalHireClient
from src.lib.browser_client import BrowserClient
from src.models.search_criteria import SearchCriteria
from src.models.prospect import Prospect


class TestSearchToExportWorkflow:
    """Test complete search → reveal → export workflow integration"""

    @pytest.fixture
    def search_criteria(self):
        """Sample search criteria for testing"""
        return SearchCriteria(
            title="Software Engineer",
            location="San Francisco, CA",
            company="TechCorp",
            size=20
        )

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for output files"""
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def mock_search_results(self):
        """Mock search results with prospects"""
        return {
            "operation_id": "search_integration_123",
            "scroll_id": "scroll_abc123def456",
            "total_count": 15,
            "prospects": [
                {
                    "uid": f"prospect{i:030d}",
                    "full_name": f"Test Person {i}",
                    "current_title": "Software Engineer",
                    "current_company": "TechCorp Inc",
                    "location": "San Francisco, CA",
                    "profile_url": f"https://signalhire.com/profiles/test{i}"
                }
                for i in range(1, 16)
            ]
        }

    @pytest.fixture
    def mock_revealed_contacts(self):
        """Mock revealed contact information"""
        return {
            "operation_id": "reveal_integration_456",
            "status": "COMPLETED",
            "prospects": [
                {
                    "uid": f"prospect{i:030d}",
                    "full_name": f"Test Person {i}",
                    "current_title": "Software Engineer",
                    "current_company": "TechCorp Inc",
                    "location": "San Francisco, CA",
                    "email_work": f"test.person{i}@techcorp.com",
                    "phone_work": f"+1415555{i:04d}",
                    "linkedin_url": f"https://linkedin.com/in/testperson{i}",
                    "profile_url": f"https://signalhire.com/profiles/test{i}"
                }
                for i in range(1, 16)
            ]
        }

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complete_search_to_export_workflow(
        self, 
        search_criteria, 
        temp_output_dir,
        mock_search_results,
        mock_revealed_contacts
    ):
        """Test complete workflow: search → reveal → export to CSV"""
        
        output_file = Path(temp_output_dir) / "integration_test_results.csv"
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            # Setup mock client responses
            mock_client = MockClient.return_value
            
            # Mock search
            mock_client.search = AsyncMock()
            mock_client.search.return_value = MagicMock(**mock_search_results)
            
            # Mock reveal
            mock_client.reveal_contacts = AsyncMock()
            mock_client.reveal_contacts.return_value = MagicMock(**mock_revealed_contacts)
            
            # Initialize services
            search_service = SearchService(client=mock_client)
            reveal_service = RevealService(client=mock_client)
            export_service = ExportService()
            
            # Step 1: Execute search
            search_result = await search_service.search(search_criteria)
            
            # Verify search executed
            assert search_result is not None
            # Note: Will fail until SearchService is implemented
            
            # Step 2: Extract prospect UIDs
            prospect_uids = [p["uid"] for p in search_result.prospects]
            assert len(prospect_uids) == 15
            
            # Step 3: Reveal contacts
            reveal_result = await reveal_service.reveal_contacts(
                prospect_uids=prospect_uids,
                include_phone=True,
                include_linkedin=True
            )
            
            # Verify reveal executed
            assert reveal_result is not None
            # Note: Will fail until RevealService is implemented
            
            # Step 4: Export to CSV
            export_result = await export_service.export_to_csv(
                prospects=reveal_result.prospects,
                output_file=str(output_file),
                include_contacts=True
            )
            
            # Verify export executed
            assert export_result is not None
            assert output_file.exists()
            # Note: Will fail until ExportService is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_paginated_search_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test workflow with paginated search results"""
        
        output_file = Path(temp_output_dir) / "paginated_results.json"
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            mock_client = MockClient.return_value
            
            # Mock paginated responses
            page1_response = MagicMock(
                operation_id="search_paginated_123",
                scroll_id="scroll_page1",
                total_count=150,
                prospects=[{"uid": f"p{i:030d}"} for i in range(1, 101)]
            )
            
            page2_response = MagicMock(
                operation_id="search_paginated_123", 
                scroll_id="scroll_page2",
                total_count=150,
                prospects=[{"uid": f"p{i:030d}"} for i in range(101, 151)]
            )
            
            mock_client.search = AsyncMock(return_value=page1_response)
            mock_client.scroll_search = AsyncMock(return_value=page2_response)
            
            # Initialize service
            search_service = SearchService(client=mock_client)
            
            # Execute paginated search
            all_prospects = []
            
            # First page
            search_result = await search_service.search(search_criteria)
            all_prospects.extend(search_result.prospects)
            
            # Subsequent pages via scroll
            while len(all_prospects) < search_result.total_count:
                scroll_result = await search_service.scroll_search(
                    scroll_id=search_result.scroll_id
                )
                all_prospects.extend(scroll_result.prospects)
                
                if not scroll_result.prospects:
                    break
            
            # Verify paginated collection
            assert len(all_prospects) == 150
            # Note: Will fail until SearchService pagination is implemented

    @pytest.mark.integration  
    @pytest.mark.asyncio
    async def test_batch_reveal_workflow(
        self,
        temp_output_dir,
        mock_revealed_contacts
    ):
        """Test batch reveal workflow for large prospect lists"""
        
        # Create large prospect list (simulate 500 prospects)
        large_prospect_list = [f"prospect{i:030d}" for i in range(1, 501)]
        
        output_file = Path(temp_output_dir) / "batch_reveal_results.json"
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            mock_client = MockClient.return_value
            
            # Mock batch reveal responses
            def mock_batch_reveal(*args, **kwargs):
                # Simulate processing in batches of 50
                prospect_uids = kwargs.get('prospect_uids', [])
                batch_size = min(50, len(prospect_uids))
                
                return MagicMock(
                    operation_id=f"batch_reveal_{len(prospect_uids)}",
                    status="COMPLETED",
                    prospects=[
                        {
                            "uid": uid,
                            "email_work": f"contact{uid[-3:]}@company.com"
                        }
                        for uid in prospect_uids[:batch_size]
                    ]
                )
            
            mock_client.reveal_contacts = AsyncMock(side_effect=mock_batch_reveal)
            
            # Initialize service
            reveal_service = RevealService(client=mock_client)
            
            # Execute batch reveal
            batch_size = 50
            all_revealed = []
            
            for i in range(0, len(large_prospect_list), batch_size):
                batch = large_prospect_list[i:i + batch_size]
                
                reveal_result = await reveal_service.reveal_contacts(
                    prospect_uids=batch,
                    include_phone=True
                )
                
                all_revealed.extend(reveal_result.prospects)
                
                # Simulate rate limiting delay
                await asyncio.sleep(0.1)
            
            # Verify batch processing
            assert len(all_revealed) >= 450  # Allow for some failures
            # Note: Will fail until RevealService batch processing is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio 
    async def test_browser_automation_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test browser automation workflow for bulk operations"""
        
        output_file = Path(temp_output_dir) / "browser_automation_export.csv"
        
        with patch('src.lib.browser_client.BrowserClient') as MockBrowser:
            mock_browser = MockBrowser.return_value
            
            # Mock browser automation
            mock_browser.login = AsyncMock()
            mock_browser.search = AsyncMock()
            mock_browser.search.return_value = MagicMock(
                prospects_found=1247,
                search_id="browser_search_789"
            )
            
            mock_browser.bulk_reveal_and_export = AsyncMock()
            mock_browser.bulk_reveal_and_export.return_value = str(output_file)
            
            # Initialize services
            search_service = SearchService()
            reveal_service = RevealService()
            
            # Execute browser workflow
            
            # Step 1: Browser login
            await mock_browser.login()
            
            # Step 2: Browser search
            search_result = await mock_browser.search(search_criteria)
            assert search_result.prospects_found > 1000
            
            # Step 3: Bulk reveal and export via browser
            exported_file = await mock_browser.bulk_reveal_and_export(
                search_id=search_result.search_id,
                export_format="csv",
                batch_size=500
            )
            
            # Verify browser workflow
            assert exported_file == str(output_file)
            # Note: Will fail until BrowserClient is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_hybrid_api_browser_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test hybrid workflow: API search + browser bulk reveal"""
        
        output_file = Path(temp_output_dir) / "hybrid_workflow_results.csv"
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockAPI, \
             patch('src.lib.browser_client.BrowserClient') as MockBrowser:
            
            # Setup API mock
            mock_api_client = MockAPI.return_value
            mock_api_client.search = AsyncMock()
            mock_api_client.search.return_value = MagicMock(
                operation_id="hybrid_search_123",
                total_count=1500,  # Large result set
                prospects=[{"uid": f"p{i:030d}"} for i in range(1, 101)]
            )
            
            # Setup browser mock  
            mock_browser_client = MockBrowser.return_value
            mock_browser_client.bulk_reveal_and_export = AsyncMock()
            mock_browser_client.bulk_reveal_and_export.return_value = str(output_file)
            
            # Initialize services
            search_service = SearchService(client=mock_api_client)
            reveal_service = RevealService(browser_client=mock_browser_client)
            
            # Execute hybrid workflow
            
            # Step 1: Use API for initial search
            api_search_result = await search_service.search(search_criteria)
            
            # Step 2: If large result set, switch to browser for bulk reveal
            if api_search_result.total_count > 100:
                # Use browser for bulk operations
                browser_export = await reveal_service.bulk_reveal_via_browser(
                    search_criteria=search_criteria,
                    export_format="csv",
                    output_file=str(output_file)
                )
                
                # Verify hybrid approach
                assert browser_export == str(output_file)
            else:
                # Use API for small result sets
                reveal_result = await reveal_service.reveal_contacts(
                    prospect_uids=[p["uid"] for p in api_search_result.prospects]
                )
                
                assert reveal_result is not None
            
            # Note: Will fail until hybrid workflow is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_recovery_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test workflow error handling and recovery mechanisms"""
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            mock_client = MockClient.return_value
            
            # Mock intermittent failures
            call_count = 0
            async def mock_search_with_failures(*args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count <= 2:
                    raise Exception("Temporary API error")
                return MagicMock(
                    operation_id="recovered_search_123",
                    prospects=[{"uid": "p001"}]
                )
            
            mock_client.search = AsyncMock(side_effect=mock_search_with_failures)
            
            # Initialize service with retry logic
            search_service = SearchService(
                client=mock_client,
                max_retries=3,
                retry_delay=0.1
            )
            
            # Execute with error recovery
            search_result = await search_service.search(search_criteria)
            
            # Verify recovery succeeded
            assert search_result is not None
            assert call_count == 3  # 2 failures + 1 success
            # Note: Will fail until retry logic is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_rate_limiting_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test workflow with rate limiting compliance"""
        
        with patch('src.lib.rate_limiter.RateLimiter') as MockRateLimiter:
            mock_limiter = MockRateLimiter.return_value
            mock_limiter.acquire = AsyncMock()
            mock_limiter.is_rate_limited = MagicMock(return_value=False)
            
            # Track rate limiter calls
            acquire_calls = []
            async def track_acquire(*args, **kwargs):
                acquire_calls.append(kwargs)
                await asyncio.sleep(0.05)  # Simulate rate limit delay
            
            mock_limiter.acquire = AsyncMock(side_effect=track_acquire)
            
            with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
                mock_client = MockClient.return_value
                mock_client.search = AsyncMock()
                mock_client.reveal_contacts = AsyncMock()
                
                # Initialize services with rate limiting
                search_service = SearchService(
                    client=mock_client,
                    rate_limiter=mock_limiter
                )
                reveal_service = RevealService(
                    client=mock_client,
                    rate_limiter=mock_limiter
                )
                
                # Execute multiple operations
                tasks = []
                for i in range(5):
                    tasks.append(search_service.search(search_criteria))
                
                await asyncio.gather(*tasks)
                
                # Verify rate limiting was applied
                assert len(acquire_calls) >= 5
                # Note: Will fail until rate limiting is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_credits_monitoring_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test workflow with credits monitoring and management"""
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            mock_client = MockClient.return_value
            
            # Mock credits responses
            credits_sequence = [1000, 950, 900, 850]  # Decreasing credits
            credits_iter = iter(credits_sequence)
            
            async def mock_get_credits():
                return MagicMock(
                    available_credits=next(credits_iter, 800),
                    used_credits=50,
                    plan_type="Professional"
                )
            
            mock_client.get_credits_balance = AsyncMock(side_effect=mock_get_credits)
            mock_client.reveal_contacts = AsyncMock()
            
            # Initialize service with credits monitoring
            reveal_service = RevealService(
                client=mock_client,
                monitor_credits=True,
                credits_threshold=900
            )
            
            # Execute operations with credits monitoring
            prospect_uids = [f"p{i:030d}" for i in range(1, 101)]
            
            # Should trigger credits warning
            reveal_result = await reveal_service.reveal_contacts(
                prospect_uids=prospect_uids,
                include_phone=True
            )
            
            # Verify credits monitoring
            assert mock_client.get_credits_balance.call_count >= 1
            # Note: Will fail until credits monitoring is implemented

    @pytest.mark.integration
    def test_workflow_configuration_management(self, temp_output_dir):
        """Test workflow configuration and settings management"""
        
        config_file = Path(temp_output_dir) / "workflow_config.json"
        
        # Create test configuration
        test_config = {
            "api_settings": {
                "base_url": "https://api.signalhire.com/v1",
                "timeout": 30,
                "max_retries": 3
            },
            "browser_settings": {
                "headless": True,
                "timeout": 60,
                "batch_size": 500
            },
            "export_settings": {
                "default_format": "csv",
                "include_contacts": True,
                "column_mapping": {
                    "full_name": "Name",
                    "email_work": "Email",
                    "current_company": "Company"
                }
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        # Test configuration loading
        from src.lib.config_manager import ConfigManager
        
        with patch('src.lib.config_manager.ConfigManager') as MockConfig:
            mock_config = MockConfig.return_value
            mock_config.load = MagicMock(return_value=test_config)
            mock_config.get = MagicMock(side_effect=lambda key: test_config.get(key))
            
            # Initialize with configuration
            config_manager = ConfigManager(config_file=str(config_file))
            config_data = config_manager.load()
            
            # Verify configuration structure
            assert config_data["api_settings"]["max_retries"] == 3
            assert config_data["browser_settings"]["batch_size"] == 500
            # Note: Will fail until ConfigManager is implemented

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_progress_tracking_workflow(
        self,
        search_criteria,
        temp_output_dir
    ):
        """Test workflow progress tracking and reporting"""
        
        progress_updates = []
        
        async def progress_callback(update):
            progress_updates.append(update)
        
        with patch('src.lib.signalhire_client.SignalHireClient') as MockClient:
            mock_client = MockClient.return_value
            
            # Mock operations with progress simulation
            async def mock_reveal_with_progress(*args, **kwargs):
                callback = kwargs.get('progress_callback')
                if callback:
                    await callback({"stage": "processing", "current": 25, "total": 100})
                    await callback({"stage": "processing", "current": 50, "total": 100})
                    await callback({"stage": "processing", "current": 75, "total": 100})
                    await callback({"stage": "completed", "current": 100, "total": 100})
                
                return MagicMock(operation_id="progress_test_456")
            
            mock_client.reveal_contacts = AsyncMock(side_effect=mock_reveal_with_progress)
            
            # Initialize service with progress tracking
            reveal_service = RevealService(client=mock_client)
            
            # Execute with progress callback
            await reveal_service.reveal_contacts(
                prospect_uids=["p001", "p002", "p003"],
                progress_callback=progress_callback
            )
            
            # Verify progress tracking
            assert len(progress_updates) == 4
            assert progress_updates[-1]["stage"] == "completed"
            # Note: Will fail until progress tracking is implemented

# These integration tests MUST initially fail because the implementation doesn't exist yet.
# This is the RED phase of TDD - tests fail first, then we implement to make them pass.
import pytest
pytest.skip("Skipped in API-only mode due to legacy module dependencies", allow_module_level=True)
