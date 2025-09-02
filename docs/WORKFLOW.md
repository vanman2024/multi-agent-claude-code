# Complete Development Workflow

## 🚀 Quick Start

```bash
# 1. Create an issue (ALWAYS start here)
/create-issue feature "Add user authentication"

# 2. Start work (creates branch + draft PR)
/work #123

# 3. Implement, test, commit
# 4. Check off requirements in ISSUE (not PR)
# 5. Mark PR as ready
# 6. Merge when approved
```

## 📐 Architecture Overview

### The House Metaphor 🏗️
Our system is like building a house with distinct layers:

1. **Foundation** (Database) - Core data structures
2. **Plumbing** (GitHub Workflows) - Moves things, no intelligence
3. **Framing** (Backend/APIs) - Structural support
4. **Electrical** (AI Agents) - Intelligence and decisions
5. **Finishes** (Frontend) - User interface
6. **Smart Home** (Project Board) - Status monitoring

**Key Principle**: Plumbing (workflows) doesn't think - it just moves. Intelligence comes from agents.

## 🔄 The Complete Workflow

### Phase 1: Planning (Issues)

#### Step 1: Sync with Latest
```bash
# ALWAYS start from main with latest changes
git checkout main
git pull origin main
```

#### Step 2: Create Issue
```bash
/create-issue [type] "Clear description"
```

Types:
- `feature` - New functionality
- `bug` - Something broken
- `enhancement` - Improve existing
- `refactor` - Code cleanup
- `task` - Simple work item
- `hotfix` - Critical emergency fix

The issue will include:
- Requirement checkboxes (what needs to be done)
- Metadata (complexity, size, priority)
- Auto-assignment to Copilot (if simple) or Claude Code (if complex)

### Phase 2: Implementation (Pull Requests)

#### Step 3: Start Work
```bash
# Creates branch and draft PR automatically
/work #123
```

This command:
1. Verifies you're on main with latest
2. Creates feature branch
3. Creates draft PR with `Closes: #123`
4. Updates issue status to in-progress

#### Step 4: Development
- Make changes
- Commit with meaningful messages
- Check off requirements in the ISSUE as completed
- Run tests: `npm test` or `pytest`
- Run linting: `npm run lint`

#### Step 5: Finalize PR
- Ensure all issue checkboxes are checked
- Update PR description with implementation details
- Convert draft to ready for review
- Request reviews if needed

### Phase 3: Merge & Deploy

#### Step 6: Automated Validation
The `pr-checklist-required.yml` workflow:
1. Finds linked issue from `Closes: #XXX`
2. Verifies all requirement checkboxes are complete
3. Blocks merge if requirements incomplete

#### Step 7: Merge
```bash
gh pr merge --squash --delete-branch
```

This:
- Merges the PR
- Auto-closes the linked issue
- Deletes the feature branch
- Triggers deployment (if configured)

#### Step 8: Post-Merge
```bash
# MANDATORY: Pull latest after ANY merge
git checkout main
git pull origin main
```

## 🤖 Agent Assignment Logic

### Copilot vs Claude Code

**Copilot handles** (BOTH conditions must be true):
- Complexity: 1-2 (out of 5)
- Size: XS or S

**Claude Code handles**:
- Complexity: 3+ OR
- Size: M+ OR
- Has security/architecture labels

### Assignment Matrix

| Task | Complexity | Size | Agent | Why |
|------|------------|------|-------|-----|
| Fix typo | 1 | XS | Copilot | Simple & small |
| Add API endpoint | 2 | S | Copilot | Simple & small |
| Refactor module | 2 | L | Claude | Too large |
| Design auth system | 4 | M | Claude | Too complex |
| Security audit | 5 | XL | Claude | Critical complexity |

## 🏷️ Labels & Metadata

### Issue Labels
- **Type**: `bug`, `feature`, `enhancement`, `refactor`, `task`
- **Status**: `status:in-progress`, `blocked`
- **Sprint**: `sprint:current`
- **Special**: `hotfix`, `security`, `architecture`

### Issue Metadata (in body)
```markdown
## Metadata
**Priority**: P0/P1/P2/P3
**Size**: XS/S/M/L/XL
**Complexity**: 1-5
**Points**: 1-13
```

## 📋 Checkboxes: Issues vs PRs

### Issues Have Requirements
```markdown
## Fix Requirements
- [ ] Reproduce the issue
- [ ] Identify root cause
- [ ] Implement fix
- [ ] Add regression test
```

### PRs Have NO Requirements
PRs only describe what was implemented, not requirements.

**Why?** Single source of truth. Check boxes in issues, describe implementation in PRs.

## 💡 Work in Progress Pattern

You don't have to finish everything at once! PRs can stay open as you work:

### Multi-Day Development Example
```bash
# Day 1: Start work
/create-issue feature "Add user authentication"
/work #120
# Creates branch: feature-120-user-auth
# Creates DRAFT PR linked to issue #120
git add . && git commit -m "WIP: Started auth setup"
git push

# Day 2: Continue work
git checkout feature-120-user-auth  # Just checkout same branch!
# Do more work...
git add . && git commit -m "feat: Add login endpoint"
git push  # Updates the same PR

# Day 5: Add tests
git checkout feature-120-user-auth
git add . && git commit -m "test: Add auth tests"
git push  # Still updating same PR

# Day 7: Finally ready
# Check all boxes in issue #120
gh pr ready  # Convert from draft to ready
gh pr merge --squash  # NOW merge
```

### Multiple Active PRs
```bash
# You can have several PRs in progress:
# PR #121 - Working on auth (feature-120-auth branch)
# PR #122 - Fixing bug (bug-125-login branch)  
# PR #123 - Adding docs (task-130-docs branch)

# Switch between them:
git checkout feature-120-auth  # Work on auth
git checkout bug-125-login     # Switch to bug fix
git checkout task-130-docs     # Switch to docs
```

