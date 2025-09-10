#!/bin/bash

# Script to set up Claude Code permissions in any environment
# This ensures permissions work in local, Codespaces, and other environments

echo "🔧 Setting up Claude Code permissions..."

# Define the permissions JSON
PERMISSIONS_JSON='{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "autoApprovalEnabled": true,
  "dangerousMode": true,
  "requireApproval": false,
  "experimental": {
    "autoApproveAll": true,
    "skipConfirmations": true
  },
  "permissions": {
    "allow": [
      "Bash",
      "Bash(npm run:*)",
      "Bash(netstat:*)",
      "Bash(curl:*)",
      "Bash(gemini:*)",
      "Bash(codex:*)",
      "Bash(lsof:*)",
      "Bash(gh:*)",
      "Bash(git:*)",
      "Bash(claude:*)",
      "Bash(claude mcp:*)",
      "Read",
      "Write",
      "Edit",
      "MultiEdit",
      "LS",
      "Grep",
      "Glob",
      "Task",
      "TodoWrite",
      "TodoRead",
      "WebFetch",
      "WebSearch",
      "NotebookRead",
      "NotebookEdit",
      "ExitPlanMode",
      "ListMcpResourcesTool",
      "ReadMcpResourceTool",
      "BashOutput",
      "KillBash",
      "mcp__*"
    ],
    "deny": [],
    "ask": [],
    "defaultMode": "acceptEdits"
  },
  "additionalDirectories": [
    "/tmp",
    "/workspaces"
  ]
}'

# Try multiple possible locations
LOCATIONS=(
  "$HOME/.claude/settings.json"
  ".claude/settings.json"
  ".claude/settings.local.json"
  "$HOME/.config/claude/settings.json"
  "/workspaces/.claude/settings.json"
)

# Create directories and write settings to all possible locations
for location in "${LOCATIONS[@]}"; do
  dir=$(dirname "$location")
  if [ ! -d "$dir" ]; then
    echo "📁 Creating directory: $dir"
    mkdir -p "$dir" 2>/dev/null || true
  fi
  
  echo "📝 Writing permissions to: $location"
  echo "$PERMISSIONS_JSON" > "$location" 2>/dev/null && echo "   ✅ Success" || echo "   ⚠️  Failed (may not have permissions)"
done

# Special handling for Codespaces
if [ -n "$CODESPACES" ]; then
  echo "🚀 Detected GitHub Codespaces environment"
  
  # Try Codespaces-specific locations
  CODESPACE_LOCATIONS=(
    "/workspaces/.codespaces/.persistedshare/claude/settings.json"
    "$CODESPACE_VSCODE_FOLDER/.claude/settings.json"
  )
  
  for location in "${CODESPACE_LOCATIONS[@]}"; do
    dir=$(dirname "$location")
    if [ ! -d "$dir" ]; then
      mkdir -p "$dir" 2>/dev/null || true
    fi
    echo "$PERMISSIONS_JSON" > "$location" 2>/dev/null && echo "   ✅ Codespaces location: $location" || true
  done
fi

echo ""
echo "✨ Claude Code permissions setup complete!"
echo ""
echo "📋 Permissions have been written to multiple locations to ensure they work everywhere."
echo "   You may need to restart Claude Code for changes to take effect."
echo ""
echo "💡 If permissions still aren't working, try:"
echo "   1. Restart Claude Code"
echo "   2. Run: claude --settings to check which settings file is being used"
echo "   3. Copy the permissions manually to that location"