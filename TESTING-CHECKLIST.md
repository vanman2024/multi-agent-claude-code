# Testing Checklist for Multi-Agent Development Framework

## Pre-Deployment Testing

### 1. Agent Assignment Tests
- [ ] Create issue with Complexity=1, Size=XS → Verify Copilot assigned
- [ ] Create issue with Complexity=2, Size=S → Verify Copilot assigned  
- [ ] Create issue with Complexity=2, Size=M → Verify Claude handles (size too large)
- [ ] Create issue with Complexity=3, Size=XS → Verify Claude handles (too complex)
- [ ] Create issue with Complexity=5, Size=XL → Verify Claude handles

### 2. Workflow Automation Tests
- [ ] Issue creation triggers draft PR creation
- [ ] PR links back to original issue
- [ ] Project board updates when issue assigned
- [ ] Blocking issues prevent dependent PRs
- [ ] Labels are restricted to the 8 allowed types

### 3. Slash Command Tests
- [ ] `/create-feature` creates issue with correct fields
- [ ] `/deploy` deploys to DigitalOcean (backend) and Vercel (frontend)
- [ ] `/test` runs appropriate test suite
- [ ] `/setup-project` initializes new cloned repository

### 4. CI/CD Pipeline Tests
- [ ] Push to feature branch triggers CI tests
- [ ] CI blocks merge if tests fail
- [ ] Backend changes trigger backend deployment (after merge)
- [ ] Frontend changes trigger frontend deployment (after merge)
- [ ] Infrastructure issues block feature deployments

### 5. MCP Server Integration Tests
- [ ] GitHub MCP server authenticates properly
- [ ] Supabase MCP server connects to project
- [ ] Playwright MCP server can navigate pages
- [ ] File system MCP server has correct permissions

### 6. Project Setup Tests (For Cloned Repos)
- [ ] Clone creates new repository with framework
- [ ] GitHub secrets are set correctly
- [ ] Supabase project is created
- [ ] Vercel project is linked
- [ ] DigitalOcean functions are deployed
- [ ] Project board is created with correct fields

### 7. Agent Collaboration Tests
- [ ] Copilot PRs are reviewed by Claude Code
- [ ] No duplicate work on same issue
- [ ] Agents respect assignment boundaries
- [ ] PR merges update project board

## Test Execution Commands

```bash
# Run local tests
npm test
npm run lint
npm run typecheck

# Trigger CI pipeline
git push origin feature/test-branch

# Test deployment
claude /deploy --env staging

# Test agent assignment
claude /create-feature --complexity 1 --size XS --title "Test task"

# Verify project board
gh project item-list 1 --owner vanman2024
```

## Success Criteria

- [ ] All automated tests pass
- [ ] No manual intervention required for standard workflows
- [ ] Agents correctly assigned based on complexity/size
- [ ] Deployments successful to all environments
- [ ] Project board accurately reflects work status
- [ ] No duplicate issues or PRs created
- [ ] All slash commands execute without errors