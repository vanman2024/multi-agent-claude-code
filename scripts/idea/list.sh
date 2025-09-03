#!/bin/bash

# List all discussions in Ideas category

echo "📋 Fetching discussions from Ideas category..."
echo ""

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