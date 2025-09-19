#!/usr/bin/env python3
"""Lightweight test runner for AgentSwarm's backend suite."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[4]


def run_pytest(args: List[str], description: str) -> bool:
    print(f"\n🧪 {description}")
    print("=" * 50)
    try:
        completed = subprocess.run(["pytest", *args], cwd=REPO_ROOT)
        return completed.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Test run interrupted")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AgentSwarm test categories")
    parser.add_argument(
        "category",
        nargs="?",
        choices=["quick", "unit", "integration", "contract", "performance", "e2e", "all"],
        default="quick",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose pytest output")
    args = parser.parse_args()

    base_args = []
    if args.verbose:
        base_args.append("-vv")

    success = True
    if args.category == "quick":
        success &= run_pytest(base_args + ["tests/backend", "-m", "not slow"], "Quick backend suite")
    elif args.category == "unit":
        success &= run_pytest(base_args + ["tests/backend/unit"], "Unit tests")
    elif args.category == "integration":
        success &= run_pytest(base_args + ["tests/backend/integration"], "Integration tests")
    elif args.category == "contract":
        success &= run_pytest(base_args + ["tests/backend/contract"], "Contract tests")
    elif args.category == "performance":
        success &= run_pytest(base_args + ["tests/backend/performance", "-m", "performance"], "Performance guardrails")
    elif args.category == "e2e":
        success &= run_pytest(base_args + ["tests/backend/e2e"], "Workflow E2E checks")
    elif args.category == "all":
        for directory, label in [
            ("tests/backend/unit", "Unit"),
            ("tests/backend/integration", "Integration"),
            ("tests/backend/contract", "Contract"),
            ("tests/backend/performance", "Performance"),
            ("tests/backend/e2e", "E2E"),
        ]:
            success &= run_pytest(base_args + [directory], f"{label} tests")

    print("\n" + "=" * 50)
    print("✅ All tests passed!" if success else "❌ Some tests failed")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
