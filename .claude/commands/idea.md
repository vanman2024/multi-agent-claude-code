---
allowed-tools: Bash(gh api *, gh issue *), mcp__github(*), Read(*), TodoWrite(*)
description: Create and manage ideas using GitHub Discussions
argument-hint: "[create|list|convert|view] [topic or discussion number]"
---

# Idea - GitHub Discussions Integration

## Purpose
Manage ideas through GitHub Discussions to keep the codebase clean and enable team collaboration.

## Command Flow

When user runs `/idea $ARGUMENTS`:

### If no arguments provided, show menu:
```
What would you like to do with ideas?

1. 💡 Create new discussion
2. 📋 List existing discussions  
3. 🔄 Convert discussion to issue
4. 👁️ View specific discussion

Choose [1-4]:
```

### Smart argument detection:
- If `$ARGUMENTS` is a number → View that discussion
- If `$ARGUMENTS` is text → Create new discussion with that topic
- If no arguments → Show menu above

## Implementation

### Menu Option 1: Create New Discussion

When creating a new discussion:

1. **Get the topic**:
   ```bash
   # If topic provided as argument, use it
   # Otherwise ask for it
   if [[ -n "$ARGUMENTS" && ! "$ARGUMENTS" =~ ^[0-9]+$ ]]; then
     TOPIC="$ARGUMENTS"
   else
     echo "What idea would you like to discuss?"
     read TOPIC
   fi
   ```

2. **Create the discussion using GraphQL**:
   ```bash
   # Get repository node ID
   REPO_ID=$(gh api graphql -f query='
     query {
       repository(owner: "vanman2024", name: "multi-agent-claude-code") {
         id
       }
     }' --jq '.data.repository.id')
   
   # Get Ideas category ID
   CATEGORY_ID=$(gh api graphql -f query='
     query {
       repository(owner: "vanman2024", name: "multi-agent-claude-code") {
         discussionCategories(first: 10) {
           nodes {
             id
             name
           }
         }
       }
     }' --jq '.data.repository.discussionCategories.nodes[] | select(.name == "Ideas") | .id')
   
   # Create the discussion
   DISCUSSION=$(gh api graphql -f query="
     mutation {
       createDiscussion(input: {
         repositoryId: \"$REPO_ID\"
         categoryId: \"$CATEGORY_ID\"
         title: \"$TOPIC\"
         body: \"## Problem Statement\\n\\nDescribe the problem this idea solves.\\n\\n## Proposed Approach\\n\\n1. Step one\\n2. Step two\\n3. Step three\\n\\n## Questions to Consider\\n\\n- What are the main challenges?\\n- Who will benefit from this?\\n- What resources are needed?\\n\\n## Next Steps\\n\\n- [ ] Gather feedback\\n- [ ] Refine approach\\n- [ ] Decide: Convert to issue or continue discussion\"
       }) {
         discussion {
           number
           url
         }
       }
     }" --jq '.data.createDiscussion.discussion')
   
   echo "✅ Created discussion #$(echo $DISCUSSION | jq -r .number)"
   echo "🔗 URL: $(echo $DISCUSSION | jq -r .url)"
   ```

### Menu Option 2: List All Discussions

```bash
# List discussions in Ideas category
gh api graphql -f query='
  query {
    repository(owner: "vanman2024", name: "multi-agent-claude-code") {
      discussions(first: 20, categoryId: "Ideas", orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          number
          title
          createdAt
          author {
            login
          }
          comments {
            totalCount
          }
        }
      }
    }
  }' --jq '.data.repository.discussions.nodes[] | 
    "Discussion #\(.number): \(.title)\n  Created: \(.createdAt | split("T")[0])\n  Author: \(.author.login)\n  Comments: \(.comments.totalCount)\n"'
```

### Menu Option 3: Convert Discussion to Issue

When converting discussion #NUMBER to issue:

