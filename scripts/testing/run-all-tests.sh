#!/bin/bash
# Master test runner - runs all test suites
# Usage: ./scripts/testing/run-all-tests.sh [component]
# Component: hooks, agents, commands, workflows, all (default)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPONENT="${1:-all}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== Multi-Agent Claude Code Test Suite ==="
echo "Project: $PROJECT_ROOT"
echo "Component: $COMPONENT"
echo ""

# Test results
TOTAL_PASSED=0
TOTAL_FAILED=0

run_test_suite() {
    local suite_name="$1"
    local test_script="$2"
    
    echo -e "${YELLOW}Running $suite_name tests...${NC}"
    
    if [ -f "$test_script" ] && [ -x "$test_script" ]; then
        if bash "$test_script"; then
            echo -e "${GREEN}✓ $suite_name tests passed${NC}"
            ((TOTAL_PASSED++))
        else
            echo -e "${RED}✗ $suite_name tests failed${NC}"
            ((TOTAL_FAILED++))
        fi
    else
        echo -e "${RED}✗ $suite_name test script not found or not executable${NC}"
        ((TOTAL_FAILED++))
    fi
    echo ""
}

# Run tests based on component
case "$COMPONENT" in
    hooks)
        run_test_suite "Hooks Integration" "$SCRIPT_DIR/test-hooks-integration.sh"
        run_test_suite "Hook Units" "$SCRIPT_DIR/test-hooks-unit.sh"
        ;;
    agents)
        run_test_suite "Agent Coordination" "$SCRIPT_DIR/test-agent-coordination.sh"
        ;;
    commands)
        run_test_suite "Slash Commands" "$SCRIPT_DIR/test-slash-commands.sh"
        ;;
    workflows)
        echo "GitHub workflow testing requires 'act' tool"
        echo "Install: https://github.com/nektos/act"
        # run_test_suite "GitHub Workflows" "$SCRIPT_DIR/test-github-workflows.sh"
        ;;
    all|*)
        # Run all test suites
        run_test_suite "Hooks Integration" "$SCRIPT_DIR/test-hooks-integration.sh"
        run_test_suite "Hook Units" "$SCRIPT_DIR/test-hooks-unit.sh"
        run_test_suite "Agent Coordination" "$SCRIPT_DIR/test-agent-coordination.sh"
        run_test_suite "Slash Commands" "$SCRIPT_DIR/test-slash-commands.sh"
        ;;
esac

# Summary
echo "=== Test Summary ==="
echo -e "${GREEN}Passed: $TOTAL_PASSED${NC}"
echo -e "${RED}Failed: $TOTAL_FAILED${NC}"

if [ $TOTAL_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All test suites passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some test suites failed${NC}"
    exit 1
fi