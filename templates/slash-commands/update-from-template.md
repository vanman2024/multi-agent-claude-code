---
allowed-tools: Bash(*)
description: Update project with latest template changes
argument-hint: [--preview|--force|--check]
---

# Update From Template

## Your Task
Update the current project with the latest changes from the multi-agent template repository.

**Options:**
- `--check`: Show current vs latest template version
- `--preview`: Show what would be updated without applying changes  
- `--force`: Force update even if versions match
- No args: Normal update if newer template available

**Safe Update Paths** (won't overwrite your code):
- `devops/` - DevOps automation scripts
- `agentswarm/` - Agent swarm components  
- `agents/` - Agent instruction files
- `.github/workflows/version-management.yml` - Versioning workflow
- `scripts/ops` - Operations CLI
- `automation/` - Automation configs
- `.gitmessage` - Git commit template
- `VERSIONING.md` - Version documentation

**Protected Paths** (never touched):
- `src/`, `app/`, `components/`, `pages/`, `api/`, `lib/` - Your application code
- `.env*` - Environment files
- `package.json`, `pyproject.toml` - Your dependencies
- `README.md` - Your project documentation

Run: !node setup/update-from-template.js $ARGUMENTS