import os
import subprocess
import sys
from pathlib import Path
import pytest


@pytest.mark.cli
def test_ops_help_exits_zero():
    repo_root = Path(__file__).resolve().parents[3]
    ops_path = repo_root / "project-sync" / "scripts" / "ops"
    assert ops_path.exists() and os.access(ops_path, os.X_OK), "ops script not found or not executable"

    # Run `./scripts/ops help` from project-sync root to ensure paths resolve
    result = subprocess.run([str(ops_path), "help"], cwd=str(repo_root / "project-sync"), capture_output=True, text=True)
    assert result.returncode == 0, f"ops help failed: {result.stderr}"
    assert "USAGE:" in result.stdout or "Commands:" in result.stdout

