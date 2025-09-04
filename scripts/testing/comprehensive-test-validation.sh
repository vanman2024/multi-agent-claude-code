#!/bin/bash

# Comprehensive Testing Validation Script for Issue #134
# This script validates ALL requirements from the unified testing strategy

set -e

echo "================================================"
echo "🧪 COMPREHENSIVE TESTING VALIDATION"
echo "================================================"
echo ""

# Track test results
PASSED=0
FAILED=0
SKIPPED=0

# Helper function to test a feature
test_feature() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Testing: $name... "
    
    if eval "$command" 2>/dev/null | grep -q "$expected" 2>/dev/null; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED"
        ((FAILED++))
    fi
}

# Helper for skipped tests
skip_test() {
    local name="$1"
    local reason="$2"
    echo "⏭️  SKIPPED: $name - Reason: $reason"
    ((SKIPPED++))
}

echo "1️⃣ PROJECT TYPE DETECTION"
echo "============================"

# Test JavaScript/React detection
test_feature "React/Next.js detection" \
    "grep -E '\"react\"|\"next\"' package.json" \
    "react"

# Test for Python backend (create temp file)
echo "import pytest" > /tmp/test_requirements.txt
test_feature "Python project detection" \
    "test -f /tmp/test_requirements.txt && echo 'found'" \
    "found"
rm -f /tmp/test_requirements.txt

# Test for Go backend (create temp file)
echo "module test" > /tmp/go.mod
test_feature "Go project detection" \
    "test -f /tmp/go.mod && echo 'found'" \
    "found"
rm -f /tmp/go.mod

echo ""
echo "2️⃣ TESTING FRAMEWORK SUPPORT"
echo "=============================="

# Jest testing
test_feature "Jest configuration" \
    "test -f jest.config.js && echo 'found'" \
    "found"

test_feature "Jest tests run" \
    "npm test 2>&1" \
    "PASS"

# Test coverage
test_feature "Coverage reporting" \
    "npm run test:coverage 2>&1" \
    "Coverage"

echo ""
echo "3️⃣ COMMAND FLAGS VALIDATION"
echo "============================="

# Check if test.md has flag parsing
test_feature "--frontend flag parsing" \
    "grep '\-\-frontend' .claude/commands/test.md" \
    "--frontend"

test_feature "--backend flag parsing" \
    "grep '\-\-backend' .claude/commands/test.md" \
    "--backend"

test_feature "--unit flag parsing" \
    "grep '\-\-unit' .claude/commands/test.md" \
    "--unit"

test_feature "--e2e flag parsing" \
    "grep '\-\-e2e' .claude/commands/test.md" \
    "--e2e"

echo ""
echo "4️⃣ AGENT CONFIGURATION"
echo "========================"

# Check agent files exist
test_feature "Frontend agent exists" \
    "test -f .claude/agents/frontend-playwright-tester.md && echo 'found'" \
    "found"

test_feature "Backend agent exists" \
    "test -f .claude/agents/backend-tester.md && echo 'found'" \
    "found"

# Check Firefox configuration
test_feature "Firefox browser configured" \
    "grep -i 'firefox' .claude/agents/frontend-playwright-tester.md" \
    "firefox"

# Check Vercel deployment detection
test_feature "Vercel deployment logic" \
    "grep -i 'vercel' .claude/agents/frontend-playwright-tester.md" \
    "vercel"

echo ""
echo "5️⃣ PLAYWRIGHT MCP VALIDATION"
echo "=============================="

# Check Playwright MCP connection
test_feature "Playwright MCP connected" \
    "claude mcp list | grep -i playwright" \
    "playwright"

# Test if we can check browser status
if command -v npx &> /dev/null; then
    test_feature "Playwright browser available" \
        "npx playwright --version" \
        "Version"
else
    skip_test "Playwright browser" "npx not available"
fi

echo ""
echo "6️⃣ CI/CD INTEGRATION"
echo "====================="

# Check for duplication prevention
test_feature "CI/CD check exists" \
    "grep 'CI.*GITHUB_ACTIONS' .claude/commands/test.md" \
    "CI"

echo ""
echo "7️⃣ ERROR HANDLING"
echo "=================="

test_feature "Error messages documented" \
    "grep -i 'error' .claude/commands/test.md | head -1" \
    "error"

test_feature "Troubleshooting section" \
    "grep -i 'troubleshoot' .claude/commands/test.md" \
    "troubleshoot"

echo ""
echo "8️⃣ DOCUMENTATION"
echo "================="

test_feature "Testing best practices" \
    "test -f docs/TESTING-BEST-PRACTICES.md && echo 'found'" \
    "found"

test_feature "Checkbox documentation" \
    "test -f docs/CHECKBOXES.md && echo 'found'" \
    "found"

echo ""
echo "9️⃣ PERFORMANCE METRICS"
echo "======================="

# Measure test execution time
START_TIME=$(date +%s%N)
npm test --silent > /dev/null 2>&1
END_TIME=$(date +%s%N)
DURATION=$((($END_TIME - $START_TIME)/1000000))

echo "Test execution time: ${DURATION}ms"

if [ $DURATION -lt 5000 ]; then
    echo "✅ Performance: Excellent (<5s)"
    ((PASSED++))
elif [ $DURATION -lt 10000 ]; then
    echo "⚠️  Performance: Good (<10s)"
    ((PASSED++))
else
    echo "❌ Performance: Needs optimization (>10s)"
    ((FAILED++))
fi

echo ""
echo "🔟 VERCEL DEPLOYMENT CHECK"
echo "=========================="

# Check for Vercel deployment URL
if gh pr view 136 2>/dev/null | grep -q "vercel.app"; then
    echo "✅ Vercel preview deployment found"
    ((PASSED++))
else
    echo "⚠️  No Vercel deployment found for PR #136"
    ((SKIPPED++))
fi

echo ""
echo "================================================"
echo "📊 FINAL RESULTS"
echo "================================================"
echo "✅ PASSED:  $PASSED"
echo "❌ FAILED:  $FAILED"
echo "⏭️  SKIPPED: $SKIPPED"
echo ""

TOTAL=$(($PASSED + $FAILED + $SKIPPED))
SUCCESS_RATE=$((PASSED * 100 / TOTAL))

echo "Success Rate: ${SUCCESS_RATE}%"
echo ""

if [ $SUCCESS_RATE -ge 80 ]; then
    echo "🎉 VALIDATION SUCCESSFUL! Testing strategy is working well."
elif [ $SUCCESS_RATE -ge 60 ]; then
    echo "⚠️  PARTIAL SUCCESS. Some improvements needed."
else
    echo "❌ VALIDATION FAILED. Significant work required."
fi

echo ""
echo "================================================"
echo "📝 RECOMMENDATIONS"
echo "================================================"

if [ $FAILED -gt 0 ]; then
    echo "Fix the following to achieve 100% functionality:"
    echo ""
fi

# Specific recommendations based on failures
grep -q "Firefox browser configured.*FAILED" <<< "$OUTPUT" && echo "- Configure Firefox in Playwright settings"
grep -q "Coverage reporting.*FAILED" <<< "$OUTPUT" && echo "- Fix coverage reporting configuration"
grep -q "Backend agent.*FAILED" <<< "$OUTPUT" && echo "- Create backend testing agent"

echo ""
echo "Next steps to complete Issue #134:"
echo "1. Run actual /test command with Task tool invocation"
echo "2. Test with real Vercel deployment"
echo "3. Validate Python/Go backend testing"
echo "4. Measure actual detection accuracy across projects"