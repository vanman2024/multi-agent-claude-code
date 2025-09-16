"""
Performance Tests
=================

Purpose: Measure and validate performance characteristics of the system.
These tests ensure the application meets performance requirements.

Run with:
  pytest tests/performance/ -v
  pytest tests/performance/ -m performance
  
  # Run with profiling:
  pytest tests/performance/ --profile

Notes:
  - Measures response times, throughput, and resource usage
  - Compares different implementation approaches
  - Identifies performance bottlenecks
"""

import pytest
pytest.skip("Skipped in API-only mode; browser mode removed", allow_module_level=True)
"""
Performance benchmarks for API vs Browser modes comparison

These tests MUST FAIL initially (RED phase) before implementing the enhanced API-first services.
Tests verify performance characteristics, response times, and throughput differences between
API-first approach and browser automation modes.
"""

import pytest
import asyncio
import time
import statistics
import psutil
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass

from src.services.api_client import APIClient, APIResponse
from src.services.browser_client import BrowserClient
from src.services.csv_exporter import CSVExporter, ExportConfig


@dataclass
class PerformanceMetrics:
    """Performance measurement results for a test scenario"""
    operation_name: str
    mode: str  # 'api' or 'browser'
    total_time: float
    avg_time_per_item: float
    min_time: float
    max_time: float
    median_time: float
    success_rate: float
    throughput_per_second: float
    memory_usage_mb: float
    cpu_usage_percent: float
    error_count: int
    items_processed: int


