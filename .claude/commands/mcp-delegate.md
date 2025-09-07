---
allowed-tools: Bash(*), Read(*)
description: Task delegation commands for MCP servers
---

# MCP Task Delegation Commands

## Instructions for Assistant

This command provides task delegation capabilities for the enhanced MCP servers in the Multi-Agent Development Framework.

### Available MCP Servers

1. **together-ai** - Complex code generation (3000 requests/month)
2. **gemini** - Testing, documentation, code analysis (1500 requests/day)
3. **huggingface** - Specialized models and domain-specific code (30k chars/month)
4. **github** - Repository management and automation
5. **openai** - Boilerplate generation (existing)

### Command Syntax

```bash
/mcp <server> <operation> [options]
```

### Together AI Commands

```bash
# Complex code generation
/mcp together generate-code --task "implement OAuth2 authentication" --language typescript --framework fastapi

# Algorithm implementation
/mcp together generate-algorithm --type "graph-traversal" --language python --complexity high

# Code refactoring
/mcp together refactor-code --file src/auth.js --focus performance --preserve-api

# System component generation
/mcp together generate-component --name "payment-service" --type microservice --language go
```

### Gemini Commands

```bash
# Test generation
/mcp gemini generate-tests --source src/auth.js --type unit --framework jest --coverage 90

# Documentation generation
/mcp gemini generate-docs --source src/api/ --format openapi --audience api-users

# Code analysis
/mcp gemini analyze-code --file src/security.js --analysis security --standards owasp

# API documentation
/mcp gemini generate-api-docs --files "src/routes/*.js" --format openapi --base-url https://api.example.com
```

### HuggingFace Commands

```bash
# SQL generation
/mcp huggingface generate-sql --description "user analytics report with monthly aggregation" --database postgresql

# Specialized code generation
/mcp huggingface generate-specialized --task "data preprocessing pipeline" --specialty python-specialist --framework pandas

# Frontend component generation
/mcp huggingface generate-frontend --component "user profile card" --framework react --styling tailwind

# Code explanation
/mcp huggingface explain-code --file src/algorithm.py --focus optimization
```

### Multi-Agent Workflows

#### Complete Feature Development
```bash
# Step 1: Architecture design (Claude Code)
/work feature/user-authentication

# Step 2: Generate complex authentication logic (Together AI)
/mcp together generate-code --task "JWT authentication with refresh tokens" --language typescript --framework express

# Step 3: Generate comprehensive tests (Gemini)
/mcp gemini generate-tests --source generated/auth.ts --type integration --framework jest

# Step 4: Generate API documentation (Gemini)
/mcp gemini generate-docs --source generated/auth.ts --format openapi --audience developers

# Step 5: Create database queries (HuggingFace)
/mcp huggingface generate-sql --description "user authentication and session management" --database postgresql
```

#### Bug Fix and Analysis Workflow
```bash
# Step 1: Analyze problematic code (Gemini)
/mcp gemini analyze-code --file src/problematic.js --analysis all --standards eslint

# Step 2: Generate reproduction tests (Gemini)
/mcp gemini generate-tests --source src/problematic.js --type unit --focus "bug-reproduction"

# Step 3: Fix complex logic (Together AI)
/mcp together refactor-code --file src/problematic.js --focus "bug-fix" --preserve-api

# Step 4: Update documentation (Gemini)
/mcp gemini generate-docs --source src/fixed.js --format markdown --audience developers
```

### Usage Tracking and Optimization

#### Check API Usage
```bash
# Check all MCP server usage
/mcp together get-usage-stats
/mcp gemini get-usage-stats
/mcp huggingface get-usage-stats

# Get combined usage report
/mcp-usage-report --all
```

