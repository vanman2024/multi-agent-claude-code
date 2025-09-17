#!/bin/bash
# Setup production workspace with user directories
# This creates directories for user-created files that will be preserved during deployments

set -e

PRODUCTION_DIR="${1:-/home/vanman2025/Projects/signalhireagenttests2/signalhireagent}"

echo "🛠️  Setting up production workspace directories..."
echo "📁 Production directory: $PRODUCTION_DIR"

if [[ ! -d "$PRODUCTION_DIR" ]]; then
    echo "❌ Production directory doesn't exist: $PRODUCTION_DIR"
    exit 1
fi

cd "$PRODUCTION_DIR"

# Create user workspace directories
echo "📁 Creating user workspace directories..."

# Issue tracking
mkdir -p docs/issues
echo "# Production Issues" > docs/issues/README.md
echo "Track production issues, bugs, and fixes here." >> docs/issues/README.md
echo "" >> docs/issues/README.md
echo "Files in this directory will be preserved during deployments." >> docs/issues/README.md

# User notes
mkdir -p docs/notes  
echo "# Production Notes" > docs/notes/README.md
echo "Document operational notes, configurations, and procedures here." >> docs/notes/README.md
echo "" >> docs/notes/README.md
echo "Files in this directory will be preserved during deployments." >> docs/notes/README.md

# User documentation
mkdir -p docs/user
echo "# User Documentation" > docs/user/README.md
echo "Custom documentation specific to your production environment." >> docs/user/README.md
echo "" >> docs/user/README.md
echo "Files in this directory will be preserved during deployments." >> docs/user/README.md

# Operations data  
mkdir -p operations
echo "# Operations Data" > operations/README.md
echo "SignalHire agent operations data and tracking files." >> operations/README.md
echo "" >> operations/README.md
echo "Files in this directory will be preserved during deployments." >> operations/README.md

# Local configurations
mkdir -p local
echo "# Local Configuration" > local/README.md
echo "Environment-specific configurations and customizations." >> local/README.md
echo "" >> local/README.md
echo "Files in this directory will be preserved during deployments." >> local/README.md

# Data directory for exports and files
mkdir -p data
echo "# Data Directory" > data/README.md
echo "Exported contacts, search results, and other data files." >> data/README.md
echo "" >> data/README.md
echo "Files in this directory will be preserved during deployments." >> data/README.md

echo ""
echo "✅ Production workspace setup complete!"
echo ""
echo "📋 Created directories:"
echo "  📝 docs/issues/     - Track production issues and fixes"
echo "  📝 docs/notes/      - Operational notes and procedures" 
echo "  📝 docs/user/       - Custom user documentation"
echo "  🔧 operations/      - SignalHire operations data"
echo "  ⚙️  local/          - Environment-specific configurations"
echo "  📊 data/            - Exports and data files"
echo ""
echo "💡 These directories will be automatically preserved during deployments."
echo "💡 Add your own .md, .log, .notes files - they'll be preserved too."