# Testing Documentation

This directory contains documentation and guides for testing the Multi-Agent Claude Code framework locally.

## Test Categories

### 1. Hooks Testing
**Location:** Scripts in `scripts/testing/`  
**Documentation:** [hooks-testing.md](./hooks-testing.md)

- Session lifecycle hooks
- Tool-specific hooks  
- Integration with Claude Code
- Transcript mode verification

### 2. Slash Commands Testing  
**Location:** Scripts in `scripts/testing/`
**Documentation:** [slash-commands-testing.md](./slash-commands-testing.md)

- Command parsing
- MCP tool integration
- Parameter validation
- Error handling

### 3. Subagent Testing
**Location:** Scripts in `scripts/testing/`
**Documentation:** [subagents-testing.md](./subagents-testing.md)

- Agent assignment rules
- Copilot vs Claude routing
- Task coordination
- Results synchronization

### 4. GitHub Workflows Testing
**Location:** `.github/workflows/`
**Documentation:** [workflows-testing.md](./workflows-testing.md)

- Using `act` for local testing
- Workflow debugging
- Secrets and environment setup
- CI/CD pipeline validation

### 5. Integration Testing
**Location:** Scripts in `scripts/testing/`
**Documentation:** [integration-testing.md](./integration-testing.md)

- End-to-end scenarios
- Multi-component interactions
- Full feature workflows

## Quick Start

### Pre-Commit Testing (RECOMMENDED)
Run the same tests as GitHub Actions locally:
```bash
./scripts/testing/local-pre-commit.sh
```
**This is now required for all PRs.** See [Local Testing Workflow](../docs/LOCAL_TESTING_WORKFLOW.md)

### Run All Framework Tests
```bash
./scripts/testing/run-all-tests.sh
```

### Run Specific Test Suite
```bash
# Hooks only
./scripts/testing/run-all-tests.sh hooks

# Agents only  
./scripts/testing/run-all-tests.sh agents

# Commands only
./scripts/testing/run-all-tests.sh commands
```

## Testing Philosophy

### What to Test Locally (NEW: Pre-Commit Testing)
- **ALL GitHub Actions checks locally** - Use `./scripts/testing/local-pre-commit.sh`
- **Hooks execution** - Must verify in Claude Code transcript mode
- **Slash commands** - Manual execution required
- **Agent behavior** - Observe task assignment and coordination
- **Git operations** - Test branch creation, commits, pushes

### What Gets Automated
- **Code quality** - ESLint, ruff, type checking (CI/CD)
- **Unit tests** - Individual function testing (CI/CD) 
- **Build verification** - Compilation and bundling (CI/CD)
- **Security scans** - Dependency and code scanning (GitHub)

### What Can't Be Automated
- Claude Code session interactions
- Transcript mode visibility
- Real-time hook execution
- Agent spawning behavior
- GitHub API interactions (without mocks)

## Test Development Guidelines

1. **Documentation First** - Document the test scenario before writing scripts
2. **Scripts in scripts/** - All executable scripts go in `scripts/testing/`
3. **Docs in tests/** - All documentation and guides stay here
4. **Mock When Possible** - Use mock data instead of real API calls
5. **Independent Tests** - Each test should run standalone

## Required Tools

- `bash` - Shell scripting
- `jq` - JSON processing  
- `git` - Version control
- `gh` - GitHub CLI
- `claude` - Claude Code CLI (for hook testing)
- `act` - GitHub Actions local runner (optional)
- `shellcheck` - Shell script linting (recommended)

## Local Pre-Commit Testing Setup

To enable git hook reminders (optional):
```bash
cp scripts/testing/install-git-hooks.sh .git/hooks/pre-commit
```

## Debugging Tips

### Enable Debug Output
```bash
export DEBUG=1
export CLAUDE_HOOKS_DEBUG=1
```

### View Hook Execution
1. Start Claude Code
2. Press `Ctrl+R` for transcript mode
3. Execute actions that trigger hooks
4. Check `.claude/logs/` for detailed output

### Common Issues
- **Hooks not firing** - Reload with `/hooks` command
- **Scripts not executable** - Run `chmod +x scripts/testing/*.sh`
- **Path issues** - Check `CLAUDE_PROJECT_DIR` is set
- **Git issues** - Ensure on correct branch