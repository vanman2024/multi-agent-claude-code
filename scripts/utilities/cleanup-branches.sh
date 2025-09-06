#!/bin/bash

# Branch Cleanup Script for multi-agent-claude-code
# Generated on: $(date)
# Repository: github.com/vanman2024/multi-agent-claude-code

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to confirm deletion
confirm_deletion() {
    local branch_count=$1
    echo ""
    print_warning "About to delete $branch_count branches."
    print_warning "This action cannot be undone!"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " confirmation
    
    if [[ "$confirmation" != "yes" ]]; then
        print_error "Cleanup cancelled by user."
        exit 1
    fi
}

# Function to delete branch safely
delete_branch() {
    local branch=$1
    local reason=$2
    
    print_status "Deleting: $branch ($reason)"
    
    # Delete remote branch
    if git push origin --delete "$branch" 2>/dev/null; then
        echo "  ✓ Remote branch deleted"
    else
        print_warning "  ⚠ Failed to delete remote branch (may not exist)"
    fi
    
    # Delete local branch if it exists
    if git branch | grep -q " $branch$"; then
        if git branch -D "$branch" 2>/dev/null; then
            echo "  ✓ Local branch deleted"
        else
            print_warning "  ⚠ Failed to delete local branch"
        fi
    fi
    
    echo ""
}

print_status "Branch Cleanup Script Starting..."
print_status "Repository: $(git config --get remote.origin.url)"
print_status "Current branch: $(git branch --show-current)"
echo ""

# Ensure we're on main branch
if [[ "$(git branch --show-current)" != "main" ]]; then
    print_status "Switching to main branch..."
    git checkout main
fi

# Update from remote
print_status "Updating from remote..."
git fetch --all --prune

echo ""
print_status "=== BRANCHES TO KEEP ==="
echo "• main (main branch)"
echo "• feature/copilot-integration-strategy (OPEN PR #72)"
echo "• copilot/fix-54 (OPEN PR #69)"
echo ""

# Branches that are SAFE TO DELETE (MERGED PRs)
MERGED_BRANCHES=(
    "refactor/consolidate-docs"
    "task/63-test-feature--add-user-profile"
    "feature/checkbox-enforcement-system"
    "test/checkbox-enforcement"
    "feature/60-hooks-integration"
    "fix/48-milestone-strategy"
    "feature/21-user-auth"
    "bug/9-final-workflow-test-after-fixe"
    "add-claude-github-actions-1755839064973"
)

# Branches that are SAFE TO DELETE (CLOSED PRs)
CLOSED_PR_BRANCHES=(
    "copilot/fix-43"
    "copilot/fix-26"
    "copilot/fix-3718b8e9-8c59-45da-a543-e01158271e19"
    "copilot/fix-23"
    "copilot/fix-21"
    "copilot/fix-13"
    "feature/test-full-pipeline"
    "copilot/fix-7"
    "copilot/fix-3f64bce0-806d-4efa-9249-59a74b3f5e32"
    "copilot/fix-1"
)

