#!/bin/bash
# Pre-commit hook to encourage local testing
# This is a reminder hook - it won't block commits but will encourage good practices

echo ""
echo "🚨 PRE-COMMIT REMINDER 🚨"
echo ""
echo "Did you run local pre-commit testing?"
echo "  ./scripts/testing/local-pre-commit.sh"
echo ""
echo "This ensures your changes will pass GitHub Actions!"
echo ""
echo "To install this hook permanently:"
echo "  cp scripts/testing/install-git-hooks.sh .git/hooks/pre-commit"
echo ""
echo "Proceeding with commit..."
echo ""

# Always allow the commit to proceed (exit 0)
exit 0