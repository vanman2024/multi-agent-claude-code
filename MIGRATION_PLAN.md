# Migration Plan: Complex → Simple

## Current State (Too Complex)
- 20+ workflows running
- Milestones named after features
- Auto-creating branches at issue creation
- Labels duplicating Project fields
- Multiple automations fighting

## Target State (Simple)
- 5 workflows max
- Milestones = sprints
- Manual branch creation
- 5 labels only (types)
- Project fields for workflow

## Migration Steps

### Phase 1: Disable Automations (TODAY)

1. **Disable these workflows**:
```bash
# Add 'if: false' to the top of each workflow
.github/workflows/issue-to-implementation.yml
.github/workflows/project-automation.yml
.github/workflows/auto-assign.yml
.github/workflows/pr-automation.yml
```

2. **Keep these (minimal)**:
```bash
.github/workflows/label-sync.yml        # Keep labels clean
.github/workflows/pr-checklist-required.yml  # Enforce PR quality
.github/workflows/gemini-*.yml          # Code review (read-only)
```

### Phase 2: Clean Up Labels

**Delete these labels**:
```bash
# Priority (use Project field instead)
gh label delete "priority:high"
gh label delete "priority:medium"
gh label delete "priority:low"
gh label delete "P0"
gh label delete "P1"
gh label delete "P2"
gh label delete "P3"

# Status (use Project field instead)
gh label delete "status:ready"
gh label delete "status:blocked"
gh label delete "status:in-progress"
gh label delete "draft"
gh label delete "exploration"
gh label delete "research"
gh label delete "not-ready"

# Size (use Project field instead)
gh label delete "size:XS"
gh label delete "size:S"
gh label delete "size:M"
gh label delete "size:L"
gh label delete "size:XL"
```

**Keep only these 5 type labels**:
- `feature`
- `bug`
- `infra`
- `architecture` (create if missing)
- `chore`

### Phase 3: Fix Milestones

**Close old feature-based milestones**:
```bash
gh milestone close "Authentication System"
gh milestone close "User Dashboard"
gh milestone close "Payment Integration"
```

**Create sprint milestones**:
```bash
gh milestone create --title "Sprint 1 (Feb 15-29)" --due-date 2025-02-29
gh milestone create --title "Sprint 2 (Mar 1-14)" --due-date 2025-03-14
gh milestone create --title "Sprint 3 (Mar 15-28)" --due-date 2025-03-28
```

### Phase 4: Clean Project Board

**Simplify Project fields to**:
- Status (Todo, In Progress, In Review, Done)
- Priority (High, Medium, Low)
- Size (XS, S, M, L)
- Sprint (Sprint 1, Sprint 2, etc.)

**Remove these fields**:
- Component
- Complexity
- Agent Assignment
- Sprint Points
- Sprint Goal

### Phase 5: Test Manual Workflow (2 Weeks)

**Week 1**:
1. Create 5 issues manually
2. Assign to Sprint 1 milestone
3. Add type label only
4. Update Project fields manually
5. Create branches manually when starting work
6. Create PRs manually with "Fixes #X"

**Week 2**:
1. Repeat with 10 issues
2. Track what's painful
3. Note what could be automated
4. Document lessons learned

### Phase 6: Add Minimal Automation (After Manual Success)

**Priority 1 (Most Value)**:
- `/create-issue` command (with template)
- `/work #123` command (create branch, update status)

**Priority 2 (Nice to Have)**:
- Auto-move to Done when PR merges
- Auto-assign creator to issue

**Priority 3 (Maybe Never)**:
- Complex routing logic
- Auto-creation of anything
- Multiple status updates

## Success Criteria

After migration:
- [ ] Only 5 type labels exist
- [ ] Milestones are sprints, not features
- [ ] No branches created automatically
- [ ] Project board has 4 fields max
- [ ] Team can complete full cycle manually
- [ ] Velocity is predictable

## Timeline

- **Today**: Disable workflows, clean labels
- **Tomorrow**: Fix milestones, clean Project
- **Next 2 weeks**: Manual sprint
- **Week 3**: Review and add minimal automation
- **Week 4**: Document final workflow

## The Key Insight

> "Automation should make a working process faster, not create the process itself."

We tried to automate before we had a working process. Now we build the process manually, prove it works, then carefully automate only the painful parts.