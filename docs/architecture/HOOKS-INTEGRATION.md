# Claude Code Hooks Integration

> **Status**: 🟡 PARTIAL IMPLEMENTATION
> **Last Updated**: 2025-09-02
> **Stability**: Experimental

## Overview

Hooks provide local automation that complements GitHub's remote workflows.

## The Architecture: Local vs Remote

### GitHub Workflows (Remote)
- **What**: Actions that run on GitHub servers
- **When**: Issue/PR events
- **Purpose**: Plumbing - moves things without intelligence

### Claude Code Hooks (Local)
- **What**: Scripts that run in your terminal
- **When**: Before/after Claude actions
- **Purpose**: Intelligence - makes decisions

## Available Hooks

### Implemented
- `user-prompt-submit-hook` - Adds context to prompts
- Session start/end hooks

### Potential Future Hooks
- Pre-commit validation
- Test runner integration
- Documentation updates
- Linting enforcement

## Configuration

Hooks are configured in Claude Code settings:
1. Open settings
2. Add hook commands
3. They run automatically

## Best Practices

- Keep hooks fast (<1 second)
- Don't use for critical workflows
- Log output for debugging
- Handle failures gracefully

## Note

Hooks are still experimental. Use GitHub workflows for critical automation.