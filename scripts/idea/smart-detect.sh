#!/bin/bash

# Smart detection for /idea command
# Usage: ./smart-detect.sh [arguments]

ARGUMENTS="$1"

# If no arguments → Show menu
if [[ -z "$ARGUMENTS" ]]; then
  ./scripts/idea/menu.sh
  
# If argument is a number → View that discussion
elif [[ "$ARGUMENTS" =~ ^[0-9]+$ ]]; then
  ./scripts/idea/view.sh "$ARGUMENTS"
  
# Otherwise → Create new discussion with that topic
else
  ./scripts/idea/create.sh "$ARGUMENTS"
fi