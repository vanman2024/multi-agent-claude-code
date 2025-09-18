#!/bin/bash
# Deploy DevOps System to Template
#
# PURPOSE: Deploy current DevOps system to the multi-agent template
# USAGE: ./deploy-to-template.sh [target-dir]
# CONNECTS TO: multi-agent-claude-code template repository

set -euo pipefail

USAGE="Usage: $0 [target-dir]\nDeploy DevOps system to template (excluding development files)."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVOPS_SRC="$SCRIPT_DIR"
DEFAULT_TARGET="/home/vanman2025/multi-agent-claude-code"
TARGET_DIR="${1:-$DEFAULT_TARGET}"

echo "🚀 Deploying DevOps system to template..."
echo "📁 Source: $DEVOPS_SRC"
echo "📍 Target: $TARGET_DIR"
echo ""

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "❌ Target directory not found: $TARGET_DIR"
    echo ""
    echo "$USAGE"
    exit 1
fi

# Remove existing devops directory in template
TEMPLATE_DEVOPS="$TARGET_DIR/devops"
if [[ -d "$TEMPLATE_DEVOPS" ]]; then
    echo "🗑️  Removing existing DevOps system in template..."
    rm -rf "$TEMPLATE_DEVOPS"
fi

# Create fresh devops directory
mkdir -p "$TEMPLATE_DEVOPS"

echo "📋 Copying DevOps system (excluding development files)..."

# Copy DevOps system but exclude development files
rsync -a \
  --exclude 'tests/' \
  --exclude 'tests/**' \
  --exclude '*.toml' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude '.git/' \
  --exclude '*.pyc' \
  --exclude '*.pyo' \
  --exclude 'deploy-to-template.sh' \
  "$DEVOPS_SRC/" "$TEMPLATE_DEVOPS/"

# Copy the template version of pyproject.toml as a template file  
if [[ -f "$DEVOPS_SRC/pyproject.toml.template" ]]; then
    cp "$DEVOPS_SRC/pyproject.toml.template" "$TEMPLATE_DEVOPS/pyproject.toml.template"
    echo "✅ Copied pyproject.toml.template for new projects"
fi

# Update VERSION file from our pyproject.toml
if [[ -f "$DEVOPS_SRC/pyproject.toml" ]]; then
    DEVOPS_VERSION=$(python3 - "$DEVOPS_SRC/pyproject.toml" 2>/dev/null <<'PY'
import sys
import tomllib

with open(sys.argv[1], 'rb') as f:
    data = tomllib.load(f)

print(data.get('project', {}).get('version', '0.1.0'))
PY
    )
    echo "$DEVOPS_VERSION" > "$TEMPLATE_DEVOPS/VERSION"
    echo "✅ Updated VERSION to $DEVOPS_VERSION"
fi

echo ""
echo "✅ DevOps system deployment complete!"
echo ""
echo "📋 What was deployed:"
echo "  • DevOps CLI system (ops/, deploy/, ci/)"
echo "  • Template configuration (pyproject.toml.template)"
echo "  • Version tracking (VERSION file)"
echo ""
echo "📋 What was excluded (development only):"
echo "  • Tests and test cache"
echo "  • Development pyproject.toml"
echo "  • Git history and Python cache files"
echo "  • This deployment script"
echo ""
echo "🎯 Next steps:"
echo "  1. Template now has latest DevOps system"
echo "  2. New projects will get DevOps via sync-project-template.sh"
echo "  3. Each project gets customized pyproject.toml from template"