# Multi-Agent System Roster

> **Status**: 🟢 IMPLEMENTED
> **Last Updated**: 2025-09-02
> **Stability**: Production Ready

## Available Agents

### 1. GitHub Copilot
**Role:** Simple implementation tasks  
**Auto-triggers:** Complexity 1-2, Size XS-S issues
**Capabilities:**
- Unit test writing
- Simple bug fixes  
- Documentation updates
- Basic refactoring
- Small feature implementation

### 2. General Purpose Agent (`general-purpose`)
**Role:** Complex feature development
**Triggers:** Complexity 3+, Size M+ issues
**Capabilities:**
- Full feature implementation
- Complex bug investigation
- Multi-file refactoring
- Integration work

### 3. Security & Auth Agent (`security-auth-compliance`)
**Role:** Security implementations
**Triggers:** Security, auth, compliance labels
**Capabilities:**
- Authentication systems
- Security audits
- Vulnerability fixes
- Compliance checks
- Input validation

### 4. Frontend Testing Agent (`frontend-playwright-tester`)
**Role:** UI/UX testing
**Triggers:** Frontend changes, UI labels
**Capabilities:**
- E2E testing with Playwright
- Cross-browser testing
- Visual regression
- Accessibility checks

### 5. Backend Testing Agent (`backend-tester`)
**Role:** API and backend testing
**Triggers:** Backend changes, API labels
**Capabilities:**
- API endpoint testing
- Integration tests
- Database testing
- Performance testing

### 6. Code Refactorer (`code-refactorer`)
**Role:** Large-scale refactoring
**Triggers:** Refactor labels, tech debt
**Capabilities:**
- Extract common utilities
- Update deprecated APIs
- Improve code organization
- Remove duplicate code

### 7. System Architect (`system-architect`)
**Role:** Design and architecture
**Triggers:** Design discussions, architecture labels
**Capabilities:**
- Database schema design
- API architecture
- Technology evaluation
- Scalability planning

### 8. Integration Architect (`integration-architect`)
**Role:** Service integrations
**Triggers:** Webhook, integration labels
**Capabilities:**
- Webhook setup
- API integrations
- Event-driven architecture
- Service orchestration

### 9. PR Reviewer (`pr-reviewer`)
**Role:** Code review
**Triggers:** After implementation, before merge
**Capabilities:**
- Security checks
- Code standards
- Best practices
- Performance review

## Agent Selection Logic

```javascript
if (complexity <= 2 && ['XS', 'S'].includes(size)) {
  // Auto-assign to GitHub Copilot
  assign_copilot();
} else {
  // Use Claude Code with appropriate agent
  use_claude_agent(select_by_type());
}
```