class TestAPICToBrowserModeComparison:
    """Performance benchmarks comparing API-first vs Browser automation modes"""

    @pytest.fixture
    def mock_api_client(self):
        """Mock API client with realistic performance characteristics"""
        client = AsyncMock(spec=APIClient)
        
        async def mock_fast_reveal(Result_id):
            # Simulate fast API response (100-500ms)
            delay = 0.1 + (hash(Result_id) % 5) * 0.08  # 100-500ms range
            await asyncio.sleep(delay)
            
            return APIResponse(
                success=True,
                data={
                    "Result_uid": Result_id,
                    "email": f"contact@example{hash(Result_id) % 1000}.com",
                    "phone": f"+1-555-{abs(hash(Result_id)) % 10000:04d}",
                    "linkedin_url": f"https://linkedin.com/in/Result{abs(hash(Result_id)) % 1000}"
                },
                credits_used=1,
                credits_remaining=99
            )
        
        async def mock_fast_search(criteria):
            # Simulate fast search response (200-800ms)
            await asyncio.sleep(0.2 + (hash(str(criteria)) % 6) * 0.1)
            
            return APIResponse(
                success=True,
                data={
                    "results": [
                        {
                            "uid": f"api_Result_{i}_{abs(hash(str(criteria))) % 1000}",
                            "full_name": f"API Person {i}",
                            "current_title": "Engineer",
                            "current_company": "TechCorp",
                            "location": "San Francisco, CA"
                        }
                        for i in range(20)
                    ]
                }
            )
        
        async def mock_check_credits():
            await asyncio.sleep(0.05)  # Very fast credit check
            return APIResponse(
                success=True,
                data={
                    "credits": 95,
                    "daily_limit": 100,
                    "used_today": 5,
                    "reset_time": "2025-09-12T00:00:00Z"
                }
            )
        
        client.reveal_contact = mock_fast_reveal
        client.search_results = mock_fast_search
        client.check_credits = mock_check_credits
        
        return client

    @pytest.fixture
    def mock_browser_client(self):
        """Mock browser client with realistic performance characteristics"""
        client = AsyncMock(spec=BrowserClient)
        
        async def mock_slow_reveal(Result_id):
            # Simulate slower browser automation (5-30 seconds)
            delay = 5 + (hash(Result_id) % 25)  # 5-30 second range
            await asyncio.sleep(delay)
            
            # Simulate 70% success rate (browser automation challenges)
            success = abs(hash(Result_id)) % 10 < 7
            
            if success:
                return {
                    "success": True,
                    "Result_uid": Result_id,
                    "email": f"browser@example{hash(Result_id) % 1000}.com",
                    "phone": f"+1-555-{abs(hash(Result_id)) % 10000:04d}",
                    "linkedin_url": f"https://linkedin.com/in/browser{abs(hash(Result_id)) % 1000}"
                }
            else:
                return {
                    "success": False,
                    "error": "Browser automation blocked by Cloudflare"
                }
        
        async def mock_slow_search(criteria):
            # Simulate slower browser search (10-45 seconds)
            await asyncio.sleep(10 + (hash(str(criteria)) % 35))
            
            # 85% success rate for searches
            success = abs(hash(str(criteria))) % 10 < 8
            
            if success:
                return {
                    "success": True,
                    "results": [
                        {
                            "uid": f"browser_Result_{i}_{abs(hash(str(criteria))) % 1000}",
                            "full_name": f"Browser Person {i}",
                            "current_title": "Engineer", 
                            "current_company": "TechCorp",
                            "location": "San Francisco, CA"
                        }
                        for i in range(50)  # Browser can get more results
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": "Search blocked by anti-bot protection"
                }
        
        client.reveal_contact = mock_slow_reveal
        client.search_results = mock_slow_search
        
        return client

    def measure_performance(self, start_time: float, end_time: float, 
                           results: List[Any], operation_name: str, mode: str) -> PerformanceMetrics:
        """Measure and calculate performance metrics"""
        total_time = end_time - start_time
        items_processed = len(results)
        successful_results = [r for r in results if getattr(r, 'success', True)]
        
        # Calculate success rate
        success_rate = len(successful_results) / max(1, items_processed) * 100
        
        # Get system resource usage
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        return PerformanceMetrics(
            operation_name=operation_name,
            mode=mode,
            total_time=total_time,
            avg_time_per_item=total_time / max(1, items_processed),
            min_time=0.1,  # Approximate minimums
            max_time=total_time,
            median_time=total_time / 2,
            success_rate=success_rate,
            throughput_per_second=items_processed / max(0.1, total_time),
            memory_usage_mb=memory_usage_mb,
            cpu_usage_percent=cpu_percent,
            error_count=items_processed - len(successful_results),
            items_processed=items_processed
        )

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_single_contact_reveal_performance_comparison(self, mock_api_client, mock_browser_client):
        """Compare performance of single contact reveals between API and browser modes"""
        test_Result_ids = [f"test_Result_{i}" for i in range(5)]
        
        # Test API Mode Performance
        api_start = time.time()
        api_results = []
        for Result_id in test_Result_ids:
            result = await mock_api_client.reveal_contact(Result_id)
            api_results.append(result)
        api_end = time.time()
        
        api_metrics = self.measure_performance(api_start, api_end, api_results, 
                                              "single_contact_reveal", "api")
        
        # Test Browser Mode Performance (simulate shorter for testing)
        browser_start = time.time()
        browser_results = []
        for Result_id in test_Result_ids[:2]:  # Test fewer for speed
            result = await mock_browser_client.reveal_contact(Result_id)
            browser_results.append(result)
        browser_end = time.time()
        
        browser_metrics = self.measure_performance(browser_start, browser_end, browser_results,
                                                  "single_contact_reveal", "browser")
        
        # Performance Assertions
        assert api_metrics.avg_time_per_item < 1.0, f"API reveals should be <1s, got {api_metrics.avg_time_per_item:.2f}s"
        assert browser_metrics.avg_time_per_item > 5.0, f"Browser reveals should be >5s, got {browser_metrics.avg_time_per_item:.2f}s"
        assert api_metrics.success_rate > 95.0, f"API success rate should be >95%, got {api_metrics.success_rate:.1f}%"
        assert browser_metrics.success_rate < 85.0, f"Browser success rate should be <85%, got {browser_metrics.success_rate:.1f}%"
        
        # API should be at least 10x faster
        speed_improvement = browser_metrics.avg_time_per_item / api_metrics.avg_time_per_item
        assert speed_improvement >= 10.0, f"API should be 10x+ faster, got {speed_improvement:.1f}x improvement"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_batch_reveal_performance_comparison(self, mock_api_client, mock_browser_client):
        """Compare batch reveal performance between API and browser modes"""
        # Test different batch sizes
        batch_sizes = [5, 10]
        
        for batch_size in batch_sizes:
            Result_ids = [f"batch_Result_{i}" for i in range(batch_size)]
            
            # API Batch Performance
            api_start = time.time()
            api_results = await asyncio.gather(*[
                mock_api_client.reveal_contact(pid) for pid in Result_ids
            ])
            api_end = time.time()
            
            api_metrics = self.measure_performance(api_start, api_end, api_results,
                                                  f"batch_reveal_{batch_size}", "api")
            
            # Browser Batch Performance (limited for testing)
            test_browser_batch = Result_ids[:min(3, batch_size)]  # Limit for test speed
            browser_start = time.time()
            browser_results = await asyncio.gather(*[
                mock_browser_client.reveal_contact(pid) for pid in test_browser_batch
            ])
            browser_end = time.time()
            
            browser_metrics = self.measure_performance(browser_start, browser_end, browser_results,
                                                      f"batch_reveal_{len(test_browser_batch)}", "browser")
            
            # Batch Performance Assertions
            assert api_metrics.throughput_per_second > 1.0, f"API throughput should be >1/s, got {api_metrics.throughput_per_second:.2f}"
            assert browser_metrics.throughput_per_second < 0.2, f"Browser throughput should be <0.2/s, got {browser_metrics.throughput_per_second:.2f}"
            
            # API should handle batches much more efficiently
            throughput_ratio = api_metrics.throughput_per_second / browser_metrics.throughput_per_second
            assert throughput_ratio >= 5.0, f"API throughput should be 5x+ browser, got {throughput_ratio:.1f}x"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_search_performance_comparison(self, mock_api_client, mock_browser_client):
        """Compare search performance between API and browser modes"""
        search_criteria = {
            "title": "Software Engineer",
            "location": "San Francisco",
            "company": "TechCorp"
        }
        
        # API Search Performance
        api_start = time.time()
        api_search_result = await mock_api_client.search_results(search_criteria)
        api_end = time.time()
        
        api_metrics = self.measure_performance(api_start, api_end, [api_search_result],
                                              "search_results", "api")
        
        # Browser Search Performance
        browser_start = time.time()
        browser_search_result = await mock_browser_client.search_results(search_criteria)
        browser_end = time.time()
        
        browser_metrics = self.measure_performance(browser_start, browser_end, [browser_search_result],
                                                  "search_results", "browser")
        
        # Search Performance Assertions
        assert api_metrics.total_time < 1.0, f"API search should be <1s, got {api_metrics.total_time:.2f}s"
        assert browser_metrics.total_time > 10.0, f"Browser search should be >10s, got {browser_metrics.total_time:.2f}s"
        
        # API should be significantly faster for searches
        search_speed_ratio = browser_metrics.total_time / api_metrics.total_time
        assert search_speed_ratio >= 10.0, f"API should be 10x+ faster for search, got {search_speed_ratio:.1f}x"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_concurrent_operations_performance(self, mock_api_client, mock_browser_client):
        """Test performance under concurrent load"""
        # Test concurrent API operations
        api_tasks = []
        for i in range(10):
            task = mock_api_client.reveal_contact(f"concurrent_api_{i}")
            api_tasks.append(task)
        
        api_start = time.time()
        api_results = await asyncio.gather(*api_tasks)
        api_end = time.time()
        
        api_metrics = self.measure_performance(api_start, api_end, api_results,
                                              "concurrent_reveals", "api")
        
        # Test concurrent browser operations (limited)
        browser_tasks = []
        for i in range(3):  # Fewer concurrent browser operations for test speed
            task = mock_browser_client.reveal_contact(f"concurrent_browser_{i}")
            browser_tasks.append(task)
        
        browser_start = time.time()
        browser_results = await asyncio.gather(*browser_tasks)
        browser_end = time.time()
        
        browser_metrics = self.measure_performance(browser_start, browser_end, browser_results,
                                                  "concurrent_reveals", "browser")
        
        # Concurrency Performance Assertions
        # API should handle concurrency much better
        assert api_metrics.total_time < 2.0, f"API concurrent operations should be <2s, got {api_metrics.total_time:.2f}s"
        assert api_metrics.throughput_per_second > 5.0, f"API concurrent throughput should be >5/s, got {api_metrics.throughput_per_second:.2f}"
        
        # Browser operations should be much slower even with fewer items
        normalized_browser_time = browser_metrics.total_time * (10/3)  # Normalize for item count
        assert normalized_browser_time > api_metrics.total_time * 5, "Browser should be much slower even normalized"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_resource_usage_comparison(self, mock_api_client, mock_browser_client):
        """Compare system resource usage between modes"""
        # Measure baseline resource usage
        process = psutil.Process(os.getpid())
        baseline_memory = process.memory_info().rss / 1024 / 1024
        
        # Test API resource usage
        api_start_memory = process.memory_info().rss / 1024 / 1024
        for i in range(5):
            await mock_api_client.reveal_contact(f"resource_api_{i}")
        api_end_memory = process.memory_info().rss / 1024 / 1024
        api_memory_delta = api_end_memory - api_start_memory
        
        # Test browser resource usage simulation
        browser_start_memory = process.memory_info().rss / 1024 / 1024
        for i in range(2):  # Fewer operations for browser
            await mock_browser_client.reveal_contact(f"resource_browser_{i}")
        browser_end_memory = process.memory_info().rss / 1024 / 1024
        browser_memory_delta = browser_end_memory - browser_start_memory
        
        # Simulate expected browser memory usage (browser would use much more)
        simulated_browser_memory = browser_memory_delta * 10  # Browser typically uses 10x+ memory
        
        # Resource Usage Assertions
        assert api_memory_delta < 50, f"API should use <50MB memory, used {api_memory_delta:.1f}MB"
        assert simulated_browser_memory > 200, f"Browser should use >200MB memory (simulated: {simulated_browser_memory:.1f}MB)"

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_error_recovery_performance(self, mock_api_client, mock_browser_client):
        """Test performance of error handling and recovery"""
        # Create mock clients that occasionally fail
        async def api_with_occasional_failures(Result_id):
            if hash(Result_id) % 20 == 0:  # 5% failure rate
                return APIResponse(success=False, error="Rate limit exceeded", status_code=429)
            await asyncio.sleep(0.1)  # Fast operation
            return APIResponse(success=True, data={"Result_uid": Result_id})
        
        async def browser_with_frequent_failures(Result_id):
            if hash(Result_id) % 3 == 0:  # 33% failure rate
                await asyncio.sleep(2)  # Still takes time to fail
                return {"success": False, "error": "Cloudflare challenge"}
            await asyncio.sleep(8)  # Slow operation
            return {"success": True, "Result_uid": Result_id}
        
        mock_api_client.reveal_contact = api_with_occasional_failures
        mock_browser_client.reveal_contact = browser_with_frequent_failures
        
        # Test API error recovery
        api_start = time.time()
        api_results = []
        for i in range(20):
            result = await mock_api_client.reveal_contact(f"error_test_api_{i}")
            api_results.append(result)
        api_end = time.time()
        
        api_metrics = self.measure_performance(api_start, api_end, api_results,
                                              "error_recovery", "api")
        
        # Test browser error recovery (fewer items)
        browser_start = time.time()
        browser_results = []
        for i in range(6):
            result = await mock_browser_client.reveal_contact(f"error_test_browser_{i}")
            browser_results.append(result)
        browser_end = time.time()
        
        browser_metrics = self.measure_performance(browser_start, browser_end, browser_results,
                                                  "error_recovery", "browser")
        
        # Error Recovery Assertions
        assert api_metrics.success_rate > 90, f"API should maintain >90% success rate, got {api_metrics.success_rate:.1f}%"
        assert browser_metrics.success_rate < 70, f"Browser should have <70% success rate, got {browser_metrics.success_rate:.1f}%"
        
        # Even with errors, API should be much faster
        assert api_metrics.avg_time_per_item < 0.5, f"API should maintain speed with errors, got {api_metrics.avg_time_per_item:.2f}s"

    @pytest.mark.performance
    @pytest.mark.asyncio 
    async def test_csv_export_performance_comparison(self, mock_api_client, mock_browser_client):
        """Compare CSV export performance with different data volumes"""
        # Generate test data sets
        small_dataset = [{"uid": f"small_{i}", "name": f"Person {i}", "email": f"person{i}@example.com"} for i in range(100)]
        medium_dataset = [{"uid": f"medium_{i}", "name": f"Person {i}", "email": f"person{i}@example.com"} for i in range(1000)]
        
        # Test API mode export (fast data collection + export)
        api_export_start = time.time()
        api_exporter = CSVExporter(ExportConfig(output_path="api_test_export.csv"))
        api_result = api_exporter.export_results(medium_dataset)
        api_export_end = time.time()
        
        # Test browser mode export (slower data collection simulation + export)
        browser_export_start = time.time()
        # Simulate slower browser data collection
        await asyncio.sleep(5)  # Simulate 5 seconds of browser data collection
        browser_exporter = CSVExporter(ExportConfig(output_path="browser_test_export.csv"))
        browser_result = browser_exporter.export_results(small_dataset)  # Less data due to failures
        browser_export_end = time.time()
        
        # Export Performance Assertions
        api_export_time = api_export_end - api_export_start
        browser_export_time = browser_export_end - browser_export_start
        
        assert api_export_time < 1.0, f"API export should be fast, got {api_export_time:.2f}s"
        assert browser_export_time > 5.0, f"Browser workflow should be slower, got {browser_export_time:.2f}s"
        
        # API should handle more data faster
        api_throughput = len(medium_dataset) / api_export_time
        browser_throughput = len(small_dataset) / browser_export_time
        
        assert api_throughput > browser_throughput * 5, f"API should be 5x+ faster throughput"
        
        # Verify export results
        assert api_result.success, "API export should succeed"
        assert browser_result.success, "Browser export should succeed" 
        assert api_result.total_rows == len(medium_dataset), "API should export all data"
        assert browser_result.total_rows == len(small_dataset), "Browser should export available data"

    def generate_performance_report(self, metrics_list: List[PerformanceMetrics]) -> Dict[str, Any]:
        """Generate a comprehensive performance comparison report"""
        api_metrics = [m for m in metrics_list if m.mode == 'api']
        browser_metrics = [m for m in metrics_list if m.mode == 'browser']
        
        if not api_metrics or not browser_metrics:
            return {"error": "Insufficient metrics for comparison"}
        
        # Calculate aggregate statistics
        api_avg_time = statistics.mean([m.avg_time_per_item for m in api_metrics])
        browser_avg_time = statistics.mean([m.avg_time_per_item for m in browser_metrics])
        api_success_rate = statistics.mean([m.success_rate for m in api_metrics])
        browser_success_rate = statistics.mean([m.success_rate for m in browser_metrics])
        api_throughput = statistics.mean([m.throughput_per_second for m in api_metrics])
        browser_throughput = statistics.mean([m.throughput_per_second for m in browser_metrics])
        
        return {
            "performance_comparison": {
                "speed_improvement": browser_avg_time / api_avg_time,
                "reliability_improvement": api_success_rate - browser_success_rate,
                "throughput_improvement": api_throughput / browser_throughput,
            },
            "api_performance": {
                "avg_time_per_item": api_avg_time,
                "success_rate": api_success_rate,
                "throughput_per_second": api_throughput,
                "avg_memory_usage": statistics.mean([m.memory_usage_mb for m in api_metrics]),
            },
            "browser_performance": {
                "avg_time_per_item": browser_avg_time,
                "success_rate": browser_success_rate,
                "throughput_per_second": browser_throughput,
                "avg_memory_usage": statistics.mean([m.memory_usage_mb for m in browser_metrics]),
            },
            "recommendations": self._generate_recommendations(api_avg_time, browser_avg_time, api_success_rate, browser_success_rate)
        }
    
    def _generate_recommendations(self, api_time: float, browser_time: float, api_success: float, browser_success: float) -> List[str]:
        """Generate performance-based recommendations"""
        recommendations = []
        
        if api_time < browser_time * 10:
            recommendations.append("Use API mode for all operations under 100 contacts/day for optimal speed")
        
        if api_success > browser_success + 20:
            recommendations.append("API mode provides significantly higher reliability")
        
        if api_time < 1.0:
            recommendations.append("API mode is suitable for real-time user interfaces")
        
        if browser_time > 10.0:
            recommendations.append("Browser mode should only be used for bulk operations when API limits are exceeded")
        
        return recommendations

    @pytest.mark.performance
    def test_performance_summary_report(self):
        """Generate and validate performance summary report"""
        # Create sample metrics for report testing
        sample_metrics = [
            PerformanceMetrics("reveal", "api", 2.0, 0.2, 0.1, 0.5, 0.2, 98.0, 5.0, 45.0, 5.0, 1, 10),
            PerformanceMetrics("reveal", "browser", 50.0, 10.0, 5.0, 30.0, 10.0, 70.0, 0.2, 150.0, 15.0, 3, 5),
            PerformanceMetrics("search", "api", 0.8, 0.8, 0.5, 1.0, 0.8, 100.0, 1.25, 40.0, 3.0, 0, 1),
            PerformanceMetrics("search", "browser", 25.0, 25.0, 15.0, 35.0, 25.0, 85.0, 0.04, 180.0, 25.0, 1, 1),
        ]
        
        report = self.generate_performance_report(sample_metrics)
        
        # Validate report structure
        assert "performance_comparison" in report
        assert "api_performance" in report  
        assert "browser_performance" in report
        assert "recommendations" in report
        
        # Validate performance improvements
        comparison = report["performance_comparison"]
        assert comparison["speed_improvement"] > 10, "API should be 10x+ faster"
        assert comparison["reliability_improvement"] > 10, "API should be 10%+ more reliable"
        assert comparison["throughput_improvement"] > 5, "API should have 5x+ throughput"
        
        # Validate recommendations
        recommendations = report["recommendations"]
        assert len(recommendations) > 0, "Should generate performance recommendations"
        assert any("API mode" in rec for rec in recommendations), "Should recommend API mode"
