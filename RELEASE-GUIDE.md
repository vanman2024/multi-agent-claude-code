# 📦 Release & Versioning Guide

## Quick Version Rules

**MAJOR.MINOR.PATCH** (e.g., 1.2.3)

- **PATCH** (1.2.3 → 1.2.4): Bug fixes only
- **MINOR** (1.2.3 → 1.3.0): New features, backward compatible  
- **MAJOR** (1.2.3 → 2.0.0): Breaking changes

## How It Works With Our System

### Clear Separation of Concepts
- **Milestones**: Feature groups or sprints (e.g., "Authentication", "Dashboard", "API v2")
- **Git Tags**: Version markers (e.g., v1.0.0, v1.1.0)
- **GitHub Releases**: Published from tags with release notes

### Milestones = Feature Planning (NOT Versions)
Milestones should describe WHAT you're building, not version numbers:
- ✅ GOOD: "Authentication System", "Payment Integration", "Dashboard UI"
- ❌ BAD: "v1.0.0", "v1.1.0", "v1.2.0"

### Simple Workflow

```bash
# 1. Work on features in a milestone (e.g., "Authentication System")
git checkout -b feature/user-auth
# ... develop multiple features ...
git push

# 2. When milestone complete, decide on version and tag
git checkout main
git pull
git tag -a v1.0.0 -m "Release: Authentication System"
git push origin v1.0.0

# 3. GitHub automatically creates release from tag
# Release notes include all issues from completed milestone(s)
```

### Milestone → Release Mapping

One or more milestones can contribute to a release:

| Milestones Completed | Release Tag | Release Title |
|---------------------|-------------|---------------|
| Authentication System | v1.0.0 | Initial Release |
| Bug Fixes + Dashboard UI | v1.1.0 | Dashboard & Fixes |
| API v2 + Performance | v2.0.0 | API v2 (Breaking Changes) |

## Version Progression Examples

### Starting Out (Pre-1.0)
```
v0.1.0 - Initial framework
v0.2.0 - Add agent system
v0.3.0 - Add GitHub automation
v0.4.0 - Add MCP servers
v1.0.0 - First stable release
```

### After 1.0 (Stable)
```
v1.0.0 - Initial release
v1.0.1 - Fix: Agent routing bug
v1.1.0 - Add: New security agent
v1.1.1 - Fix: Hook execution order
v2.0.0 - Breaking: New agent API format
```

## GitHub Actions for Releases

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            ## What's Changed
            See [milestone](https://github.com/${{ github.repository }}/milestone) for details
          draft: false
          prerelease: false
```

## Release Checklist

Before tagging a release:

- [ ] All milestone issues closed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (optional)
- [ ] Version bumped in package.json (if applicable)

## Quick Commands

```bash
# View current version
git describe --tags --abbrev=0

# Create patch release (bug fix)
git tag -a v1.0.1 -m "Fix: Agent routing issue"

# Create minor release (new feature)
git tag -a v1.1.0 -m "Add: Security compliance agent"

# Create major release (breaking change)
git tag -a v2.0.0 -m "Breaking: New agent architecture"

# Push tag to GitHub
git push origin --tags
```

## Pre-Release Versions

For testing before official release:

```bash
# Beta release
git tag -a v1.0.0-beta.1 -m "Beta release"

# Release candidate
git tag -a v1.0.0-rc.1 -m "Release candidate"
```

## Integration with Issues

### Issue Labels Help Determine Version Bumps
- `breaking` → Next MAJOR version
- `enhancement` → Next MINOR version
- `bug` → Next PATCH version

### Milestone Naming Examples (Feature-Based)
- **Current Sprint**: "Authentication System"
- **Next Sprint**: "Dashboard Features"
- **Q1 Goals**: "Q1 2025 - Core Features"
- **Bug Sprint**: "January Bug Fixes"
- **Performance**: "Performance Optimization"

### How to Decide Version Numbers

When completing milestone(s), check the issues:
- All bugs? → PATCH bump (1.0.0 → 1.0.1)
- New features? → MINOR bump (1.0.0 → 1.1.0)
- Breaking changes? → MAJOR bump (1.0.0 → 2.0.0)

## For This Template

Since this is a template/framework:

1. **Template Version**: The framework itself (this repo)
   - Currently: `v1.0.0` (once stable)
   - Tags on this repo track template evolution

2. **Project Version**: Projects created from template
   - Start at `v0.1.0` for new projects
   - Each project has its own versioning

## How It Integrates

### With GitHub Issues
- Each issue gets complexity/size labels
- Issues grouped in milestone (e.g., `v1.1.0`)
- When milestone complete → create release tag

### With Agents
- Agents see current version in git tags
- Can suggest version bumps based on changes
- PR reviewer agent checks for breaking changes

### With GitHub Actions
- Auto-release when tag pushed
- Auto-close milestone on release
- Auto-generate release notes from commits

## Simple Rules to Remember

1. **Don't overthink it** - Start at 0.1.0, increment as you go
2. **Use milestones** for planning, **tags** for releases
3. **Breaking changes** = major bump (be careful!)
4. **New features** = minor bump (most common)
5. **Bug fixes** = patch bump (frequent)

## When to Release

- **Weekly**: Patch releases for bug fixes
- **Bi-weekly**: Minor releases for features
- **Monthly**: Review for major version needs
- **On-demand**: Critical patches anytime

Remember: Version numbers are for **users**, not developers. They communicate change impact.