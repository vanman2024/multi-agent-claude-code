# Claude Code Hooks

These minimal hooks enhance your local development workflow while letting GitHub automation handle the heavy lifting.

## Active Hooks

### 1. current-work.sh
- **Event**: UserPromptSubmit
- **Purpose**: Injects current GitHub issue context into every prompt
- **Benefit**: Claude always knows what issue you're working on

### 2. auto-commit.sh
- **Event**: PostToolUse (after Edit/Write/MultiEdit)
- **Purpose**: Creates atomic commits as you work
- **Benefit**: Automatic version history without thinking about it

### 3. test-before-push.sh
- **Event**: PreToolUse (before git push)
- **Purpose**: Runs tests before allowing push to GitHub
- **Benefit**: Prevents broken code from reaching CI/CD

## Installation

These hooks need to be registered in Claude Code. Run `/hooks` and add:

### UserPromptSubmit Hook
```json
{
  "hooks": [{
    "type": "command",
    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/current-work.sh"
  }]
}
```

### PostToolUse Hook (for auto-commit)
- Matcher: `Edit|Write|MultiEdit`
- Command: `$CLAUDE_PROJECT_DIR/.claude/hooks/auto-commit.sh`

### PreToolUse Hook (for test-before-push)
- Matcher: `Bash.*git push`
- Command: `$CLAUDE_PROJECT_DIR/.claude/hooks/test-before-push.sh`

## How They Work Together

1. **current-work.sh** runs when you start talking to Claude, adding issue context
2. **auto-commit.sh** creates commits as Claude edits files
3. **test-before-push.sh** validates everything before it goes to GitHub
4. GitHub workflows take over once code is pushed

## Why These Three?

- **Minimal**: Only what GitHub automation doesn't handle
- **Local-focused**: Work with your local development
- **Non-blocking**: Won't interrupt your flow (except test failures)
- **Complementary**: Work with, not against, your GitHub automation

## Testing

To test the hooks manually:

```bash
# Test current-work
./.claude/hooks/current-work.sh

# Test auto-commit (needs JSON input)
echo '{"tool_input":{"file_path":"test.md"}}' | ./.claude/hooks/auto-commit.sh

# Test before-push (needs JSON input)
echo '{"tool_input":{"command":"git push"}}' | ./.claude/hooks/test-before-push.sh
```