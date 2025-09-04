---
allowed-tools: Bash(*), Read(*), Task(*), mcp__github(*)
description: Unified testing strategy with intelligent project detection
argument-hint: [--frontend|--backend|--unit|--e2e] [options]
---

# Test - Unified Testing Command

## Context
- Current branch: !git branch --show-current
- Repository: vanman2024/multi-agent-claude-code

## Your Task

When user runs `/test $ARGUMENTS`, intelligently detect project type and run appropriate tests.

### Parse Optional Arguments

Check `$ARGUMENTS` for optional flags:
- `--frontend` - Run only frontend tests
- `--backend` - Run only backend tests
- `--unit` - Run only unit tests  
- `--e2e` - Run only E2E tests
- `--ci` - Trigger CI pipeline tests
- No arguments - Auto-detect and run all relevant tests

**Note**: Flags are optional enhancements. Primary behavior is auto-detection.

### Step 1: Auto-Detect Project Type

Detect what type of project this is:

!echo "🔍 Detecting project type..."

Check for frontend indicators:
!test -f package.json && grep -q -E '"react"|"vue"|"angular"|"svelte"|"next"' package.json && echo "✓ Frontend: JavaScript/TypeScript detected"

Check for backend indicators:
!test -f requirements.txt && echo "✓ Backend: Python detected"
!test -f go.mod && echo "✓ Backend: Go detected"
!test -f package.json && grep -q -E '"express"|"fastify"|"nestjs"|"koa"' package.json && echo "✓ Backend: Node.js detected"

Check for full-stack:
!test -f package.json && test -f requirements.txt && echo "✓ Full-stack: Multiple technologies detected"

### Step 2: Route to Appropriate Testing

Based on detection and arguments, determine test approach:

#### Frontend Testing (React/Vue/Angular)

If frontend detected or `--frontend` flag:
- For E2E tests: Use Task tool with frontend-playwright-tester agent
- For unit tests: !npm test or !npm run test:unit
- For all: Both unit and E2E

!test -f package.json && npm list playwright >/dev/null 2>&1 && echo "📋 Playwright available for E2E testing"

#### Backend Testing (Python/Go/Node)

If backend detected or `--backend` flag:
- Python: !pytest or !python -m pytest
- Go: !go test ./...
- Node.js: !npm test or !jest

!which pytest >/dev/null 2>&1 && echo "📋 Pytest available for Python testing"
!which go >/dev/null 2>&1 && echo "📋 Go test available"

#### Full-Stack Testing

If both frontend and backend detected:
1. Run backend tests first
2. Then run frontend tests
3. Finally run E2E tests

### Step 3: Execute Tests Based on Detection

#### For Frontend Projects

!echo "🧪 Running frontend tests..."

Unit tests:
!test -f package.json && npm test 2>&1 | head -50

E2E tests (if not unit-only):
Use Task tool:
```
prompt: Run E2E tests using Playwright for the frontend application. Check for test files in tests/ or e2e/ directories. Run all browser tests and report results.
subagent_type: frontend-playwright-tester
description: Run frontend E2E tests
```

#### For Backend Projects  

!echo "🧪 Running backend tests..."

Python projects:
!test -f requirements.txt && pytest -v --tb=short 2>&1 | head -50

Node.js projects:
!test -f package.json && grep -q '"express"' package.json && npm test 2>&1 | head -50

Go projects:
!test -f go.mod && go test -v ./... 2>&1 | head -50

#### For Full-Stack Projects

!echo "🧪 Running full-stack test suite..."

Run both backend and frontend tests sequentially.

### Step 4: CI Pipeline Trigger (if --ci flag)

If `--ci` in arguments:

Get current branch:
!BRANCH=$(git branch --show-current) && echo "Branch: $BRANCH"

Trigger CI workflow using mcp__github__run_workflow:
- workflow_id: "ci-cd-pipeline.yml"
- ref: current branch
- Monitor status and report results

### Step 5: Report Results

Parse test output and provide summary:

!echo "
📊 Test Summary
==============="

Check for test results:
!test -f coverage/lcov-report/index.html && echo "📈 Coverage report: coverage/lcov-report/index.html"
!test -f htmlcov/index.html && echo "📈 Coverage report: htmlcov/index.html"

### Step 6: Update PR Status (if applicable)

Check if on PR branch:
!gh pr view --json number -q .number 2>/dev/null && PR_EXISTS=true

If PR exists, add test results comment using mcp__github__add_issue_comment

## Output Examples

### Success Output
```
🔍 Detecting project type...
✓ Frontend: React/Next.js detected
✓ Backend: Node.js/Express detected
📋 Running full-stack test suite...

Frontend Tests:
  ✓ Component tests: 15/15 passed
  ✓ E2E tests: 8/8 passed

Backend Tests:
  ✓ Unit tests: 42/42 passed
  ✓ Integration tests: 12/12 passed

✅ All tests passed!
```

### With Optional Flags
```
$ /test --backend
🔍 Running backend tests only...
✓ Unit tests: 42/42 passed
✓ Integration tests: 12/12 passed
✅ Backend tests passed!
```

## Error Handling

If detection fails:
!echo "⚠️ Could not auto-detect project type. Please specify: /test --frontend or /test --backend"

If tests fail:
- Show failing test names
- Suggest re-running with verbose output
- Provide debugging tips

## Implementation Notes

1. **NO code blocks** - Use `!` syntax for all bash commands
2. **Auto-detection is primary** - Flags are optional overrides
3. **Use Task tool for complex testing** - Especially E2E tests
4. **Support multiple frameworks** - Jest, Pytest, Go test, etc.
5. **Clear output** - Show what's being tested and results