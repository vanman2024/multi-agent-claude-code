# Agent System Documentation

## Overview
Multi-agent orchestration system using Claude Code agents + GitHub Copilot for complete development automation.

## Agent Roster

### 1. GitHub Copilot
**Role:** Simple implementation tasks
**Triggers:** Complexity 1-2, Size XS-S issues
**Capabilities:**
- Unit test writing
- Simple bug fixes
- Documentation updates
- Basic refactoring
- Small feature implementation

### 2. General Purpose Agent
**Role:** Complex feature development
**Triggers:** Complexity 3+, Size M+ issues
**Capabilities:**
- Full feature implementation
- Complex bug investigation
- Multi-file refactoring
- Integration work

### 3. Security & Auth Agent
**Role:** Security implementations
**Triggers:** Security, auth, compliance labels
**Capabilities:**
- Authentication systems
- Security audits
- Vulnerability fixes
- Compliance checks
- Input validation

### 4. Frontend Testing Agent
**Role:** UI/UX testing
**Triggers:** Frontend changes, UI labels
**Capabilities:**
- E2E testing with Playwright
- Cross-browser testing
- Visual regression
- Accessibility checks

### 5. Backend Testing Agent
**Role:** API and backend testing
**Triggers:** Backend changes, API labels
**Capabilities:**
- API endpoint testing
- Integration tests
- Load testing
- Database testing

### 6. Code Refactoring Agent
**Role:** Code improvement
**Triggers:** Refactor labels, technical debt
**Capabilities:**
- Large-scale refactoring
- Performance optimization
- Code standardization
- Dependency updates

### 7. System Architecture Agent
**Role:** Design decisions
**Triggers:** Architecture labels, design docs
**Capabilities:**
- Database schema design
- API architecture
- System design docs
- Technology selection

### 8. Integration Architect Agent
**Role:** Service integration
**Triggers:** Integration labels, webhooks
**Capabilities:**
- Webhook setup
- API integrations
- Event-driven architecture
- Service orchestration

## Orchestration Strategy

### Assignment Rules
```javascript
// Simplified routing logic
if (complexity <= 2 && size in ['XS', 'S']) {
  assign_to: 'GitHub Copilot'
} else if (labels.includes('security')) {
  assign_to: 'Security Agent'
} else if (labels.includes('architecture')) {
  assign_to: 'System Architecture Agent'
} else {
  assign_to: 'General Purpose Agent'
}
```

### Workflow Integration
1. Issue created → Auto-assign based on complexity/labels
2. Agent works → Creates feature branch
3. Implementation → Opens PR
4. Review → Human or Copilot review
5. Merge → Deploy

## MCP Tool Access

All agents have access to:
- Read, Write, Edit, MultiEdit
- Bash, TodoWrite
- Task (for sub-agents)
- mcp__github (for GitHub operations)

Specialized access:
- Frontend Testing: mcp__playwright, mcp__browserbase
- Backend Testing: Database tools, API testing
- Security: Auth configuration tools
- Integration: Webhook, event bus tools

## Implementation Status

### Currently Active
- General Purpose Agent (via Task tool)
- GitHub Copilot (manual assignment needed)

### To Be Implemented
- Automated agent assignment in workflows
- Agent performance tracking
- Agent collaboration patterns
- Agent handoff procedures

## Best Practices

### DO
- Let Copilot handle simple tasks first
- Use specialized agents for their domains
- Chain agents for complex workflows
- Track agent performance metrics

### DON'T
- Assign architecture to Copilot
- Skip agent specialization
- Mix agent responsibilities
- Bypass review process

## Future Enhancements
- Agent learning/improvement loops
- Cross-agent collaboration
- Automatic agent selection refinement
- Performance-based routing