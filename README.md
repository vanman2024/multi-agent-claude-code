# Multi-Agent Claude Code

A comprehensive project demonstrating GitHub integration with Claude AI through Model Context Protocol (MCP) servers and automated workflows.

## 🎯 Overview

This project showcases how to integrate Claude AI with GitHub repositories using:
- **GitHub Actions workflows** for automated CI/CD and task management
- **Model Context Protocol (MCP) servers** for external tool interactions
- **Multi-agent collaboration** patterns for code development and review
- **Issue tracking and automation** with intelligent agent responses

## 🚀 Installation

### Prerequisites

- GitHub account with repository access
- Claude AI integration setup
- Basic understanding of GitHub Actions and workflows

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vanman2024/multi-agent-claude-code.git
   cd multi-agent-claude-code
   ```

2. **Set up GitHub Actions:**
   - The repository comes with pre-configured workflows in `.github/workflows/`
   - Ensure your repository has the necessary secrets configured for Claude integration

3. **Configure MCP servers (if using Claude Code):**
   ```bash
   # List configured servers
   claude mcp list
   
   # Add GitHub server
   claude mcp add github <github-server-url>
   
   # Verify connection
   /mcp
   ```

## 📖 Usage

### GitHub Integration

The project includes several automated workflows:

#### 1. Claude Code Integration (`claude.yml`)
- **Triggers:** Issue comments, PR reviews, issue creation
- **Functionality:** Responds to `@claude` mentions automatically
- **Usage:** Simply mention `@claude` in issues or PR comments

Example:
```
@claude can you help review this code change?
```

#### 2. CI/CD Pipeline (`ci.yml`)
- Automated testing and validation
- Code quality checks
- Deployment processes

#### 3. Auto-Assignment (`auto-assign.yml`)
- Automatically assigns issues and PRs
- Manages team workload distribution

#### 4. Scheduled Tasks (`scheduled-tasks.yml`)
- Regular maintenance tasks
- Automated cleanup and monitoring

### Working with Issues

Use the provided issue template (`issue-template.md`) for structured issue creation:

```markdown
## 📝 Description
[Brief description of the feature/bug/task]

## 🎯 Objective
[What problem does this solve?]

## 📋 Tasks
- [ ] Implementation
- [ ] Testing
- [ ] Documentation
```

### MCP Server Management

For Claude Code users, manage MCP servers using:

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Add new server
claude mcp add <server-name> <server-url>

# Remove server
claude mcp remove github
```

### WSL File Access (Windows Users)

When working in WSL and accessing Windows files:

```bash
# Windows path: C:/Users/user/Documents/project
# WSL path: /mnt/c/Users/user/Documents/project
```

## 🏗️ Project Structure

```
multi-agent-claude-code/
├── .github/
│   ├── workflows/          # GitHub Actions workflows
│   │   ├── claude.yml      # Claude AI integration
│   │   ├── ci.yml          # CI/CD pipeline
│   │   ├── auto-assign.yml # Auto-assignment
│   │   └── scheduled-tasks.yml
│   └── ISSUE_TEMPLATE/     # Issue templates
├── CLAUDE.md              # Claude-specific documentation
├── issue-template.md      # Structured issue template
└── README.md             # This file
```

## 🔧 Configuration

### GitHub Secrets

Ensure the following secrets are configured in your repository:

- `GITHUB_TOKEN`: For GitHub API access
- `CLAUDE_API_KEY`: For Claude AI integration (if applicable)

### Workflow Customization

Edit the workflow files in `.github/workflows/` to customize:

- Trigger conditions
- Agent response patterns
- Automation rules
- Notification settings

## 🤖 Multi-Agent Patterns

This project demonstrates several multi-agent collaboration patterns:

### 1. Issue Triage Agent
- Automatically labels and categorizes new issues
- Assigns appropriate team members
- Sets priorities and milestones

### 2. Code Review Agent
- Provides automated code reviews
- Suggests improvements and best practices
- Identifies potential issues early

### 3. Documentation Agent
- Maintains and updates documentation
- Ensures consistency across files
- Generates examples and guides

### 4. Testing Agent
- Runs automated tests
- Reports test results and coverage
- Suggests additional test scenarios

## 📚 Documentation

- [`CLAUDE.md`](./CLAUDE.md) - Claude Code specific documentation and MCP server management
- [`issue-template.md`](./issue-template.md) - Template for structured issue creation
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official GitHub Actions docs

## 🔗 Examples

### Creating an Issue with Agent Interaction

1. Create a new issue using the template
2. Mention `@claude` in the description or comments
3. The Claude workflow will automatically respond and assist

### Triggering Automated Workflows

```yaml
# Example workflow trigger
on:
  issues:
    types: [opened, assigned]
  issue_comment:
    types: [created]
```

### MCP Server Integration

```bash
# Check server status
/mcp

# Add development tools
claude mcp add dev-tools https://dev-tools-server.example.com

# List available functions
claude mcp get dev-tools
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and commit: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request and mention `@claude` for automated review

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- Create an issue for bug reports or feature requests
- Mention `@claude` for AI-assisted support
- Check existing workflows for automation capabilities
- Review documentation in `CLAUDE.md` for Claude-specific help

---

**Built with ❤️ using Claude AI and GitHub Actions**