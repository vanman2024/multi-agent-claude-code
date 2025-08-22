# Multi-Agent Claude Code Repository

A comprehensive template repository demonstrating advanced GitHub integration with Claude Code for multi-agent collaboration, automated workflows, and intelligent code assistance.

## 🚀 Project Description

This repository showcases the power of multi-agent Claude Code integration with GitHub, featuring:

- **Intelligent Code Reviews**: Automated Claude-powered PR reviews with constructive feedback
- **Smart Issue Management**: Auto-assignment, labeling, and branch creation for issues
- **Scheduled Maintenance**: Automated dependency updates and repository cleanup
- **Comprehensive Templates**: Structured issue and PR templates for consistent collaboration
- **CI/CD Pipeline**: Automated testing, security scanning, and deployment workflows
- **MCP Integration**: GitHub Model Context Protocol (MCP) server integration for seamless tool usage

Perfect for teams looking to enhance their development workflow with AI-powered automation and intelligent code assistance.

## 📋 Table of Contents

- [Installation](#-installation)
- [GitHub MCP Integration](#-github-mcp-integration)
- [Key GitHub MCP Tools](#-key-github-mcp-tools)
- [Creating Issues with Templates](#-creating-issues-with-templates)
- [GitHub Actions Workflows](#-github-actions-workflows)
- [Issue and Workflow Templates](#-issue-and-workflow-templates)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Installation

### Prerequisites

- GitHub repository with Actions enabled
- Claude Code access with OAuth token
- Node.js 18+ (if extending with custom scripts)

### Setup Instructions

1. **Use this template**:
   ```bash
   # Use GitHub's template feature or clone directly
   git clone https://github.com/vanman2024/multi-agent-claude-code.git
   cd multi-agent-claude-code
   ```

2. **Configure Claude Code OAuth Token**:
   - Go to your repository Settings → Secrets and Variables → Actions
   - Add a new secret named `CLAUDE_CODE_OAUTH_TOKEN`
   - Set the value to your Claude Code OAuth token

3. **Customize workflows** (optional):
   - Edit `.github/workflows/*.yml` files to match your project needs
   - Update assignees in issue templates (`.github/ISSUE_TEMPLATE/*.yml`)
   - Modify branch names and triggers as needed

4. **Enable GitHub Actions**:
   - Ensure Actions are enabled in your repository settings
   - All workflows will automatically activate on the next push

## 🔧 GitHub MCP Integration

The repository includes comprehensive GitHub MCP (Model Context Protocol) integration that enables Claude to interact directly with your GitHub repository. Here's how to use it effectively:

### Basic Usage

**Trigger Claude in Issues or PRs**:
```markdown
@claude Can you help review this code change?
@claude Create a comprehensive test plan for this feature
@claude What are the potential security implications of this change?
```

**Automatic Code Reviews**:
- Claude automatically reviews all PRs opened in the repository
- Provides feedback on code quality, security, performance, and best practices
- Uses sticky comments that update with new commits

### Advanced MCP Commands

**Repository Analysis**:
```markdown
@claude Analyze the repository structure and suggest improvements
@claude Review all workflows and recommend optimizations
@claude Check for potential security vulnerabilities
```

**Issue Management**:
```markdown
@claude Create a detailed implementation plan for this feature
@claude Break down this issue into smaller subtasks
@claude Suggest relevant labels and assignees for this issue
```

### Configuration Options

The Claude workflows support extensive customization:

```yaml
# In .github/workflows/claude.yml
custom_instructions: |
  Follow our coding standards
  Ensure all new code has tests
  Use TypeScript for new files

allowed_tools: "Bash(npm install),Bash(npm run build),Bash(npm run test:*)"

# Different models available
model: "claude-opus-4-1-20250805"  # For advanced reasoning
# model: "claude-sonnet-4"         # Default, balanced performance
```

## 🧰 Key GitHub MCP Tools

This repository provides access to a comprehensive set of GitHub MCP tools:

### Repository Management
- **`github-get_file_contents`**: Read any file from the repository
- **`github-list_commits`**: Analyze commit history and changes
- **`github-get_commit`**: Detailed commit information and diffs
- **`github-list_branches`**: Branch management and analysis

### Issue and PR Management
- **`github-list_issues`**: Query and filter repository issues
- **`github-get_issue`**: Detailed issue information and context
- **`github-get_issue_comments`**: Full conversation history
- **`github-list_pull_requests`**: PR discovery and analysis
- **`github-get_pull_request`**: Comprehensive PR details
- **`github-get_pull_request_diff`**: Code change analysis
- **`github-get_pull_request_files`**: File-level change tracking

### Code Analysis
- **`github-search_code`**: Find specific code patterns across the repository
- **`github-list_code_scanning_alerts`**: Security and quality alerts
- **`github-get_code_scanning_alert`**: Detailed security analysis

### Workflow and Actions
- **`github-list_workflows`**: Discover available workflows
- **`github-list_workflow_runs`**: Track workflow execution history
- **`github-get_workflow_run`**: Detailed run information
- **`github-get_job_logs`**: Debug failed builds and tests

### Advanced Features
- **`github-search_repositories`**: Discover related projects
- **`github-search_issues`**: Cross-repository issue search
- **`github-search_pull_requests`**: Advanced PR discovery
- **`github-get_latest_release`**: Release management

## 📝 Creating Issues with Templates

The repository includes two comprehensive issue templates designed for different scenarios:

### Bug Reports

Create detailed bug reports using the structured template:

1. **Navigate to Issues** → **New Issue**
2. **Select "Bug Report"** template
3. **Fill in required fields**:
   - Version information
   - Browser compatibility
   - Bug severity level
   - Current vs expected behavior
   - Reproduction steps
   - Relevant logs

**Example Bug Report**:
```yaml
Version: v1.0.0
Browsers: Chrome, Firefox
Severity: 🟠 High - Major feature broken
Current Behavior: Claude integration fails to respond
Expected Behavior: Claude should process @claude mentions
Steps to Reproduce:
1. Create new issue
2. Mention @claude in comment
3. Wait for response
4. No response received
```

### Feature Requests

Propose new features with comprehensive planning:

1. **Select "Feature Request"** template
2. **Complete all sections**:
   - Detailed description
   - Priority level
   - Affected components
   - Implementation tasks
   - Pre-submission checklist

**Example Feature Request**:
```yaml
Priority: High
Components: Frontend, Backend API
Description: Add support for custom Claude prompts in workflow triggers

Implementation Tasks:
- [x] Research Claude API capabilities
- [ ] Design configuration schema
- [ ] Implement backend validation
- [ ] Create frontend UI
- [ ] Write comprehensive tests
- [ ] Update documentation
```

### Using the Markdown Template

For quick issues, use the provided `issue-template.md`:

```markdown
## 📝 Description
[Brief description of the feature/bug/task]

## 🎯 Objective
[What problem does this solve? Why is it needed?]

## 📋 Tasks
- [ ] Research and planning
- [ ] Design/architecture decision
- [ ] Implementation
- [ ] Write unit tests
- [ ] Update documentation

## ✅ Acceptance Criteria
- [ ] Feature works as described
- [ ] All tests pass
- [ ] No regression in existing features
```

## ⚙️ GitHub Actions Workflows

The repository includes five specialized workflows for comprehensive automation:

### 1. CI/CD Pipeline (`ci.yml`)

**Triggers**: Push to main/develop, PRs to main, manual dispatch

**Features**:
- **Testing**: Automated unit and integration tests
- **Linting**: Code quality and style enforcement
- **Security**: npm audit and CodeQL analysis  
- **Building**: Project compilation and validation
- **Deployment**: Automatic production deployment from main branch
- **Notifications**: Team alerts for deployment status

```yaml
# Environment configuration
NODE_VERSION: '18'
PYTHON_VERSION: '3.11'

# Parallel job execution
jobs: [test, security-scan, deploy]
```

### 2. Auto Assignment (`auto-assign.yml`)

**Triggers**: New issues and PRs

**Automated Actions**:
- **Issue Assignment**: Auto-assign to issue creator
- **Smart Labeling**: Keywords-based label application
  - `[BUG]` → `bug` label
  - `[FEATURE]` → `enhancement` label
  - `[DOCS]` → `documentation` label
  - `[URGENT]` → `priority:high` label
- **Branch Creation**: Automatic feature branches for issues
- **Notifications**: Comment with branch information

### 3. Claude Integration (`claude.yml`)

**Triggers**: @claude mentions in issues, PRs, and comments

**Capabilities**:
- **Intelligent Responses**: Context-aware AI assistance
- **Code Analysis**: Deep code review and suggestions
- **Issue Processing**: Automated issue breakdown and planning
- **Multi-trigger Support**: Comments, reviews, issue assignments

**Configuration**:
```yaml
# Custom model selection
model: "claude-opus-4-1-20250805"

# Custom instructions
custom_instructions: |
  Follow our coding standards
  Ensure all new code has tests
  Use TypeScript for new files
```

### 4. Automated Code Review (`claude-code-review.yml`)

**Triggers**: PR opens and updates

**Review Focus**:
- **Code Quality**: Best practices and maintainability
- **Security**: Vulnerability detection and prevention
- **Performance**: Optimization opportunities
- **Testing**: Coverage analysis and test quality
- **Architecture**: Design pattern compliance

**Features**:
- **Sticky Comments**: Persistent review comments that update
- **Conditional Reviews**: Filter by author or file types
- **Custom Prompts**: Tailored review criteria

### 5. Scheduled Maintenance (`scheduled-tasks.yml`)

**Schedule**: Every Monday at 2 AM UTC

**Automated Tasks**:
- **Dependency Updates**: Check for outdated packages
- **Issue Creation**: Weekly maintenance reminders
- **Stale Cleanup**: Close inactive issues (30+ days)
- **Repository Health**: Automated maintenance reports

## 📁 Issue and Workflow Templates

### `.github/ISSUE_TEMPLATE/` Directory

**Bug Report Template** (`bug_report.yml`):
- Structured form with dropdowns and validation
- Version tracking and browser compatibility
- Severity classification system
- Step-by-step reproduction guides
- Log output collection

**Feature Request Template** (`feature_request.yml`):
- Priority and component classification
- Implementation task breakdown
- Pre-submission validation checklist
- Multi-component selection support

### `.github/workflows/` Directory

Five specialized workflows providing:

1. **Continuous Integration**: Automated testing and quality assurance
2. **Smart Assignment**: Intelligent issue and PR management
3. **AI Integration**: Claude-powered assistance and automation
4. **Code Review**: Automated, intelligent PR reviews
5. **Maintenance**: Scheduled repository health management

### Template Customization

**Modify Issue Templates**:
```yaml
# In .github/ISSUE_TEMPLATE/bug_report.yml
assignees:
  - your-username  # Change default assignee
labels: ["bug", "triage", "your-label"]  # Add custom labels
```

**Customize Workflows**:
```yaml
# In .github/workflows/*.yml
on:
  push:
    branches: [ main, your-branch ]  # Add custom branches
  schedule:
    - cron: '0 9 * * 1'  # Change schedule timing
```

## 🤝 Contributing

We welcome contributions to improve this multi-agent Claude Code template! Here's how to get started:

### Development Workflow

1. **Fork the repository** and create a feature branch:
   ```bash
   git checkout -b feature/your-improvement
   ```

2. **Make your changes** following these guidelines:
   - Keep workflows focused and maintainable
   - Add comprehensive comments to YAML files
   - Test workflow changes in a fork first
   - Update documentation for any new features

3. **Test your changes**:
   - Validate YAML syntax: `yamllint .github/`
   - Test workflow logic in your fork
   - Verify Claude integration works correctly

4. **Submit a Pull Request** with:
   - Clear description of changes
   - Screenshots of any UI changes
   - Test results and validation steps

### Contribution Guidelines

**Code Standards**:
- Use consistent YAML formatting
- Add meaningful comments to complex workflow logic
- Follow GitHub Actions best practices
- Maintain backward compatibility when possible

**Documentation**:
- Update README.md for new features
- Add inline comments to workflow files
- Include usage examples for new templates

**Testing**:
- Test workflows in a fork before submitting
- Verify Claude integration functionality
- Check that all existing workflows still function

### Areas for Contribution

- **New Workflow Templates**: Additional automation scenarios
- **Enhanced Claude Prompts**: More sophisticated AI interactions
- **Additional Issue Templates**: Specialized templates for different project types
- **Documentation**: Improved examples and use cases
- **Integration Examples**: Sample projects using these templates

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Questions or suggestions?** Open an issue using our templates or mention @claude for AI-powered assistance!

**Want to see this in action?** Check out the Issues and Pull Requests tabs to see Claude Code in action! 🚀