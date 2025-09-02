# End-to-End Workflow Testing Plan

## The Complete Development Lifecycle Test

### Phase 1: Template → New Project
- [ ] Clone this template to new repository
- [ ] Run `/project-setup` to initialize
- [ ] Verify all secrets are configured
- [ ] Confirm Vercel project created
- [ ] Check GitHub workflows enabled

### Phase 2: Create Feature Issue
- [ ] Run `/create-issue` 
- [ ] Select "New Feature"
- [ ] Set complexity (test both low and high)
- [ ] Verify issue created with correct labels
- [ ] Check project board placement
- [ ] Confirm NO branch created yet
- [ ] Confirm NO PR created yet

### Phase 3: Local Development Start
- [ ] Run `/work #[issue-number]`
- [ ] Verify pulls latest main first
- [ ] Confirm creates feature branch
- [ ] Check creates draft PR with "Closes #X"
- [ ] Verify issue moves to "In Progress"
- [ ] Confirm local branch tracks remote

### Phase 4: Implementation
- [ ] Make actual code changes
- [ ] Run local tests (`npm test`)
- [ ] Run local lint (`npm run lint`)
- [ ] Commit changes locally
- [ ] Push to remote branch
- [ ] Verify PR updates automatically

### Phase 5: CI/CD Pipeline
- [ ] GitHub Actions runs tests
- [ ] Linting checks pass
- [ ] Type checking passes
- [ ] Preview deployment triggers
- [ ] Vercel bot comments with preview URL
- [ ] Preview environment accessible

### Phase 6: PR Completion
- [ ] Check all PR checkboxes
- [ ] Convert draft to ready
- [ ] Request review (manual or Copilot)
- [ ] Address review feedback
- [ ] All checks pass

### Phase 7: Merge & Deploy
- [ ] Merge PR (squash & merge)
- [ ] Verify issue auto-closes
- [ ] Branch auto-deletes
- [ ] Production deployment triggers
- [ ] Vercel deploys to production
- [ ] Production URL works

### Phase 8: Rollback Test
- [ ] Introduce breaking change
- [ ] Deploy to production
- [ ] Verify rollback procedure
- [ ] Test instant revert in Vercel
- [ ] Confirm previous version restored

## The Gap: Local vs GitHub Development

### Current Problem
When Copilot creates a PR from an issue:
1. It skips local development entirely
2. Works directly on GitHub
3. No local testing happens
4. You can't see/test changes locally

### The Missing Link
We need to bridge:
- **GitHub-only** (Copilot's world)
- **Local-first** (Your development)
- **Hybrid mode** (Both working together)

## Test Scenarios

### Scenario A: Simple Feature (Copilot-friendly)
1. Create issue with complexity 1-2
2. Assign to Copilot
3. Copilot creates PR
4. You pull PR branch locally
5. Test locally
6. Push any fixes
7. Merge when ready

### Scenario B: Complex Feature (Claude Code)
1. Create issue with complexity 3+
2. Use `/work` locally
3. Implement with Claude Code
4. Push changes
5. Test in preview
6. Merge when ready

### Scenario C: Parallel Development
1. Create 2 issues
2. Assign one to Copilot
3. Work on other locally
4. Both create separate PRs
5. No branch conflicts
6. Both merge independently

## Local Testing Environment Setup

### What We Need
```bash
# 1. Actual application code
src/
  components/
  pages/
  api/

# 2. Package.json with scripts
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "test": "jest",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit"
  }
}

# 3. Test files
__tests__/
  unit/
  integration/
  e2e/

# 4. Local environment
.env.local (Git ignored)
.env.test (For test runs)
```

### Template vs Project

**This Repository = TEMPLATE**
- Framework and automation
- GitHub workflows
- Commands and agents
- NO actual application

**After Cloning = PROJECT**
- Your actual application
- Business logic
- User features
- Real deployments

## The Deployment Gap

### What's Missing
1. **No package.json** = Nothing to build
2. **No src/ directory** = No application code
3. **Only index.html** = Static placeholder
4. **No API routes** = No backend to test

### What Happens
- Vercel deploys the static index.html
- No build process runs
- No tests execute (no test files)
- Vercel bot has nothing meaningful to preview

## Action Items

### Immediate Needs
1. Create minimal Next.js app IN THIS REPO for testing
2. Add package.json with test/lint/build scripts
3. Create sample API route
4. Add basic component with test
5. Deploy to Vercel to activate bot

### Then Test
1. Full workflow from issue to deployment
2. Rollback procedure
3. Multiple agents working in parallel
4. Local development with Copilot PRs

## Success Criteria

- [ ] Can create issue and see it through to deployment
- [ ] Local changes sync with GitHub PR
- [ ] Copilot and local development coexist
- [ ] Preview deployments work
- [ ] Production deployments work
- [ ] Rollback works
- [ ] Multiple developers don't conflict
- [ ] Tests run in CI and locally
- [ ] Vercel bot appears in PRs