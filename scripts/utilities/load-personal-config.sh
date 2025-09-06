#!/bin/bash

# Load Personal Configuration into current project
# This reads from ~/.claude-code/personal-config.json and creates .env

CONFIG_FILE="$HOME/.claude-code/personal-config.json"
ENV_FILE=".env"

echo "📥 Loading Personal Configuration"
echo "================================="
echo ""

# Check if personal config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ No personal config found at: $CONFIG_FILE"
    echo ""
    echo "Run this first to create one:"
    echo "  ./scripts/utilities/setup-personal-config.sh"
    exit 1
fi

# Check if .env already exists
if [ -f "$ENV_FILE" ]; then
    echo "⚠️  .env file already exists. Overwrite? (y/n): "
    read -r OVERWRITE
    if [ "$OVERWRITE" != "y" ]; then
        echo "Keeping existing .env file."
        exit 0
    fi
fi

# Parse JSON and create .env
echo "Loading configuration..."

# Read values from JSON (using python for cross-platform compatibility)
ANTHROPIC_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['anthropic_key'])" 2>/dev/null)
GITHUB_TOKEN=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['github_token'])" 2>/dev/null)
SUPABASE_TOKEN=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['supabase_token'])" 2>/dev/null)
OPENAI_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['openai_key'])" 2>/dev/null)
VERCEL_TOKEN=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['vercel_token'])" 2>/dev/null)
POSTMAN_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['postman_key'])" 2>/dev/null)

# Create .env file
cat > "$ENV_FILE" << EOF
# Environment Variables - Loaded from personal config
# Generated: $(date)
# DO NOT COMMIT THIS FILE

# Core Services
ANTHROPIC_API_KEY="$ANTHROPIC_KEY"
GITHUB_TOKEN="$GITHUB_TOKEN"

# Optional Services
EOF

# Add optional keys if they exist
if [ -n "$SUPABASE_TOKEN" ]; then
    echo "SUPABASE_ACCESS_TOKEN=\"$SUPABASE_TOKEN\"" >> "$ENV_FILE"
fi

if [ -n "$OPENAI_KEY" ]; then
    echo "OPENAI_API_KEY=\"$OPENAI_KEY\"" >> "$ENV_FILE"
fi

if [ -n "$VERCEL_TOKEN" ]; then
    echo "VERCEL_TOKEN=\"$VERCEL_TOKEN\"" >> "$ENV_FILE"
fi

if [ -n "$POSTMAN_KEY" ]; then
    echo "POSTMAN_API_KEY=\"$POSTMAN_KEY\"" >> "$ENV_FILE"
fi

echo ""
echo "✅ Created .env file with your personal configuration"
echo ""
echo "Services configured:"
[ -n "$ANTHROPIC_KEY" ] && echo "  ✓ Anthropic (Claude)"
[ -n "$GITHUB_TOKEN" ] && echo "  ✓ GitHub"
[ -n "$SUPABASE_TOKEN" ] && echo "  ✓ Supabase"
[ -n "$OPENAI_KEY" ] && echo "  ✓ OpenAI"
[ -n "$VERCEL_TOKEN" ] && echo "  ✓ Vercel"
[ -n "$POSTMAN_KEY" ] && echo "  ✓ Postman"
echo ""
echo "Next steps:"
echo "  1. Run: claude"
echo "  2. Run: /add-mcp"