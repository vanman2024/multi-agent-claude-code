# PR Comments

## Purpose
Fetch and display all comments from a GitHub pull request, including both issue-level and code review comments.

## Usage
```
/pr-comments [PR_NUMBER|all|recent]
```

Options:
- `PR_NUMBER` - Show comments for specific PR (e.g., `/pr-comments 61`)
- `all` - Show comments from all open PRs
- `recent` - Show comments from the 3 most recent PRs (default)
- No argument - Shows comments from most recent PR or lists available PRs

## Your Task

When user runs `/pr-comments`, fetch and format PR comments using the MCP GitHub server:

### Step 1: Determine Which PR(s) to Check

**If no argument or "recent":**
1. Use `mcp__github__list_pull_requests` with state="open", sort="updated", perPage=3
2. Show comments from the most recent 3 PRs
3. If only 1 PR exists, show its comments
4. If multiple exist, show all their comments grouped by PR

**If "all":**
1. Use `mcp__github__list_pull_requests` with state="open"
2. Fetch comments for ALL open PRs

**If specific number provided:**
1. Use the provided PR number from $ARGUMENTS
2. Fetch comments for that specific PR only

**If current branch has a PR:**
1. Detect current git branch
2. Try to find PR associated with current branch name
3. If found, default to that PR

### Step 2: Fetch Comments Using MCP GitHub Server
**IMPORTANT: Use MCP GitHub tools exclusively - do NOT use gh CLI or bash commands**

Use these MCP tools:
1. `mcp__github__get_issue_comments` - Fetches PR-level discussion comments
   - Parameters: owner, repo, issue_number (PR number)
2. `mcp__github__get_pull_request_comments` - Fetches code review line comments  
   - Parameters: owner, repo, pullNumber
3. `mcp__github__get_pull_request` - Get PR details first
   - Parameters: owner, repo, pullNumber

### Step 3: Format Output

**For Single PR:**
```markdown
## PR #[NUMBER]: [TITLE]
**Status:** [open/closed] | **Author:** @[author] | **Updated:** [timestamp]

### Discussion Comments ([count])
[For each issue comment:]
**@[author]** - [timestamp]
> [comment body]

### Code Review Comments ([count])
[For each review comment:]
**@[author]** on `[file]:[line]`
```diff
[diff context if available]
```
> [comment body]
```

**For Multiple PRs:**
```markdown
## PR Comments Summary
Found [X] open PRs with [Y] total comments

---

### PR #[NUMBER]: [TITLE]
**[count] comments** - Last activity: [timestamp]

#### Recent Comments:
[Show last 2-3 comments from each PR]
**@[author]**: [truncated comment preview...]

---
[Repeat for each PR]

*Use `/pr-comments [NUMBER]` to see all comments for a specific PR*
```

### Step 4: Handle Edge Cases
- No comments: Display "No comments found on PR #[NUMBER]"
- PR not found: Display "PR #[NUMBER] not found"
- Not in git repo: Display "Not in a git repository"

## Implementation Details

### Required MCP GitHub Tools
**ALWAYS use the mcp__github__ tools - NEVER use gh CLI or bash commands:**

```javascript
// Get PR details
mcp__github__get_pull_request({
  owner: "vanman2024",  // or detected owner
  repo: "multi-agent-claude-code",  // or detected repo
  pullNumber: PR_NUMBER
})

// Get issue-level comments (discussion)
mcp__github__get_issue_comments({
  owner: "vanman2024",
  repo: "multi-agent-claude-code", 
  issue_number: PR_NUMBER
})

// Get code review comments
mcp__github__get_pull_request_comments({
  owner: "vanman2024",
  repo: "multi-agent-claude-code",
  pullNumber: PR_NUMBER
})
```

### Example Flow
1. First detect repository owner/name from git context or use defaults
2. Determine which PR(s) to check:
   - If number provided → fetch that specific PR
   - If "all" → fetch all open PRs
   - If "recent" or no arg → fetch 3 most recent PRs
   - Smart detection: Check if current branch has associated PR
3. For each PR:
   - Use `mcp__github__get_pull_request` to get PR title and details
   - Use `mcp__github__get_issue_comments` for discussion comments
   - Use `mcp__github__get_pull_request_comments` for code review comments
4. Format output based on single vs multiple PRs
5. Include helpful hints like total comment counts and navigation tips

### Smart PR Detection Priority
When no argument provided, check in this order:
1. Current git branch → find associated PR
2. Most recently updated PR with new comments
3. PR with most recent activity from the user
4. Fall back to showing list of available PRs

## Notes
- **CRITICAL**: Always use MCP GitHub server tools (mcp__github__*) 
- **NEVER** use gh CLI commands or bash for GitHub operations
- Format timestamps in relative format when possible
- Group comments by type (discussion vs code review)
- Show diff context for code review comments when available
- Handle cases where PR has no comments gracefully