# Template Versioning & Release Management

This template implements **automatic semantic versioning** that works specifically for template repositories while avoiding workflow conflicts with deployed components.

## Core Principle: Template-Only Versioning

**CRITICAL**: This template has its own versioning workflow that does NOT interfere with:
- DevOps component workflows (in `/devops/` folder)
- AgentSwarm component workflows (in `/agentswarm/` folder)
- Project-specific workflows when template is cloned

## How Template Versioning Works

### 🤖 Automatic Version Management
- **GitHub Action** analyzes commit messages on main branch pushes
- **VERSION file** updated automatically based on conventional commits
- **GitHub releases** created automatically with changelogs
- **Component versions tracked** but not managed by template workflow

### 📝 Commit Message Format (Conventional Commits)

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### 🏷️ Version Bump Rules

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | **Minor** (3.0.0 → 3.1.0) | `feat: add new sync feature` |
| `fix:` | **Patch** (3.0.0 → 3.0.1) | `fix: resolve deployment issue` |
| `BREAKING CHANGE:` | **Major** (3.0.0 → 4.0.0) | See breaking changes below |

### ⚠️ Breaking Changes

For major version bumps, add `BREAKING CHANGE:` in commit body:

```
feat: restructure template architecture

BREAKING CHANGE: Projects using old sync-project-template.sh need to update
```

### 🚫 Non-Versioning Commit Types

These update the repository but don't trigger version bumps:
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks  
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `ci:` - CI/CD changes
- `style:` - Code formatting

## VERSION File Structure

The template maintains a clean VERSION file structure:

```json
{
  "version": "v3.1.0",
  "commit": "abc123def456...",
  "build_date": "2025-09-18T15:30:00Z", 
  "build_type": "production",
  "components": {
    "devops": "1.3.0",
    "agentswarm": "1.2.0"
  }
}
```

**Fields Explained:**
- `version`: Template version (managed by workflow)
- `commit`: Git commit SHA of the version
- `build_date`: When the version was created
- `build_type`: Always "production" for releases
- `components`: Versions of deployed components (read-only)

## Workflow Configuration

### Template Workflow (This Repo)
File: `.github/workflows/version-management.yml`
- **Trigger**: Push to main branch (template changes only)
- **Scope**: Template repository versioning only
- **Outputs**: VERSION file updates, GitHub releases

### Component Workflows (External Repos)
- **DevOps**: `github.com/vanman2024/devops` - Has its own versioning
- **AgentSwarm**: `github.com/vanman2024/agentswarm` - Has its own versioning
- **Deployment**: External workflows deploy to this template

### Preventing Workflow Conflicts

**Critical Configuration**: Template workflow only runs on template-specific changes:

```yaml
# Template workflow ONLY triggers on template files
on:
  push:
    branches: [main]
    paths-ignore:
      - 'devops/**'           # Ignore DevOps component changes
      - 'agentswarm/**'       # Ignore AgentSwarm component changes
      - 'devops-VERSION'      # Ignore legacy version files
      - 'agentswarm-VERSION'  # Ignore legacy version files
```

This prevents:
- ❌ Double-triggering when components are deployed
- ❌ Version conflicts between template and components
- ❌ Circular workflow dependencies
- ❌ Unnecessary version bumps on component updates

**Status**: ✅ FULLY AUTOMATED! 
- DevOps repo automatically creates AND merges PRs when it has updates
- AgentSwarm repo automatically creates AND merges PRs when it has updates  
- **Zero manual intervention required** - components auto-update in real-time

## Quick Setup for New Projects

When you clone this template for a new project:

1. **Configure git commit template:**
   ```bash
   git config commit.template .gitmessage
   ```

2. **Example workflow:**
   ```bash
   # Make changes to YOUR project (not template)
   git add .
   git commit  # Opens template with conventional commit format
   # Type: feat: add user authentication system
   git push
   # Your project VERSION file automatically updated
   ```

## Template vs Project Versioning

### Template Repository (This Repo)
- **Purpose**: Track template framework evolution
- **Version**: Currently v3.x.x
- **Changes**: Template improvements, documentation, workflow updates
- **Users**: Template maintainers

