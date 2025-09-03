#!/bin/bash

# Convert a discussion to an issue
# Note: GitHub API doesn't support native conversion, so we create a linked issue

echo "⚠️  Note: GitHub API doesn't support native discussion->issue conversion."
echo "This will create a new issue linked to the discussion."
echo ""

# List discussions first
./scripts/idea/list.sh

echo ""
echo -n "Enter discussion number to convert: "
read NUMBER

# Get discussion details
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

# Analyze content to determine issue type
echo "Analyzing discussion content to determine issue type..."

# Default to enhancement
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
echo -n "Press Enter to accept '$ISSUE_TYPE' or choose [1-4]: "
read USER_CHOICE

case "$USER_CHOICE" in
  1) ISSUE_TYPE="feature" ;;
  2) ISSUE_TYPE="enhancement" ;;
  3) ISSUE_TYPE="bug" ;;
  4) ISSUE_TYPE="task" ;;
  "") echo "Using suggested type: $ISSUE_TYPE" ;;
esac

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