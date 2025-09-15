## Multi-Agent Coordination Principles

### VIII. Agent Autonomy & Coordination
- Each AI agent operates independently within its specialized domain
- Agents coordinate through standardized interfaces and shared context
- No agent can override another's decisions without explicit user approval
- Security agent decisions always take precedence

### IX. Context Hierarchy
All agents MUST check and incorporate context in this order:
1. **Project Constitution** (.specify/memory/constitution.md) - Project-specific rules
2. **CLAUDE.md** - General AI assistant instructions
3. **Agent-specific context** (.claude/agents/*.md) - Domain expertise
4. **Current project state** - Active issues, PRs, dependencies

### X. Agent Decision Authority

| Agent | Domain | Authority Level |
|-------|--------|----------------|
| @claude/system-architect | Architecture, DB schema, API design | Can block structural changes |
| @claude/security-auth-compliance | Security, auth, compliance | VETO power - cannot be overridden |
| @claude/pr-reviewer | Code quality, standards | Advisory only |
| @claude/backend-tester | API testing, validation | Can block deployment |
| @claude/frontend-playwright-tester | UI testing, E2E | Can block deployment |
| @claude/code-refactorer | Large refactoring | Requires approval for major changes |
| @copilot | Simple tasks (Complexity ≤2, Size XS-S) | Auto-assigned for small work |

### XI. Testing Requirements (Agent-Enforced)
- Backend changes MUST pass API tests (@claude/backend-tester)
- Frontend changes MUST pass UI tests (@claude/frontend-playwright-tester)
- Security changes MUST pass security review (@claude/security-auth-compliance)
- Architecture changes MUST be approved (@claude/system-architect)
- All tests must pass before deployment

### XII. Agent Conflict Resolution
When agents disagree:
1. Security concerns override all other considerations
2. Architecture decisions win for structural changes
3. Testing agents can block but not modify code
4. User makes final decision if deadlock occurs
5. All conflicts logged for review