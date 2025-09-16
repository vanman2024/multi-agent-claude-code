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

from pathlib import Path
import re

import pytest
from click.testing import CliRunner

def _stub_stagehand():
    import sys
    from types import ModuleType
    _dummy = ModuleType("stagehand")
    _dummy.Stagehand = object
    sys.modules.setdefault("stagehand", _dummy)


pytestmark = pytest.mark.contract


def test_default_filename_includes_timestamp_and_format():
    _stub_stagehand()
    from src.cli.export_commands import get_default_filename
    name = get_default_filename("xlsx", search_id="search_abc123")
    assert name.endswith(".xlsx")
    # Expect yyyymmdd_hhmmss somewhere
    assert re.search(r"\d{8}_\d{6}", name)


def test_cli_export_search_to_xlsx_creates_file(tmp_path):
    """Exporting to xlsx via CLI should produce a real file (not placeholder)."""
    runner = CliRunner()
    out_file = tmp_path / "test_export.xlsx"
    # Minimal invocation; implementation should write an actual file
    # Invoke the export CLI group directly
    _stub_stagehand()
    from src.cli.export_commands import export
    result = runner.invoke(
        export,
        [
            "search",
            "--search-id",
            "search_abc123",
            "--format",
            "xlsx",
            "--output",
            str(out_file),
            "--overwrite",
        ],
        obj={"config": type("Cfg", (), {"output_format": "human", "debug": False})()},
    )

    assert result.exit_code == 0
    assert out_file.exists() and out_file.stat().st_size > 0


@pytest.mark.asyncio
async def test_export_service_supports_xlsx_future_path(tmp_path):
    """ExportService should expose an xlsx path similar to CSV (contract)."""
    from src.services.export_service import ExportService
    service = ExportService()
    out_file = tmp_path / "svc_export.xlsx"
    # Contract: provide an async method or parameter to export to xlsx
    # This will FAIL until implemented (e.g., export_to_excel or export with format)
    results = [
        {"uid": "p1", "full_name": "Jane Doe", "current_title": "SE", "current_company": "Acme"}
    ]

    # Placeholder expected API; adjust when implementing
    if hasattr(service, "export_to_excel"):
        res = await service.export_to_excel(results=results, output_file=str(out_file))  # type: ignore[attr-defined]
        assert res.success is True
        assert Path(res.file_path).exists()
    else:
        pytest.fail("ExportService.export_to_excel is required by enhanced contract")
