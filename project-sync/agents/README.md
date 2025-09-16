# Solo Developer AI Agent Team

## Personal AI Development Partners (@Symbol Coordination)

This directory contains context files for each AI agent in your personal development toolkit using the @symbol coordination pattern for individual productivity.

### Your AI Development Partners

#### @claude (CTO-Level Engineering Reviewer & Strategic Guide)
- **File**: `CLAUDE.md`
- **Role**: Strategic technical leadership, architecture decisions, quality gates
- **Specialization**: Complex integration, security reviews, architectural oversight
- **Subagents**: general-purpose, code-refactorer, pr-reviewer, backend-tester, integration-architect, system-architect, security-auth-compliance, frontend-playwright-tester
- **Usage**: Via subscription (use strategically for critical decisions)

#### @copilot (GitHub Copilot - Fast Development Implementation)
- **File**: `.github/copilot-instructions.md` (not in agents folder)
- **Powered By**: Grok AI + Claude Sonnet models
- **Role**: Fast development implementation across all complexity levels
- **Integration**: VS Code GitHub Copilot interface
- **Cost**: FREE with GitHub Pro

#### @codex (OpenAI Codex - FRONTEND ONLY Specialist)
- **File**: `AGENTS.md`
- **Role**: FRONTEND EXCLUSIVE - React, UI/UX, frontend testing
- **Specialization**: React components, styling, frontend state, accessibility
- **Restriction**: NEVER handles backend work (that's other agents' domain)
- **Cost**: Via API

#### @gemini (Google Gemini - Analysis & Documentation Specialist)
- **File**: `GEMINI.md`
- **Dual Models**:
  - Gemini 2.5 Pro (OAuth): 1000 req/day FREE
  - Gemini 2.0 Flash Exp (API): ~1000+ req/day FREE experimental
- **Specialization**: Large codebase analysis (2M context), bulk documentation
- **Combined Capacity**: ~2000+ requests/day between both models
- **Cost**: Both models currently FREE

#### @qwen (Qwen CLI - Performance Optimization Specialist)
- **File**: `QWEN.md`
- **Access**: CLI-based interface (NOT Ollama)
- **Capacity**: 2000 req/day FREE (OAuth)
- **Specialization**: Performance optimization, algorithm improvement, everyday development
- **Cost**: FREE via OAuth login
### Task Assignment (@Symbol Coordination System)

The @symbol system is our revolutionary coordination pattern - simple, universal, and incredibly effective.

#### Task Format in specs/*/tasks.md:
```markdown
### Backend Tasks
- [ ] T010 @claude Design database schema architecture
- [ ] T011 @copilot Implement user authentication endpoints
- [ ] T012 @qwen Optimize database query performance

### Frontend Tasks  
- [ ] T020 @codex Create responsive dashboard component
- [ ] T021 @codex Implement user profile UI
- [ ] T022 @codex Add form validation components

### Analysis Tasks
- [ ] T030 @gemini Research caching strategies
- [ ] T031 @gemini Document API endpoints
- [x] T032 @gemini Performance analysis complete ✅

### Coordination Tasks
- [ ] T040 @claude Review and integrate all components
- [ ] T041 @claude Validate system architecture
```

#### Task Completion Protocol:
1. **Find your assignments**: `grep "@agent" specs/*/tasks.md`
2. **Complete the work** according to your specialization
3. **Mark complete**: Change `[ ]` to `[x]` and add ✅
4. **Commit with reference**: Include task number in commit message

### Updating Agent Context

Use the update script to keep agent context current:

```bash
# Update all agent contexts
./scripts/update-agent-context.sh all

# Update specific agent
./scripts/update-agent-context.sh claude
./scripts/update-agent-context.sh gemini
```

### Agent Communication

Agents coordinate through:
- **Task dependencies**: `(depends on T001)`
- **Shared memory**: MCP memory server
- **Git commits**: Standardized commit messages with agent identity
- **Issue comments**: Progress updates and coordination