# Calculate total branches to delete
TOTAL_SAFE_BRANCHES=$((${#MERGED_BRANCHES[@]} + ${#CLOSED_PR_BRANCHES[@]}))

echo ""
print_status "=== SAFE TO DELETE - PHASE 1: MERGED PR BRANCHES ==="
echo "These branches have MERGED PRs and are safe to delete:"
for branch in "${MERGED_BRANCHES[@]}"; do
    echo "• $branch"
done

echo ""
print_status "=== SAFE TO DELETE - PHASE 1: CLOSED PR BRANCHES ==="
echo "These branches have CLOSED PRs and are safe to delete:"
for branch in "${CLOSED_PR_BRANCHES[@]}"; do
    echo "• $branch"
done

# Confirm deletion for safe branches
confirm_deletion $TOTAL_SAFE_BRANCHES

print_status "Starting Phase 1 cleanup (MERGED PRs)..."
for branch in "${MERGED_BRANCHES[@]}"; do
    delete_branch "$branch" "MERGED PR"
done

print_status "Starting Phase 1 cleanup (CLOSED PRs)..."
for branch in "${CLOSED_PR_BRANCHES[@]}"; do
    delete_branch "$branch" "CLOSED PR"
done

# Branches that need investigation (no PRs, recent commits)
echo ""
print_status "=== PHASE 2: BRANCHES NEEDING INVESTIGATION ==="
print_warning "The following branches have NO associated PRs but are recent:"
print_warning "These may be active development branches or stale feature attempts."
print_warning "Review each one manually before deciding to delete."
echo ""

NO_PR_BRANCHES=(
    "1-add-readme-documentation"
    "bug/51-test--bug-fix-milestone-assign"
    "bug/9--bug--final-workflow-test-afte"
    "claude/issue-1-20250822-0511"
    "enhance/46-feature-add-mcp-servers-and-what-clis-to-use"
    "enhance/48-improve-release-milestone-strategy-separate-featur"
    "enhance/52-enhance-github-workflows-auto-sync-pr-checkboxes-w"
    "enhance/53-feature-pr-checkbox-auto-sync-with-todowrite"
    "enhance/64-slash-command-redesign-simplify-to-create-issue-an"
    "enhance/71-implement-copilot-auto-assignment-strategy"
    "feature/21-user-authentication-flow"
    "feature/22-add-real-time-collaboration-fo"
    "feature/28-implement-user-dashboard-with"
    "feature/33-real-time-analytics-dashboard"
    "feature/37-payment-processing-system"
    "feature/39-database-schema-setup"
    "feature/40-user-authentication-api"
    "feature/45-test-feature--user-authenticat"
    "feature/45-test-feature-user-authentication"
    "feature/46--feature---add-mcp-servers-and"
    "feature/49-test--add-user-authentication"
    "feature/49-test-add-user-authentication-system"
    "feature/52-enhance-github-workflows--auto"
    "feature/53-feature--pr-checkbox-auto-sync"
    "feature/60-claude-code-hooks-integration"
    "feature/60-claude-code-hooks-integration-system"
    "feature/64-slash-command-redesign--simpli"
    "feature/71-implement-copilot-auto-assignm"
    "fix/51-test-bug-fix-milestone-assignment"
    "task/13--p0--critical--fix-project-boa"
    "task/13-critical--fix-project-board-au"
    "task/15--p1--frontend--test-complete-p"
    "task/15-frontend--test-complete-projec"
    "task/16--test--check-if-project-automa"
    "task/16-check-if-project-automation-wo"
    "task/17--p2--backend--test-with-update"
    "task/17-backend--test-with-updated-tok"
    "task/18--test--dynamic-workflow-test"
    "task/18-dynamic-workflow-test"
    "task/19--test--fixed-dynamic-workflow"
    "task/20--test--project--11-workflow"
    "task/20-project--11-workflow"
    "task/21-frontend--implement-user-authe"
    "task/22-add-real-time-collaboration-fo"
    "task/23-add-dashboard-analytics-for-ag"
    "task/26-build-notification-system-with"
    "task/34-design--real-time-analytics-da"
    "task/35-implementation--real-time-anal"
    "task/36-testing--real-time-analytics-d"
    "task/43-add-user-profile-management-ap"
    "task/54-diagnose-and-fix-github-workfl"
    "task/59-test--sync-pr-checkboxes-with"
    "task/66-test--issue-checkbox-enforceme"
    "task/8--test--workflow-permissions-va"
)

for branch in "${NO_PR_BRANCHES[@]}"; do
    last_commit=$(git log -1 --format="%ci" "origin/$branch" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    echo "• $branch (last commit: $last_commit)"
done

echo ""
print_warning "To delete Phase 2 branches, run this script with the --phase2 flag"
print_warning "Example: ./cleanup-branches.sh --phase2"
echo ""

# Check if user wants to run phase 2
if [[ "$1" == "--phase2" ]]; then
    echo ""
    print_status "=== PHASE 2 CLEANUP ==="
    print_warning "You are about to delete ${#NO_PR_BRANCHES[@]} branches with no PRs."
    print_warning "These branches may contain active development work!"
    echo ""
    
    confirm_deletion ${#NO_PR_BRANCHES[@]}
    
    print_status "Starting Phase 2 cleanup..."
    for branch in "${NO_PR_BRANCHES[@]}"; do
        delete_branch "$branch" "No PR, likely stale"
    done
fi

print_status "Branch cleanup completed!"
print_status "Summary:"
echo "• Deleted $TOTAL_SAFE_BRANCHES branches with MERGED/CLOSED PRs"
if [[ "$1" == "--phase2" ]]; then
    echo "• Deleted ${#NO_PR_BRANCHES[@]} branches with no PRs"
else
    echo "• ${#NO_PR_BRANCHES[@]} branches with no PRs require manual review"
fi

echo ""
print_status "Remaining branches:"
git branch -r | grep -v "HEAD" | sed 's/.*origin\///' | sort