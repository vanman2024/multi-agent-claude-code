#!/bin/bash

# Setup Personal Configuration for Claude Code
# This creates a personal config file that can be reused across projects

CONFIG_DIR="$HOME/.claude-code"
CONFIG_FILE="$CONFIG_DIR/personal-config.json"

echo "🔧 Claude Code Personal Configuration Setup"
echo "=========================================="
echo ""
echo "This will create a personal config file at:"
echo "$CONFIG_FILE"
echo ""
echo "Your keys will be stored locally and can be reused across projects."
echo ""

# Create directory if it doesn't exist
mkdir -p "$CONFIG_DIR"

# Check if config already exists
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Existing config found. Update it? (y/n): "
    read -r UPDATE
    if [ "$UPDATE" != "y" ]; then
        echo "Keeping existing config."
        exit 0
    fi
fi

# Collect keys
echo ""
echo "📝 Enter your API keys (press Enter to skip optional ones):"
echo ""

# Anthropic (Required)
echo "1. Anthropic API Key (REQUIRED for Claude Code):"
echo "   Get from: https://console.anthropic.com/settings/keys"
read -r ANTHROPIC_KEY
while [ -z "$ANTHROPIC_KEY" ]; do
    echo "   ❌ Anthropic key is required. Please enter it:"
    read -r ANTHROPIC_KEY
done

# GitHub Token
echo ""
echo "2. GitHub Token (press Enter to use 'gh auth token'):"
read -r GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    GITHUB_TOKEN=$(gh auth token 2>/dev/null)
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "   ⚠️  No GitHub token found. Run 'gh auth login' first."
    else
        echo "   ✓ Using token from gh CLI"
    fi
fi

# Supabase
echo ""
echo "3. Supabase Access Token (optional):"
echo "   Get from: https://supabase.com/dashboard/account/tokens"
read -r SUPABASE_TOKEN

# OpenAI
echo ""
echo "4. OpenAI API Key (optional):"
echo "   Get from: https://platform.openai.com/api-keys"
read -r OPENAI_KEY

# Vercel
echo ""
echo "5. Vercel Token (optional):"
echo "   Get from: https://vercel.com/account/tokens"
read -r VERCEL_TOKEN

# Postman
echo ""
echo "6. Postman API Key (optional):"
echo "   Get from: https://postman.com/settings/me/api-keys"
read -r POSTMAN_KEY

# Create JSON config
cat > "$CONFIG_FILE" << EOF
{
  "anthropic_key": "$ANTHROPIC_KEY",
  "github_token": "$GITHUB_TOKEN",
  "supabase_token": "$SUPABASE_TOKEN",
  "openai_key": "$OPENAI_KEY",
  "vercel_token": "$VERCEL_TOKEN",
  "postman_key": "$POSTMAN_KEY",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# Set secure permissions
chmod 600 "$CONFIG_FILE"

echo ""
echo "✅ Personal config saved to: $CONFIG_FILE"
echo "🔒 File permissions set to 600 (only you can read/write)"
echo ""
echo "To use in a new project, run:"
echo "  /project-setup --use-personal-config"
echo ""
echo "To update later, run this script again."