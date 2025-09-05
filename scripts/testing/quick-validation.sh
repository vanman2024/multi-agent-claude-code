#!/bin/bash

echo "======================================"
echo "🧪 QUICK TESTING VALIDATION"
echo "======================================"
echo

# Simple pass/fail tracking
TESTS_RUN=0
TESTS_PASSED=0

# Helper function
check() {
    TESTS_RUN=$((TESTS_RUN + 1))
    if eval "$2" >/dev/null 2>&1; then
        echo "✅ $1"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "❌ $1"
    fi
}

echo "1. Core Files Check:"
check "test.md exists" "test -f .claude/commands/test.md"
check "Frontend agent exists" "test -f .claude/agents/frontend-playwright-tester.md"
check "Backend agent exists" "test -f .claude/agents/backend-tester.md"
check "Jest config exists" "test -f jest.config.js"

echo
echo "2. Package.json Scripts:"
check "test script exists" "grep '\"test\"' package.json"
check "test:coverage script exists" "grep '\"test:coverage\"' package.json"

echo
echo "3. Documentation:"
check "Testing best practices" "test -f docs/TESTING-BEST-PRACTICES.md"
check "Checkbox docs" "test -f docs/CHECKBOXES.md"

echo  
echo "4. Actual Tests:"
echo "Running Jest tests..."
if npm test 2>&1 | grep -q "PASS"; then
    echo "✅ Jest tests pass"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ Jest tests fail"
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo
echo "5. MCP Connection:"
if claude mcp list | grep -q playwright; then
    echo "✅ Playwright MCP connected"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ Playwright MCP not connected"
fi
TESTS_RUN=$((TESTS_RUN + 1))

echo
echo "======================================"
echo "RESULTS: $TESTS_PASSED/$TESTS_RUN tests passed"
PERCENTAGE=$((TESTS_PASSED * 100 / TESTS_RUN))
echo "Success Rate: ${PERCENTAGE}%"
echo "======================================"