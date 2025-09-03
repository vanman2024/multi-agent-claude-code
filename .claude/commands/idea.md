---
allowed-tools: mcp__github(*), Bash(gh api *, gh issue *), Read(*), TodoWrite(*)
description: Create and manage ideas using GitHub Discussions
argument-hint: "[topic or discussion number]"
---

# Idea - GitHub Discussions Integration

## Context
- Current branch: !`git branch --show-current`
- Repository: vanman2024/multi-agent-claude-code
- Idea template: @templates/idea-template.md

## Your Task

When user runs `/idea $ARGUMENTS`, manage ideas through GitHub Discussions.

### Initial Setup Check

First, verify GitHub Discussions are enabled:
1. Use mcp__github__list_discussion_categories to check if Discussions are enabled
2. Show available categories (General, Ideas, Q&A, Show and Tell, etc.)
3. If Discussions not enabled, inform user:
   - Go to repository Settings → Features → Enable Discussions
4. Let user choose which category to use for ideas (default to "Ideas" if exists, otherwise "General")

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
1. List available categories using mcp__github__list_discussion_categories
2. Ask user which category to use (suggest "Ideas" if exists, else "General")
3. Use the idea template structure from @templates/idea-template.md to format the discussion body
4. Create discussion using Bash with gh CLI, adapting the template format:
   - Category: User's choice or default
   - Title: User's topic
   - Body: Formatted using idea-template sections (Context, Current State, Proposed Solution, etc.)
5. Ensure the discussion follows the template structure for consistency

### Option 2: List Discussions

1. Get all categories using mcp__github__list_discussion_categories
2. Ask user which category to view (or "All" for all discussions)
3. Use mcp__github__list_discussions with:
   - owner: "vanman2024"
   - repo: "multi-agent-claude-code"  
   - category: (selected category ID or omit for all)
   - perPage: 20
4. Display discussions with their category labels for context

### Option 3: Convert Discussion to Issue

**Note**: GitHub API doesn't support native conversion. We create a linked issue.

1. List discussions and let user choose one
2. Get discussion details via mcp__github__get_discussion
3. Analyze content for keywords to suggest issue type:
   - Bug keywords → suggest "bug" (use @templates/local_dev/bug-template.md)
   - Feature keywords → suggest "feature" (use @templates/local_dev/feature-template.md)
   - Otherwise → suggest "task" (use @templates/local_dev/task-template.md)
4. Let user confirm or change type
5. Create issue with mcp__github__create_issue:
   - Use appropriate template based on type
   - Title with [TYPE] prefix
   - Link to original discussion
   - Adapt discussion content to fit the chosen template structure
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

- If Discussions not enabled: "❌ GitHub Discussions must be enabled in Settings → Features"
- If no categories exist: "❌ Please create at least one Discussion category"  
- If discussion not found: "❌ Discussion #XXX not found"
- If API fails: Show error and suggest using GitHub web UI