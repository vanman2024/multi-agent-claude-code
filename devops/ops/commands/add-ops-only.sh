#!/bin/bash
# Add ONLY the ops automation CLI to another project
#
# Usage: ./add-ops-only.sh <target-project-path>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_PROJECT="$1"

if [[ -z "$TARGET_PROJECT" ]]; then
    echo "Usage: $0 <target-project-path>"
    echo ""
    echo "This copies ONLY the ops CLI and config, not the whole SignalHire system"
    exit 1
fi

if [[ ! -d "$TARGET_PROJECT" ]]; then
    echo "❌ Target directory does not exist: $TARGET_PROJECT"
    exit 1
fi

cd "$TARGET_PROJECT"

echo "🚀 Adding ops automation CLI to $(basename "$TARGET_PROJECT")..."

# Copy ONLY the ops script
echo "📁 Copying ops CLI..."
mkdir -p scripts
cp "$REPO_ROOT/scripts/ops" scripts/
chmod +x scripts/ops

# Create minimal config
echo "⚙️ Creating automation config..."
mkdir -p .automation
cat > .automation/config.yml << EOF
# Automation Config for $(basename "$TARGET_PROJECT")
versioning:
  strategy: conventional_commits
  source: package.json

targets:
  - $(basename "$TARGET_PROJECT")-deploy

release:
  changelog: true
  tag_prefix: v
  
qa:
  lint: true
  typecheck: true
  tests: "not slow"
  
env:
  wsl_check: true
  
hooks:
  auto_sync: false
EOF

# Update .gitignore if it exists
if [[ -f ".gitignore" ]]; then
    if ! grep -q ".automation/state" ".gitignore"; then
        echo "" >> .gitignore
        echo "# Automation" >> .gitignore
        echo ".automation/state/" >> .gitignore
    fi
fi

echo "✅ Ops CLI installed!"
echo ""
echo "🎯 Available commands:"
echo "  ./scripts/ops setup      # Initial setup"
echo "  ./scripts/ops qa         # Quality checks"
echo "  ./scripts/ops build      # Production builds"
echo "  ./scripts/ops release    # Create releases"
echo "  ./scripts/ops status     # Show status"
echo ""
echo "🚀 Quick start: ./scripts/ops help"