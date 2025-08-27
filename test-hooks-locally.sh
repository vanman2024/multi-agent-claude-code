#!/bin/bash
# Local Testing Script for Claude Code Hooks
# Run this before marking PR checkboxes as complete

echo "=== Claude Code Hooks Local Testing ==="
echo "This script verifies all hooks work correctly"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo -e "${YELLOW}Testing: $test_name${NC}"
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓ PASSED${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $test_name"
        echo "  Expected: $expected_result"
        ((TESTS_FAILED++))
    fi
    echo ""
}

echo "=== Pre-Test Setup ==="
echo "1. Ensure you've reloaded hooks with /hooks command in Claude Code"
echo "2. Enter transcript mode with Ctrl+R to see hook execution"
echo "3. Have a test file ready for editing"
echo ""
read -p "Press Enter when ready to start testing..."

echo ""
echo "=== Test 1: Hook Configuration ==="
run_test "Settings file exists" \
    "test -f .claude/settings.json" \
    "Settings file should exist"

run_test "All hook scripts are executable" \
    "test -x .claude/hooks/*.sh && test -x .claude/hooks/*.py" \
    "All scripts should be executable"

echo "=== Test 2: Hook Script Validation ==="
run_test "load-context.sh syntax check" \
    "bash -n .claude/hooks/load-context.sh" \
    "No syntax errors"

run_test "log-agent-task.sh syntax check" \
    "bash -n .claude/hooks/log-agent-task.sh" \
    "No syntax errors"

run_test "sync-agent-results.py syntax check" \
    "python3 -m py_compile .claude/hooks/sync-agent-results.py" \
    "No syntax errors"

echo "=== Test 3: Manual Hook Triggers ==="
echo "These tests require manual verification in Claude Code:"
echo ""

echo "[ ] TEST: Edit a file in Claude Code"
echo "    - Expected: auto-commit.sh should trigger"
echo "    - Verify: Check git log for automatic commit"
echo ""

echo "[ ] TEST: Submit a prompt in Claude Code"
echo "    - Expected: current-work.sh should inject context"
echo "    - Verify: See GitHub issues in transcript mode"
echo ""

echo "[ ] TEST: Run 'git push' command (without actually pushing)"
echo "    - Expected: test-before-push.sh should intercept"
echo "    - Verify: See test execution in transcript"
echo ""

echo "[ ] TEST: Use Task tool"
echo "    - Expected: log-agent-task.sh should log"
echo "    - Verify: Check .claude/logs/agent-tasks.log"
echo ""

echo "[ ] TEST: Restart Claude Code session"
echo "    - Expected: load-context.sh should run"
echo "    - Verify: See context loaded message"
echo ""

echo "=== Test 4: Log File Creation ==="
mkdir -p .claude/logs

run_test "Log directory exists" \
    "test -d .claude/logs" \
    "Log directory should be created"

echo "=== Test 5: Hook Input/Output ==="
# Test hook with mock input
TEST_INPUT='{"tool_name":"Task","tool_input":{"subagent_type":"test","description":"Test task"},"session_id":"test123"}'

echo "$TEST_INPUT" | .claude/hooks/log-agent-task.sh > /dev/null 2>&1
run_test "log-agent-task.sh processes input" \
    "test -f .claude/logs/agent-tasks.log" \
    "Log file should be created"

echo "=== Test Results ==="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 elman
    echo -e "${GREEN}All automated tests passed!${NC}"
    echo "Now complete the manual tests above before marking PR checkboxes."
else
    echo -e "${RED}Some tests failed. Fix issues before proceeding.${NC}"
fi

echo ""
echo "=== Checklist Before PR Merge ==="
echo "[ ] All automated tests pass"
echo "[ ] All manual tests verified in Claude Code"
echo "[ ] Hooks execute visibly in transcript mode"
echo "[ ] No errors in .claude/logs/"
echo "[ ] Documentation matches actual behavior"
echo "[ ] TodoWrite sync hook implemented (if required)"
echo ""
echo "Only check PR boxes after ALL items above are verified!"