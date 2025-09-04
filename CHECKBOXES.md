# Checkbox Workflow Documentation

## 📋 The Golden Rule: Issues = Requirements, PRs = Implementation

This framework uses a clear separation of concerns:
- **Issues** contain requirement checkboxes (what needs to be done)
- **Pull Requests** describe implementation (what was done)

## Why This Separation?

### ❌ The Problem We Solved
Previously, we had checkboxes in both issues AND pull requests, which caused:
- Duplicate tracking of the same requirements
- Confusion about where to mark things complete
- Inconsistent checkbox states between issues and PRs
- Workflows failing because people checked boxes in the wrong place

### ✅ The Solution
- **One Source of Truth**: Requirements live ONLY in issues
- **Clear Workflow**: Check off requirements in the issue as you complete them
- **PR Validation**: The workflow checks the linked issue's checkboxes before allowing merge

## How It Works

### 1. Creating an Issue
When you create an issue (using `/create-issue` or GitHub UI), it includes requirement checkboxes:

```markdown
## Fix Requirements
- [ ] Reproduce the issue
- [ ] Identify root cause  
- [ ] Implement fix
- [ ] Add test to prevent regression
- [ ] Verify fix resolves the issue
```

These checkboxes represent the work that needs to be done.

### 2. Starting Work
When you run `/work #123`, it:
1. Creates a feature branch
2. Creates a DRAFT pull request
3. Links the PR to the issue with `Closes: #123`

The PR does NOT have requirement checkboxes - just implementation details.

### 3. During Development
As you complete each requirement:
1. Check it off in the ISSUE (not the PR)
2. The issue tracks your progress
3. The PR describes what you implemented

### 4. Ready to Merge
When all work is complete:
1. All checkboxes in the issue should be checked ✅
2. Convert the draft PR to ready for review
3. The `pr-checklist-required.yml` workflow runs

### 5. The Validation Workflow
The workflow (`pr-checklist-required.yml`):
1. Finds the linked issue from `Closes: #XXX` in the PR body
2. Checks if that issue has any unchecked boxes
3. Fails if requirements are incomplete
4. Passes if all requirements are complete

## Workflow Enforcement

### Branch Protection Rule
The repository has a branch protection rule requiring:
- Status check: `Require Issue Checkboxes Complete`
- This prevents merging PRs with incomplete issue requirements

### Hotfix Exception
PRs from branches starting with `hotfix-` bypass this check for emergency fixes.

## Common Scenarios

### Scenario 1: Normal Feature Development
```bash
# 1. Create issue with requirements
/create-issue feature "Add user dashboard"

# 2. Start work (creates branch and draft PR)
/work #123

# 3. As you work, check off requirements in issue #123
# 4. When done, mark PR as ready
# 5. Workflow validates all checkboxes are complete
# 6. Merge PR (auto-closes issue)
```

### Scenario 2: Bug Fix
```bash
# 1. Create bug issue
/create-issue bug "Login fails with special characters"

# Issue includes:
# - [ ] Reproduce the issue
# - [ ] Identify root cause
# - [ ] Implement fix
# - [ ] Add regression test

# 2. Work on it
/work #124

# 3. Check off each requirement in issue as completed
# 4. PR can only merge when all boxes checked
```

### Scenario 3: Emergency Hotfix
```bash
# 1. Create hotfix issue
/create-issue hotfix "Production database connection failing"

# 2. Create hotfix branch (bypasses checkbox validation)
git checkout -b hotfix-database-connection

# 3. Fix and push immediately
# 4. Create PR - merges without checkbox validation
```

## Best Practices

### DO ✅
- Keep requirements in issues clear and specific
- Check off items as you complete them
- Use issue checkboxes as your todo list
- Link every PR to an issue with `Closes: #XXX`

### DON'T ❌
- Add requirement checkboxes to PRs
- Check boxes for work not yet done
- Create PRs without linked issues
- Try to bypass the workflow (except hotfixes)

## Troubleshooting

### "PR must be linked to an issue"
Your PR body must contain `Closes: #123` (or `Fixes:` or `Resolves:`)

### "Issue has unchecked requirements"
Go to the linked issue and check off all completed requirements

### "Can't find the issue"
Make sure the issue number in `Closes: #XXX` is correct

### Workflow not running
Check that your PR is targeting the `main` branch

## 🚀 Deployment Blocking (Vercel Integration)

### Why Block Deployments?
Prevents incomplete or broken features from reaching production when checkboxes are unchecked.

### How Vercel Blocking Works
1. **Vercel Ignore Build Script** (`scripts/deployment/vercel-ignore-build.sh`)
   - Checks PR's linked issue for unchecked boxes
   - Returns exit code 0 (skip) if boxes unchecked
   - Returns exit code 1 (build) if all complete

2. **Configuration in Vercel Dashboard**
   - Go to Project Settings → Git → Ignored Build Step Command
   - Set to: `./scripts/deployment/vercel-ignore-build.sh`
   - Vercel runs this before every deployment

3. **The Flow**
   ```
   Push to PR → Vercel checks script → 
   If unchecked boxes → Skip deployment ❌
   If all checked → Deploy preview ✅
   ```

### Status Reporting
The `status-reporter.yml` workflow ensures GitHub shows proper status:
- Creates "Issue Checkboxes" status on every push
- Shows failure if unchecked boxes exist
- Prevents "Waiting for status to be reported" message

## Technical Details

### Workflow Files
- `.github/workflows/pr-checklist-required.yml` - Blocks PR merge
- `.github/workflows/status-reporter.yml` - Creates commit statuses
- `scripts/deployment/vercel-ignore-build.sh` - Blocks Vercel deployments

### How it finds the issue
```javascript
const issueMatch = pr.body?.match(/(?:Closes|Fixes|Resolves)\s+#(\d+)/i);
```

### How it counts checkboxes
```javascript
const uncheckedBoxes = (issue.body?.match(/- \[ \]/g) || []).length;
const checkedBoxes = (issue.body?.match(/- \[x\]/gi) || []).length;
```

### Branch protection
Configured via GitHub Settings → Branches → Protection Rules

### Vercel configuration
Configured via Vercel Dashboard → Project Settings → Git → Ignored Build Step Command

## Summary

**Remember**: 
- Issues = Planning (what to build) with requirement checkboxes
- PRs = Implementation (what was built) with NO requirement checkboxes
- Check boxes in the ISSUE, not the PR
- The workflow enforces this automatically

This separation keeps our workflow clean, prevents confusion, and ensures all requirements are met before code is merged.