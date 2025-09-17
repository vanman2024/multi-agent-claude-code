#!/bin/bash
# Extract AgentSwarm package to a clean directory for templating/reuse.

set -euo pipefail

USAGE="Usage: $0 <target-dir>\nCopy the agentswarm package (excluding tests) to the target directory."

if [[ $# -lt 1 ]]; then
  echo "$USAGE"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
AGENTSWARM_SRC="$REPO_ROOT/agentswarm"
TARGET_DIR="$1"

if [[ ! -d "$AGENTSWARM_SRC" ]]; then
  echo "AgentSwarm directory not found at $AGENTSWARM_SRC"
  exit 1
fi

rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

rsync -a \
  --exclude 'tests/' \
  --exclude 'tests/**' \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude '.pytest_cache/**' \
  "$AGENTSWARM_SRC/" "$TARGET_DIR/"

# Double-check unwanted dirs removed
rm -rf "$TARGET_DIR/tests" "$TARGET_DIR/.pytest_cache"

# Create VERSION file from agentswarm config
VERSION_FILE="$AGENTSWARM_SRC/config/agentswarm.toml"
if [[ -f "$VERSION_FILE" ]]; then
  AGENTSWARM_VERSION=$(grep '^version = ' "$VERSION_FILE" | sed 's/version = "\(.*\)"/\1/')
  echo "$AGENTSWARM_VERSION" > "$TARGET_DIR/VERSION"
fi
