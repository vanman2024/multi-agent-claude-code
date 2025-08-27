#!/bin/bash
# Git helper functions used by various scripts
# Source this file: source scripts/utilities/git-helpers.sh

# Get current branch
get_current_branch() {
    git branch --show-current 2>/dev/null
}

# Check if branch exists
branch_exists() {
    local branch="$1"
    git show-ref --verify --quiet "refs/heads/$branch"
}

# Get PR number for current branch
get_pr_number() {
    local branch="${1:-$(get_current_branch)}"
    gh pr list --head "$branch" --json number --jq '.[0].number' 2>/dev/null
}

# Check if working directory is clean
is_working_directory_clean() {
    [ -z "$(git status --porcelain)" ]
}

# Get list of changed files
get_changed_files() {
    git diff --name-only HEAD
}

# Safe commit with message
safe_commit() {
    local message="$1"
    if ! is_working_directory_clean; then
        git add -A
        git commit -m "$message" --no-verify
        return $?
    fi
    return 1
}

# Safe push to remote
safe_push() {
    local branch="${1:-$(get_current_branch)}"
    if [ -n "$branch" ]; then
        git push origin "$branch" --no-verify
        return $?
    fi
    return 1
}

# Create branch from main
create_branch_from_main() {
    local new_branch="$1"
    local main_branch="${2:-main}"
    
    git checkout "$main_branch" && \
    git pull origin "$main_branch" && \
    git checkout -b "$new_branch"
}

# Get repo info
get_repo_info() {
    local remote_url=$(git remote get-url origin 2>/dev/null)
    if [ -n "$remote_url" ]; then
        # Extract owner and repo from URL
        if [[ "$remote_url" =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
            echo "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
        fi
    fi
}