#!/bin/bash
# Production bundle helper for DevOps template projects.
# Usage: ./devops/deploy/commands/build-production.sh <target_dir> [--force]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROJECT_NAME="$(basename "$REPO_ROOT")"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status(){ echo -e "${BLUE}[BUILD]${NC} $1"; }
print_success(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error(){ echo -e "${RED}[ERROR]${NC} $1"; }

TARGET_DIR="${1:-}";
FORCE=false
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=true ;;
    -h|--help)
      cat <<HELP
Usage: $(basename "$0") <target_dir> [--force]
Creates a clean production bundle containing src/, docs/, metadata, and CLI wrappers.
HELP
      exit 0
      ;;
    *) print_error "Unknown option: $1"; exit 1 ;;
  esac
  shift
 done

if [[ -z "$TARGET_DIR" ]]; then
  print_error "Target directory is required"
  exit 1
fi

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

if [[ -f "$REPO_ROOT/VERSION" ]]; then
  VERSION_VALUE=$(python3 - <<'PY'
import json
from pathlib import Path
text = Path('VERSION').read_text().strip()
try:
    data = json.loads(text)
    value = data.get('version') or text
except json.JSONDecodeError:
    value = text or '0.0.0-dev'
print(value)
PY
)
else
  VERSION_VALUE="0.0.0-dev"
fi

COMMIT_HASH=$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

print_status "Assembling bundle (version $VERSION_VALUE, commit $COMMIT_HASH)"

BUNDLE_DIR="$WORK_DIR/$PROJECT_NAME"
mkdir -p "$BUNDLE_DIR"

[[ -d "$REPO_ROOT/src" ]] && rsync -a --exclude '__pycache__' --exclude '.pytest_cache' "$REPO_ROOT/src/" "$BUNDLE_DIR/src/"
[[ -d "$REPO_ROOT/docs" ]] && rsync -a "$REPO_ROOT/docs/" "$BUNDLE_DIR/docs/"
[[ -f "$REPO_ROOT/README.md" ]] && cp "$REPO_ROOT/README.md" "$BUNDLE_DIR/"
[[ -f "$REPO_ROOT/VERSION" ]] && cp "$REPO_ROOT/VERSION" "$BUNDLE_DIR/"
[[ -f "$REPO_ROOT/requirements.txt" ]] && cp "$REPO_ROOT/requirements.txt" "$BUNDLE_DIR/"
[[ -f "$REPO_ROOT/install.sh" ]] && cp "$REPO_ROOT/install.sh" "$BUNDLE_DIR/"

for wrapper in "$PROJECT_NAME" "${PROJECT_NAME}.sh" "agentswarm"; do
  if [[ -f "$REPO_ROOT/$wrapper" ]]; then
    cp "$REPO_ROOT/$wrapper" "$BUNDLE_DIR/$wrapper"
  fi
 done

cat > "$BUNDLE_DIR/BUILD_INFO" <<EOF_META
project=$PROJECT_NAME
version=$VERSION_VALUE
commit=$COMMIT_HASH
built_at=$BUILD_DATE
EOF_META

chmod +x "$BUNDLE_DIR"/* 2>/dev/null || true

print_status "Writing bundle to $TARGET_DIR"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
rsync -a "$BUNDLE_DIR/" "$TARGET_DIR/"

print_success "Build complete: $TARGET_DIR"
