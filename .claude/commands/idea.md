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

**Note**: GitHub doesn't provide native API support for converting discussions to issues.
This command creates a new issue linked to the discussion, but the discussion remains open.
The native "Convert to Issue" button is only available in the GitHub UI.

When converting discussion #NUMBER to issue:

1. **Get discussion details**:
   ```bash
   DISCUSSION=$(gh api graphql -f query="
     query {
       repository(owner: \"vanman2024\", name: \"multi-agent-claude-code\") {
         discussion(number: $NUMBER) {
           id
           title
           body
           url
         }
       }
     }" --jq '.data.repository.discussion')
   
   DISCUSSION_ID=$(echo $DISCUSSION | jq -r .id)
   TITLE=$(echo $DISCUSSION | jq -r .title)
   BODY=$(echo $DISCUSSION | jq -r .body)
   URL=$(echo $DISCUSSION | jq -r .url)
   ```

2. **Analyze content to determine issue type**:
   ```bash
   # Analyze discussion content for keywords
   echo "Analyzing discussion content to determine issue type..."
   
   # Default to feature for new functionality
   ISSUE_TYPE="enhancement"
   
   # Check for bug indicators
   if echo "$TITLE $BODY" | grep -iE "(bug|fix|broken|error|issue|problem)" > /dev/null; then
     echo "Detected bug-related keywords"
     ISSUE_TYPE="bug"
   fi
   
   # Check for feature indicators
   if echo "$TITLE $BODY" | grep -iE "(feature|new|add|create|implement)" > /dev/null; then
     echo "Detected feature-related keywords"
     ISSUE_TYPE="feature"
   fi
   
   # Ask user to confirm or change
   echo ""
   echo "Suggested type: $ISSUE_TYPE"
   echo ""
   echo "What type of issue should this become?"
   echo "1. feature - New functionality"
   echo "2. enhancement - Improve existing feature"
   echo "3. bug - Something to fix"
   echo "4. task - Work item"
   echo ""
   echo "Press Enter to accept '$ISSUE_TYPE' or choose [1-4]:"
   read USER_CHOICE
   
   case "$USER_CHOICE" in
     1) ISSUE_TYPE="feature" ;;
     2) ISSUE_TYPE="enhancement" ;;
     3) ISSUE_TYPE="bug" ;;
     4) ISSUE_TYPE="task" ;;
     "") echo "Using suggested type: $ISSUE_TYPE" ;;
   esac
   ```

3. **Create the issue with appropriate template**:
   ```bash
   # Set title prefix based on type
   case "$ISSUE_TYPE" in
     feature) TITLE_PREFIX="[FEATURE]" ;;
     enhancement) TITLE_PREFIX="[ENHANCEMENT]" ;;
     bug) TITLE_PREFIX="[BUG]" ;;
     task) TITLE_PREFIX="[TASK]" ;;
   esac
   
   # Create issue with reference to discussion
   ISSUE_NUMBER=$(gh issue create \
     --title "$TITLE_PREFIX $TITLE" \
     --body "## Summary

Based on discussion: $URL

## Original Discussion

$BODY

## Implementation Requirements

- [ ] Analyze requirements from discussion feedback
- [ ] Design solution approach
- [ ] Implement core functionality
- [ ] Write tests for new code
- [ ] Update documentation
- [ ] Validate with stakeholders

## Acceptance Criteria

- [ ] Solution addresses the original discussion points
- [ ] Implementation follows project standards
- [ ] Tests pass and coverage maintained
- [ ] Documentation updated appropriately

## Metadata
**Converted from**: Discussion #$NUMBER
**Type**: $ISSUE_TYPE
**Priority**: TBD
**Size**: TBD" \
     --label "$ISSUE_TYPE" \
     --assignee "@me" | grep -oE '[0-9]+$')
   
   echo "✅ Created issue #$ISSUE_NUMBER from discussion #$NUMBER"
   
   # Add comment to discussion linking to the issue
   gh api graphql -f query="
     mutation {
       addDiscussionComment(input: {
         discussionId: \"$DISCUSSION_ID\"
         body: \"🔄 **Converted to Issue**\n\nThis discussion has been converted to issue #$ISSUE_NUMBER for implementation.\n\n➡️ Continue implementation discussion in the issue: #$ISSUE_NUMBER\n\n*Note: The discussion remains open for reference. Native API conversion is not available, so this was created as a new linked issue.*\"
       }) {
         comment {
           id
         }
       }
     }"
   
   echo "✅ Added comment to discussion linking to issue #$ISSUE_NUMBER"
   echo ""
   echo "⚠️  Note: The discussion remains open. You can manually close it in GitHub UI if desired."
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