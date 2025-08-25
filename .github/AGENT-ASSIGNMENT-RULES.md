# Agent Assignment Rules - NO OVERLAP POLICY

## Critical Rule: One Issue, One Agent

**NEVER have two agents working on the same issue.**

## Assignment Methods & Tracking

### Method 1: Issue Assignment (Recommended)
```bash
# This is tracked in GitHub Projects
gh issue edit 26 --add-assignee copilot
```
- ✅ Shows in project board
- ✅ Clear ownership
- ✅ No confusion

### Method 2: PR Creation (Avoid for now)
```javascript
// This creates "orphan" PRs not tracked in projects
mcp__github__create_pull_request_with_copilot()
```
- ❌ Doesn't show in project board
- ❌ Can overlap with existing work
- ❌ Hard to track

## How to Check Before Assigning

### Before assigning ANYTHING to Copilot:

1. **Check if someone's already working on it:**
```bash
gh issue view <number> --json assignees
```

2. **Check for existing PRs:**
```bash
gh pr list --search "fixes:#<number>"
```

3. **Check your local work:**
```bash
git branch | grep -E "(feature|fix).*<issue-number>"
```

## The Safe Workflow

### Step 1: Create Issue with Clear Owner Designation
```markdown
## Owner: Copilot
This issue is designated for Copilot implementation.
Claude Code should NOT work on this.
```

OR

```markdown
## Owner: Claude Code
This issue requires complex logic.
Do NOT assign to Copilot.
```

### Step 2: Use Labels for Clarity
- `copilot-assigned` - Copilot is working on this
- `claude-assigned` - Claude is working on this
- `in-progress` - Someone is actively working on it

### Step 3: Assignment Rules

**For Copilot:**
- Small, well-defined tasks
- Has clear acceptance criteria
- No architectural decisions needed
- Tagged with `copilot-assigned`

**For Claude Code:**
- Complex logic required
- Architecture decisions needed
- Security implementations
- Tagged with `claude-assigned`

## Handling PR #42 (The Current Situation)

You have options:

1. **Accept it** - It's good work, review and merge
2. **Close it** - If you want Claude to handle instead
3. **Use it as reference** - Cherry-pick good parts

## Preventing Future Overlaps

### Automated Prevention
Add to `.github/workflows/prevent-overlap.yml`:
```yaml
name: Prevent Assignment Overlap

on:
  issues:
    types: [assigned]

jobs:
  check-overlap:
    runs-on: ubuntu-latest
    steps:
      - name: Check for Existing Assignees
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const assignees = issue.assignees.map(a => a.login);
            
            if (assignees.length > 1 && 
                assignees.includes('copilot') && 
                assignees.includes(context.actor)) {
              // Remove Copilot if human assigns themselves
              await github.rest.issues.removeAssignees({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                assignees: ['copilot']
              });
              
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: '⚠️ Removed Copilot assignment to prevent overlap with human developer.'
              });
            }
```

## Best Practice Going Forward

### Morning Workflow
1. Review all open issues
2. Tag with `copilot-assigned` OR `claude-assigned`
3. Batch assign to Copilot:
```bash
gh issue list --label "copilot-assigned" --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --add-assignee copilot
```

### During Development
- Check assignees before starting work
- One issue = one agent
- Use draft PRs to show work in progress

### Clear Separation
```
Simple/Defined Tasks → Copilot
Complex/Design Tasks → Claude Code
Never Both → Same Issue
```