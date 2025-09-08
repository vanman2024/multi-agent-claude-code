#!/bin/bash
# Hook: TodoWrite-post
# Purpose: Register session with project only

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Just register the session with the project
bash "$(dirname "$0")/register-session.sh" 2>/dev/null

exit 0