# Hooks Testing Guide

## Overview
Claude Code hooks enable automated actions triggered by specific events during development. Testing these hooks requires both automated scripts and manual verification in Claude Code.

## Test Script Location
```bash
./scripts/testing/test-hooks-integration.sh
```

## Hook Categories to Test

### 1. SessionStart Hooks
**Trigger:** When Claude Code session starts  
**Hook:** `load-context.sh`  
**Test:**
1. Start new Claude Code session
2. Check transcript mode (Ctrl+R) for context loading
3. Verify CLAUDE.md and project info loaded

### 2. UserPromptSubmit Hooks  
**Trigger:** When user submits a prompt  
**Hooks:** 
- `current-work.sh` - Injects GitHub issues/PRs
- `verify-sync-before-claude.sh` - Checks GitHub sync status

**Test:**
1. Submit any prompt in Claude Code
2. Check transcript for injected GitHub context
3. Verify sync warnings if out of date

### 3. PreToolUse Hooks
**Trigger:** Before tool execution  
**Hooks:**
- `test-before-push.sh` - Intercepts git push
- `log-agent-task.sh` - Logs Task tool usage

**Test:**
1. Run `git push` (without --no-verify)
2. Verify tests run before push proceeds
3. Use Task tool and check `.claude/logs/agent-tasks.log`

### 4. PostToolUse Hooks
**Trigger:** After tool execution  
**Hooks:**
- `auto-commit.sh` - Auto-commits file changes
- `sync-to-github.sh` - Pushes to GitHub
- `sync-todo-checkboxes.py` - Syncs TodoWrite with PR

**Test:**
1. Edit a file in Claude Code
2. Check `git log` for auto-commit
3. Verify GitHub has latest changes
4. Use TodoWrite and check PR checkbox updates

### 5. SubagentStop Hooks
**Trigger:** When subagent completes  
**Hook:** `sync-agent-results.py`  
**Test:**
1. Run Task tool with agent
2. Wait for completion
3. Check results synchronization

## Manual Testing Checklist

### Before Testing
- [ ] Run `./scripts/development/setup-local-env.sh`
- [ ] Export `CLAUDE_PROJECT_DIR=$(pwd)`
- [ ] Reload hooks with `/hooks` in Claude Code
- [ ] Enter transcript mode with `Ctrl+R`

### During Testing
- [ ] SessionStart: New session loads context
- [ ] UserPromptSubmit: GitHub issues injected
- [ ] Edit file: Auto-commit triggers
- [ ] Git push: Tests run first
- [ ] Task tool: Logged to file
- [ ] TodoWrite: PR checkboxes update

### After Testing
- [ ] Check `.claude/logs/` for errors
- [ ] Verify git history is clean
- [ ] Confirm GitHub sync worked
- [ ] Review transcript for issues

## Debugging Hook Issues

### Hook Not Firing
```bash
# Check hook is configured
jq '.hooks' .claude/settings.json

# Reload hooks
/hooks  # In Claude Code

# Check permissions
ls -la .claude/hooks/*.sh
```

### Hook Errors
```bash
# Check logs
tail -f .claude/logs/*.log

# Test hook manually
echo '{"tool_name":"Edit","file_path":"test.txt"}' | .claude/hooks/auto-commit.sh

# Enable debug mode
export CLAUDE_HOOKS_DEBUG=1
```

### Common Problems

| Problem | Solution |
|---------|----------|
| Hooks not executing | Reload with `/hooks` command |
| Permission denied | `chmod +x .claude/hooks/*.sh` |
| JSON parse errors | Check input format with `jq` |
| Git errors | Ensure on correct branch |
| Logs not created | Set `CLAUDE_PROJECT_DIR` |

## Automated Testing

Run the integration test:
```bash
./scripts/testing/test-hooks-integration.sh
```

This tests:
- Configuration validity
- Script syntax
- File permissions
- Log directory creation
- JSON parsing
- Git operations

## Expected Behavior

### Successful Hook Execution
```
[Transcript Mode]
> Running PreToolUse hook: test-before-push.sh
✅ Tests passed, proceeding with push
> Tool execution: Bash (git push)
> Running PostToolUse hook: sync-to-github.sh
🔄 Synced to GitHub
```

### Failed Hook
```
[Transcript Mode]
> Running PreToolUse hook: test-before-push.sh
❌ Tests failed, blocking push
> Tool execution blocked
```

## Performance Expectations

- Hooks should complete in < 2 seconds
- No blocking operations in hooks
- Async operations should be backgrounded
- Log files should stay < 10MB