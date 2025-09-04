#!/bin/bash
# Test Orchestrator for /work Command - Complete User Story Simulation
# This script mimics all the scenarios from the user test story and tracks progress

set -e

WORKTREE_DIR="/home/gotime2022/Projects/worktrees/issue-126-fix-work-command"
cd "$WORKTREE_DIR"

echo "🎭 /work Command Test Orchestrator"
echo "=================================="
echo "This script will simulate all user scenarios and prepare for manual testing"
echo ""

# Create a test results file
TEST_RESULTS="test-results.md"
echo "# /work Command Test Results" > $TEST_RESULTS
echo "Generated: $(date)" >> $TEST_RESULTS
echo "" >> $TEST_RESULTS

# Function to log test steps
log_test() {
    echo "## $1" >> $TEST_RESULTS
    echo "$2" >> $TEST_RESULTS
    echo "" >> $TEST_RESULTS
    echo "📝 $1"
    echo "   $2"
}

# Function to check implementation
check_implementation() {
    local feature="$1"
    local pattern="$2"
    local file=".claude/commands/work.md"
    
    if grep -q "$pattern" "$file"; then
        echo "✅ IMPLEMENTED: $feature"
        echo "- ✅ **$feature**: IMPLEMENTED" >> $TEST_RESULTS
        return 0
    else
        echo "❌ MISSING: $feature"
        echo "- ❌ **$feature**: MISSING" >> $TEST_RESULTS
        return 1
    fi
}

echo "🔍 PHASE 1: Implementation Verification"
echo "======================================="

log_test "Scenario 1: Branch Enforcement" "Command should check if user is on main branch and stop if not"
check_implementation "Main branch check" "git branch --show-current"
check_implementation "Auto-pull functionality" "git pull origin main"

log_test "Scenario 2: Worktree Prompts" "Should ask user about worktree creation when on different branch"
check_implementation "Worktree detection" "git worktree list"
check_implementation "User choice prompt" "Choose.*1.*2.*3"

log_test "Scenario 3: GitHub Branch Creation" "Must use gh issue develop to create GitHub-linked branch"
check_implementation "GitHub branch creation" "gh issue develop"
check_implementation "Branch checkout" "checkout"

log_test "Scenario 4: Issue Reference Enforcement" "All commits must reference the issue number"
check_implementation "Commit template setup" "git config commit.template"
check_implementation "Issue reference format" "Related to #"

log_test "Scenario 5: No Manual PR Creation" "Should NOT create PRs manually"
if ! grep -q "gh pr create" .claude/commands/work.md || grep -q "DO NOT.*gh pr create" .claude/commands/work.md; then
    echo "✅ IMPLEMENTED: No manual PR creation"
    echo "- ✅ **No manual PR creation**: IMPLEMENTED" >> $TEST_RESULTS
else
    echo "❌ ISSUE: Manual PR creation found"
    echo "- ❌ **No manual PR creation**: ISSUE FOUND" >> $TEST_RESULTS
fi

log_test "Scenario 6: Intelligent Selection" "Should prioritize issues based on blockers, priority, size"
check_implementation "Issue listing" "mcp__github__list_issues"
check_implementation "Priority checking" "priority.*P0.*P1.*P2"
check_implementation "Blocker analysis" "blocked.*label"

log_test "Scenario 7: Checkbox Workflow" "Should work through issue checkboxes systematically"
check_implementation "Checkbox mention" "checkbox"
check_implementation "TodoWrite usage" "TodoWrite"

log_test "Scenario 8: Template Compliance" "Should use ! syntax and MCP functions"
BASH_BLOCKS=$(grep -c '```bash' .claude/commands/work.md || echo 0)
MCP_FUNCTIONS=$(grep -c 'mcp__github__' .claude/commands/work.md)
EXCLAMATION_SYNTAX=$(grep -c '!\`' .claude/commands/work.md)

if [ "$BASH_BLOCKS" -eq 0 ]; then
    echo "✅ IMPLEMENTED: No bash code blocks"
    echo "- ✅ **Template compliance**: No bash blocks ✓" >> $TEST_RESULTS
else
    echo "❌ ISSUE: Found $BASH_BLOCKS bash blocks"
    echo "- ❌ **Template compliance**: Found $BASH_BLOCKS bash blocks" >> $TEST_RESULTS
fi

if [ "$MCP_FUNCTIONS" -gt 5 ]; then
    echo "✅ IMPLEMENTED: Uses MCP functions ($MCP_FUNCTIONS found)"
    echo "- ✅ **MCP functions**: $MCP_FUNCTIONS found ✓" >> $TEST_RESULTS
else
    echo "⚠️  LIMITED: Only $MCP_FUNCTIONS MCP functions found"
    echo "- ⚠️ **MCP functions**: Only $MCP_FUNCTIONS found" >> $TEST_RESULTS
fi

echo "" >> $TEST_RESULTS

echo ""
echo "🎯 PHASE 2: Manual Testing Preparation"
echo "====================================="

