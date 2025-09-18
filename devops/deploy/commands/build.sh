#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEFAULT_TARGET="$REPO_ROOT/.build/$(basename "$REPO_ROOT")"
TARGET="${1:-$DEFAULT_TARGET}"

mkdir -p "$TARGET"
"$REPO_ROOT/devops/deploy/commands/build-production.sh" "$TARGET" --force

echo "✅ Build artifacts written to $TARGET"