### Projects Created from Template
- **Purpose**: Track individual project progress
- **Version**: Start at v0.1.0 for new projects
- **Changes**: Project-specific features, business logic
- **Users**: Project developers

## Benefits of This Approach

✅ **No manual versioning** - Automatic based on commits
✅ **No workflow conflicts** - Template and components separate
✅ **Component tracking** - Know which versions are deployed
✅ **Clean separation** - Template vs project versioning
✅ **Standard practices** - Follows conventional commits
✅ **Automatic releases** - GitHub releases with changelogs

## DevOps Integration

### Using ops CLI in Projects
When you use this template in projects, use the ops CLI for releases:

```bash
# Project development workflow
./scripts/ops qa                    # Quality checks
./scripts/ops build --target dist/  # Build verification
./scripts/ops release patch         # Project version bump (not template)
```

**Important**: The ops CLI manages **project versions**, not template versions.

## Template Update System for Existing Projects

### 🚨 The Missing Piece: Reverse Synchronization

While components (DevOps, AgentSwarm) automatically update the template, **existing projects created from the template** need a way to receive these updates. This was the gap that's now solved.

### 🔄 How Template Updates Work

**Problem**: When DevOps or AgentSwarm get updated in the template, existing projects don't automatically receive those updates.

**Solution**: Template Update System

### ⚙️ Template Update Components

**1. Version Tracking (`.template-version`)**
Every project gets automatic version tracking:
```bash
TEMPLATE_VERSION=v3.7.2
TEMPLATE_REPO=https://github.com/vanman2024/multi-agent-claude-code
SYNC_DATE=2025-09-18

# Template Update Commands:
# /update-from-template --check     # Check for updates
# /update-from-template --preview   # Preview changes  
# /update-from-template             # Apply updates
```

**2. Update Script (`setup/update-from-template.js`)**
Intelligent update system that:
- ✅ Updates safe components (devops/, agentswarm/, agents/, automation/)
- 🛡️ Preserves user code (src/, app/, package.json, .env files)
- 📋 Shows preview before applying changes
- 🏷️ Tracks version history

**3. Slash Command Integration (`/update-from-template`)**
```bash
/update-from-template --check    # Check if updates available
/update-from-template --preview  # Show what would change
/update-from-template            # Apply updates safely
/update-from-template --force    # Force update even if same version
```

### 🔄 Complete Update Flow

**Template Evolution**:
```
1. DevOps repo changes → Auto-deploy to template → v3.7.2 → v3.8.0
2. AgentSwarm changes → Auto-deploy to template → v3.8.0 → v3.8.1  
3. Template improvements → Template versioning → v3.8.1 → v3.9.0
```

**Project Updates**:
```
1. Project checks: /update-from-template --check
   "Current: v3.7.2, Latest: v3.9.0 - Updates available!"

2. Preview changes: /update-from-template --preview
   "Will update: devops/, agentswarm/, agents/, .gitmessage"
   "Protected: src/, package.json, README.md (your code safe)"

3. Apply updates: /update-from-template
   "✅ Updated to v3.9.0 - Applied 8 changes"
```

### 🛡️ Safety Features

**Safe Update Paths** (automatically updated):
- `devops/` - DevOps automation scripts
- `agentswarm/` - Agent swarm components  
- `agents/` - Agent instruction files
- `.github/workflows/version-management.yml` - Versioning workflow
- `scripts/ops` - Operations CLI
- `automation/` - Automation configurations
- `.gitmessage` - Git commit template
- `VERSIONING.md` - This documentation

**Protected Paths** (never touched):
- `src/`, `app/`, `components/`, `pages/`, `api/`, `lib/` - Your application code
- `.env*` - Environment files  
- `package.json`, `pyproject.toml`, `requirements.txt` - Your dependencies
- `README.md` - Your project documentation

### 📋 Automatic Deployment

**New Projects**: Template update system automatically included
```bash
./sync-project-template.sh

# Automatically creates:
# ✅ .template-version (tracks current version)
# ✅ setup/update-from-template.js (update script)  
# ✅ /update-from-template slash command
```

