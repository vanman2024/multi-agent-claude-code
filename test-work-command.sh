#!/bin/bash
# Test Script for /work Command Validation
# Run this to verify all /work command fixes are working

set -e  # Exit on any error

echo "🧪 Testing /work Command Implementation"
echo "======================================="

WORKTREE_DIR="/home/gotime2022/Projects/worktrees/issue-126-fix-work-command"
cd "$WORKTREE_DIR"

echo ""
echo "📍 Current location: $(pwd)"
echo "📍 Current branch: $(git branch --show-current)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
PASS_COUNT=0
FAIL_COUNT=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((PASS_COUNT++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((FAIL_COUNT++))
    fi
}

echo "🔍 TEST 1: Template Format Compliance"
echo "-----------------------------------"

# Test: No bash code blocks
BASH_BLOCKS=$(grep -c '```bash' .claude/commands/work.md || true)
test_result $([ "$BASH_BLOCKS" -eq 0 ] && echo 0 || echo 1) "No bash code blocks found"

# Test: Uses ! syntax
EXCLAMATION_SYNTAX=$(grep -c '!\`' .claude/commands/work.md || true)
test_result $([ "$EXCLAMATION_SYNTAX" -gt 5 ] && echo 0 || echo 1) "Uses ! syntax for commands ($EXCLAMATION_SYNTAX found)"

# Test: Uses MCP functions
MCP_FUNCTIONS=$(grep -c 'mcp__github__' .claude/commands/work.md || true)
test_result $([ "$MCP_FUNCTIONS" -gt 3 ] && echo 0 || echo 1) "Uses MCP GitHub functions ($MCP_FUNCTIONS found)"

echo ""
echo "🔍 TEST 2: Critical Features Present"
echo "-----------------------------------"

# Test: gh issue develop mentioned
GH_ISSUE_DEVELOP=$(grep -c 'gh issue develop' .claude/commands/work.md || true)
test_result $([ "$GH_ISSUE_DEVELOP" -gt 0 ] && echo 0 || echo 1) "Uses 'gh issue develop' for branch creation"

# Test: No manual PR creation
MANUAL_PR=$(grep -c 'gh pr create' .claude/commands/work.md || true)
test_result $([ "$MANUAL_PR" -eq 0 ] && echo 0 || echo 1) "No manual PR creation commands"

# Test: Worktree support
WORKTREE_SUPPORT=$(grep -c 'worktree' .claude/commands/work.md || true)
test_result $([ "$WORKTREE_SUPPORT" -gt 3 ] && echo 0 || echo 1) "Includes worktree support"

# Test: Issue reference enforcement
ISSUE_REFERENCE=$(grep -c 'Related to #' .claude/commands/work.md || true)
test_result $([ "$ISSUE_REFERENCE" -gt 0 ] && echo 0 || echo 1) "Enforces issue references in commits"

# Test: Checkbox workflow
CHECKBOX_WORKFLOW=$(grep -c 'checkbox' .claude/commands/work.md || true)
test_result $([ "$CHECKBOX_WORKFLOW" -gt 2 ] && echo 0 || echo 1) "Implements checkbox-first workflow"

echo ""
echo "🔍 TEST 3: Branch Enforcement Logic"
echo "-----------------------------------"

# Test: Branch checking
BRANCH_CHECK=$(grep -c 'git branch --show-current' .claude/commands/work.md || true)
test_result $([ "$BRANCH_CHECK" -gt 2 ] && echo 0 || echo 1) "Checks current branch"

# Test: Main branch requirement
MAIN_REQUIREMENT=$(grep -c 'main branch' .claude/commands/work.md || true)
test_result $([ "$MAIN_REQUIREMENT" -gt 1 ] && echo 0 || echo 1) "Requires main branch"

# Test: Auto-pull functionality
AUTO_PULL=$(grep -c 'git pull' .claude/commands/work.md || true)
test_result $([ "$AUTO_PULL" -gt 1 ] && echo 0 || echo 1) "Includes auto-pull functionality"

echo ""
echo "🔍 TEST 4: File Structure Validation"
echo "------------------------------------"

# Test: Command file exists and is readable
test_result $([ -f .claude/commands/work.md ] && echo 0 || echo 1) "work.md command file exists"

# Test: Has proper frontmatter
FRONTMATTER=$(head -n 5 .claude/commands/work.md | grep -c 'allowed-tools\|description\|argument-hint' || true)
test_result $([ "$FRONTMATTER" -eq 3 ] && echo 0 || echo 1) "Has proper YAML frontmatter"

# Test: File is not empty
FILE_SIZE=$(wc -l < .claude/commands/work.md)
test_result $([ "$FILE_SIZE" -gt 100 ] && echo 0 || echo 1) "File has substantial content ($FILE_SIZE lines)"

echo ""
echo "🔍 TEST 5: Commit History Validation"
echo "------------------------------------"

# Test: Recent commits reference issue
RECENT_COMMITS=$(git log --oneline -5 --grep="#126" | wc -l)
test_result $([ "$RECENT_COMMITS" -gt 2 ] && echo 0 || echo 1) "Recent commits reference issue #126 ($RECENT_COMMITS found)"

# Test: Branch is ahead of main
COMMITS_AHEAD=$(git rev-list --count main..HEAD)
test_result $([ "$COMMITS_AHEAD" -gt 0 ] && echo 0 || echo 1) "Branch has commits ahead of main ($COMMITS_AHEAD commits)"

echo ""
echo "📊 SUMMARY"
echo "=========="
echo -e "✅ ${GREEN}PASSED${NC}: $PASS_COUNT tests"
echo -e "❌ ${RED}FAILED${NC}: $FAIL_COUNT tests"

TOTAL_TESTS=$((PASS_COUNT + FAIL_COUNT))
SUCCESS_RATE=$((PASS_COUNT * 100 / TOTAL_TESTS))
echo "📈 Success Rate: ${SUCCESS_RATE}%"

echo ""
if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! The /work command implementation looks good.${NC}"
    echo ""
    echo "✅ Ready for manual testing of actual slash command execution"
    exit 0
else
    echo -e "${RED}⚠️ Some tests failed. Review the implementation before manual testing.${NC}"
    exit 1
fi