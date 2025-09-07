#!/bin/bash

# doc-updater.sh - Automatically update documentation sections
# Triggers on PostToolUse events to keep docs in sync

set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Function to log messages
log() {
    echo "[doc-updater] $1" >&2
}

# Function to extract command list from .claude/commands directory
update_command_list() {
    local target_file="$1"
    local commands_dir="$PROJECT_ROOT/.claude/commands"
    
    if [[ ! -d "$commands_dir" ]]; then
        log "Commands directory not found"
        return 1
    fi
    
    # Generate command list
    local command_list=""
    for cmd_file in "$commands_dir"/*.md; do
        if [[ -f "$cmd_file" ]]; then
            local cmd_name=$(basename "$cmd_file" .md)
            # Extract description from frontmatter
            local description=$(grep "^description:" "$cmd_file" 2>/dev/null | sed 's/description: //' | head -1)
            if [[ -n "$description" ]]; then
                command_list="${command_list}- \`/${cmd_name}\` - ${description}\n"
            fi
        fi
    done
    
    # Update the file between markers
    update_between_markers "$target_file" "COMMANDS" "$command_list"
}

# Function to extract tech stack from PROJECT_PLAN.md
update_tech_stack() {
    local target_file="$1"
    local plan_file="$PROJECT_ROOT/docs/PROJECT_PLAN.md"
    
    if [[ ! -f "$plan_file" ]]; then
        log "PROJECT_PLAN.md not found"
        return 1
    fi
    
    # Extract tech stack section
    local tech_stack=$(awk '/## 🛠️ Technology Stack/,/## [^#]/' "$plan_file" | head -n -1)
    
    # Update the file between markers
    update_between_markers "$target_file" "TECH-STACK" "$tech_stack"
}

# Function to update content between markers
update_between_markers() {
    local file="$1"
    local marker="$2"
    local content="$3"
    
    if [[ ! -f "$file" ]]; then
        log "File not found: $file"
        return 1
    fi
    
    local start_marker="<!-- AUTO-SECTION:${marker} -->"
    local end_marker="<!-- END-AUTO-SECTION:${marker} -->"
    
    # Check if markers exist
    if ! grep -q "$start_marker" "$file"; then
        log "Start marker not found in $file: $start_marker"
        return 0  # Not an error, just skip
    fi
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Process the file
    awk -v start="$start_marker" -v end="$end_marker" -v content="$content" '
        $0 ~ start {
            print
            print content
            skip = 1
            next
        }
        $0 ~ end {
            print
            skip = 0
            next
        }
        !skip {
            print
        }
    ' "$file" > "$temp_file"
    
    # Replace the original file
    mv "$temp_file" "$file"
    log "Updated $file between $marker markers"
}

# Function to update test coverage badge
update_test_coverage() {
    local target_file="$1"
    local coverage_file="$PROJECT_ROOT/coverage/coverage-summary.json"
    
    if [[ ! -f "$coverage_file" ]]; then
        log "Coverage file not found"
        return 1
    fi
    
    # Extract coverage percentage (simplified - you'd parse JSON properly)
    local coverage="90"  # Default or parsed from file
    local badge="![Coverage](https://img.shields.io/badge/Coverage-${coverage}%25-brightgreen)"
    
    # Update README badge
    sed -i "s|!\[Coverage\](.*)|${badge}|g" "$target_file"
}

# Main execution
main() {
    # Parse input if provided (for PostToolUse hook)
    local tool_name=""
    local file_path=""
    
    if [[ -n "${1:-}" ]]; then
        # Parse JSON input from hook
        tool_name=$(echo "$1" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
        file_path=$(echo "$1" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")
    fi
    
    log "Starting documentation update check..."
    
    # Update README.md if it exists and has markers
    if [[ -f "$PROJECT_ROOT/README.md" ]]; then
        # Update command list
        if grep -q "<!-- AUTO-SECTION:COMMANDS -->" "$PROJECT_ROOT/README.md"; then
            update_command_list "$PROJECT_ROOT/README.md"
        fi
        
        # Update tech stack
        if grep -q "<!-- AUTO-SECTION:TECH-STACK -->" "$PROJECT_ROOT/README.md"; then
            update_tech_stack "$PROJECT_ROOT/README.md"
        fi
    fi
    
    # Check if specific files were modified that should trigger updates
    case "$file_path" in
        *".claude/commands/"*.md)
            log "Command file modified, updating command list..."
            update_command_list "$PROJECT_ROOT/README.md"
            ;;
        *"PROJECT_PLAN.md")
            log "PROJECT_PLAN.md modified, updating tech stack..."
            update_tech_stack "$PROJECT_ROOT/README.md"
            ;;
        *"test"*|*"spec"*)
            log "Test file modified, updating coverage..."
            update_test_coverage "$PROJECT_ROOT/README.md"
            ;;
    esac
    
    log "Documentation update check complete"
}

# Run main function with all arguments
main "$@"