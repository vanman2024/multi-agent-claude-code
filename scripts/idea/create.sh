#!/bin/bash

# Create a new discussion
# Usage: ./create.sh [topic]

TOPIC="$1"

# If no topic provided, ask for it
if [[ -z "$TOPIC" ]]; then
  echo "What idea would you like to discuss?"
  read TOPIC
fi

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