# Changelog

All notable changes to the Multi-Agent Development Framework will be documented in this file.

## [2.0.0] - 2025-09-06

### 🎯 Major Changes

#### New Primary Workflow: Work-in-Progress (WIP) Development
- **`/wip` command** - Start exploratory work without creating issues
- **`/wip-status` command** - View all WIP branches with worktree indicators
- **Worktree support** - Create and manage parallel development branches
- **TodoWrite integration** - Persistent tracking of WIP branches

#### Simplified Command Structure
- Removed complex conditional logic from slash commands
- Fixed hardcoded issue references and non-existent labels
- Added helpful usage comments to all commands
- Streamlined workflow from issue→branch→PR→merge

### ✨ New Features

- **`/worktree` command** - Manage git worktrees (list, add, remove, clean)
- **Enhancement template** - Added templates/local_dev/enhancement-template.md
- **Worktree detection** - Automatic detection and navigation help for worktree branches
- **Branch scope guidance** - One branch = one logical feature documentation

### 🐛 Bug Fixes

- Fixed `/create-issue` hardcoded issue #123 references
- Removed non-existent label operations (blocked, sprint:current)
- Fixed conditional execution issues in slash commands
- Resolved git stash conflicts with command files
- Fixed merge conflicts in workflow documentation

### 📚 Documentation

- **WORKFLOW.md** - Complete rewrite with simplified approach
- Moved from docs/ to root for better visibility
- Added branch scope guidance (one branch per feature)
- Added decision tree for choosing workflows
- Updated all command files with usage guidance comments

### 🔧 Improvements

- Simplified `/copilot-review` command workflow
- Added --quick and --thorough options for Copilot PR reviews
- Improved error handling in slash commands
- Better git pull reminders throughout workflow
- Consolidated duplicate documentation files

### 🗑️ Removed

- Deleted duplicate FLAGS.md from root (kept docs/FLAGS.md)
- Removed overly complex automation attempts
- Eliminated unnecessary conditional bash commands in slash files

### 📦 Dependencies

- No new dependencies added
- Framework remains lightweight and focused

## [1.0.0] - 2025-09-01

### Initial Release

- Multi-agent development framework template
- GitHub Copilot integration for simple tasks
- Claude Code integration for complex tasks
- Project board automation
- Slash command system
- CI/CD pipeline with GitHub Actions
- Vercel deployment configuration