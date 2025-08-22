# Multi-Agent Claude Code

A demonstration repository showcasing GitHub integration with Claude Code for automated code assistance and review capabilities.

## Overview

This repository demonstrates how to set up and use Claude Code's GitHub Actions integration to provide AI-powered code assistance directly in your GitHub workflow. It includes two main automation workflows:

- **Interactive Claude Code**: Responds to `@claude` mentions in issues and pull requests
- **Automated Code Review**: Provides automatic code reviews on pull requests

## Features

- 🤖 **AI-Powered Code Assistance**: Get help with coding tasks by mentioning `@claude` in issues or PR comments
- 📝 **Automated Code Reviews**: Receive detailed code reviews automatically on pull requests
- 🔧 **Flexible Configuration**: Customize trigger phrases, models, and behavior for your specific needs
- 🛡️ **Secure Integration**: Uses OAuth tokens for secure communication with Claude Code services

## Installation

### Prerequisites

- A GitHub repository with admin access
- A Claude Code OAuth token from Anthropic

### Setup Steps

1. **Clone this repository or copy the workflow files**:
   ```bash
   git clone https://github.com/vanman2024/multi-agent-claude-code.git
   cd multi-agent-claude-code
   ```

2. **Set up the required secret**:
   - Go to your repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add a new repository secret named `CLAUDE_CODE_OAUTH_TOKEN`
   - Set the value to your Claude Code OAuth token

3. **Copy the workflow files to your repository**:
   ```bash
   mkdir -p .github/workflows
   cp .github/workflows/claude.yml .github/workflows/
   cp .github/workflows/claude-code-review.yml .github/workflows/
   ```

4. **Customize the workflows** (optional):
   - Edit the workflow files to match your project needs
   - Configure allowed tools, custom instructions, or trigger phrases
   - Set up file path filters for code reviews

## Usage

### Interactive Code Assistance

Once set up, you can get help from Claude Code by mentioning `@claude` in:

- **Issue comments**: Ask questions, request implementations, or get explanations
- **Pull request comments**: Get help with specific code changes or reviews
- **Pull request reviews**: Include `@claude` in your review comments

#### Example Usage

**In an issue comment:**
```
@claude Can you help me implement a user authentication system using JWT tokens?
```

**In a pull request comment:**
```
@claude Please review this function for potential security issues and suggest improvements.
```

### Automated Code Reviews

The automated review workflow runs on every pull request and provides:

- Code quality analysis
- Best practices recommendations
- Potential bug identification
- Security considerations
- Performance suggestions

Reviews are posted as comments on the pull request automatically.

## Configuration Options

### Claude Code Workflow (`claude.yml`)

```yaml
# Optional: Specify model
model: "claude-sonnet-4"  # or "claude-opus-4-1-20250805"

# Optional: Custom trigger phrase
trigger_phrase: "/claude"  # instead of "@claude"

# Optional: Allow specific commands
allowed_tools: "Bash(npm install),Bash(npm run build),Bash(npm run test:*)"

# Optional: Custom instructions
custom_instructions: |
  Follow our coding standards
  Ensure all new code has tests
  Use TypeScript for new files
```

### Code Review Workflow (`claude-code-review.yml`)

```yaml
# Optional: Filter by file types
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"

# Optional: Filter by author association
if: github.event.pull_request.author_association == 'FIRST_TIME_CONTRIBUTOR'

# Optional: Use sticky comments
use_sticky_comment: true
```

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       ├── claude.yml                # Interactive Claude Code workflow
│       └── claude-code-review.yml    # Automated review workflow
├── CLAUDE.md                         # Claude Code configuration and instructions
└── README.md                         # This file
```

## Workflow Triggers

### Interactive Claude Code
- Issue comments containing `@claude`
- Pull request review comments containing `@claude`
- Pull request reviews containing `@claude`
- Issues opened/assigned with `@claude` in title or body

### Automated Code Review
- Pull requests opened
- Pull requests synchronized (new commits pushed)

## Security Considerations

- The workflows use OAuth tokens for authentication
- Claude Code has read-only access to repository contents
- No sensitive information should be included in prompts or responses
- Review generated code before merging

## Troubleshooting

### Common Issues

1. **Claude doesn't respond to mentions**:
   - Check that the `CLAUDE_CODE_OAUTH_TOKEN` secret is set correctly
   - Verify the workflow file syntax is valid
   - Ensure the mention includes `@claude` exactly

2. **Automated reviews not working**:
   - Check the workflow triggers in `claude-code-review.yml`
   - Verify file path filters if configured
   - Review workflow permissions

3. **Workflow failures**:
   - Check the Actions tab for error details
   - Verify OAuth token permissions
   - Review workflow logs for specific error messages

### Getting Help

- Review the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- Check workflow run logs in the Actions tab
- Create an issue in this repository for support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the Claude Code workflows
5. Submit a pull request

## License

This project is provided as a demonstration and reference implementation. Feel free to use and modify for your own projects.

---

*Generated with [Claude Code](https://claude.ai/code)*