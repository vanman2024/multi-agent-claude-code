---
allowed-tools: Read(*), Bash(gh api*), TodoWrite(*)
description: Create GitHub Discussion for new ideas and concepts
argument-hint: "idea summary or description"
---

# Create Idea

## Context
- Idea template: @/home/gotime2022/Projects/multi-agent-claude-code/templates/discussions/idea-template.md
- Repository constants:
  - Repo ID: R_kgDOPiMFvA
  - Ideas Category ID: DIC_kwDOPiMFvM4Cui7U

## Important: Context Preservation
If the user references "what we discussed" or "that idea about X":
1. Ask ONE clarifying question to confirm understanding
2. Summarize what you think they mean
3. Then proceed with the decision question (Issue/Discussion/Skip)

## Your Task

When user runs `/create-idea $ARGUMENTS`, follow these exact steps:

### Step 1: Parse Input and Determine Type
Extract the idea summary from $ARGUMENTS
- If empty, ask user for a summary
- If too vague (less than 10 words), ask for more details

**CRITICAL: Ask the user what this should become:**
```
Based on what you've described, what should this become?

1. 📝 Issue - Ready to implement now (clear requirements)
2. 💭 Discussion - Needs exploration first (open questions)
3. ❌ Skip - Not worth tracking

Please enter 1, 2, or 3:
```

- If user chooses 1 (Issue): Stop here and suggest using `/create-issue` command instead
- If user chooses 2 (Discussion): Continue with Step 2
- If user chooses 3 (Skip): Exit with "Idea not tracked"

### Step 2: Load and Fill Template
1. READ file: @/home/gotime2022/Projects/multi-agent-claude-code/templates/discussions/idea-template.md
2. Fill template sections based on the summary:
   - **Title**: Extract a concise title from the summary (5-10 words)
   - **Context**: Expand summary into 2-3 sentences explaining why this matters
   - **Current State**: Identify 3 limitations or issues being addressed
   - **Proposed Solution**: Articulate the idea clearly in 2-3 sentences
   - **Benefits**: List 3 concrete improvements (efficiency, quality, DX)
   - **Complexity**: Assess based on scope (Low/Medium/High)
   - **Effort**: Estimate time (Days/Weeks/Months)
   - **Priority**: Determine urgency (Now/Soon/Later)
   - **Questions**: Generate 3 relevant questions to explore
   - **Next Steps**: Create 4 actionable checkbox items
   - **Resources**: Add placeholder for related issues/docs
   - **Category**: Identify from content (Workflow/Feature/Architecture/Integration)

### Step 3: Create Discussion via GitHub CLI
Execute this exact command with filled template:

```bash
# Escape special characters in title and body for JSON
TITLE="[FILLED_TITLE]"
BODY="[FILLED_BODY_WITH_ESCAPED_QUOTES_AND_NEWLINES]"

# Create the discussion and capture response
gh api graphql -f query='
mutation {
  createDiscussion(input: {
    repositoryId: "R_kgDOPiMFvA",
    categoryId: "DIC_kwDOPiMFvM4Cui7U",
    title: "'"$TITLE"'",
    body: "'"$BODY"'"
  }) {
    discussion {
      number
      url
    }
  }
}' --jq '.data.createDiscussion.discussion'

# Store the discussion number from the output (you'll see it in the response)
# For example, if output shows {"number": 57, "url": "..."}, use that number
```

### Step 3.5: Add @claude Comment for Analysis
After creating the discussion, immediately add a comment with @claude:

**Use the discussion number from Step 3 output:**

```bash
# Get the discussion number from the previous output (e.g., 57)
DISCUSSION_NUMBER=[NUMBER_FROM_PREVIOUS_OUTPUT]

# Add @claude comment using the discussion number
gh api repos/vanman2024/multi-agent-claude-code/discussions/$DISCUSSION_NUMBER/comments \
  -X POST \
  -f body="@claude Please provide a comprehensive analysis of this idea:

1. Assess technical feasibility
2. Identify potential challenges  
3. Suggest implementation approach
4. Estimate complexity and effort
5. Recommend if this should become an issue now or needs more exploration

Consider our existing codebase, architecture patterns, and current workflows in your analysis."

echo "✅ Added @claude for automated analysis"
```

### Step 4: Handle Response
1. Display the discussion URL
2. Confirm @claude comment was added
3. Show final output:
   ```
   ✅ Created Discussion: [title]
   📍 Category: Ideas
   🔗 URL: [discussion_url]
   🤖 @claude analysis requested
   ```
4. If any step failed, show error and suggest manual creation

### Step 5: Optional Issue Creation
Ask: "Would you like to create a tracking issue for this idea? (y/n)"

If yes:
- Use mcp__github__create_issue (if available) or gh issue create
- Title: "Explore: [idea title]"
- Body: Link to discussion + summary
- Labels: ["idea-exploration", "discussion"]

## Examples

### Basic Usage
```
/create-idea "Use Claude GitHub App for automated workflow validation"
```
Creates discussion about integrating Claude for workflow checks.

### Detailed Idea
```
/create-idea "Implement automatic PR checkbox syncing between TodoWrite and GitHub PRs to maintain consistency"
```
Creates discussion with full implementation approach.

### Category Hint
```
/create-idea "workflow: Add pre-commit hooks for automatic code formatting"
```
Recognizes "workflow" category from prefix.

## Error Handling
- Empty input: Prompt for idea summary
- GraphQL error: Display error message and manual instructions
- Network issues: Retry once, then fail gracefully

## Output Format
```
✅ Created Discussion: [title]
📍 Category: Ideas
🔗 URL: https://github.com/vanman2024/multi-agent-claude-code/discussions/[number]
🤖 @claude analysis requested (check discussion for AI insights)

Would you like to create a tracking issue? (y/n)
```