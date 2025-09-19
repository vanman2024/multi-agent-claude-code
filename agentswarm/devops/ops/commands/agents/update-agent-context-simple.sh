#!/usr/bin/env bash
# Simple and consistent agent context file updater
# Treats all agent files equally with smart section management

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "001-looking-to-build")

# Agent files
CLAUDE_FILE="$REPO_ROOT/CLAUDE.md"
GEMINI_FILE="$REPO_ROOT/GEMINI.md"
AGENTS_FILE="$REPO_ROOT/AGENTS.md"
COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"

AGENT_TYPE="${1:-all}"

# Function to add content to a section or create section if it doesn't exist
add_to_section() {
    local file="$1"
    local section_title="$2"
    local content="$3"
    local action="${4:-append}"  # append or replace
    
    if [ ! -f "$file" ]; then
        echo "File $file doesn't exist, skipping..."
        return 1
    fi
    
    # Check if section exists
    if grep -q "^${section_title}$" "$file"; then
        if [ "$action" = "replace" ]; then
            echo "  Replacing section: $section_title"
            # Replace entire section
            local temp_file=$(mktemp)
            awk -v section="$section_title" -v new_content="$content" '
                BEGIN { in_section=0; section_found=0 }
                $0 == section { 
                    print $0
                    print new_content
                    in_section=1
                    section_found=1
                    next
                }
                /^## / && in_section && $0 != section {
                    in_section=0
                }
                !in_section || !section_found { print }
            ' "$file" > "$temp_file"
            mv "$temp_file" "$file"
        else
            echo "  Adding to existing section: $section_title"
            # Add to existing section (before next ## or end of file)
            local temp_file=$(mktemp)
            awk -v section="$section_title" -v new_content="$content" '
                BEGIN { in_section=0 }
                $0 == section { 
                    print $0
                    in_section=1
                    next
                }
                /^## / && in_section && $0 != section {
                    print new_content
                    in_section=0
                }
                { print }
                END { if (in_section) print new_content }
            ' "$file" > "$temp_file"
            mv "$temp_file" "$file"
        fi
    else
        echo "  Creating new section: $section_title"
        # Add new section at end of file (before MANUAL ADDITIONS if it exists)
        if grep -q "<!-- MANUAL ADDITIONS START -->" "$file"; then
            # Insert before manual additions
            local temp_file=$(mktemp)
            awk -v section="$section_title" -v content="$content" '
                /<!-- MANUAL ADDITIONS START -->/ {
                    print ""
                    print section
                    print content
                }
                { print }
            ' "$file" > "$temp_file"
            mv "$temp_file" "$file"
        else
            # Add at end of file
            echo "" >> "$file"
            echo "$section_title" >> "$file"
            echo "$content" >> "$file"
        fi
    fi
}

# Function to update a single agent file
update_agent_file() {
    local target_file="$1"
    local agent_name="$2"
    
    echo "Updating $agent_name context file: $target_file"
    
    if [ ! -f "$target_file" ]; then
        echo "Creating new $agent_name context file..."
        cat > "$target_file" << EOF
# $(basename "$REPO_ROOT") Development Guidelines

Auto-generated from all feature plans. Last updated: $(date +%Y-%m-%d)

## Active Technologies
- Python 3.11 + asyncio
- Stagehand (AI browser automation with Playwright)
- FastAPI (callback server for webhooks/status)
- httpx (async HTTP client for API monitoring only)
- pandas (CSV data processing and export)
- pydantic (data validation and models)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
EOF
    fi
    
    # Always update basic sections for consistency
    add_to_section "$target_file" "## Active Technologies" "- Python 3.11 + asyncio ($(basename $(pwd)))
- Stagehand (AI browser automation with Playwright)
- FastAPI (callback server for webhooks/status)
- httpx (async HTTP client for API monitoring only)  
- pandas (CSV data processing and export)
- pydantic (data validation and models)" "replace"
    
    echo "  ✅ Updated $agent_name successfully"
}

# Update files based on argument
case "$AGENT_TYPE" in
    "claude")
        update_agent_file "$CLAUDE_FILE" "Claude Code"
        ;;
    "gemini")
        update_agent_file "$GEMINI_FILE" "Gemini CLI"
        ;;
    "agents")
        update_agent_file "$AGENTS_FILE" "Repository Guidelines"
        ;;
    "copilot")
        update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        ;;
    "all"|"")
        # Update all existing files
        [ -f "$CLAUDE_FILE" ] && update_agent_file "$CLAUDE_FILE" "Claude Code"
        [ -f "$GEMINI_FILE" ] && update_agent_file "$GEMINI_FILE" "Gemini CLI" 
        [ -f "$AGENTS_FILE" ] && update_agent_file "$AGENTS_FILE" "Repository Guidelines"
        [ -f "$COPILOT_FILE" ] && update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        ;;
    *)
        echo "Unknown agent type: $AGENT_TYPE"
        echo "Usage: $0 [claude|gemini|agents|copilot|all]"
        exit 1
        ;;
esac

echo ""
echo "Summary: All agent files updated with consistent section management"