1. **Get discussion details**:
   ```bash
   DISCUSSION=$(gh api graphql -f query="
     query {
       repository(owner: \"vanman2024\", name: \"multi-agent-claude-code\") {
         discussion(number: $NUMBER) {
           title
           body
           url
         }
       }
     }" --jq '.data.repository.discussion')
   
   TITLE=$(echo $DISCUSSION | jq -r .title)
   BODY=$(echo $DISCUSSION | jq -r .body)
   URL=$(echo $DISCUSSION | jq -r .url)
   ```

2. **Determine issue type**:
   ```
   What type of issue should this become?
   1. feature - New functionality
   2. enhancement - Improve existing feature
   3. bug - Something to fix
   4. task - Work item
   
   Choose [1-4]:
   ```

3. **Create the issue**:
   ```bash
   # Create issue with reference to discussion
   gh issue create \
     --title "$TITLE" \
     --body "## Summary
   
   Based on discussion: $URL
   
   ## Original Discussion
   
   $BODY
   
   ## Implementation Plan
   
   - [ ] Define requirements
   - [ ] Design solution
   - [ ] Implement feature
   - [ ] Write tests
   - [ ] Update documentation
   
   ## Acceptance Criteria
   
   [To be defined based on discussion feedback]" \
     --label "$ISSUE_TYPE"
   
   # Add comment to discussion
   gh api graphql -f query="
     mutation {
       addDiscussionComment(input: {
         discussionId: \"$DISCUSSION_ID\"
         body: \"This discussion has been converted to issue #$ISSUE_NUMBER\"
       }) {
         comment {
           id
         }
       }
     }"
   ```

### Menu Option 4: View Specific Discussion

```bash
# Get discussion details
gh api graphql -f query="
  query {
    repository(owner: \"vanman2024\", name: \"multi-agent-claude-code\") {
      discussion(number: $NUMBER) {
        title
        body
        createdAt
        author {
          login
        }
        comments(first: 10) {
          nodes {
            body
            author {
              login
            }
            createdAt
          }
        }
      }
    }
  }" --jq '
    .data.repository.discussion | 
    "Discussion #'$NUMBER': \(.title)\n" +
    "Author: \(.author.login)\n" +
    "Created: \(.createdAt | split("T")[0])\n\n" +
    "Body:\n\(.body)\n\n" +
    if .comments.nodes | length > 0 then
      "Comments:\n" + 
      (.comments.nodes | map("- \(.author.login): \(.body | split("\n")[0])") | join("\n"))
    else
      "No comments yet"
    end'
```

## Smart Detection Logic

```bash
# If no arguments → Show menu
if [[ -z "$ARGUMENTS" ]]; then
  # Display menu and get user choice
  
# If argument is a number → View that discussion
elif [[ "$ARGUMENTS" =~ ^[0-9]+$ ]]; then
  # Jump directly to viewing Discussion #$ARGUMENTS
  
# Otherwise → Create new discussion with that topic
else
  # Use $ARGUMENTS as the topic for new discussion
fi
```

## Key Principles

1. **No code blocks** - Keep discussions readable as plain text
2. **Simple format** - Problem, approach, steps, decision
3. **GitHub native** - Use Discussions API, not local files
4. **Clean codebase** - No scratchpad folders or temp files
5. **Team visibility** - All ideas visible in GitHub

## Examples

### Interactive menu:
```bash
/idea
→ Shows menu with 4 options
→ User selects action
```

### Quick create:
```bash
/idea "Add user dashboard with analytics"  
→ Skips menu, creates Discussion #125 directly
```

### Quick view:
```bash
/idea 125
→ Skips menu, shows Discussion #125 directly
```

### Convert workflow:
```bash
/idea
→ Choose option 3 (Convert)
→ Shows list of discussions
→ Select #125 to convert
→ Creates issue from Discussion #125

## Error Handling

- If Discussions not enabled: "❌ GitHub Discussions must be enabled for this repository"
- If Ideas category missing: "❌ Please create an 'Ideas' category in GitHub Discussions"
- If discussion not found: "❌ Discussion #XXX not found"
- If GraphQL fails: Show error and suggest using GitHub web UI