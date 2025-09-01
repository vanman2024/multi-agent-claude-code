# Complete Development Flow - Master Reference

## 📚 Document Map

This document ties together all our workflow documentation:

- **[WORKFLOW.md](./drafts/WORKFLOW.md)** - Core issue→PR→merge process
- **[BRANCHING_STRATEGY_IDEAS.md](./approved/BRANCHING_STRATEGY_IDEAS.md)** - Branch naming and management
- **[COPILOT_STRATEGY.md](./wip/COPILOT_STRATEGY.md)** - Agent assignment logic
- **[DEPLOY.md](./wip/DEPLOY.md)** - Deployment process
- **[PROJECT.md](./wip/PROJECT.md)** - Project board automation
- **[GITHUB_WORKFLOWS.md](./wip/GITHUB_WORKFLOWS.md)** - Automation details
- **[CHECKBOXES.md](./wip/CHECKBOXES.md)** - PR checkbox requirements

## 🔄 The Complete Flow

### 🤖 Automated vs Manual
- **Phase 1 (Issue)**: Manual via `/create-issue`
- **Phase 2 (Implementation)**: Manual coding
- **Phase 3 (Testing)**: AUTOMATIC on every PR push
- **Phase 4 (Review)**: Manual approval required
- **Phase 5 (Deploy)**: AUTOMATIC on merge to main

### Phase 1: ISSUE CREATION
**Command**: `/create-issue`
**Docs**: See [WORKFLOW.md](./drafts/WORKFLOW.md#1-issue-planning-phase)

1. **Pull latest** (MANDATORY)
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create issue with metadata**
   - Uses templates from `templates/local_dev/`
   - Adds metadata section for automation:
     ```markdown
     **Priority**: P2
     **Size**: M
     **Points**: 5
     **Goal**: Features
     **Component**: Backend
     **Milestone**: MVP [REQUIRED except bugs]
     ```

3. **Automatic routing**
   - See [COPILOT_STRATEGY.md](./wip/COPILOT_STRATEGY.md)
   - If Size ≤ S AND Complexity ≤ 2 → Copilot
   - Otherwise → Claude Code agents

4. **Project board assignment**
   - See [PROJECT.md](./wip/PROJECT.md)
   - Fields mapped from metadata
   - Sprint assignment if specified

### Phase 2: IMPLEMENTATION
**Command**: `/work #123`
**Docs**: See [WORKFLOW.md](./drafts/WORKFLOW.md#2-pull-request-implementation-phase)

1. **Branch creation** (just-in-time)
   - Format: `type/issue-number-description`
   - See [BRANCHING_STRATEGY_IDEAS.md](./approved/BRANCHING_STRATEGY_IDEAS.md)

2. **Draft PR creation**
   - Links to issue with "Closes #123"
   - Checkboxes auto-added
   - See [CHECKBOXES.md](./wip/CHECKBOXES.md)

3. **Development**
   - All commits go in PR
   - Tests must pass
   - Linting must pass

### Phase 3: TESTING (CI/CD Pipeline)
**Triggers**: AUTOMATIC on:
- PR opened
- PR updated (new commits)
- PR reopened
- Push to main/develop

**Workflow**: [ci-cd-pipeline.yml](./../.github/workflows/ci-cd-pipeline.yml)

1. **Quality Gates** (Stage 1)
   - Linting (ESLint/Flake8)
   - Type checking
   - Code formatting (Prettier)

2. **Unit Tests** (Stage 2)
   - Run test suites
   - Coverage reporting
   - Must pass for merge

3. **Integration Tests** (Stage 3)
   - API endpoint testing
   - Database migrations
   - E2E tests (if configured)

4. **Security Scans** (Stage 4)
   - Dependency vulnerabilities
   - Code security analysis
   - Secret scanning

### Phase 4: REVIEW & MERGE
**Docs**: See [GITHUB_WORKFLOWS.md](./wip/GITHUB_WORKFLOWS.md)

1. **Check all boxes**
   - Implementation complete
   - Tests passing (from CI/CD)
   - Documentation updated
   - See [CHECKBOXES.md](./wip/CHECKBOXES.md)

2. **Convert draft to ready**

3. **Merge** (only if CI/CD passes)
   ```bash
   gh pr merge --squash --delete-branch
   ```

### Phase 5: DEPLOYMENT
**Docs**: See [DEPLOY.md](./wip/DEPLOY.md)

1. **Automatic deployment** (if configured)
   - Triggered on merge to main
   - Vercel preview for PRs
   - Production on main

2. **Manual deployment** (if needed)
   ```bash
   /deploy production
   ```

## 🎯 Key Principles

1. **Issues are planning docs** - NO code, NO branches
2. **PRs contain implementation** - ALL code, ALL commits
3. **Metadata drives automation** - Not labels (except type)
4. **Milestones are REQUIRED** - Except for bugs
5. **Always pull before starting** - Prevent divergence

## 🚀 Quick Commands

```bash
# Start new work
git checkout main && git pull
/create-issue "Feature: Add user authentication"

# Begin implementation
/work #123

# Complete work
gh pr merge --squash --delete-branch

# Deploy (if not automatic)
/deploy production
```

## 🔗 Related Documentation

### Commands
- `/create-issue` - [create-issue.md](./../.claude/commands/create-issue.md)
- `/work` - [work.md](./../.claude/commands/work.md)
- `/deploy` - [deploy.md](./../.claude/commands/deploy.md)

### Workflows
- Issue automation - [issue-to-implementation.yml](./../.github/workflows/issue-to-implementation.yml)
- Project automation - [project-automation.yml](./../.github/workflows/project-automation.yml)
- CI/CD Pipeline - [ci-cd-pipeline.yml](./../.github/workflows/ci-cd-pipeline.yml)

### Templates
- Feature - [feature-template.md](./../templates/local_dev/feature-template.md)
- Bug - [bug-template.md](./../templates/local_dev/bug-template.md)
- Enhancement - [enhancement-template.md](./../templates/local_dev/enhancement-template.md)