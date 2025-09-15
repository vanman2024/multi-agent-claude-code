## Multi-Agent Coordination Principles
<!-- Added by Multi-Agent Framework -->

### VI. Agent Autonomy & Coordination
Each AI agent operates independently within its specialized domain; Agents coordinate through standardized interfaces and shared context; No agent can override another's decisions without explicit user approval; Security agent decisions always take precedence

### VII. Context Hierarchy
All agents MUST check and incorporate context in this order: 1) Project Constitution (.specify/memory/constitution.md) - Project-specific rules, 2) CLAUDE.md - General AI assistant instructions, 3) Agent-specific context (.claude/agents/*.md) - Domain expertise, 4) Current project state - Active issues, PRs, dependencies

### VIII. Agent Decision Authority
@claude/system-architect controls architecture, DB schema, API design (can block structural changes); @claude/security-auth-compliance has VETO power for security/auth/compliance (cannot be overridden); @claude/pr-reviewer provides code quality advisory; @claude/backend-tester and @claude/frontend-playwright-tester can block deployment; @claude/code-refactorer requires approval for major changes; @copilot auto-assigned for simple tasks (Complexity ≤2, Size XS-S)

### IX. Testing Requirements (Agent-Enforced)
Backend changes MUST pass API tests (@claude/backend-tester); Frontend changes MUST pass UI tests (@claude/frontend-playwright-tester); Security changes MUST pass security review (@claude/security-auth-compliance); Architecture changes MUST be approved (@claude/system-architect); All tests must pass before deployment

### X. Agent Conflict Resolution
When agents disagree: Security concerns override all other considerations; Architecture decisions win for structural changes; Testing agents can block but not modify code; User makes final decision if deadlock occurs; All conflicts logged for review