**Existing Projects**: Can add update system manually
```bash
# Copy from template:
cp template/setup/update-from-template.js setup/
cp template/templates/slash-commands/update-from-template.md templates/slash-commands/

# Create version tracking:
echo "TEMPLATE_VERSION=v3.7.2" > .template-version
```

### 🔄 Integration with Component Updates

**Complete Automation Chain**:
```
External Repo → Template → Existing Projects
     ↓              ↓            ↓
DevOps v1.4.0 → Auto-merge → /update-from-template
AgentSwarm → Auto-merge → Project gets latest
```

**Timeline Example**:
- 9:00 AM: DevOps repo releases v1.4.0
- 9:01 AM: Auto-deploy creates PR in template  
- 9:02 AM: PR auto-merges to template
- 9:03 AM: Project developer runs `/update-from-template --check`
- 9:04 AM: Project updated with latest DevOps automation

## Component Synchronization

### How Components Get Updated (FULLY AUTOMATED)
1. **External repositories** (devops, agentswarm) have changes committed to main
2. **Their semantic-release workflows** automatically create new versions
3. **Auto-deploy step** in their workflows automatically:
   - Creates a branch in this template repo
   - Copies production-ready files to `/devops/` or `/agentswarm/`
   - Updates component VERSION files
   - Creates a Pull Request with the changes
   - **AUTO-MERGES the PR immediately** ✅
4. **Template workflow** ignores these merges (due to `paths-ignore`)
5. **Component versions** are automatically tracked in main VERSION file
6. **No manual intervention required!** 🚀

### Manual Template Updates
Only template maintainers should trigger template versions:

```bash
# Template framework improvements
git commit -m "feat: improve agent coordination system"
# Creates new template version (e.g., v3.1.0)

git commit -m "docs: update component integration guide" 
# No version bump (docs: type)
```

## Troubleshooting

### Version Not Updating
- Check commit message follows conventional format
- Ensure push is to main branch
- Verify workflow has permissions (GITHUB_TOKEN)
- Check workflow logs in Actions tab

### Workflow Conflicts
- Verify `paths-ignore` is configured in template workflow
- Check that component workflows target correct repositories
- Ensure no circular dependencies between workflows

### Component Version Mismatches
- Check latest component deployments
- Verify external workflows are functioning
- Review component VERSION files in their source repositories

## Advanced Configuration

### Custom Release Branches
For projects needing release branches:

```yaml
# In project .github/workflows/
branches: ["main", "release/*"]
```

### Pre-release Versions
For beta/RC releases:

```bash
# Beta release
git commit -m "feat: experimental feature

BREAKING CHANGE: This is a beta feature"
# Results in v4.0.0-beta.1
```

## Best Practices

### For Template Maintainers
- Use conventional commits consistently
- Test template changes before committing
- Document breaking changes thoroughly
- Coordinate with component maintainers

### For Project Developers
- Start new projects at v0.1.0
- Use ops CLI for project versioning (`./scripts/ops release patch`)
- Don't modify template versioning files
- Follow project-specific versioning strategy
- **Use template update system regularly**: 
  - Check for updates weekly: `/update-from-template --check`
  - Preview before applying: `/update-from-template --preview` 
  - Keep projects synchronized with latest DevOps/AgentSwarm improvements

### For Template Updates
- **Never modify user code paths** when updating template
- **Test update system** before releasing template changes
- **Document breaking changes** that might affect existing projects
- **Coordinate with DevOps/AgentSwarm teams** on component updates

This complete versioning system ensures:
- ✅ **Clean separation** between template evolution and project development
- ✅ **Component synchronization** via automated DevOps/AgentSwarm deployment
- ✅ **Project updates** via template update system
- ✅ **Workflow conflict prevention** with proper path ignoring
- ✅ **Bidirectional flow**: Template ↔ Components ↔ Projects
- ✅ **Zero manual intervention** for component updates
- ✅ **Safe project updates** that preserve user code

**The system is now complete with full automation for both template evolution and project synchronization.**

---
*Last updated: September 18, 2025 - Template update system implementation*