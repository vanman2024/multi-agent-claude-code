#!/bin/bash

# Update Agent Context Script
# Incrementally updates agent context files for different AI assistants and development guidelines

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project paths
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/agents"
CLAUDE_COMMANDS_DIR="$PROJECT_ROOT/.claude/commands"

# Log function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

error() {
    echo -e "${RED}❌${NC} $1"
}

# Extract project details from key files
extract_project_details() {
    local language=""
    local framework=""
    local project_type=""
    
    # Detect language and framework from package.json
    if [[ -f "$PROJECT_ROOT/package.json" ]]; then
        if grep -q "next" "$PROJECT_ROOT/package.json"; then
            framework="Next.js"
            language="TypeScript/JavaScript"
            project_type="Full-stack Web Application"
        elif grep -q "react" "$PROJECT_ROOT/package.json"; then
            framework="React"
            language="TypeScript/JavaScript"
            project_type="Frontend Application"
        elif grep -q "express" "$PROJECT_ROOT/package.json"; then
            framework="Express"
            language="JavaScript/Node.js"
            project_type="Backend API"
        else
            framework="Node.js"
            language="JavaScript"
            project_type="Node.js Application"
        fi
    elif [[ -f "$PROJECT_ROOT/requirements.txt" ]] || [[ -f "$PROJECT_ROOT/pyproject.toml" ]]; then
        language="Python"
        if grep -q "fastapi\|uvicorn" "$PROJECT_ROOT/requirements.txt" 2>/dev/null; then
            framework="FastAPI"
            project_type="API Server"
        elif grep -q "django" "$PROJECT_ROOT/requirements.txt" 2>/dev/null; then
            framework="Django"
            project_type="Web Application"
        elif grep -q "flask" "$PROJECT_ROOT/requirements.txt" 2>/dev/null; then
            framework="Flask"
            project_type="Web Application"
        else
            framework="Python"
            project_type="Python Application"
        fi
    else
        language="Unknown"
        framework="Unknown"
        project_type="Unknown"
    fi
    
    echo "$language|$framework|$project_type"
}

# Update Claude agent context
update_claude_context() {
    log "Updating Claude agent context..."
    
    local claude_file="$AGENTS_DIR/CLAUDE.md"
    
    if [[ ! -f "$claude_file" ]]; then
        warning "Claude context file not found at $claude_file"
        return 1
    fi
    
    # Extract project details
    local details=$(extract_project_details)
    local language=$(echo "$details" | cut -d'|' -f1)
    local framework=$(echo "$details" | cut -d'|' -f2)
    local project_type=$(echo "$details" | cut -d'|' -f3)
    
    # Update project context section
    if grep -q "### Current Project Context" "$claude_file"; then
        # Create temporary file with updated context
        local temp_file=$(mktemp)
        awk -v lang="$language" -v fw="$framework" -v type="$project_type" '
        /### Current Project Context/ {
            print $0
            print "- **Language**: " lang
            print "- **Framework**: " fw
            print "- **Project Type**: " type
            print "- **Coordination**: @Symbol task assignment system"
            print "- **MCP Servers**: Local filesystem, git, github, memory, sequential-thinking, playwright, sqlite, supabase, postman"
            print ""
            # Skip until next section
            while (getline && !/^###/) {}
            print $0
            next
        }
        { print }
        ' "$claude_file" > "$temp_file"
        
        mv "$temp_file" "$claude_file"
        success "Updated Claude context with current project details"
    else
        warning "Could not find project context section in Claude file"
    fi
}

# Update Gemini agent context
update_gemini_context() {
    log "Updating Gemini agent context..."
    
    local gemini_file="$AGENTS_DIR/GEMINI.md"
    
    if [[ ! -f "$gemini_file" ]]; then
        warning "Gemini context file not found at $gemini_file"
        return 1
    fi
    
    # Update current sprint focus based on recent commits
    if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
        local recent_topics=$(git log --oneline -10 | grep -o -E "(feat|fix|docs|refactor|perf):\s*[^(]*" | head -5 || echo "")
        
        if [[ -n "$recent_topics" ]]; then
            # Update sprint focus section
            local temp_file=$(mktemp)
            awk -v topics="$recent_topics" '
            /### Current Sprint Focus/ {
                print $0
                print "Based on recent development activity:"
                print topics | "fmt -w 80"
                close("fmt -w 80")
                print ""
                # Skip until next section
                while (getline && !/^###/) {}
                print $0
                next
            }
            { print }
            ' "$gemini_file" > "$temp_file"
            
            mv "$temp_file" "$gemini_file"
            success "Updated Gemini context with recent development topics"
        fi
    fi
}

