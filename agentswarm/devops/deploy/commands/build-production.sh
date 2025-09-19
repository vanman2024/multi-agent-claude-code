#!/bin/bash
# Production build helper for AgentSwarm.
# Copies the project into a clean directory with metadata so it can be deployed
# or archived. Usage:
#   ./devops/deploy/commands/build-production.sh <target_dir> [--force]

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[BUILD]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

cd "$REPO_ROOT"

if [[ ! -f "README.md" ]]; then
  print_error "Run this script from the repository root."
  exit 1
fi

TARGET_DIR="${1:-}"
FORCE=false
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=true
      ;;
    *)
      print_error "Unknown option: $1"
      exit 1
      ;;
  esac
  shift
done

if [[ -z "$TARGET_DIR" ]]; then
  print_error "Usage: build-production.sh <target_dir> [--force]"
  exit 1
fi

if [[ -d "$TARGET_DIR" && "$FORCE" != true ]]; then
  print_error "Target directory exists. Use --force to overwrite."
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if [[ -f VERSION ]]; then
  VERSION=$(python3 - <<'PY'
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
  VERSION="0.0.0-dev"
fi
COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")"
BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

print_status "Assembling bundle (version $VERSION, commit $COMMIT)"

mkdir -p "$TMP_DIR/agentswarm"

rsync -a \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  src/ "$TMP_DIR/agentswarm/src/"

[[ -d docs ]] && rsync -a docs/ "$TMP_DIR/agentswarm/docs/"
[[ -f README.md ]] && cp README.md "$TMP_DIR/agentswarm/"
[[ -f VERSION ]] && cp VERSION "$TMP_DIR/agentswarm/"
[[ -f requirements.txt ]] && cp requirements.txt "$TMP_DIR/agentswarm/"
[[ -f install.sh ]] && cp install.sh "$TMP_DIR/agentswarm/"
[[ -f agentswarm ]] && cp agentswarm "$TMP_DIR/agentswarm/"

cat > "$TMP_DIR/agentswarm/BUILD_INFO" <<EOF_META
version=$VERSION
commit=$COMMIT
built_at=$BUILD_DATE
EOF_META

chmod +x "$TMP_DIR/agentswarm/install.sh" 2>/dev/null || true
chmod +x "$TMP_DIR/agentswarm/agentswarm" 2>/dev/null || true

print_status "Writing bundle to $TARGET_DIR"
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"
rsync -a "$TMP_DIR/agentswarm/" "$TARGET_DIR/"

print_success "Build complete: $TARGET_DIR"
print_status "Contents:"
find "$TARGET_DIR" -maxdepth 1 -type f -or -maxdepth 2 -type d -name src -print
