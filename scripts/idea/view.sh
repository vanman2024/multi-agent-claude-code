#!/bin/bash

# View a specific discussion
# Usage: ./view.sh [number]

NUMBER="$1"

# If no number provided, ask for it
if [[ -z "$NUMBER" ]]; then
  echo -n "Enter discussion number to view: "
  read NUMBER
fi

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