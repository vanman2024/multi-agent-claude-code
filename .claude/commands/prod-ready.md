---
description: Scan project for mock implementations and production readiness issues
argument-hint: [--fix] [--verbose] [--format json|markdown]
allowed-tools: Bash, Read, Write, Task
---

Run comprehensive production readiness scan using the mock detection script and production specialist sub-agent.

## Execution Process

### Step 1: Run Mock Detection Script
```bash
python .claude/scripts/mock_detector.py --verbose --format markdown
```

### Step 2: Pass Results to Production Specialist
Use the production-specialist sub-agent to:
- Analyze the script results provided above
- Fix critical mock implementations found
- Validate the fixes work correctly
- Perform additional targeted scans with grep/read tools

### Step 3: Handle Arguments
- If `--fix` is provided, ask the production-specialist to attempt auto-fixes
- If `--verbose` is provided, include detailed file contents in analysis
- If `--format json` is provided, also generate JSON output for programmatic use

The production-specialist sub-agent will provide specific implementation steps for each critical issue found.