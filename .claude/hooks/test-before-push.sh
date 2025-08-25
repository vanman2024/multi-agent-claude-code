#!/bin/bash
# Hook: Run tests before allowing git push
# Event: PreToolUse (Bash.*git push)
# Purpose: Prevents pushing broken code to GitHub

# Read the tool input
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Check if this is a git push command
if echo "$COMMAND" | grep -qE "git\s+push"; then
  echo "🧪 Running tests before push..."
  
  # Determine which test command to run based on project type
  if [ -f "package.json" ]; then
    # Node.js project
    if grep -q '"test"' package.json; then
      echo "Running: npm test"
      npm test
      TEST_RESULT=$?
    else
      echo "⚠️  No test script found in package.json"
      TEST_RESULT=0  # Don't block if no tests configured
    fi
  elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    # Python project
    if [ -f "pytest.ini" ] || [ -d "tests" ]; then
      echo "Running: pytest"
      pytest
      TEST_RESULT=$?
    else
      echo "⚠️  No tests found"
      TEST_RESULT=0
    fi
  elif [ -f "go.mod" ]; then
    # Go project
    echo "Running: go test ./..."
    go test ./...
    TEST_RESULT=$?
  else
    echo "⚠️  Unknown project type, skipping tests"
    TEST_RESULT=0
  fi
  
  if [ $TEST_RESULT -ne 0 ]; then
    echo "❌ Tests failed! Push blocked."
    echo "Fix the failing tests before pushing."
    exit 2  # Exit code 2 blocks the operation
  else
    echo "✅ Tests passed! Proceeding with push..."
  fi
fi

# Pass through for non-push commands
exit 0