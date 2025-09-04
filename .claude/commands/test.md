---
allowed-tools: Task(*), Bash(*), Read(*), TodoWrite(*), mcp__github(*)
description: Unified testing strategy with intelligent project detection and agent routing
argument-hint: [--quick|--create|--frontend|--backend|--unit|--e2e] [options]
---

# Test - Unified Testing Command

## Context
- Current branch: !git branch --show-current
- Repository: vanman2024/multi-agent-claude-code
- Recent commits: !git log --oneline -5
- Changed files: !git diff --name-only HEAD~1

## Your Task

When user runs `/test $ARGUMENTS`, intelligently detect project type and route to appropriate testing agents.

### Progress Indicators

Show clear progress throughout the testing process:

```
🔍 Detecting project type...
✅ Project type: [Next.js/React/Python/etc]
🧪 Running [frontend/backend/full-stack] tests...
⏱️  Estimated time: [2-5 minutes]
```

### Step 1: Analyze Context

Parse optional arguments in `$ARGUMENTS`:
- `--quick` - Run existing tests without agents (minimal tokens ~50)
- `--create` - Force creation of new tests using agents (~5000+ tokens)
- `--update` - Update existing tests using agents (~2000+ tokens)
- `--frontend` - Run only frontend tests
- `--backend` - Run only backend tests  
- `--unit` - Run only unit tests
- `--e2e` - Run only E2E tests
- `--ci` - Trigger CI pipeline tests
- No arguments - Auto-detect and use --quick if tests exist

**Token-Efficient Mode**: By default, checks for existing tests first.
**WARNING**: Only use `--create` or `--update` when necessary (high token usage).

### Step 2: Check for Existing Tests (Token Optimization)

**CRITICAL**: Before using any agents, check if tests already exist:

```bash
# Check for existing test files
!TEST_EXISTS=false
!test -d __tests__ && TEST_EXISTS=true
!test -d tests && TEST_EXISTS=true  
!test -d test && TEST_EXISTS=true
!ls *.test.* *.spec.* 2>/dev/null | head -1 && TEST_EXISTS=true

if TEST_EXISTS=true and not --create and not --update:
   echo "✅ Existing tests found - using quick mode (minimal tokens)"
   # Jump to Step 6: Quick Test Execution
else if TEST_EXISTS=false and not --create:
   echo "⚠️ No tests found. Options:"
   echo "1. Run: /test --create (create new tests ~5000 tokens)"
   echo "2. Write tests manually"
   echo "3. Skip testing"
   # Exit unless --create flag provided
```

### Step 3: Intelligent Detection (Only if needed)

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

### Step 4: Route to Testing Agents (Only for --create or --update)

**⚠️ HIGH TOKEN USAGE - Only executed with --create or --update flags**

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

### Step 5: CI/CD Integration & Deduplication

#### Check if CI/CD is already running:
!gh run list --workflow=ci-cd-pipeline.yml --branch=$(git branch --show-current) --status=in_progress --json databaseId -q '.[0].databaseId' 2>/dev/null

If CI/CD already running:
```
⚠️  CI/CD pipeline already running for this branch
🔗 View at: https://github.com/vanman2024/multi-agent-claude-code/actions
⏭️  Skipping duplicate test run
```

#### CI Pipeline Trigger (if --ci flag and not already running)

If `--ci` in arguments and no active CI run:

Get current branch:
!BRANCH=$(git branch --show-current) && echo "Branch: $BRANCH"

Use mcp__github__run_workflow:
- owner: vanman2024
- repo: multi-agent-claude-code
- workflow_id: "ci-cd-pipeline.yml"
- ref: $BRANCH

Then monitor status:
Use mcp__github__get_workflow_run to check status

Show progress:
```
🚀 CI/CD pipeline triggered
⏱️  Waiting for pipeline to start...
✅ Pipeline running: [link to GitHub Actions]
```

### Step 6: Quick Test Execution (Default for existing tests)

**For --quick flag or when tests exist (LOW TOKEN USAGE ~50-100)**:

