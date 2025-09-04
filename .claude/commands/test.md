---
allowed-tools: Task(*), Bash(*), Read(*), TodoWrite(*), mcp__github(*)
description: Unified testing strategy with intelligent project detection and agent routing
argument-hint: [--frontend|--backend|--unit|--e2e] [options]
---

# Test - Unified Testing Command

## Context
- Current branch: !git branch --show-current
- Repository: vanman2024/multi-agent-claude-code
- Recent commits: !git log --oneline -5
- Changed files: !git diff --name-only HEAD~1

## Your Task

When user runs `/test $ARGUMENTS`, intelligently detect project type and route to appropriate testing agents.

### Step 1: Analyze Context

Parse optional arguments in `$ARGUMENTS`:
- `--frontend` - Run only frontend tests
- `--backend` - Run only backend tests  
- `--unit` - Run only unit tests
- `--e2e` - Run only E2E tests
- `--ci` - Trigger CI pipeline tests
- No arguments - Auto-detect based on recent changes and project structure

**Note**: Flags are optional enhancements. Primary behavior is intelligent detection.

### Step 2: Intelligent Detection

Detect what to test based on:

1. **Recent changes** (if no flags provided):
   !git diff --name-only HEAD~1 | head -20
   - If changes in `src/components`, `pages/`, `*.tsx`, `*.jsx` → Frontend
   - If changes in `api/`, `server/`, `*.py`, `backend/` → Backend
   - If changes in both → Full-stack

2. **Project structure** (fallback):
   !test -f package.json && grep -q -E '"react"|"vue"|"angular"|"svelte"|"next"' package.json && echo "Frontend project detected"
   !test -f requirements.txt && echo "Python backend detected"
   !test -f go.mod && echo "Go backend detected"
   !test -f package.json && grep -q -E '"express"|"fastify"|"nestjs"' package.json && echo "Node backend detected"

3. **Ask user** (if unclear):
   If detection is ambiguous and no flags provided, ask:
   "What type of tests should I run? (frontend/backend/both)"

### Step 3: Route to Testing Agents

Based on detection or flags, use appropriate agents:

#### Frontend Testing (React/Vue/Angular/Next.js)

If frontend testing needed:

Use Task tool with:
- subagent_type: frontend-playwright-tester
- description: Run frontend E2E and component tests
- prompt: |
    Run comprehensive frontend tests for this project:
    1. Check for test files in tests/, e2e/, or __tests__ directories
    2. Run component tests if available (Jest/Vitest)
    3. Run E2E tests using Playwright
    4. Test across multiple browsers if configured
    5. Generate coverage report if available
    6. Report results with pass/fail summary
    
    Test type requested: $ARGUMENTS
    Focus on: ${detected_changes_or_all}

#### Backend Testing (Python/Go/Node.js)

If backend testing needed:

Use Task tool with:
- subagent_type: backend-tester
- description: Run backend API and unit tests
- prompt: |
    Run comprehensive backend tests for this project:
    1. Detect testing framework (pytest/go test/jest/mocha)
    2. Run unit tests for all services and utilities
    3. Run integration tests for API endpoints
    4. Test database operations with proper rollback
    5. Validate API responses and status codes
    6. Generate coverage report if available
    7. Report results with detailed failures
    
    Test type requested: $ARGUMENTS
    Focus on: ${detected_changes_or_all}

#### Full-Stack Testing

If both frontend and backend testing needed:

First, use TodoWrite to plan the testing sequence:
1. Run backend tests first (ensure APIs work)
2. Run frontend unit tests
3. Run E2E tests (depends on backend)

Then execute both agents sequentially:

Use Task tool with:
- subagent_type: backend-tester
- description: Run backend tests first
- prompt: [backend testing prompt above]

After backend tests pass:

Use Task tool with:
- subagent_type: frontend-playwright-tester  
- description: Run frontend tests including E2E
- prompt: [frontend testing prompt above]

### Step 4: CI Pipeline Trigger (if --ci flag)

If `--ci` in arguments:

Get current branch:
!BRANCH=$(git branch --show-current) && echo "Branch: $BRANCH"

Use mcp__github__run_workflow:
- owner: vanman2024
- repo: multi-agent-claude-code
- workflow_id: "ci-cd-pipeline.yml"
- ref: $BRANCH

Then monitor status:
Use mcp__github__get_workflow_run to check status

### Step 5: Report Consolidated Results

After all testing agents complete:

Provide unified summary:
```
📊 Test Results Summary
======================
Frontend: [status from agent]
Backend: [status from agent]
Coverage: [if available]
Duration: [total time]

Failed tests (if any):
- [List failures from agents]

Next steps:
- [Suggestions based on results]
```

Update PR if exists:
!gh pr view --json number -q .number 2>/dev/null && PR_NUMBER=$(gh pr view --json number -q .number)

If PR exists, use mcp__github__add_issue_comment to add test results.

## Error Handling

If detection unclear and no user response:
- Default to running both frontend and backend tests
- Inform user: "Running full test suite. Use flags to specify: /test --frontend or /test --backend"

If agent fails:
- Report which agent failed and why
- Suggest running that specific test type again
- Provide debugging commands

## Implementation Notes

1. **Smart detection** - Look at git diff first, then project structure
2. **Agent routing** - Use proper agents, not inline bash commands
3. **Optional flags** - Flags override auto-detection
4. **Sequential for full-stack** - Backend must pass before E2E
5. **Clear reporting** - Unified results from all agents