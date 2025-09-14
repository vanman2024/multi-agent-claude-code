# Multi-Agent Development Team

## Agent Coordination System

This directory contains context files for each AI agent in our multi-agent development system.

### Active Agents

#### @claude (Architecture & Integration)
- **File**: `CLAUDE.md`
- **Specialization**: Complex architecture, multi-file integration, system design
- **MCP Access**: Full local server access (filesystem, git, github, memory, etc.)

#### @copilot (Code Generation)
- **File**: `COPILOT_SUMMARY.md` 
- **Specialization**: Simple implementations (Complexity ≤2, Size XS/S)
- **Auto-assignment**: Via GitHub for qualifying tasks

#### @gemini (Research & Documentation)
- **File**: `GEMINI.md`
- **Specialization**: Research, documentation, performance analysis
- **MCP Access**: filesystem, brave-search, memory

#### @qwen (Performance Optimization)
- **File**: `QWEN.md`
- **Specialization**: Performance optimization, algorithm improvement
- **MCP Access**: remote-filesystem, git, memory
- **Installation**: FREE via Ollama


### Task Assignment

All agents use the @symbol coordination system with markdown task files:

```markdown
- [ ] T001 @claude Design database schema
- [ ] T002 @copilot Implement API endpoints
- [ ] T003 @qwen Optimize query performance
- [ ] T005 @gemini Document API endpoints
```

### Updating Agent Context

Use the update script to keep agent context current:

```bash
# Update all agent contexts
./scripts/update-agent-context.sh all

# Update specific agent
./scripts/update-agent-context.sh claude
./scripts/update-agent-context.sh gemini
```

### Agent Communication

Agents coordinate through:
- **Task dependencies**: `(depends on T001)`
- **Shared memory**: MCP memory server
- **Git commits**: Standardized commit messages with agent identity
- **Issue comments**: Progress updates and coordination