#### Fallback Chain Example
```bash
# Primary: Gemini for test generation
/mcp gemini generate-tests --source src/auth.js || {
  # Fallback 1: HuggingFace with code generation model
  /mcp huggingface generate-specialized --task "generate unit tests for authentication" --specialty code-generation || {
    # Fallback 2: Claude Code manual implementation
    /test-generate --source src/auth.js --method manual || {
      # Fallback 3: Assign to Copilot if simple
      gh issue create --assignee copilot --title "Generate tests for src/auth.js"
    }
  }
}
```

### File Operations

#### Read Project Context
```bash
# All MCP servers can read project context
/mcp together read-project-context
/mcp gemini read-project-context
/mcp huggingface read-project-context
```

#### File Read/Write Operations
```bash
# Read source files (all servers support this)
/mcp gemini read-source-file --filename src/utils.js

# Write generated content to files
/mcp together generate-code --task "utility functions" | /mcp together write-file --filename src/new-utils.js

# Backup and safe file operations (automatic)
# All servers create backups before overwriting files
```

### Advanced Patterns

#### Batch Operations
```bash
# Generate multiple related files
for component in auth user profile; do
  /mcp together generate-component --name "$component-service" --type api
  /mcp gemini generate-tests --source "generated/${component}-service.js"
  /mcp gemini generate-docs --source "generated/${component}-service.js"
done
```

#### Context-Aware Generation
```bash
# MCP servers automatically read PROJECT_CONTEXT.md for:
# - Current project goals
# - Technology stack
# - Architecture patterns
# - Coding standards

# Example: Generate code that fits project architecture
/mcp together generate-code --task "user service" --context-aware
# Server reads PROJECT_CONTEXT.md and generates code matching the project's patterns
```

#### Quality Assurance Chain
```bash
# Step 1: Generate with Together AI
code=$(mcp together generate-code --task "payment processing")

# Step 2: Analyze quality with Gemini
analysis=$(mcp gemini analyze-code --content "$code" --analysis quality)

# Step 3: Generate tests with Gemini
tests=$(mcp gemini generate-tests --content "$code" --type unit)

# Step 4: Security review with Gemini
security=$(mcp gemini analyze-code --content "$code" --analysis security)
```

## Implementation Notes

### Error Handling
All MCP commands include automatic error handling:
- Rate limit detection and fallback suggestions
- File access validation and security checks
- API authentication verification
- Character/token limit monitoring

### Security Features
- File access restricted to project directory
- Automatic backup before file modifications
- Input validation on all parameters
- API key management through environment variables

### Performance Optimization
- Context caching to avoid repeated PROJECT_CONTEXT.md reads
- Batch request optimization for similar tasks
- Usage tracking to prevent rate limit violations
- Intelligent model selection based on task complexity

### Integration with Existing Workflow
- Compatible with existing `/work`, `/test-generate`, and `/deploy` commands
- Integrates with GitHub Copilot assignment for simple tasks
- Maintains audit trail through git commits
- Supports project board automation

## Usage Examples

### User: "Generate authentication system"
```bash
# Complex task - use Together AI for main logic
/mcp together generate-code --task "OAuth2 authentication system with JWT" --language typescript --framework express

# Generate comprehensive tests
/mcp gemini generate-tests --source generated/auth.ts --type integration --coverage 95

# Create API documentation
/mcp gemini generate-docs --source generated/auth.ts --format openapi
```

### User: "Fix performance issue in algorithm"
```bash
# Analyze current performance
/mcp gemini analyze-code --file src/slow-algorithm.js --analysis performance

# Optimize with Together AI
/mcp together refactor-code --file src/slow-algorithm.js --focus performance --preserve-api

# Generate benchmarking tests
/mcp gemini generate-tests --source src/optimized-algorithm.js --type performance
```

### User: "Create SQL queries for reporting"
```bash
# Use specialized SQL model
/mcp huggingface generate-sql --description "monthly user activity report with cohort analysis" --database postgresql --schema "schema.sql"

# Document the queries
/mcp gemini generate-docs --source generated/reports.sql --format markdown --audience analysts
```

This delegation system enables efficient task distribution across specialized AI models while maintaining cost efficiency through free tier optimization and intelligent fallback patterns.