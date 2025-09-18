#!/usr/bin/env python3
"""Generic pytest runner for DevOps template projects."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]

CATEGORIES: List[Tuple[str, List[str]]] = [
    ("unit", ["tests/unit"]),
    ("integration", ["tests/integration"]),
    ("contract", ["tests/contract"]),
    ("performance", ["tests/performance", "-m", "performance"]),
    ("e2e", ["tests/e2e"]),
    ("quick", ["tests/unit", "-m", "not slow"]),
]


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
    parser = argparse.ArgumentParser(description="Run project test categories")
    parser.add_argument(
        "category",
        nargs="?",
        choices=[name for name, _ in CATEGORIES] + ["all"],
        default="quick",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose pytest output")
    args = parser.parse_args()

    base_args: List[str] = []
    if args.verbose:
        base_args.append("-vv")

    if args.category == "all":
        success = True
        for name, opts in CATEGORIES:
            success &= run_pytest(base_args + opts, f"{name.title()} tests")
        print("\n" + "=" * 50)
        print("✅ All tests passed!" if success else "❌ Some tests failed")
        return 0 if success else 1

    for name, opts in CATEGORIES:
        if name == args.category:
            success = run_pytest(base_args + opts, f"{name.title()} tests")
            print("\n" + "=" * 50)
            print("✅ Tests passed" if success else "❌ Tests failed")
            return 0 if success else 1

    print(f"Unknown category: {args.category}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
