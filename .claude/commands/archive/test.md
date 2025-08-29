---
allowed-tools: Bash(*), Read(*), mcp__github(*)
description: Run tests locally or trigger CI tests
argument-hint: [test-type] [options]
---

# Test Command

## Context
- Current branch: !`git branch --show-current`
- Project files: @package.json
- Test config: @jest.config.js @pytest.ini @.github/workflows/ci-cd-pipeline.yml

## Your Task

When user runs `/test $ARGUMENTS`, execute tests based on arguments:

### Parse Arguments
Determine test type from $ARGUMENTS:
- `unit` - Run unit tests only
- `integration` - Run integration tests only  
- `e2e` - Run end-to-end tests
- `all` or empty - Run all tests
- `ci` - Trigger CI pipeline tests
- `specific <pattern>` - Run tests matching pattern

### Step 1: Detect Test Framework
Check which test framework exists:
```
Check package.json for: jest, vitest, mocha, jasmine
Check for: pytest, unittest, nose
Check for: go test, cargo test, dotnet test
```

### Step 2: Run Local Tests (if not CI)

#### For JavaScript/TypeScript Projects:
```bash
# Check if test command exists
!`grep -q '"test"' package.json && echo "found"`

# Run based on argument
if [ "$ARGUMENTS" = "unit" ]; then
  npm run test:unit || npm test -- --testPathPattern=unit
elif [ "$ARGUMENTS" = "integration" ]; then
  npm run test:integration || npm test -- --testPathPattern=integration
elif [ "$ARGUMENTS" = "e2e" ]; then
  npm run test:e2e || npm test -- --testPathPattern=e2e
elif [[ "$ARGUMENTS" == specific* ]]; then
  pattern="${ARGUMENTS#specific }"
  npm test -- --testNamePattern="$pattern"
else
  npm test
fi
```

#### For Python Projects:
```bash
# Check for pytest
!`which pytest || which python -m pytest`

# Run based on argument
if [ "$ARGUMENTS" = "unit" ]; then
  pytest tests/unit -v
elif [ "$ARGUMENTS" = "integration" ]; then
  pytest tests/integration -v
elif [[ "$ARGUMENTS" == specific* ]]; then
  pattern="${ARGUMENTS#specific }"
  pytest -k "$pattern" -v
else
  pytest -v
fi
```

### Step 3: Trigger CI Tests (if CI argument)
If $ARGUMENTS contains "ci":

Use mcp__github to trigger workflow:
1. Get current branch and commit
2. Trigger CI workflow: mcp__github__run_workflow
3. Monitor workflow status
4. Report results

### Step 4: Coverage Report
After tests complete:
```bash
# For JS/TS with coverage
!`test -f coverage/lcov-report/index.html && echo "Coverage report: coverage/lcov-report/index.html"`

# For Python with coverage
!`test -f htmlcov/index.html && echo "Coverage report: htmlcov/index.html"`
```

### Step 5: Handle Test Failures
If tests fail:
1. Parse error output
2. Identify failing tests
3. Suggest next steps:
   - Run specific failing test: `/test specific "test-name"`
   - Debug with verbose output
   - Check recent changes: `git diff`

### Step 6: Update PR Status (if in PR branch)
Check if current branch has open PR:
```bash
# Get PR number if exists
!`gh pr view --json number -q .number 2>/dev/null`
```

If PR exists, update status using mcp__github:
- Add test results as comment
- Update PR checks status
- Add coverage badge if applicable

## Output Format

### Success:
```
✅ All tests passed!

Test Summary:
- Unit Tests: 45 passed
- Integration Tests: 12 passed
- Coverage: 87%

View coverage report: coverage/lcov-report/index.html
```

### Failure:
```
❌ Tests failed

Failed Tests:
- UserAuth.test.js > should validate email format
- API.test.js > should return 404 for invalid route

Run specific test:
  /test specific "validate email"

Debug with verbose output:
  npm test -- --verbose
```

### CI Triggered:
```
🚀 CI Pipeline triggered!

Workflow: CI Testing & Quality Pipeline
Run ID: #1234
Status: In Progress

Monitor at: https://github.com/[owner]/[repo]/actions/runs/1234

Or check status:
  gh run view 1234
```

## Notes
- Detect test framework automatically
- Support multiple languages/frameworks
- Provide actionable failure messages
- Update PR status when applicable
- Show coverage reports
- NO code snippets, just reference what to run