### Benefits
- **PR is your "save point"** - All work backed up on GitHub
- **Others can see progress** - PR shows what you're working on
- **CI runs on each push** - Tests run, catching issues early
- **No local accumulation** - Everything pushed, no drift
- **Easy context switching** - Just checkout different branch

## 🚨 Hotfix Process

For critical production issues:

```bash
# 1. Create hotfix issue
/create-issue hotfix "Database connection failing"

# 2. Create hotfix branch (bypasses validation)
git checkout -b hotfix-database-fix

# 3. Fix, test, push
git push origin hotfix-database-fix

# 4. Create PR (auto-bypasses checkbox validation)
gh pr create --title "HOTFIX: Database connection"
```

## 🔄 Synchronization Points

### MANDATORY Pull Points
**ALWAYS** run `git pull` at these times:

1. **Before creating any issue** - Start fresh
2. **After ANY PR merges** - Stay synced
3. **Before running /work** - Start from latest
4. **Before making commits** - Avoid conflicts
5. **Start of each session** - Always begin fresh

### Why This Matters
- Copilot works in GitHub (remote)
- You work locally
- Without pulling, you work on OLD code
- Results in conflicts and duplicate work

## 📊 Project Board Integration

### Automatic Updates
GitHub Actions automatically:
- Move issues to "In Progress" when PR created
- Move to "In Review" when PR ready
- Move to "Done" when PR merged
- Update sprint progress

### Manual Updates
You handle:
- Adding issues to sprints
- Setting milestones
- Priority adjustments

## 🧪 Testing Requirements

### Before Marking PR Ready
```bash
# TypeScript/JavaScript projects
npm test
npm run lint
npm run typecheck

# Python projects
pytest
ruff check
mypy .
```

### CI/CD Pipeline
1. Tests run on every push
2. Linting checks code style
3. Type checking validates types
4. Coverage reports generated
5. Deploy preview created (Vercel)

## 🚫 Common Mistakes to Avoid

### DON'T
- Create PR without issue first (except minor doc updates)
- Work without being on latest main
- Check boxes in PRs (only in issues)
- Skip tests before marking ready
- Merge without all checks passing
- Forget to pull after merges

### DO
- Always start with an issue (except for typos/examples)
- Keep main branch updated
- Use draft PRs while working
- Check requirements in issues
- Run tests locally first
- Document your changes

### When Full Workflow is Optional

**Direct updates OK for:**
- Fixing typos or grammar
- Adding examples to docs
- Clarifying existing documentation  
- Updating code comments
- Formatting improvements (no logic changes)

**Full workflow REQUIRED for:**
- Any functional changes
- New features or enhancements
- Bug fixes
- Refactoring code
- Adding/removing files
- Configuration changes

## 🛠️ Slash Commands Reference

### /create-issue
```bash
/create-issue [type] "title"
```
Creates issue with requirements, metadata, and auto-assigns to appropriate agent.

### /work
```bash
/work [#issue]           # Work on specific issue
/work                    # Auto-select next priority
/work --test            # Run test suite
/work --deploy          # Deploy to production
```

### Other Commands
- `/pr-review` - Request code review
- `/copilot-review` - Request Copilot review
- `/build-feature` - Build complete feature

## 📈 Complexity & Size Guide

### Complexity Levels
1. **Trivial** - Copy existing pattern exactly
2. **Simple** - Minor variations of existing code
3. **Moderate** - Multiple components, clear approach
4. **Complex** - Architectural decisions needed
5. **Very Complex** - Novel solutions, research required

### Size Estimates
- **XS**: < 1 hour
- **S**: 1-4 hours
- **M**: 1-2 days
- **L**: 3-5 days
- **XL**: > 1 week

## 🔍 Validation & Checks

### Required Status Checks
1. **Require Issue Checkboxes Complete** - All requirements done
2. **Run Tests** - All tests passing
3. **Vercel Deploy** - Preview deployment successful

### Branch Protection
- No direct pushes to main
- Require PR reviews (optional)
- Require status checks to pass
- Require branches to be up to date

## 📚 Related Documentation

- [CHECKBOXES.md](./CHECKBOXES.md) - Detailed checkbox workflow
- [CLAUDE.md](./CLAUDE.md) - AI assistant instructions
- [MCP_SERVERS_GUIDE.md](./MCP_SERVERS_GUIDE.md) - MCP server setup
- [.github/COPILOT-WORKFLOW.md](./.github/COPILOT-WORKFLOW.md) - Copilot integration

## 💡 Pro Tips

1. **Use TodoWrite** - Track complex tasks with Claude's todo list
2. **Batch Reviews** - Review multiple small PRs together
3. **Sprint Planning** - Keep sprint size to ~10 issues
4. **Quick Wins** - Start sprints with XS tasks for momentum
5. **Dependencies** - Use "Depends on #XX" in issue body
6. **Templates** - Customize issue templates for your needs

## 🆘 Troubleshooting

### "PR must be linked to an issue"
Add `Closes: #123` to PR body

### "Issue has unchecked requirements"
Check off all boxes in the linked issue

### "Cannot push to main"
Never push directly to main - always use PRs

### "Merge blocked"
Check that all required status checks are passing

### "Conflicts with main"
```bash
git checkout main
git pull origin main
git checkout your-branch
git rebase main
# Resolve conflicts
git push --force-with-lease
```

## 📝 Summary

**The Golden Path**:
1. Issue first (planning)
2. Then PR (implementation)
3. Check requirements in issue
4. Merge when complete
5. Always stay synced with main

**Remember**: This workflow ensures quality, prevents confusion, and maintains a clean git history. Follow it consistently for best results.