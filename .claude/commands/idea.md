---
allowed-tools: mcp__github(*), Bash(gh api *, gh issue *), Read(*), TodoWrite(*)
description: Create and manage ideas using GitHub Discussions
argument-hint: "[topic or discussion number]"
---

# Idea - GitHub Discussions Integration

## Context
- Current branch: !`git branch --show-current`
- Open discussions: !`gh api graphql -f query='query { repository(owner: "vanman2024", name: "multi-agent-claude-code") { discussions(first: 5, categoryId: "Ideas") { totalCount } } }' --jq '.data.repository.discussions.totalCount'`

## Your Task

When user runs `/idea $ARGUMENTS`, manage ideas through GitHub Discussions.

### Smart Argument Detection

Check what the user wants:
- If no arguments → Show interactive menu
- If `$ARGUMENTS` is a number → View Discussion #$ARGUMENTS  
- If `$ARGUMENTS` is text → Create new discussion with that topic

### Menu Flow (when no arguments)

Show this menu:
```
What would you like to do with ideas?

1. 💡 Create new discussion
2. 📋 List existing discussions  
3. 🔄 Convert discussion to issue
4. 👁️ View specific discussion

Choose [1-4]:
```

### Option 1: Create New Discussion

Get topic from user if not provided, then:
1. Get repository ID using mcp__github__search_repositories
2. Get Ideas category ID via GraphQL
3. Create discussion using GraphQL mutation with structured template

### Option 2: List Discussions

Use mcp__github__list_discussions with:
- owner: "vanman2024"
- repo: "multi-agent-claude-code"
- category: "Ideas"
- perPage: 20

### Option 3: Convert Discussion to Issue

**Note**: GitHub API doesn't support native conversion. We create a linked issue.

1. List discussions and let user choose one
2. Get discussion details via mcp__github__get_discussion
3. Analyze content for keywords to suggest issue type:
   - Bug keywords → suggest "bug"
   - Feature keywords → suggest "feature"  
   - Otherwise → suggest "enhancement"
4. Let user confirm or change type
5. Create issue with mcp__github__create_issue including:
   - Title with [TYPE] prefix
   - Link to original discussion
   - Implementation requirements checklist
   - Acceptance criteria
6. Add comment to discussion linking to new issue

### Option 4: View Specific Discussion

Use mcp__github__get_discussion with:
- owner: "vanman2024"
- repo: "multi-agent-claude-code"
- discussionNumber: chosen number

Then get comments with mcp__github__get_discussion_comments

## Key Principles

1. **No code blocks** - Keep discussions readable as plain text
2. **GitHub native** - Use Discussions API, not local files
3. **Clean codebase** - No scratchpad folders or temp files
4. **Team visibility** - All ideas visible in GitHub

## API Limitations

- GitHub doesn't expose native "Convert to Issue" functionality via API
- Discussions cannot be automatically closed when converted
- The conversion creates a new linked issue, not a true conversion
- Manual UI interaction required for native conversion

## Error Handling

- If Discussions not enabled: "❌ GitHub Discussions must be enabled"
- If Ideas category missing: "❌ Please create an 'Ideas' category in GitHub Discussions"  
- If discussion not found: "❌ Discussion #XXX not found"
- If API fails: Show error and suggest using GitHub web UI