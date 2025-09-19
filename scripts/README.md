# Scripts Directory - Template Framework

This directory contains development automation scripts that transfer with the template to new projects.

## Structure

```
scripts/
├── development/          # Environment setup
│   └── wsl-setup.sh     # WSL optimization for development
├── git/                 # Git automation (transferred via template)
│   └── push-bypass      # Bypass git hook guidance for testing  
├── utilities/           # Core development utilities
│   ├── git-helpers.sh   # Git helper functions
│   └── cleanup-branches.sh  # Branch maintenance
└── README.md           # This file
```

## What Transfers with Template

**Core Development Scripts (ALWAYS transfer):**
- `development/wsl-setup.sh` - Environment optimization
- `git/push-bypass` - Git hook bypass for testing
- `utilities/git-helpers.sh` - Git utility functions
- `utilities/cleanup-branches.sh` - Git maintenance
- Git hooks (`.git/hooks/pre-push`) - Professional commit guidance

**Template Management Only (NEVER transfer):**
- Template sync scripts
- Project creation utilities
- MCP sync scripts (obsolete - CLI tools auto-configure)

## Key Principles

1. **CLI Tools Auto-Configure MCP** - Qwen/Gemini have built-in MCP configs
2. **Git Hooks for Professional Workflow** - Guidance for commit accumulation
3. **WSL Optimization** - Essential for Windows development
4. **Core Utilities Only** - No project-specific scripts

## Usage After Template Sync

```bash
# Environment setup (run once)
./scripts/development/wsl-setup.sh

# Git workflow helpers
source scripts/utilities/git-helpers.sh
cleanup_old_branches

# Testing bypass (when needed)
./scripts/git/push-bypass
```

## Automation Integration

- **Git Hooks**: Auto-installed during template sync
- **Ops CLI**: Available via `./scripts/ops` after sync
- **MCP Servers**: Auto-configured by CLI tools (Qwen, Gemini, etc.)
- **Professional Commits**: Guided by pre-push hook