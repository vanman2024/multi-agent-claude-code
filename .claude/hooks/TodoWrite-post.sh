#!/bin/bash
# This hook runs after TodoWrite tool is used

# Register the session with the project
bash "$(dirname "$0")/register-session.sh" 2>/dev/null

echo "✅ Todo list updated and session registered"