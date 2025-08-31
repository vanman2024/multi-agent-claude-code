# Claude Code Hooks Testing Guide

## Testing Strategy

Our testing approach is divided into three layers:

### 1. CI/CD Automated Tests (GitHub Actions)
**What**: Code quality, syntax, type checking, coverage
**When**: On every push and PR
**Where**: `.github/workflows/`

- ✅ Syntax validation (ESLint, ruff, etc.)
- ✅ Type checking (TypeScript, mypy)
- ✅ Unit test execution
- ✅ Code coverage reports
- ✅ Security scanning

### 2. Hook Unit Tests (Local/CI)
**What**: Individual hook function testing
**When**: Before PR merge, during development
**Where**: `.claude/hooks/tests/`

Run unit tests:
```bash
# Bash hook tests
bash .claude/hooks/tests/test_hooks.sh

# Python hook tests  
python -m pytest .claude/hooks/tests/
```

Tests cover:
- JSON parsing and input handling
- File path validation
- Git operation safety
- Log file creation
- Environment variable handling
- Error conditions

### 3. Integration Testing (Local Manual)
**What**: End-to-end hook behavior in Claude Code
**When**: Before marking PR complete
**Where**: Local Claude Code session

Run integration tests:
```bash
# Run the comprehensive test script
./test-hooks-locally.sh
```

Manual verification required for:
- Hook execution in transcript mode (Ctrl+R)
- Slash command functionality
- Agent spawning and coordination
- TodoWrite ↔ GitHub sync
- Auto-commit and push behavior

## Testing Checklist

### Before Creating PR
- [ ] Run unit tests locally
- [ ] Test hooks in transcript mode
- [ ] Verify slash commands work
- [ ] Check log files for errors

### Before Merging PR
- [ ] All CI checks pass
- [ ] Unit tests pass (automated)
- [ ] Integration tests complete (manual)
- [ ] @claude bot review complete
- [ ] PR checkboxes validated

## Hook-Specific Testing

### SessionStart Hooks
```bash
# Test: Restart Claude Code session
# Expected: load-context.sh runs
# Verify: Context message in transcript
```

### UserPromptSubmit Hooks
```bash
# Test: Submit any prompt
# Expected: current-work.sh injects context
# Verify: GitHub issues shown in transcript
```

### PreToolUse Hooks
```bash
# Test: Run git push
# Expected: test-before-push.sh intercepts
# Verify: Tests run before push

# Test: Use Task tool
# Expected: log-agent-task.sh logs
# Verify: Check .claude/logs/agent-tasks.log
```

### PostToolUse Hooks
```bash
# Test: Edit any file
# Expected: auto-commit.sh and sync-to-github.sh trigger
# Verify: Git log shows commits, GitHub has latest

# Test: Use TodoWrite
# Expected: sync-todo-checkboxes.py runs
# Verify: PR checkboxes update
```

## Creating New Tests

### For New Hooks
1. Add unit test to `.claude/hooks/tests/`
2. Add integration test to `test-hooks-locally.sh`
3. Document expected behavior here
4. Test in Claude Code transcript mode

### For Slash Commands
1. Test command parsing
2. Test MCP tool integration
3. Test error handling
4. Document in command file

## Known Testing Limitations

### Cannot Automate
- Claude Code session interactions
- Transcript mode verification
- Agent spawning behavior
- Real GitHub API interactions (need mocks)
- Hook timing and sequencing

### Must Test Manually
- Slash command execution
- Hook visibility in transcript
- Agent coordination
- GitHub sync timing
- Error recovery

## Testing Tools

### Required
- `jq` - JSON parsing
- `bash` - Shell testing
- `python3` - Python tests
- `git` - Version control
- `gh` - GitHub CLI

### Optional
- `pytest` - Python testing framework
- `shellcheck` - Shell script linting
- `coverage` - Code coverage

## Debugging Hooks

### Enable Debug Mode
```bash
# In hook scripts, add:
DEBUG=1  # Enable debug output

# Or set globally:
export CLAUDE_HOOKS_DEBUG=1
```

### View Hook Execution
1. Enter transcript mode: `Ctrl+R`
2. Execute action that triggers hook
3. Check transcript for hook output
4. Check `.claude/logs/` for detailed logs

### Common Issues
- **Hooks not firing**: Reload with `/hooks` command
- **Permission denied**: Run `chmod +x .claude/hooks/*.sh`
- **JSON parse errors**: Check input format with `jq`
- **Git errors**: Ensure on correct branch
- **Log not created**: Check `CLAUDE_PROJECT_DIR` is set

## Test Coverage Requirements

### Minimum Coverage
- All hooks must have unit tests
- All slash commands must be tested
- Critical paths must have integration tests
- Error conditions must be tested

### Coverage Goals
- Unit test coverage: 80%+
- Integration test coverage: Core flows
- Manual test coverage: All user-facing features