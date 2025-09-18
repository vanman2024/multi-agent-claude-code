#!/bin/bash
# Simple Production Deployment Script
# Only updates specific system files, preserves everything else

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configuration
PRODUCTION_DIR="${1:-/home/vanman2025/Projects/signalhireagenttests2/signalhireagent}"

echo "🚀 Simple Deployment to Production..."
echo "📁 Production directory: $PRODUCTION_DIR"

cd "$PROJECT_ROOT"

# Get version from pyproject.toml
if [[ -f "pyproject.toml" ]]; then
    VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
    echo "📋 Version: v$VERSION"
else
    echo "❌ No pyproject.toml found"
    exit 1
fi

# Create production directory if it doesn't exist
mkdir -p "$PRODUCTION_DIR"

# Create temporary build
BUILD_DIR="$(mktemp -d)"
./scripts/build/build-production.sh "$BUILD_DIR/signalhireagent" --version "v$VERSION" --force

echo "📦 Updating system files only..."

# Only update these specific files/directories (whitelist approach)
SYSTEM_FILES=(
    "src/"
    "requirements.txt"
    "VERSION"
    "BUILD_INFO.md"
    "install.sh"
    "signalhire-agent"
    ".env"
)

for file in "${SYSTEM_FILES[@]}"; do
    if [[ -e "$BUILD_DIR/signalhireagent/$file" ]]; then
        echo "  ⬆️  Updating: $file"
        if [[ -d "$BUILD_DIR/signalhireagent/$file" ]]; then
            # Directory: remove old, copy new
            rm -rf "$PRODUCTION_DIR/$file"
            cp -r "$BUILD_DIR/signalhireagent/$file" "$PRODUCTION_DIR/"
        else
            # File: just copy over
            cp "$BUILD_DIR/signalhireagent/$file" "$PRODUCTION_DIR/"
        fi
    fi
done

# Make scripts executable
cd "$PRODUCTION_DIR"
chmod +x install.sh signalhire-agent 2>/dev/null || true

echo "✅ Deployment complete!"
echo "📊 Version: v$VERSION"
echo "🔄 All user files preserved"
echo ""
echo "Test: ./signalhire-agent --help"

# Cleanup
rm -rf "$BUILD_DIR"