# Slash Command Templates

## Template for Commands WITH MCP Servers

```markdown
---
allowed-tools: mcp__github(*), mcp__supabase(*), mcp__playwright(*), Bash(*), Read(*)
description: [Brief description using MCP servers]
argument-hint: [expected arguments]
---

# [Command Name]

## Context
- Current branch: !`git branch --show-current`
- Project info: @package.json

## Your Task

When user runs `/[command-name] $ARGUMENTS`, use MCP servers to:

### Using GitHub MCP
- Create issues: mcp__github__create_issue
- List PRs: mcp__github__list_pull_requests
- Create PR: mcp__github__create_pull_request

### Using Supabase MCP
- Query database: mcp__supabase__execute_sql
- Insert data: mcp__supabase__insert_data
- Update data: mcp__supabase__update_data

### Using Playwright MCP
- Navigate: mcp__playwright__navigate
- Click: mcp__playwright__click
- Screenshot: mcp__playwright__screenshot

[Add specific MCP operations as needed]
```

## Template for Commands WITHOUT Agents or MCP

```markdown
---
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
description: [Brief description]
argument-hint: [expected arguments]
---

# [Command Name]

## Context
- Current status: !`git status`
- Files: @package.json

## Your Task

When user runs `/[command-name] $ARGUMENTS`, follow these steps:

[Add steps using bash commands and file references]
```

## Template for Commands WITH Agents

```markdown
---
allowed-tools: Task(*), Bash(*), Read(*), Write(*), TodoWrite(*)
description: [Brief description]
argument-hint: [expected arguments]
---

# [Command Name]

## Context
- Current branch: !`git branch --show-current`
- Project info: @package.json

## Your Task

When user runs `/[command-name] $ARGUMENTS`, coordinate these agents:

### Step 1: [First Agent Task]
Use Task tool with:
- subagent_type: [agent-name]
- description: [what to do]
- prompt: [detailed prompt with $ARGUMENTS]

### Step 2: [Second Agent Task]
Use Task tool with:
- subagent_type: [agent-name]
- description: [what to do]
- prompt: [detailed prompt]

[Continue with more agents as needed]
```

## Available Sub-Agents

### Build Agents
- frontend-build - React/Next.js components
- backend-build - Python/FastAPI services
- database-build - PostgreSQL/Supabase schemas
- api-build - REST/GraphQL endpoints
- mobile-build - React Native apps
- ai-build - ML/AI features
- devops-build - CI/CD pipelines

### Testing Agents
- test-writer - Create test suites
- test-runner - Execute tests
- debugger - Fix failures
- mcp-tester - Test MCP servers

### GitHub Agents
- pr-creator - Create pull requests
- issue-analyzer - Analyze GitHub issues
- project-to-issue - Convert features to issues
- issue-to-buildplan - Create build plans

### Workflow Agents
- cleanup-agent - Clean temp files
- workspace-manager - Setup worktrees
- documentation-agent - Generate docs
- enhancement-agent - Improve code
- feature-agent - Coordinate features
- state-manager - Track state
- sdlc-initializer - Initialize SDLC workflow
- deploy-manager - Handle deployments
- workflow-builder - Create GitHub workflows

## Official Claude Syntax

### File References (@)
Include file contents:
```
Review @src/utils/helpers.js
Compare @old.js with @new.js
```

### Bash Commands (!)
Execute with backticks:
```
Current dir: !`pwd`
Git status: !`git status`
Test: !`npm test`
```

### Arguments ($ARGUMENTS)
Pass dynamic values:
```
Process: $ARGUMENTS
Build feature: $ARGUMENTS
```

### Task Tool
For agents:
```
Use Task tool with:
- subagent_type: frontend-build
- description: Build UI
- prompt: Create components for $ARGUMENTS
```

## Examples

### MCP-based Command
```markdown
---
allowed-tools: mcp__supabase(*), Bash(*), Read(*)
description: Sync local schema with Supabase database
argument-hint: [schema-file]
---

# Database Sync

## Context
- Schema file: @$ARGUMENTS
- Current branch: !`git branch --show-current`

## Your Task

Sync the schema from $ARGUMENTS with Supabase:

1. Extract current schema: mcp__supabase__extract_complete_schema
2. Compare with local schema file
3. Apply migration: mcp__supabase__apply_migration
4. Verify: mcp__supabase__execute_sql with "SELECT * FROM information_schema.tables"
```

### Simple Command (no MCP, no agents)
```markdown
---
allowed-tools: Bash(npm test:*), Bash(jest:*), Read(*)
description: Run specific test suites
argument-hint: [test-pattern]
---

# Run Tests

## Context
- Test config: @jest.config.js
- Available tests: !`find . -name "*.test.js" | head -10`

## Your Task
Run tests matching: $ARGUMENTS
```

### Agent-based Command
```markdown
---
allowed-tools: Task(*), Bash(*), TodoWrite(*)
description: Build complete features with multiple agents
argument-hint: [feature-name]
---

# Build Feature

## Context
- Current branch: !`git branch --show-current`

## Your Task
Build feature: $ARGUMENTS

### Step 1: Database Schema
Use Task tool with:
- subagent_type: database-build
- description: Create schema
- prompt: Design schema for feature: $ARGUMENTS

### Step 2: Backend API
Use Task tool with:
- subagent_type: backend-build
- description: Build API
- prompt: Create API endpoints for: $ARGUMENTS

### Step 3: Frontend UI
Use Task tool with:
- subagent_type: frontend-build
- description: Build UI
- prompt: Create React components for: $ARGUMENTS
```