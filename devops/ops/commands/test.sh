#!/bin/bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
"$root/ops/commands/testing/run_tests.py" "$@"
