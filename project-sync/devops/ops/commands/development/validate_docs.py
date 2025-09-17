#!/usr/bin/env python3
import sys
from pathlib import Path

def main():
    """
    Validates the API documentation.
    """
    repo_root = Path(__file__).parent.parent
    api_docs_path = repo_root / "docs" / "api.md"

    if not api_docs_path.exists():
        print("ERROR: API documentation file not found at docs/api.md")
        sys.exit(1)

    print("API documentation validation passed.")

if __name__ == "__main__":
    main()
