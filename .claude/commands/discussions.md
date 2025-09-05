---
allowed-tools: mcp__github(*), Bash(gh api *, gh issue *), Read(*), TodoWrite(*)
description: Create and manage GitHub Discussions
argument-hint: "[topic or discussion number]"
---

# Discussions - GitHub Discussions Management

## Context
- Current branch: !`git branch --show-current`
- Repository: vanman2024/multi-agent-claude-code
- Idea template: @templates/idea-template.md

## Your Task

When user runs `/discussions $ARGUMENTS`, manage GitHub Discussions.

**IMPORTANT**: 
- DO NOT create any scripts or files
- Use MCP functions and Bash commands directly
- STOP after completing the requested action (don't update command files)
- To create issues from discussions, use `/work --discussion <number>` instead

### Initial Setup Check

First, verify GitHub Discussions are enabled:
1. Use mcp__github__list_discussion_categories to check if Discussions are enabled
2. Show available categories (General, Ideas, Q&A, Show and Tell, etc.)
3. If Discussions not enabled, inform user:
   - Go to repository Settings → Features → Enable Discussions
4. Let user choose which category to use for ideas (default to "Ideas" if exists, otherwise "General")

### Smart Argument Detection

**CRITICAL**: Check `$ARGUMENTS` first:
1. **If empty/no arguments** → Show the menu below (DO NOT create anything)
2. **If a number (e.g., "125")** → View Discussion #125 directly
3. **If text (e.g., "branching strategy")** → Create new discussion with that as the topic

### Menu Flow (ONLY when NO arguments provided)

When `$ARGUMENTS` is empty, show this menu and wait for user choice:
```
What would you like to do with discussions?

1. 💡 Create new discussion
2. 📋 List existing discussions  
3. 👁️ View specific discussion
4. 🔍 Find similar/overlapping discussions
5. 🔗 Consolidate multiple discussions

Choose [1-5]:
```

### Option 1: Create New Discussion

For topic provided in `$ARGUMENTS` or asked from user:
1. **Quick overlap check** (to avoid duplicates):
   - Use mcp__github__search_issues with key terms from topic (limit 5 results)
   - Check recent discussions in same category (limit 10)
   - If matches found, show them and ask if user wants to continue
2. Use mcp__github__list_discussion_categories to get available categories
3. Select appropriate category based on topic (Ideas, General, Q&A, etc.)
4. Format discussion:
   - **Title**: Just the topic itself (no prefix - category shows context)
   - **Body**: Use @templates/idea-template.md structure
   - **Category**: Acts like a single label (can't add multiple labels like issues)
5. Warn if similar issues/discussions exist but let user proceed if desired
6. Use gh CLI with GraphQL to create the discussion with proper mutation syntax
7. Show success message with discussion number and URL

### Option 2: List Discussions

1. Get all categories using mcp__github__list_discussion_categories
2. Ask user which category to view (or "All" for all discussions)
3. Use mcp__github__list_discussions with:
   - owner: "vanman2024"
   - repo: "multi-agent-claude-code"  
   - category: (selected category ID or omit for all)
   - perPage: 20
4. Display discussions with their category labels for context

### Option 3: View Specific Discussion

Use mcp__github__get_discussion with:
- owner: "vanman2024"
- repo: "multi-agent-claude-code"
- discussionNumber: chosen number

Then get comments with mcp__github__get_discussion_comments

### Option 4: Find Similar/Overlapping Content

When checking for overlaps (efficiently):
1. Ask user for keywords or topic to search
2. **Search existing issues** using mcp__github__search_issues:
   - Query: `"keyword1 keyword2" in:title,body is:open`
   - Limit to 10 most relevant results
   - Show issue number, title, and labels
3. **Search discussions** (recent only to save tokens):
   - Use mcp__github__list_discussions with perPage: 20
   - Filter client-side for matching keywords
4. Look for patterns:
   - Similar keywords (e.g., "milestone", "milestones", "milestone strategy")
   - Related concepts (e.g., "branching" and "git workflow")
   - Same feature areas (e.g., multiple auth-related discussions)
5. Show results grouped by type (Issues vs Discussions)
6. Suggest consolidation or linking if high overlap detected

### Option 5: Consolidate Multiple Discussions

For consolidating overlapping content:
1. **Check if existing issue already covers this**:
   - Search issues using main keywords
   - If suitable issue exists, link discussions to it instead
2. Let user select multiple discussions to consolidate
3. Analyze selected discussions for common themes
4. **Decision point**:
   - If existing issue found → Add discussions as comments/references
   - If no issue → Create new consolidated issue with:
     - Combined requirements from all discussions
     - Links to all source discussions
     - Clear sections for each aspect
     - Unified implementation plan
5. Add comments to each discussion linking to issue
6. Consider creating multiple focused issues if topics are distinct

**Note**: This prevents duplicate issues when topic already being worked on

## Discussion Lifecycle Management

### Using Labels for Status Tracking
We have dedicated discussion labels in .github/labels.yml for tracking lifecycle.

### Apply These Labels to Discussions:
- `discussion:exploring` - Initial state, gathering feedback
- `discussion:approved` - Ready for implementation
- `discussion:in-progress` - Being actively implemented
- `discussion:implemented` - Completed and deployed
- `discussion:declined` - Won't be implemented
- `discussion:blocked` - Waiting on dependencies

### Also Add Status Comments for Details

When a discussion progresses, update BOTH the label AND add a comment:

**Initial Discussion:**
```
📍 Status: Exploring
🎯 Goal: Gather feedback and refine idea
```

**When Creating Issue:**
```
📍 Status: In Progress
🔗 Issue: #[number]
📅 Started: [date]
```

**When PR Created:**
```
🚀 Status: Implementation Started
🔗 Issue: #[number]
📁 PR: #[number]
```

**When Complete:**
```
✅ Status: Implemented
🔗 Issue: #[number] (closed)
📁 PR: #[number] (merged)
📦 Released: [version/date]
```

### Optional Title Prefixes
Since we can't use labels, you may optionally use minimal title prefixes:
- `[WIP]` - Work in progress
- `[DONE]` - Implemented
- No prefix = Still exploring

But comments are the primary tracking mechanism.

## Key Principles

1. **No code blocks** - Keep discussions readable as plain text
2. **GitHub native** - Use Discussions API, not local files
3. **Clean codebase** - No scratchpad folders or temp files
4. **Team visibility** - All ideas visible in GitHub
5. **Comment-based tracking** - Use status comments since labels are restricted

## API Limitations

- GitHub doesn't expose native "Convert to Issue" functionality via API
- Discussions cannot be automatically closed when converted
- Manual UI interaction required for native conversion
- **Use `/work --discussion <number>` to create issues from discussions with proper workflow**

## Efficiency Considerations

- **Don't list ALL issues** - Use search API with specific keywords (saves tokens)
- **Limit results** - Cap searches at 5-10 most relevant items
- **Use targeted queries** - `is:open` `in:title,body` filters for better results
- **Check issues first** - Prevents creating discussions for already-tracked work

## Error Handling

- If Discussions not enabled: "❌ GitHub Discussions must be enabled in Settings → Features"
- If no categories exist: "❌ Please create at least one Discussion category"  
- If discussion not found: "❌ Discussion #XXX not found"
- If API fails: Show error and suggest using GitHub web UI