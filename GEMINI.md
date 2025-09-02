# Gemini Integration for Multi-Agent Development Framework

This repository integrates Google's **official** Gemini CLI through GitHub Actions, providing automated code review, issue triage, and general AI assistance powered by Google's `google-github-actions/run-gemini-cli` action.

## Quick Start

To use Gemini in this repository, simply mention `@gemini-cli` or `@gemini` in:
- Issue comments
- Pull request comments  
- Pull request reviews

### Examples

```bash
@gemini-cli /review          # Request code review
@gemini-cli /triage          # Request issue triage  
@gemini-cli help             # Show available commands
@gemini-cli explain this code # Ask questions about code

# Both formats work:
@gemini /review              # Alternative format
@gemini explain this code    # Alternative format
```

## Official Google Implementation

This integration uses Google's official `google-github-actions/run-gemini-cli@v0` action, which provides:
- **Full Gemini CLI capabilities** with tool calling support
- **GitHub integration** with gh CLI access
- **Code analysis and modification** capabilities
- **Plan-based execution** for complex tasks

## Multi-Agent Claude Code Project Context

This document provides context for interacting with the "Multi-Agent Claude Code" project.

## Project Overview

Based on the README.md file and initial directory analysis, this project appears to be a sophisticated multi-agent system designed to streamline software development workflows. It leverages GitHub Actions for CI/CD, integrates with GitHub Copilot for code generation and review, and incorporates Gemini AI for automated assistance. The system is highly structured, using hooks and a well-defined directory structure to manage agents, commands, and results.

The core workflow revolves around creating issues and then using AI assistance to implement them. The system intelligently routes tasks to appropriate AI agents based on complexity and requirements.

## Key Technologies

*   **GitHub Actions:**  The primary automation engine, managing CI/CD pipelines and various development tasks.
*   **GitHub Copilot:** Used for code generation, suggestions, and simpler code review tasks.
*   **Local Claude Instance:**  Handles more complex tasks requiring advanced reasoning and problem-solving capabilities.
*   **Node.js:** Used for the `agent-dispatcher.js` and likely other parts of the system.
*   **Python:** Used for various scripts, including those related to synchronization and automation.
*   **Vercel:** Used for deployment of the frontend and backend components.

## Directory Structure

*   `.claude/`: Contains agent definitions, commands, hooks, logs, and results.
*   `.github/`: Houses GitHub Actions workflows and configuration files.
*   `docs/`: Contains project documentation.
*   `scratchpad/`: Appears to be a workspace for notes, ideas, and drafts.
*   `scripts/`: Contains various scripts for automation and utility tasks.
*   `templates/`: Contains templates for issues, commands, and other project artifacts.
*   `tests/`: Contains test files and related resources.

## Commands

The project utilizes a set of commands, primarily accessed via the terminal.  Based on the README, the core commands are:

*   `/create-issue`: Creates a new issue, automatically routing it based on complexity and size.
*   `/work [issue number]`:  Starts the implementation process for a given issue, leveraging Copilot or Claude as needed.  Additional options include `--deploy` and `--test`.

Other commands include `/project-setup`, `/add-mcp`, and `/copilot-review`.

## Further Exploration

To gain a deeper understanding, further analysis of the following files is recommended:

*   `.github/workflows/*.yml`:  GitHub Actions workflows.
*   `.claude/agents/*.md`: Agent definitions.
*   `.claude/commands/*.md`: Command descriptions.
*   `scripts/*.sh` and `scripts/*.py`:  Various scripts used in the system.

This document will be updated as more information becomes available.