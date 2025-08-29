# Claude Code Hooks Guide

## Quick Start

Claude Code hooks are now fully integrated and ready to use! This guide explains how to use and customize the hooks system for your local development workflow.

## Active Hooks

### 1. **load-context.sh** (SessionStart)
- **When**: Claude Code session starts
- **What**: Loads project context including git state, assigned issues, and open PRs
- **Why**: Gives Claude immediate awareness of your current work

### 2. **current-work.sh** (UserPromptSubmit)
- **When**: You submit a prompt
- **What**: Injects your current GitHub issues into context
- **Why**: Helps Claude understand what you're working on

### 3. **test-before-push.sh** (PreToolUse: Bash)
- **When**: Before any bash command executes
- **What**: Intercepts `git push` commands and runs tests
- **Why**: Prevents pushing broken code to GitHub

### 4. **auto-commit.sh** (PostToolUse: Edit|Write|MultiEdit)
- **When**: After file modifications
- **What**: Creates atomic commits automatically
- **Why**: Maintains granular git history

### 5. **log-agent-task.sh** (PreToolUse: Task)
- **When**: Before Task tool (agent) invocations
- **What**: Logs agent operations to `.claude/logs/`
- **Why**: Tracks multi-agent coordination

### 6. **sync-agent-results.py** (SubagentStop)
- **When**: After a subagent completes
- **What**: Captures and saves agent results
- **Why**: Coordinates multi-agent workflows

## Activating Hooks

### First Time Setup
1. Hooks are already configured in `.claude/settings.json`
2. Restart Claude Code or use `/hooks` command to activate
3. Use transcript mode (Ctrl+R) to see hook execution

### Testing Hooks
```bash
# Test that hooks are active
claude hooks

# See hook execution in real-time
# Press Ctrl+R to enter transcript mode
# Then run any command that triggers hooks
```

## Viewing Hook Output

### Transcript Mode
- Press **Ctrl+R** to enter transcript mode
- You'll see hook execution messages like:
  - `📝 Logged agent task: ...`
  - `🧪 Running tests before push...`
  - `✅ Tests passed! Proceeding with push...`

### Log Files
Hooks create logs in `.claude/logs/`:
- `agent-tasks.jsonl` - Structured agent task log
- `agent-tasks.log` - Human-readable agent log
- `agent-completions.jsonl` - Agent completion tracking

## Customizing Hooks

### Modify Existing Hooks
Edit any hook script in `.claude/hooks/`:
```bash
# Example: Change test command
vi .claude/hooks/test-before-push.sh
```

### Add New Hooks
1. Create script in `.claude/hooks/`
2. Make it executable: `chmod +x script.sh`
3. Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "EventName": [{
      "matcher": "ToolName",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
      }]
    }]
  }
}
```
4. Reload with `/hooks` in Claude Code

## Hook Events Reference

| Event | When It Fires | Common Use Cases |
|-------|--------------|------------------|
| SessionStart | Claude Code starts | Load context, setup environment |
| UserPromptSubmit | You submit a prompt | Inject context, validate prompts |
| PreToolUse | Before tool executes | Validate, block, or modify operations |
| PostToolUse | After tool completes | Log results, trigger followups |
| SubagentStop | Subagent completes | Sync results, coordinate agents |
| Stop | Claude finishes response | Cleanup, final checks |

## Troubleshooting

### Hooks Not Firing?
1. **Check configuration**: Run `claude hooks`
2. **Reload hooks**: Use `/hooks` command in Claude Code
3. **Check transcript mode**: Press Ctrl+R to see execution
4. **Verify permissions**: `chmod +x .claude/hooks/*.sh`

### Debug Mode
```bash
# Run Claude Code with debug output
claude --debug

# Check hook logs
tail -f .claude/logs/agent-tasks.log
```

### Common Issues

**Issue**: "Hooks configured but not executing"
- **Solution**: Restart Claude Code or use `/hooks` to reload

**Issue**: "Can't see hook output"
- **Solution**: Enter transcript mode with Ctrl+R

**Issue**: "Hook blocks operation unexpectedly"
- **Solution**: Check exit codes (exit 2 blocks, exit 0 allows)

## Best Practices

### Writing Hooks
1. **Fast execution**: Keep hooks under 1 second
2. **Clear output**: Use emojis and concise messages
3. **Proper exit codes**: 0=success, 2=block operation
4. **Error handling**: Always handle JSON parsing errors
5. **Logging**: Write to `.claude/logs/` for debugging

### Security
- Never log sensitive data (passwords, tokens)
- Validate all inputs
- Use absolute paths with `$CLAUDE_PROJECT_DIR`
- Escape shell variables properly
- Set timeouts for long operations

## Example: Custom Hook

Create a hook that notifies you when Claude modifies important files:

```bash
#!/bin/bash
# .claude/hooks/notify-important-changes.sh

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Check if editing important files
if [[ "$FILE_PATH" == *"package.json"* ]] || 
   [[ "$FILE_PATH" == *".env"* ]] || 
   [[ "$FILE_PATH" == *"database"* ]]; then
   
   echo "⚠️  Modifying important file: $FILE_PATH"
   
   # Could also send system notification
   # notify-send "Claude Code" "Modifying $FILE_PATH"
fi

exit 0  # Allow operation to proceed
```

## Next Steps

1. **Test current hooks**: Try a `git push` to see test-before-push in action
2. **Monitor logs**: Check `.claude/logs/` to see agent coordination
3. **Customize for your workflow**: Modify hooks to match your needs
4. **Share patterns**: Create reusable hooks for the team

## Support

- **Documentation**: See `.claude/hooks/README.md` for technical details
- **Examples**: Check individual hook files for implementation patterns
- **Issues**: Report problems in GitHub issues with `hooks` label

---

Remember: Hooks are YOUR personal development assistant. They run locally, enhance your workflow, and complement (not replace) GitHub's automation!