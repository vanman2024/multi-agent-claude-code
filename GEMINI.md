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

## Required Configuration

For the Gemini integration to work properly, you need to set up the following secrets and variables:

### Required Secrets
- `GEMINI_API_KEY` - Your Google AI Studio API key (get from https://makersuite.google.com/app/apikey)

### Required Variables  
- `GEMINI_MODEL` - Set to `"gemini-1.5-pro"` (required for Linux compatibility)
- `GEMINI_CLI_VERSION` - Set to `"latest"` or specific version

### Optional GitHub App Variables (for enhanced authentication)
- `APP_ID` - GitHub App ID
- `APP_PRIVATE_KEY` - GitHub App private key

### Optional Google Cloud Variables (for advanced features)
- `GCP_WIF_PROVIDER` - Workload Identity Provider
- `GOOGLE_CLOUD_PROJECT` - GCP Project ID  
- `GOOGLE_CLOUD_LOCATION` - GCP Region
- `SERVICE_ACCOUNT_EMAIL` - GCP Service Account
- `GOOGLE_GENAI_USE_VERTEXAI` - Use Vertex AI (true/false)
- `GOOGLE_GENAI_USE_GCA` - Use Gemini Code Assist (true/false)

## Setting Up Variables

```bash
# Required secrets
gh secret set GEMINI_API_KEY --body "your-api-key-here"

# Required variables  
gh variable set GEMINI_MODEL --body "gemini-1.5-pro"
gh variable set GEMINI_CLI_VERSION --body "latest"

# Optional debugging
gh variable set DEBUG --body "false"
```

## Workflow Architecture

The Gemini integration uses several GitHub Actions workflows:

### Core Workflows
- **`gemini-dispatch.yml`** - Routes all Gemini requests to appropriate handlers
- **`gemini-invoke.yml`** - Handles general `@gemini` commands and questions
- **`gemini-triage.yml`** - Analyzes and labels individual issues
- **`gemini-pr-review.yml`** - Provides code review for pull requests

### Automation Workflows
- **`gemini-scheduled-triage.yml`** - Automatically triages unlabeled issues every 4 hours
- **`gemini-test-mode.yml`** - Safe testing environment for validating the integration

## Testing the Setup

### Safe Testing Mode

Before using Gemini in production, test the integration safely:

1. **Create a test issue** 
2. **Add the `test-gemini` label** to the issue
3. **The test mode workflow will run automatically**
4. **Check the issue for test results**

You can also trigger a manual test:
```bash
# Go to Actions tab > Gemini Test Mode > Run workflow
# Enter an issue number and test command
```

### Production Testing

1. Create a new issue or PR
2. Comment: `@gemini-cli are you there?`
3. Gemini should respond within a few minutes

If you don't see a response, check the [Actions tab](../../actions) for error logs.

## Automated Triage

The system includes **scheduled triage** that automatically:
- Runs every 4 hours
- Finds unlabeled issues
- Analyzes and applies appropriate labels
- Helps keep your repository organized

## Security Features

The integration includes several security measures:
- **Input validation** on all user requests
- **Restricted shell commands** (read-only operations only)
- **No write access** to system files
- **Safe command allowlist** (echo, ls, grep, etc.)
- **No network access** from shell commands

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