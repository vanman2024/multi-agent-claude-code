## Multi-Agent Coordination Principles
<!-- Added by Multi-Agent Framework -->

### VI. Agent Autonomy & Coordination
Each AI agent operates independently within its specialized domain; Agents coordinate through standardized interfaces and shared context; No agent can override another's decisions without explicit user approval; Security agent decisions always take precedence

### VII. Context Hierarchy
All agents MUST check and incorporate context in this order: 1) Project Constitution (.specify/memory/constitution.md) - Project-specific rules, 2) CLAUDE.md - General AI assistant instructions, 3) Agent-specific context (.claude/agents/*.md) - Domain expertise, 4) Current project state - Active issues, PRs, dependencies

### VIII. Agent Decision Authority
@claude controls backend architecture, API design, Python/pytest testing (testing/backend/); @copilot controls frontend development, UI/UX, Playwright testing (testing/frontend/); @claude/security-auth-compliance has VETO power for security/auth/compliance (cannot be overridden); @claude/pr-reviewer provides code quality advisory; @claude/code-refactorer requires approval for major changes; @copilot auto-assigned for simple tasks (Complexity ≤2, Size XS-S)

### IX. Dual Testing Architecture (Agent-Enforced)
**Backend Testing** (@claude): Python/pytest in testing/backend/ for API logic, data processing, integrations; Contract testing for external APIs; Performance and load testing; **Frontend Testing** (@copilot): Playwright/TypeScript in testing/frontend/ for UI, E2E, visual regression, accessibility; Smart E2E strategy (5-10% critical journeys, 90-95% other test types); WCAG 2.1 AA compliance mandatory; **Ops Integration**: ./devops/ops/ops qa --backend, --frontend, --all for quality gates; All tests must pass before deployment

### X. Agent Conflict Resolution
When agents disagree: Security concerns override all other considerations; Architecture decisions win for structural changes; Testing agents can block but not modify code; User makes final decision if deadlock occurs; All conflicts logged for review