#!/bin/bash

# Script to disable all GitHub workflows across repositories
echo "Disabling GitHub workflows to stop failure notifications..."

# List of repositories to check
repos=(
  "multi-agent-claude-code"
  "project-seed-template"
  "taskflow-demo"
  "multi-agent-observability-system"
  "recruitment_ops"
  "synapseai"
  "mcp-kernel-clean"
  "mcp-kernel-dev"
  "DevLoop2"
  "v0-project-planning-ai-interface"
  "Synergy-New"
  "Synergy"
  "-SynergyBootstrap-"
  "Synapse-new"
  "Synapse"
  "New-Staff-Hive"
  "staffhive"
  "Client_Website_Job_Widget"
  "GroceryPricePro"
)

# Function to disable workflows for a repository
disable_repo_workflows() {
  local repo=$1
  echo ""
  echo "=== Processing repository: $repo ==="
  
  # List workflows
  workflows=$(gh workflow list --repo vanman2024/$repo --json id,name,state 2>/dev/null)
  
  if [ -z "$workflows" ] || [ "$workflows" = "[]" ]; then
    echo "  No workflows found"
    return
  fi
  
  # Parse and disable each active workflow
  echo "$workflows" | jq -r '.[] | select(.state == "active") | .id' | while read -r workflow_id; do
    workflow_name=$(echo "$workflows" | jq -r ".[] | select(.id == $workflow_id) | .name")
    echo "  Disabling workflow: $workflow_name (ID: $workflow_id)"
    
    # Try to disable by ID first
    if ! gh workflow disable $workflow_id --repo vanman2024/$repo 2>/dev/null; then
      # If that fails, try by filename
      workflow_file=$(gh api repos/vanman2024/$repo/actions/workflows/$workflow_id --jq '.path' 2>/dev/null)
      if [ -n "$workflow_file" ]; then
        echo "    Attempting to disable via file: $workflow_file"
        gh workflow disable "$workflow_file" --repo vanman2024/$repo 2>/dev/null || echo "    Could not disable workflow"
      fi
    else
      echo "    Successfully disabled"
    fi
  done
}

# Process each repository
for repo in "${repos[@]}"; do
  disable_repo_workflows "$repo"
done

echo ""
echo "=== Summary ==="
echo "Workflow disable process completed."
echo "Note: Some workflows may not be disableable if they're required by repository settings."
echo ""
echo "To completely stop notifications, you can also:"
echo "1. Go to GitHub Settings > Notifications"
echo "2. Unwatch repositories you're no longer working on"
echo "3. Or delete the workflow files from the repositories"