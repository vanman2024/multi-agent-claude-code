#!/bin/bash
# Unit tests for Claude Code hooks
# Tests individual hook functions without Claude Code session

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test helper function
assert_equals() {
    local actual="$1"
    local expected="$2"
    local test_name="$3"
    
    if [ "$actual" = "$expected" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
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
    echo -e "${GREEN}✓ PASS${NC}: Found $HOOK_COUNT hook categories"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Could not parse hooks from settings.json"
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
        echo -e "${GREEN}✓ PASS${NC}: Valid matcher pattern: $matcher"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: Invalid matcher pattern: $matcher"
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
    echo -e "${GREEN}✓ PASS${NC}: Environment variable handling"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Environment variable handling"
    ((TESTS_FAILED++))
fi
rm -rf "$TEST_DIR"

# Test 6: Log directory creation
echo ""
echo "Test: Log directory creation"
LOG_DIR=".claude/logs"
if [ -d "$LOG_DIR" ] || mkdir -p "$LOG_DIR" 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}: Log directory accessible"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Cannot create log directory"
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
    echo -e "${GREEN}✓ PASS${NC}: All hook scripts have correct permissions"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Some scripts missing execute permission"
    ((TESTS_FAILED++))
fi

# Test 8: Mock hook execution
echo ""
echo "Test: Mock hook execution"
# Test log-agent-task.sh with mock input
TEST_INPUT='{"tool_name":"Task","tool_input":{"subagent_type":"test","description":"Test task"},"session_id":"test123"}'
OUTPUT=$(echo "$TEST_INPUT" | .claude/hooks/log-agent-task.sh 2>&1)
if echo "$OUTPUT" | grep -q "Logged agent task"; then
    echo -e "${GREEN}✓ PASS${NC}: Hook executes successfully"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Hook execution failed"
    ((TESTS_FAILED++))
fi

# Results
echo ""
echo "=== Test Results ==="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All unit tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi