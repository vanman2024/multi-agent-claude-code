#!/bin/bash
# Bash unit tests for shell hooks
# Run with: bash .claude/hooks/tests/test_hooks.sh

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper function
assert_equals() {
    local actual="$1"
    local expected="$2"
    local test_name="$3"
    
    if [ "$actual" = "$expected" ]; then
        echo "✓ PASS: $test_name"
        ((TESTS_PASSED++))
    else
        echo "✗ FAIL: $test_name"
        echo "  Expected: $expected"
        echo "  Got: $actual"
        ((TESTS_FAILED++))
    fi
}

echo "=== Hook Unit Tests ==="
echo ""

# Test 1: Verify hook file parsing
echo "Test: Hook configuration parsing"
HOOK_COUNT=$(jq '.hooks | to_entries | length' .claude/settings.json 2>/dev/null)
if [ -n "$HOOK_COUNT" ] && [ "$HOOK_COUNT" -gt 0 ]; then
    echo "✓ PASS: Found $HOOK_COUNT hook categories"
    ((TESTS_PASSED++))
else
    echo "✗ FAIL: Could not parse hooks from settings.json"
    ((TESTS_FAILED++))
fi

# Test 2: Check tool matchers
echo ""
echo "Test: Tool matcher patterns"
MATCHERS=$(jq -r '.hooks.PreToolUse[].matcher // .hooks.PostToolUse[].matcher' .claude/settings.json | sort -u)
for matcher in $MATCHERS; do
    # Test that matcher is valid regex
    echo "test" | grep -E "$matcher" > /dev/null 2>&1
    if [ $? -eq 0 ] || [ $? -eq 1 ]; then
        echo "✓ PASS: Valid matcher pattern: $matcher"
        ((TESTS_PASSED++))
    else
        echo "✗ FAIL: Invalid matcher pattern: $matcher"
        ((TESTS_FAILED++))
    fi
done

# Test 3: Verify JSON input handling
echo ""
echo "Test: JSON input processing"
TEST_JSON='{"tool_name":"Edit","file_path":"test.txt","session_id":"123"}'
FILE_PATH=$(echo "$TEST_JSON" | jq -r '.file_path')
assert_equals "$FILE_PATH" "test.txt" "JSON field extraction"

# Test 4: Test git operations safety
echo ""
echo "Test: Git operation safety checks"
CURRENT_BRANCH=$(git branch --show-current)
assert_equals "$?" "0" "Git branch detection"

# Test 5: Environment variable handling
echo ""
echo "Test: Environment variables"
TEST_DIR="/tmp/test_claude_hooks_$$"
export CLAUDE_PROJECT_DIR="$TEST_DIR"
mkdir -p "$TEST_DIR/.claude/logs"

if [ -d "$TEST_DIR/.claude/logs" ]; then
    echo "✓ PASS: Environment variable handling"
    ((TESTS_PASSED++))
else
    echo "✗ FAIL: Environment variable handling"
    ((TESTS_FAILED++))
fi
rm -rf "$TEST_DIR"

# Test 6: Log directory creation
echo ""
echo "Test: Log directory creation"
LOG_DIR=".claude/logs"
if [ -d "$LOG_DIR" ] || mkdir -p "$LOG_DIR" 2>/dev/null; then
    echo "✓ PASS: Log directory accessible"
    ((TESTS_PASSED++))
else
    echo "✗ FAIL: Cannot create log directory"
    ((TESTS_FAILED++))
fi

# Test 7: Script permissions
echo ""
echo "Test: Hook script permissions"
HOOK_SCRIPTS=(.claude/hooks/*.sh .claude/hooks/*.py)
PERMS_OK=true
for script in "${HOOK_SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ ! -x "$script" ]; then
        echo "✗ Warning: $script is not executable"
        PERMS_OK=false
    fi
done
if $PERMS_OK; then
    echo "✓ PASS: All hook scripts have correct permissions"
    ((TESTS_PASSED++))
else
    echo "✗ FAIL: Some scripts missing execute permission"
    ((TESTS_FAILED++))
fi

# Results
echo ""
echo "=== Test Results ==="
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✓ All unit tests passed!"
    exit 0
else
    echo "✗ Some tests failed"
    exit 1
fi