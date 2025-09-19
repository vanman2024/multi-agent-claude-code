#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET="${1:-$REPO_ROOT/.build/agentswarm}"

mkdir -p "$TARGET"
"$REPO_ROOT/devops/deploy/commands/build-production.sh" "$TARGET" --force

echo "✅ Build artifacts written to $TARGET"
