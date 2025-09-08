#!/bin/bash

# Script to consolidate duplicate project entries in ~/.claude/projects/
# Moves todos from old locations to new /Projects/ locations

set -e

CLAUDE_PROJECTS="$HOME/.claude/projects"
BACKUP_DIR="$HOME/.claude/projects-backup-$(date +%Y%m%d-%H%M%S)"

echo "🔧 Project Consolidation Tool"
echo "=============================="
echo

# Create backup first
echo "📦 Creating backup at: $BACKUP_DIR"
cp -r "$CLAUDE_PROJECTS" "$BACKUP_DIR"
echo "✅ Backup created"
echo

# Projects to consolidate (old -> new)
declare -A PROJECT_MAP=(
    ["-home-gotime2022-recruitment-ops"]="-home-gotime2022-Projects-recruitment-ops"
    ["-home-gotime2022-test-todo-app"]="-home-gotime2022-Projects-test-todo-app"
    ["-home-gotime2022-synapseai"]="-home-gotime2022-Projects-synapseai"
    ["-home-gotime2022-mcp-kernel-new"]="-home-gotime2022-Projects-mcp-kernel-new"
    ["-home-gotime2022-project-seed"]="-home-gotime2022-Projects-project-seed"
    ["-home-gotime2022-project-seed-clean"]="-home-gotime2022-Projects-project-seed-clean"
    ["-home-gotime2022-project-seed-template"]="-home-gotime2022-Projects-project-seed-template"
    ["-home-gotime2022-multi-agent-observability-system"]="-home-gotime2022-Projects-multi-agent-observability-system"
)

echo "📋 Projects to consolidate:"
for old in "${!PROJECT_MAP[@]}"; do
    new="${PROJECT_MAP[$old]}"
    echo "  $old → $new"
done
echo

read -p "Continue with consolidation? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 1
fi

# Process each project
for old_project in "${!PROJECT_MAP[@]}"; do
    new_project="${PROJECT_MAP[$old_project]}"
    old_dir="$CLAUDE_PROJECTS/$old_project"
    new_dir="$CLAUDE_PROJECTS/$new_project"
    
    if [ -d "$old_dir" ]; then
        echo
        echo "Processing: $old_project"
        
        # If new directory doesn't exist, just rename
        if [ ! -d "$new_dir" ]; then
            echo "  ➜ Moving entire project to new location"
            mv "$old_dir" "$new_dir"
        else
            # Merge sessions from old to new
            echo "  ➜ Merging sessions into existing project"
            
            # Copy all session files that don't exist in new location
            for session_file in "$old_dir"/*.jsonl; do
                if [ -f "$session_file" ]; then
                    filename=$(basename "$session_file")
                    if [ ! -f "$new_dir/$filename" ]; then
                        cp "$session_file" "$new_dir/"
                        echo "    ✓ Copied session: $filename"
                    fi
                fi
            done
            
            # Remove old directory
            rm -rf "$old_dir"
            echo "  ✓ Removed old project directory"
        fi
    fi
done

echo
echo "🎉 Consolidation complete!"
echo

# Show current state
echo "📊 Current projects in ~/.claude/projects/:"
ls -d "$CLAUDE_PROJECTS"/*/ 2>/dev/null | while read dir; do
    project_name=$(basename "$dir")
    session_count=$(ls -1 "$dir"/*.jsonl 2>/dev/null | wc -l)
    echo "  • $project_name ($session_count sessions)"
done

echo
echo "💡 Tips:"
echo "  - Backup saved at: $BACKUP_DIR"
echo "  - To restore: rm -rf $CLAUDE_PROJECTS && mv $BACKUP_DIR $CLAUDE_PROJECTS"
echo "  - Dashboard should now show consolidated projects"