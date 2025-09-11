# How We Enhance Spec-Kit

## Spec-Kit Provides (The Foundation)

### Clean Architecture Pattern
```
scripts/ → templates/ → commands/
```

### Workflow Commands
1. `/specify` - Functional requirements (WHAT)
2. `/plan` - Technical approach (HOW)
3. `/tasks` - Task breakdown (STEPS)

### Task Organization
- T001-T010: Infrastructure/Setup
- T011-T028: Tests (TDD)
- T029-T037: Core/Domain
- T038+: Features/UI

## Our Enhancements (Built on Top)

### 1. `/implement` Command (NEW)
Bridges spec-kit tasks to execution:
- Imports tasks from spec-kit
- Loads into TodoWrite for tracking
- Routes to appropriate agents
- Tracks progress visually

### 2. Agent Routing
Spec-kit generates tasks → We route them:
- Simple tasks → Direct execution
- Complex tasks → Claude Code agents
- Documentation → Gemini CLI
- Architecture → OpenAI CLI
- Code review → Codex CLI

### 3. GitHub Integration
- Convert tasks to GitHub issues
- Create PRs automatically
- Track task completion in issues
- Link commits to tasks

### 4. Hooks System (Coming)
- Pre-task validation
- Post-task verification
- Commit reminders
- Session tracking

### 5. Sub-Agents (Coming)
- backend-tester
- frontend-playwright-tester
- security-auth-compliance
- system-architect
- code-refactorer

## The Combined Workflow

```mermaid
graph LR
    A[/specify] --> B[Functional Spec]
    B --> C[/plan]
    C --> D[Technical Plan]
    D --> E[/tasks]
    E --> F[Task List T001-T052]
    F --> G[/implement]
    G --> H[TodoWrite]
    H --> I[Agent Routing]
    I --> J[Execution]
    J --> K[GitHub Issues/PRs]
```

## Key Principles

### What Spec-Kit Does Well
- Structured specification process
- Clean task generation
- Infrastructure-first approach
- TDD methodology

### What We Add
- Visual progress tracking (TodoWrite)
- Intelligent agent routing
- GitHub workflow automation
- Multiple AI CLI integration
- Hooks and monitoring

### What We DON'T Change
- Spec-kit's core workflow
- Task numbering system (T001-T052)
- Directory structure
- Template system

## Example: Building a Feature

### Step 1: Spec-Kit Foundation
```bash
/specify Build a photo gallery with albums
/plan Use Next.js and Supabase
/tasks
# Generates T001-T052 in specs/001-photo-gallery/tasks.md
```

### Step 2: Our Enhancement
```bash
/implement 001-photo-gallery
# Loads tasks into TodoWrite
# Routes T001-T010 to infrastructure agent
# Routes T011-T028 to test agent
# Tracks progress visually
```

### Step 3: Execution
```bash
# Infrastructure first (automatic)
codex exec "Create Next.js project structure"
codex exec "Setup Supabase connection"

# Tests next (TDD)
gemini -p "Generate test suite for photo gallery"

# Implementation
/work T029  # Our system handles the rest
```

## Configuration Alignment

### Spec-Kit Uses
- `memory/constitution.md` - Project principles
- `scripts/*.sh` - Automation scripts
- `templates/*.md` - Document templates
- `specs/*/` - Feature specifications

### We Add
- `.claude/agents/` - Specialized agents
- `.claude/hooks/` - Event handlers
- `.github/workflows/` - CI/CD
- `spec-kit-docs/` - Reference documentation

## The Beauty of This Approach

1. **Clean Separation**: Spec-kit handles planning, we handle execution
2. **No Conflicts**: Our enhancements don't modify spec-kit's core
3. **Best of Both**: Spec-kit's structure + our automation
4. **Extensible**: Easy to add more agents/hooks/integrations

## Summary

Spec-kit is the **brain** (planning and structure)
Our framework is the **nervous system** (execution and coordination)
Together they create a complete development system!