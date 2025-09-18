#!/bin/bash
# Deploy current repository to a target directory using the production bundle.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROJECT_NAME="$(basename "$REPO_ROOT")"
CONFIG_FILE="$REPO_ROOT/devops/ops/config.yml"
DEVOPS_CONFIG="$REPO_ROOT/config/devops.toml"

BLUE='\033[0;34m'; GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
print_status(){ echo -e "${BLUE}[DEPLOY]${NC} $1"; }
print_success(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error(){ echo -e "${RED}[ERROR]${NC} $1"; }

get_default_target() {
  if [[ -f "$DEVOPS_CONFIG" ]]; then
    python3 - "$DEVOPS_CONFIG" <<'PY'
import sys, tomllib
with open(sys.argv[1], 'rb') as fh:
    cfg = tomllib.load(fh)
print(cfg.get('deploy', {}).get('target', ''), end='')
PY
    return
  fi
  if [[ -f "$CONFIG_FILE" ]]; then
    python3 - "$CONFIG_FILE" <<'PY'
import pathlib, sys
cfg = pathlib.Path(sys.argv[1])
section = None
for raw in cfg.read_text().splitlines():
    line = raw.rstrip()
    if not line.strip() or line.lstrip().startswith('#'):
        continue
    if not raw.startswith(' '):
        section = line.rstrip(':')
        continue
    if section == 'targets' and line.strip().startswith('- '):
        print(line.strip()[2:].strip())
        break
PY
    return
  fi
  echo "$HOME/deploy/$PROJECT_NAME"
}

TARGET_DIR="${1:-}";
[[ -z "$TARGET_DIR" ]] && TARGET_DIR="$(get_default_target)"

if [[ -z "$TARGET_DIR" ]]; then
  print_error "No deployment target configured. Pass a path or set deploy.target in config/devops.toml"
  exit 1
fi

print_status "Preparing deployment to $TARGET_DIR"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

BUNDLE_DIR="$WORK_DIR/artifact"
"$REPO_ROOT/devops/deploy/commands/build-production.sh" "$BUNDLE_DIR" --force

mkdir -p "$TARGET_DIR"
rsync -a --delete "$BUNDLE_DIR/" "$TARGET_DIR/"

print_success "Deployment completed -> $TARGET_DIR"
