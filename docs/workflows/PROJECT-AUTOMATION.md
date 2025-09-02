# Project Board Automation

> **Status**: 🟢 IMPLEMENTED (PR #92 pending)
> **Last Updated**: 2025-09-02  
> **Stability**: Production Ready

## Automatic Status Transitions

### Issue Created → "To Do"
- Triggered by: New issue (UI or `/create-issue`)
- Workflow: `project-automation.yml`
- Adds to project board automatically

### PR Created → "In Progress"
- Triggered by: PR with "Closes #XX" in body
- Workflow: `project-automation.yml` (after PR #92)
- Updates linked issue status
- Adds comment to issue

### PR Merged → "Done"
- Triggered by: PR merge
- Native GitHub behavior
- Closes linked issue

## Field Mappings

Issues with metadata in body:
```markdown
**Priority**: P0/P1/P2/P3
**Component**: Frontend/Backend/Database/Auth
**Points**: 1-13
```

These map to project board fields automatically.

## Manual Overrides

**When needed:**
- Moving between sprints
- Changing priority
- Reassigning work

**Never manually:**
- Update status (let automation handle it)
- Create branches at issue creation
- Skip the issue → PR flow