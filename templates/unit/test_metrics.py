import pytest
from unittest.mock import patch
from src.lib.metrics import MetricsCollector

@patch('builtins.print')
def test_metrics_collector_increment(mock_print):
    """
    Tests that the increment method prints the correct metric.
    """
    collector = MetricsCollector()
    collector.increment("operations.success")
    
    mock_print.assert_called_with("METRIC: operations.success | COUNT | 1")

@patch('builtins.print')
def test_metrics_collector_gauge(mock_print):
    """
    Tests that the gauge method prints the correct metric.
    """
    collector = MetricsCollector()
    collector.gauge("memory.usage", 123.45)
    
    mock_print.assert_called_with("METRIC: memory.usage | GAUGE | 123.45")
