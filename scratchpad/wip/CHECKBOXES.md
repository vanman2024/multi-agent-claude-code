# Checkbox System Documentation

## Overview
Comprehensive checkbox enforcement system for tracking work items in issues and PRs.

## Issue Checkboxes

### Purpose
- Track implementation progress
- Define acceptance criteria
- Ensure nothing is forgotten
- Gate PR merging

### Format
```markdown
## Implementation Tasks
- [ ] Create database schema
- [ ] Implement API endpoints
- [ ] Add frontend components
- [ ] Write unit tests
- [ ] Update documentation

## Acceptance Criteria
- [ ] Feature works as described
- [ ] Tests pass
- [ ] Documentation updated
```

### Enforcement
- GitHub Actions check completion
- Branch protection requires all checked
- Can't merge PR with unchecked boxes

## PR Checkboxes

### Purpose
- Ensure quality standards
- Track review items
- Confirm deployment readiness

### Standard PR Template
```markdown
## Pre-Merge Checklist
- [ ] Tests pass
- [ ] Lint passes
- [ ] Documentation updated
- [ ] Breaking changes documented
- [ ] Security review (if applicable)
- [ ] Performance impact considered
```

### Auto-Generated from Issues
When PR references issue, checkboxes auto-populate from issue tasks.

## Issue vs PR Checkboxes

### Issue Checkboxes (What to Build)
- Define WHAT needs to be done
- Created when issue opens
- Track implementation progress
- Usually technical tasks

### PR Checkboxes (Quality Gates)
- Confirm HOW WELL it was done
- Created when PR opens
- Track quality/review items
- Usually validation tasks

### Relationship
```
Issue: "Build feature X"
- [ ] Create component     → PR: "Implements feature X"
- [ ] Add tests           → - [ ] Tests pass
- [ ] Update docs         → - [ ] Docs updated
```

## Automation & Sync

### TodoWrite Integration
```javascript
// When using TodoWrite in Claude Code
TodoWrite([
  {content: "Create API endpoint", status: "completed"}
])
// Automatically updates:
// - [ ] Create API endpoint → - [x] Create API endpoint
```

### Sync Hook
`.claude/hooks/sync-todo-checkboxes.py`
- Monitors TodoWrite changes
- Updates issue checkboxes
- Maintains sync between local and GitHub

### Workflow Automation
1. Issue created → Checkboxes added
2. Work begins → TodoWrite tracks
3. Tasks complete → Checkboxes update
4. PR opened → Checks enforcement
5. All checked → Ready to merge

## Enforcement Workflows

### Required Workflows
1. `pr-checklist-required.yml` - Blocks merge if unchecked
2. `issue-checklist-enforcer.yml` - Tracks issue progress
3. `checkbox-enforcer.yml` - Overall enforcement

### Branch Protection
```yaml
Required checks:
- Require All Checkboxes
- Tests Pass
- Lint Pass
```

## Best Practices

### DO
- ✅ Keep checkboxes specific and actionable
- ✅ Mark optional items with "(optional)"
- ✅ Update as you work
- ✅ Break large tasks into subtasks
- ✅ Use consistent format

### DON'T
- ❌ Create vague checkboxes
- ❌ Skip updating when complete
- ❌ Add checkboxes after work is done
- ❌ Mix implementation and review items

## Special Cases

### Optional Checkboxes
```markdown
- [ ] Performance optimization (optional)
- [ ] Add animations (nice-to-have)
```
These won't block merging.

### Dependent Checkboxes
```markdown
- [ ] Create database
  - [ ] Design schema
  - [ ] Run migrations
  - [ ] Seed data
```
Parent can't be checked until children complete.

## Troubleshooting

### Checkboxes Not Syncing
1. Check hook is enabled in `.claude/settings.json`
2. Verify Python dependencies installed
3. Check GitHub token has correct permissions

### Can't Merge Despite Checks
1. Refresh PR page
2. Re-run workflows
3. Check branch protection settings

## Future Enhancements
- Auto-check based on commit messages
- Progress percentage display
- Checkbox templates by issue type
- Cross-issue checkbox dependencies