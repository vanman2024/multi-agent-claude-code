#!/bin/bash
# Frontend Smoke Test Runner
#
# PURPOSE: Run a fast, stable smoke subset locally or in CI
# USAGE: ./tests/run-smoke.sh [--headed] [--debug]
# PART OF: Frontend testing template for local development
# CONNECTS TO: Playwright test runner and playwright.config.ts

set -euo pipefail

HEADLESS=1
DEBUG=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --headed) HEADLESS=0; shift ;;
    --debug) DEBUG=1; shift ;;
    -h|--help)
      grep -E '^# (PURPOSE|USAGE|PART OF|CONNECTS TO):' "$0" | sed 's/^# //'
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

ARGS=("--grep=@smoke")
[[ $HEADLESS -eq 0 ]] && ARGS+=("--headed")
[[ $DEBUG -eq 1 ]] && ARGS+=("--debug")

# Prefer Chromium-only for speed and stability
export ALL_BROWSERS=
export PW_NO_SANDBOX=1
export SKIP_WEBSERVER=${SKIP_WEBSERVER:-true}

echo "🏃 Running smoke tests: npx playwright test ${ARGS[*]}"
npx playwright test "${ARGS[@]}"

echo "✅ Smoke tests completed"

