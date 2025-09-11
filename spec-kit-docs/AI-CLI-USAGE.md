# AI CLI Programmatic Usage Guide

## Available AI CLIs

### 1. Codex CLI (OpenAI)
**Path**: `~/.local/bin/codex`
**Version**: 0.34.0

#### Interactive Mode
```bash
codex
```

#### Non-Interactive Execution Mode
```bash
# Execute specific commands
codex exec "fix the CI failure"
codex exec "add error handling to the API endpoints"
codex exec "refactor the database queries for performance"
```

### 2. Gemini CLI (Google)
**Path**: `~/.nvm/versions/node/v20.14.0/bin/gemini`
**Version**: 0.4.0

#### Usage
```bash
# Simple prompt
gemini -p "write a function to validate email addresses"

# From file
gemini -f prompt.txt

# With specific model
gemini -m gemini-pro -p "explain this code"
```

### 3. OpenAI CLI
**Path**: `~/.local/bin/openai`

#### Usage
```bash
# Simple prompt
openai "write a hello world in Python"

# With specific model
openai -m gpt-4 "explain quantum computing"

# Set max tokens
openai -k 1000 "write a detailed explanation"

# Interactive chat
openai chat
```

## Programmatic Usage in Slash Commands

### Example: Multi-Agent Code Review
```markdown
---
allowed-tools: Bash(*), Read(*), Write(*)
description: Use AI CLIs for specialized code review
---

# AI Code Review

## Step 1: Codex - Implementation Review
!codex exec "review this code for bugs and best practices: $(cat $FILE)"

## Step 2: Gemini - Documentation Review  
!gemini -p "review documentation and suggest improvements: $(cat $FILE)"

## Step 3: OpenAI - Architecture Review
!openai "analyze architecture and design patterns: $(cat $FILE)"
```

### Example: Spec-Kit Enhancement
```markdown
---
allowed-tools: Bash(*), Read(*), Write(*)
---

# Enhance Spec with AI

## Technical Details (Codex)
!codex exec "suggest database schema for: $(cat specs/001-feature/spec.md | head -30)"

## User Experience (Gemini)
!gemini -p "suggest UI/UX improvements for: $(cat specs/001-feature/spec.md | head -30)"

## Business Logic (OpenAI)
!openai "identify edge cases and business rules: $(cat specs/001-feature/spec.md | head -30)"
```

## Specialized AI Roles

### Task Assignment by Complexity

| AI Tool | Best For | Example Commands |
|---------|----------|------------------|
| **Codex** | Code implementation, debugging, refactoring | `codex exec "implement auth middleware"` |
| **Gemini** | Documentation, explanations, tutorials | `gemini -p "document this API"` |
| **OpenAI** | Architecture, design patterns, planning | `openai "design microservices architecture"` |

## Bash Script Integration

### Example: ai-review.sh
```bash
#!/bin/bash
FILE=$1

echo "=== Codex Review ==="
codex exec "review for bugs: $(cat $FILE)"

echo "=== Gemini Docs ==="
gemini -p "improve docs: $(cat $FILE | head -50)"

echo "=== OpenAI Architecture ==="
openai "analyze design: $(cat $FILE | head -50)"
```

### Example: spec-enhance.sh
```bash
#!/bin/bash
SPEC=$1

# Generate technical details
TECH=$(codex exec "create database schema for: $(cat $SPEC)")

# Generate UX improvements
UX=$(gemini -p "suggest UI flow for: $(cat $SPEC)")

# Generate business rules
RULES=$(openai "extract business rules from: $(cat $SPEC)")

# Combine into enhanced spec
cat >> "${SPEC%.md}-enhanced.md" <<EOF
## AI-Enhanced Specifications

### Technical Architecture
$TECH

### User Experience
$UX

### Business Rules
$RULES
EOF
```

## Environment Variables

Set these in ~/.bashrc:
```bash
# API Keys
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."

# Model preferences
export OPENAI_MODEL="gpt-4"
export GEMINI_MODEL="gemini-pro"
```

## Non-Interactive Patterns

### Pipe Input
```bash
cat code.js | codex exec "add error handling"
```

### Command Substitution
```bash
REVIEW=$(codex exec "review: $(cat file.py)")
echo "$REVIEW" > review.md
```

### Parallel Execution
```bash
codex exec "task 1" &
gemini -p "task 2" &
openai "task 3" &
wait
```

## Integration with Spec-Kit Workflow

### Phase 1: Specification Enhancement
```bash
# After /specify
codex exec "add technical constraints to: $(cat specs/001/spec.md)"
```

### Phase 2: Planning Enhancement
```bash
# After /plan
gemini -p "validate tech stack choices in: $(cat specs/001/plan.md)"
```

### Phase 3: Task Generation
```bash
# After /tasks
openai "identify missing tasks in: $(cat specs/001/tasks.md)"
```

### Phase 4: Implementation
```bash
# During implementation
codex exec "implement task T001 from: $(cat specs/001/tasks.md)"
```

## Tips for Effective Usage

1. **Keep prompts focused** - Single responsibility per call
2. **Use appropriate context** - Include relevant code snippets
3. **Chain commands** - Use output from one as input to another
4. **Handle errors** - Check return codes and validate output
5. **Cache responses** - Save AI output for reuse

## Debugging

### Check if CLIs are accessible
```bash
which codex gemini openai
```

### Test each CLI
```bash
codex --version
gemini --version
openai --help
```

### Verify API keys
```bash
echo $OPENAI_API_KEY
echo $GEMINI_API_KEY
```