```bash
# Determine test command based on project type
!if [ -f package.json ]; then
    if grep -q '"test"' package.json; then
        echo "🧪 Running: npm test"
        !npm test
    elif grep -q '"jest"' package.json; then
        echo "🧪 Running: jest"
        !jest
    elif grep -q '"vitest"' package.json; then
        echo "🧪 Running: vitest"
        !vitest run
    fi
elif [ -f requirements.txt ] || [ -f pyproject.toml ]; then
    if command -v pytest &> /dev/null; then
        echo "🧪 Running: pytest"
        !pytest
    elif command -v python -m pytest &> /dev/null; then
        echo "🧪 Running: python -m pytest"
        !python -m pytest
    fi
elif [ -f go.mod ]; then
    echo "🧪 Running: go test"
    !go test ./...
else
    echo "❌ No test runner detected. Supported: npm test, jest, vitest, pytest, go test"
fi

# Check for coverage if requested
!if [[ "$ARGUMENTS" == *"--coverage"* ]]; then
    if [ -f package.json ] && grep -q '"test:coverage"' package.json; then
        echo "📊 Running coverage: npm run test:coverage"
        !npm run test:coverage
    fi
fi
```

Show results:
```
✅ Tests completed
📊 Results: [pass/fail count]
⏱️  Duration: [time]
💰 Tokens used: ~50-100 (quick mode)
```

### Step 7: Report Consolidated Results

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

### Detection Errors
If detection unclear and no user response:
```
⚠️  Could not auto-detect project type
📝 Running full test suite (frontend + backend)
💡 Tip: Use flags for specific tests: /test --frontend or /test --backend
```

### Test Failures
If tests fail, provide actionable feedback:
```
❌ Test Failure: [specific test name]
📍 Location: [file:line]
🔧 Suggested fix: [actionable suggestion]
📚 Documentation: [link to relevant docs]
```

### Agent Failures
If agent fails:
```
❌ [Agent Name] encountered an error
📝 Error: [specific error message]
🔄 Retry: /test --[test-type]
🐛 Debug: npm test -- --verbose (or equivalent)
```

### Common Issues & Solutions
| Issue | Solution | Command |
|-------|----------|---------|
| Module not found | Install dependencies | `npm install` or `pip install -r requirements.txt` |
| Port already in use | Kill process on port | `lsof -ti:3000 \| xargs kill` |
| Database connection failed | Check connection string | Verify `.env` file |
| Permission denied | Fix file permissions | `chmod +x script.sh` |
| Out of memory | Increase heap size | `NODE_OPTIONS=--max-old-space-size=4096` |

## Implementation Notes

1. **Smart detection** - Look at git diff first, then project structure
2. **Agent routing** - Use proper agents, not inline bash commands
3. **Optional flags** - Flags override auto-detection
4. **Sequential for full-stack** - Backend must pass before E2E
5. **Clear reporting** - Unified results from all agents

## Performance & Security

### Performance Monitoring
Track detection overhead to ensure <10% impact:
```bash
# Start timer
!START_TIME=$(date +%s%N)

# ... detection logic ...

# Calculate overhead
!END_TIME=$(date +%s%N) && OVERHEAD=$((($END_TIME - $START_TIME) / 1000000)) && echo "Detection time: ${OVERHEAD}ms"
```

Target metrics:
- Detection time: <500ms
- Total overhead: <10% of test runtime
- Memory usage: <100MB for detection

### Security Measures

#### Credential Handling
Never expose sensitive data in test output:
- Mask API keys: `****-****-****-XXXX`
- Hide passwords: `********`
- Sanitize URLs: Remove tokens/auth from URLs
- Use environment variables for secrets

#### Test Data Security
```bash
# Check for exposed secrets before running tests
!grep -r "api_key\|password\|token\|secret" --include="*.test.*" --include="*.spec.*" . 2>/dev/null | grep -v "mock\|fake\|test" && echo "⚠️ Warning: Possible secrets in test files"

# Ensure .env.test is used instead of .env
!test -f .env.test && echo "✅ Using .env.test for testing" || echo "⚠️ Create .env.test with test credentials"
```

### Zero False Positives Strategy
Ensure test results are accurate:
1. **Deterministic tests** - No random/time-dependent logic
2. **Clean state** - Reset database/cache before tests
3. **Isolated tests** - No test interdependencies
4. **Retry flaky tests** - Max 3 retries for network issues
5. **Clear assertions** - Specific error messages