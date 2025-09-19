#!/bin/bash
# Deploy the current repository to a production directory.
# Usage: ./devops/deploy/commands/deploy-to-production.sh [target_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DEVOPS_CONFIG="$REPO_ROOT/config/devops.toml"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status(){ echo -e "${BLUE}[DEPLOY]${NC} $1"; }
print_success(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error(){ echo -e "${RED}[ERROR]${NC} $1"; }

get_config_target() {
  if [[ -f "$DEVOPS_CONFIG" ]]; then
    python3 - "$DEVOPS_CONFIG" <<'PY'
import sys, tomllib
with open(sys.argv[1], 'rb') as fh:
    cfg = tomllib.load(fh)
print(cfg.get('deploy', {}).get('target', ''), end='')
PY
  fi
}

TARGET_DIR="${1:-}";
if [[ -z "$TARGET_DIR" ]]; then
  TARGET_DIR="$(get_config_target)"
fi

if [[ -z "$TARGET_DIR" ]]; then
  print_error "No deployment target configured. Pass a path or set deploy.target in config/devops.toml"
  exit 1
fi

print_status "Deploying to $TARGET_DIR"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

BUILD_DIR="$WORK_DIR/artifact"
"$REPO_ROOT/devops/deploy/commands/build-production.sh" "$BUILD_DIR" --force

mkdir -p "$TARGET_DIR"
rsync -a --delete "$BUILD_DIR/" "$TARGET_DIR/"

print_success "Deployment completed -> $TARGET_DIR"
