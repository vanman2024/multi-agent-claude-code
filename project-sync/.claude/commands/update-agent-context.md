# /update-agent-context

Updates AI agent context files based on the current feature plan.

## Usage

```
/update-agent-context [--claude] [--gemini] [--copilot] [--codex]
```

## Flags

- `--claude`: Update only CLAUDE.md
- `--gemini`: Update only GEMINI.md  
- `--copilot`: Update only .github/copilot-instructions.md
- `--codex`: Update only AGENT.md
- No flags: Update all existing agent context files

## What it does

1. Reads the current feature plan from `specs/{branch}/plan.md`
2. Extracts technology stack information (language, framework, database, etc.)
3. Updates the specified agent context files with new information
4. Preserves existing manual additions between markers
5. Updates recent changes (keeps last 3)

## File Mapping

- **Claude Code CLI** → `CLAUDE.md`
- **Gemini CLI** → `GEMINI.md`
- **GitHub Copilot** → `.github/copilot-instructions.md`  
- **Codex Agent** → `AGENT.md`

## Examples

```bash
# Update all existing agent files
/update-agent-context

# Update only Claude context
/update-agent-context --claude

# Update multiple specific agents
/update-agent-context --claude --gemini
```

## Implementation

Runs the script: `./scripts/update-agent-context.sh [agent_type]`