---
allowed-tools: Bash(gh api *, gh issue *), mcp__github(*), Read(*), TodoWrite(*)
description: Create and manage ideas using GitHub Discussions
argument-hint: "[create|list|convert|view] [topic or discussion number]"
---

# Idea - GitHub Discussions Integration

## Purpose
Manage ideas through GitHub Discussions to keep the codebase clean and enable team collaboration.

## Command Syntax

When user runs `/idea $ARGUMENTS`, parse the command:

### 1. Create New Discussion
```bash
/idea "topic name"
/idea create "topic name"
```

### 2. List All Discussions
```bash
/idea list
/idea
```

### 3. Convert Discussion to Issue
```bash
/idea convert 121
```

### 4. View Specific Discussion
```bash
/idea view 121
```

## Implementation

### Create New Discussion

When creating a new discussion:

1. **Parse the topic**:
   ```bash
   # Extract topic from arguments
   if [[ "$1" == "create" ]]; then
     TOPIC="${@:2}"  # Everything after 'create'
   elif [[ "$1" != "list" && "$1" != "convert" && "$1" != "view" ]]; then
     TOPIC="$@"  # Entire argument is the topic
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

### List All Discussions

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

### Convert Discussion to Issue

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

### View Specific Discussion

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

## Smart Detection

Automatically determine intent from arguments:

```bash
# If no arguments or just "list"
if [[ -z "$ARGUMENTS" || "$ARGUMENTS" == "list" ]]; then
  # Show list of discussions
  
# If starts with number
elif [[ "$ARGUMENTS" =~ ^[0-9]+$ ]]; then
  # View that discussion number
  
# If starts with "convert" followed by number
elif [[ "$ARGUMENTS" =~ ^convert[[:space:]]+([0-9]+)$ ]]; then
  # Convert that discussion to issue
  
# If starts with "view" followed by number
elif [[ "$ARGUMENTS" =~ ^view[[:space:]]+([0-9]+)$ ]]; then
  # View that discussion
  
# Otherwise treat as new topic
else
  # Create new discussion with topic
fi
```

## Key Principles

1. **No code blocks** - Keep discussions readable as plain text
2. **Simple format** - Problem, approach, steps, decision
3. **GitHub native** - Use Discussions API, not local files
4. **Clean codebase** - No scratchpad folders or temp files
5. **Team visibility** - All ideas visible in GitHub

## Examples

### Create new idea:
```bash
/idea "Add user dashboard with analytics"
→ Creates Discussion #125: "Add user dashboard with analytics"
```

### List all ideas:
```bash
/idea list
→ Shows all discussions in Ideas category
```

### Convert to issue:
```bash
/idea convert 125
→ Creates issue from Discussion #125
→ Adds reference link in issue body
→ Comments on discussion with issue link
```

### View discussion:
```bash
/idea view 125
→ Shows full discussion with comments
```

## Error Handling

- If Discussions not enabled: "❌ GitHub Discussions must be enabled for this repository"
- If Ideas category missing: "❌ Please create an 'Ideas' category in GitHub Discussions"
- If discussion not found: "❌ Discussion #XXX not found"
- If GraphQL fails: Show error and suggest using GitHub web UI