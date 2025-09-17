# AgentSwarm Bundle

This directory contains the production-ready AgentSwarm package.

## Files
- agentswarm/                 # Core code (CLI, orchestrator, workflows, docs)
- install.sh                  # Installation script (creates venv, installs deps)
- requirements.txt            # Production dependencies
- VERSION                     # AgentSwarm version (from agentswarm.toml)
- agentswarm                  # CLI entry point script (use `./agentswarm --help`)

## Usage
```bash
./install.sh
source venv/bin/activate
./agentswarm --help
```
