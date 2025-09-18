# Automatic Version Management

This repository uses **automatic semantic versioning** based on conventional commits to solve the template repository maintenance problem.

## How It Works

### 🤖 Automatic Versioning
- **GitHub Action** automatically analyzes commit messages
- **VERSION file** gets updated automatically on every push to main
- **Component versions** are tracked for deployed DevOps and AgentSwarm

### 📝 Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>
```

### 🏷️ Version Bump Rules

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | **Minor** (0.1.0 → 0.2.0) | `feat: add new sync feature` |
| `fix:` | **Patch** (0.1.0 → 0.1.1) | `fix: resolve deployment issue` |
| `BREAKING CHANGE:` | **Major** (0.1.0 → 1.0.0) | See breaking changes below |

### ⚠️ Breaking Changes

For major version bumps, add `BREAKING CHANGE:` in the commit body:

```
feat: restructure template architecture

BREAKING CHANGE: Projects using old sync-project-template.sh will need to update
```

### 🚫 Non-Versioning Types

These types update the repository but don't trigger version bumps:
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks  
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `ci:` - CI/CD changes
- `style:` - Code formatting

## Quick Setup

1. **Configure git to use commit template:**
   ```bash
   git config commit.template .gitmessage
   ```

2. **Example workflow:**
   ```bash
   # Make changes
   git add .
   git commit  # Opens template
   # Type: feat: add new deployment script
   git push
   # VERSION file automatically updated to next minor version
   ```

## VERSION File Structure

```json
{
  "version": "v0.1.1",
  "commit": "abc123...",
  "build_date": "2025-09-17T22:32:13Z", 
  "build_type": "production",
  "components": {
    "devops": "0.1.0",
    "agentswarm": "0.1.1"
  }
}
```

## Benefits

✅ **No manual versioning** - Can't forget to update  
✅ **Semantic versioning** - Follows standard practices  
✅ **Component tracking** - Know which versions are deployed  
✅ **Release automation** - GitHub releases created automatically  
✅ **Conventional commits** - Clear commit history

## Why This Solves Template Repo Problems

Template repositories have a unique problem: they provide DevOps tools but can't use their own tools for self-management. This creates a circular dependency.

Our solution:
- **External CI/CD** handles versioning (not template DevOps)
- **Conventional commits** are a standard practice anyway
- **Automatic process** removes human error
- **Component tracking** ensures deployment compatibility