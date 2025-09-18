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
- Use ops CLI for project versioning
- Don't modify template versioning files
- Follow project-specific versioning strategy

This versioning system ensures clean separation between template evolution and project development while maintaining component synchronization and avoiding workflow conflicts.

---
*Last updated: September 18, 2025*