log_test "Test Setup Instructions" "What user needs to do to test each scenario"

# Create detailed test instructions
cat << 'EOF' >> $TEST_RESULTS

## Manual Testing Instructions

### Setup Phase
```bash
# 1. Go to main repository (not worktree)
cd /home/gotime2022/Projects/multi-agent-claude-code

# 2. Ensure clean state
git status
# Should show: On branch main, nothing to commit, working tree clean
```

### Test Scenario 1: Branch Enforcement
```bash
# Test from wrong branch (should FAIL)
git checkout 134-feature-unified-testing-strategy-for-frontend-and-backend
/work #126

# Expected: Error message about needing to be on main
# Expected: Instructions to run: git checkout main && git pull origin main
```

### Test Scenario 2: Auto-Pull Detection  
```bash
# Simulate being behind (optional - only if you want to test this)
git checkout main
git reset --hard HEAD~1  # Go back one commit
/work #126

# Expected: Auto-pull message and successful pull
```

### Test Scenario 3: Worktree Prompt
```bash
# From feature branch
git checkout 134-feature-unified-testing-strategy-for-frontend-and-backend
/work #150  # Use different issue number

# Expected: Prompt with 3 options:
# 1. Create worktree (recommended)
# 2. Switch to main  
# 3. Cancel
```

### Test Scenario 4: Proper GitHub Branch Creation
```bash
# From main branch
git checkout main  
git pull origin main
/work #151  # Use new test issue

# Expected: 
# 1. Command runs gh issue develop #151 --checkout
# 2. Creates branch on GitHub first
# 3. Checks out locally
# 4. Shows branch name like: 151-feature-description
```

### Test Scenario 5: Issue Reference Setup
```bash
# After /work creates branch, check:
cat .gitmessage
# Expected: Should contain "Related to #151" or similar

git config --get commit.template
# Expected: Should show .gitmessage path
```

### Test Scenario 6: No Manual PR Creation
```bash
# During /work execution, watch output carefully
# Expected: NO "gh pr create" commands executed
# Expected: Message about automation handling PR creation
```

### Test Scenario 7: Intelligent Issue Selection  
```bash
# Test with no arguments
/work

# Expected: Analysis of available issues
# Expected: Explanation of WHY specific issue was selected
# Expected: Priority/blocker analysis
```

EOF

echo ""
echo "📊 PHASE 3: Test Results Summary"  
echo "==============================="

# Count implementations
IMPLEMENTED=$(grep -c "✅.*IMPLEMENTED" $TEST_RESULTS || echo 0)
ISSUES=$(grep -c "❌.*ISSUE\|❌.*MISSING" $TEST_RESULTS || echo 0)
WARNINGS=$(grep -c "⚠️" $TEST_RESULTS || echo 0)

echo "✅ Implemented: $IMPLEMENTED"
echo "❌ Issues: $ISSUES" 
echo "⚠️  Warnings: $WARNINGS"

log_test "Summary" "Implementation: $IMPLEMENTED ✅, Issues: $ISSUES ❌, Warnings: $WARNINGS ⚠️"

# Add checklist to results
cat << 'EOF' >> $TEST_RESULTS

## Testing Checklist

### Pre-Test Verification
- [ ] All implementation checks passed
- [ ] Test environment is clean  
- [ ] On main branch with latest changes

### Manual Test Execution
- [ ] Scenario 1: Branch enforcement (should fail from wrong branch)
- [ ] Scenario 2: Auto-pull detection (pulls latest changes)
- [ ] Scenario 3: Worktree prompts (offers 3 choices)
- [ ] Scenario 4: GitHub branch creation (uses gh issue develop)
- [ ] Scenario 5: Commit template setup (creates .gitmessage)
- [ ] Scenario 6: No manual PR creation (automation only)
- [ ] Scenario 7: Intelligent selection (analyzes and explains)

### Post-Test Validation  
- [ ] All commits reference issue numbers
- [ ] Branch appears in GitHub issue Development section
- [ ] No manual PRs were created
- [ ] Worktree functions correctly (if tested)
- [ ] Issue status updated correctly

## Test Execution Notes
(Add notes here during manual testing)

EOF

echo ""
echo "📋 Test results saved to: $TEST_RESULTS"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo "🎉 All implementation checks passed!"
    echo "✅ Ready for manual testing with /work command"
    echo ""
    echo "Next steps:"
    echo "1. Review test results: cat $TEST_RESULTS"
    echo "2. Follow manual testing instructions"
    echo "3. Run actual /work command for each scenario"
    echo "4. Check off items in the testing checklist"
else
    echo "⚠️ Found $ISSUES implementation issues"
    echo "📝 Review test results before manual testing"
fi

echo ""
echo "🔗 All test artifacts:"
echo "- Test results: $TEST_RESULTS"
echo "- Implementation: .claude/commands/work.md" 
echo "- Validation script: test-work-command.sh"
echo "- This orchestrator: test-orchestrator.sh"