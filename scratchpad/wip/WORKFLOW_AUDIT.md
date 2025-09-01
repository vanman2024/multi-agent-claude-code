# GitHub Workflow Audit - What's Actually Running

## Workflows Triggered on Issue Creation
1. **issue-to-implementation.yml** - Creates branch, draft PR, assigns milestone
2. **auto-assign.yml** - Assigns creator to issue
3. **project-automation.yml** - Adds to project board
4. **label-sync.yml** - Enforces allowed labels

## Workflows Triggered on PR Creation  
1. **pr-automation.yml** - Various PR automations
2. **pr-checklist-required.yml** - Enforces checkboxes
3. **copilot-pr-handler.yml** - Handles Copilot PRs
4. **infrastructure-check.yml** - Checks dependencies
5. **quick-fix-handler.yml** - NEW: Detects Track 2 PRs

## Problems Found
- ❌ Too many workflows (20+ active)
- ❌ Multiple workflows fighting over same issue
- ❌ Old issues have wrong milestones (v0.x.x)
- ❌ Checkboxes confusion (issue vs PR)
- ❌ No clear Track 1 vs Track 2 separation

## What Should Happen

### Track 1: Real Work (Issue → PR)
1. Create issue with `/create-issue`
2. Issue gets: label, milestone, assignment
3. Work starts with `/work #123`
4. Creates branch and draft PR
5. Implementation happens
6. PR ready → merge → issue closes

### Track 2: Quick Fix (Direct PR)
1. Create branch for typo/cleanup
2. Make change and commit
3. Create PR (no issue)
4. Gets 'quick-fix' label
5. Fast-track merge

## Recommendations
1. **Consolidate workflows** - Too many doing similar things
2. **Fix milestone logic** - Remove version-based completely
3. **Clear Track separation** - Different paths for different work
4. **Simplify automations** - Less is more