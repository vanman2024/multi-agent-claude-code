# Feature Implementation Tasks

## Project: [Feature Name]
## Swarm Deployment: `swarm /path/to/project "Feature description"`

### Architecture & Analysis
- [ ] T001 @gemini Research current authentication system architecture
- [ ] T002 @gemini Document integration points and dependencies  
- [ ] T003 @gemini Analyze security requirements and constraints

### Performance & Optimization
- [ ] T010 @qwen Profile database query performance for auth endpoints
- [ ] T011 @qwen Optimize user session management algorithms
- [ ] T012 @qwen Implement caching strategy for user permissions

### Frontend Development
- [ ] T020 @codex Create user login/registration components
- [ ] T021 @codex Implement protected route navigation
- [ ] T022 @codex Add user profile management UI

### Integration & Quality (Claude Coordination)
- [ ] T030 @claude Review all agent work and ensure integration
- [ ] T031 @claude Validate security implementation across components
- [ ] T032 @claude Create end-to-end tests for complete auth flow

## Task Assignment Protocol

### How Agents Find Their Tasks
1. **Swarm deployment** automatically finds this file
2. **Extracts tasks** assigned to each agent using @symbol
3. **Deploys agents** with their specific task assignments
4. **Agents mark complete** by changing `[ ]` to `[x]`

### Example Task Completion
```markdown
- [x] T001 @gemini Research current authentication system architecture ✅
  - Analyzed JWT implementation in src/auth/
  - Documented OAuth integration patterns
  - Identified 3 security improvement areas
```

### Agent Responsibilities
- **@gemini**: Analysis, research, documentation, architecture review
- **@qwen**: Performance optimization, algorithm improvement, caching
- **@codex**: Frontend components, UI/UX, React development
- **@claude**: Integration, security review, quality gates, coordination

## Task Dependencies
```markdown
### Sequential Dependencies
- [x] T001 @gemini Research architecture ✅ (must complete first)
- [ ] T010 @qwen Optimize based on T001 findings (depends on T001)
- [ ] T020 @codex Build UI based on T001 design (depends on T001)

### Parallel Tasks (can run simultaneously)
- [ ] T011 @qwen Database optimization
- [ ] T021 @codex Frontend styling  
- [ ] T003 @gemini Security documentation
```

## Swarm Coordination Notes

**Before Deployment:**
1. Create tasks.md with clear @agent assignments
2. Ensure tasks are specific and actionable
3. Include dependencies and priorities

**During Execution:**
1. Monitor agents via: `tail -f /tmp/agent-swarm-logs/*.log`
2. Check task completion in this file
3. Claude coordinates integration as agents complete work

**After Completion:**
1. All `[ ]` should be `[x]` 
2. Integration testing via Claude
3. Quality validation: `./ops/ops qa`