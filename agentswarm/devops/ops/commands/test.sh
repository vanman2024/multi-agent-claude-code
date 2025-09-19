#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
COMMAND_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)"
PY_LAUNCHER="$COMMAND_DIR/testing/run_tests.py"

if [[ ! -f "$PY_LAUNCHER" ]]; then
  echo "Test runner not found: $PY_LAUNCHER" >&2
  exit 1
fi

if ! pytest --help >/dev/null 2>&1; then
  echo "pytest not installed or not on PATH" >&2
  exit 1
fi

"$PY_LAUNCHER" "$@"