# Update repository guidelines (AGENTS.md)
update_agents_guidelines() {
    log "Updating repository guidelines..."
    
    local agents_file="$AGENTS_DIR/README.md"
    
    # Create agents overview file if it doesn't exist
    if [[ ! -f "$agents_file" ]]; then
        cat > "$agents_file" << 'EOF'
# Multi-Agent Development Team

## Agent Coordination System

This directory contains context files for each AI agent in our multi-agent development system.

### Active Agents

#### @claude (Architecture & Integration)
- **File**: `CLAUDE.md`
- **Specialization**: Complex architecture, multi-file integration, system design
- **MCP Access**: Full local server access (filesystem, git, github, memory, etc.)

#### @copilot (Code Generation)
- **File**: `COPILOT_SUMMARY.md` 
- **Specialization**: Simple implementations (Complexity ≤2, Size XS/S)
- **Auto-assignment**: Via GitHub for qualifying tasks

#### @gemini (Research & Documentation)
- **File**: `GEMINI.md`
- **Specialization**: Research, documentation, performance analysis
- **MCP Access**: filesystem, brave-search, memory

#### @qwen (Performance Optimization)
- **File**: `QWEN.md`
- **Specialization**: Performance optimization, algorithm improvement
- **MCP Access**: remote-filesystem, git, memory
- **Installation**: FREE via Ollama


### Task Assignment

All agents use the @symbol coordination system with markdown task files:

```markdown
- [ ] T001 @claude Design database schema
- [ ] T002 @copilot Implement API endpoints
- [ ] T003 @qwen Optimize query performance
- [ ] T005 @gemini Document API endpoints
```

### Updating Agent Context

Use the update script to keep agent context current:

```bash
# Update all agent contexts
./scripts/update-agent-context.sh all

# Update specific agent
./scripts/update-agent-context.sh claude
./scripts/update-agent-context.sh gemini
```

### Agent Communication

Agents coordinate through:
- **Task dependencies**: `(depends on T001)`
- **Shared memory**: MCP memory server
- **Git commits**: Standardized commit messages with agent identity
- **Issue comments**: Progress updates and coordination

EOF
        success "Created agents overview file"
    fi
    
    # Update project structure section
    if command -v tree >/dev/null 2>&1; then
        local project_structure=$(tree -L 2 -I 'node_modules|.git|.next|dist|build' "$PROJECT_ROOT" 2>/dev/null || echo "Project structure not available")
        
        # Add project structure to README if tree is available
        if [[ "$project_structure" != "Project structure not available" ]]; then
            local temp_file=$(mktemp)
            {
                head -n -1 "$agents_file"
                echo ""
                echo "### Current Project Structure"
                echo ""
                echo '```'
                echo "$project_structure"
                echo '```'
                echo ""
            } > "$temp_file"
            
            mv "$temp_file" "$agents_file"
            success "Updated project structure in agents overview"
        fi
    fi
}

# Update GitHub Copilot instructions
update_copilot_instructions() {
    log "Updating GitHub Copilot instructions..."
    
    local copilot_file="$PROJECT_ROOT/.github/copilot-instructions.md"
    local copilot_dir="$(dirname "$copilot_file")"
    
    # Create .github directory if it doesn't exist
    mkdir -p "$copilot_dir"
    
    if [[ ! -f "$copilot_file" ]]; then
        # Create basic copilot instructions based on current project
        local details=$(extract_project_details)
        local language=$(echo "$details" | cut -d'|' -f1)
        local framework=$(echo "$details" | cut -d'|' -f2)
        local project_type=$(echo "$details" | cut -d'|' -f3)
        
        cat > "$copilot_file" << EOF
# GitHub Copilot Instructions

## Project Context
- **Type**: $project_type
- **Language**: $language  
- **Framework**: $framework
- **Architecture**: Multi-agent development framework template

## Development Standards

### Code Style
- Follow existing patterns in the codebase
- Use TypeScript for all new JavaScript code
- Implement proper error handling with try/catch
- Use async/await over callbacks
- Include proper logging for debugging

### File Naming Conventions
- Components: PascalCase (UserProfile.tsx)
- Utilities: camelCase (userHelper.ts)
- Config files: kebab-case (api-config.ts)
- Test files: *.test.ts or *.spec.ts

### Task Assignment Criteria
GitHub Copilot handles tasks that are BOTH:
- **Complexity**: 1-2 (simple, straightforward logic)
- **Size**: XS or S (less than 2 hours work)

### Commit Message Format
```
feat: Add user validation logic

Closes #123

🤖 Generated by GitHub Copilot
Co-Authored-By: Copilot <noreply@github.com>
```

### Quality Standards
- All functions must have proper TypeScript types
- Include error handling for all external calls
- Add unit tests for new utility functions
- Follow existing code organization patterns
- Never commit secrets or API keys

### Multi-Agent Coordination
- Work on simple implementation tasks
- Hand off complex tasks to @claude
- Coordinate with other agents via task dependencies
- Update task status in specs/*/tasks.md files

EOF
        success "Created GitHub Copilot instructions"
    else
        success "GitHub Copilot instructions already exist"
    fi
}

# Main function
main() {
    local target="${1:-}"
    
    log "Starting agent context update..."
    
    # Ensure directories exist
    mkdir -p "$AGENTS_DIR"
    mkdir -p "$CLAUDE_COMMANDS_DIR"
    
    case "$target" in
        "claude")
            update_claude_context
            ;;
        "gemini")
            update_gemini_context
            ;;
        "agents")
            update_agents_guidelines
            ;;
        "copilot")
            update_copilot_instructions
            ;;
        "all"|"")
            update_claude_context
            update_gemini_context
            update_agents_guidelines
            update_copilot_instructions
            ;;
        *)
            error "Unknown target: $target"
            echo "Usage: $0 [claude|gemini|agents|copilot|all]"
            exit 1
            ;;
    esac
    
    success "Agent context update complete!"
    
    # Show summary of updated files
    echo ""
    log "Updated agent files:"
    ls -la "$AGENTS_DIR"/*.md 2>/dev/null || warning "No agent files found"
    
    if [[ -f "$PROJECT_ROOT/.github/copilot-instructions.md" ]]; then
        echo "  .github/copilot-instructions.md"
    fi
}

# Run main function with all arguments
main "$@"