import pytest
pytest.skip("Skipped in API-only mode (debug tools not present)", allow_module_level=True)

import json
import tempfile
from pathlib import Path

# from signalhire_agent.lib.debug_tools import dump_session_artifacts


def test_dump_session_artifacts_writes_files():
    with tempfile.TemporaryDirectory() as td:
        out = td  # placeholder to keep structure when skipped
        _ = {
            "session_id": "s-123",
            "error": "timeout",
            "steps": ["login", "search", "reveal"],
            "calls": [{"op": "login"}],
        }
        p = Path(out)
        assert p.exists()
        meta = json.loads((p / "metadata.json").read_text())
        assert meta["session_id"] == "s-123"
        assert (p / "calls.log").exists()
