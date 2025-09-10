#!/bin/bash

# claude-init.sh - Generate project-specific CLAUDE.md from existing project structure
# This bridges spec-kit style projects with our Claude Code framework

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 Claude Init - Generating Project-Specific CLAUDE.md${NC}"
echo ""

# Function to detect project type
detect_project_type() {
    local project_type="unknown"
    
    # Check for spec-kit
    if [ -d ".specify" ] || [ -f "memory/constitution.md" ]; then
        project_type="spec-kit"
    # Check for Next.js
    elif [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then
        project_type="nextjs"
    # Check for React
    elif [ -f "package.json" ] && grep -q "\"react\"" package.json 2>/dev/null; then
        project_type="react"
    # Check for Python
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        project_type="python"
    # Check for our multi-agent framework
    elif [ -f "docs/PROJECT_PLAN.md" ]; then
        project_type="multi-agent"
    fi
    
    echo "$project_type"
}

# Function to read spec-kit files
read_spec_kit_files() {
    local content=""
    
    if [ -f ".specify/spec.md" ]; then
        echo -e "${GREEN}✓${NC} Found spec.md" >&2
        content+="## Project Specification"
        content+=$'\n\n'
        content+="$(cat .specify/spec.md)"
        content+=$'\n\n'
    fi
    
    if [ -f ".specify/plan.md" ]; then
        echo -e "${GREEN}✓${NC} Found plan.md" >&2
        content+="## Implementation Plan"
        content+=$'\n\n'
        content+="$(cat .specify/plan.md)"
        content+=$'\n\n'
    fi
    
    if [ -f "memory/constitution.md" ]; then
        echo -e "${GREEN}✓${NC} Found constitution.md" >&2
        content+="## Project Constitution"
        content+=$'\n\n'
        content+="$(cat memory/constitution.md)"
        content+=$'\n\n'
    fi
    
    printf "%s" "$content"
}

# Function to read project plan files
read_project_files() {
    local content=""
    
    if [ -f "docs/PROJECT_PLAN.md" ]; then
        echo -e "${GREEN}✓${NC} Found PROJECT_PLAN.md" >&2
        content+="## Project Vision\n\n"
        content+="$(head -50 docs/PROJECT_PLAN.md)\n\n"
    fi
    
    if [ -f "README.md" ]; then
        echo -e "${GREEN}✓${NC} Found README.md" >&2
        content+="## Project Overview\n\n"
        content+="$(head -30 README.md)\n\n"
    fi
    
    if [ -f "package.json" ]; then
        echo -e "${GREEN}✓${NC} Found package.json" >&2
        content+="## Tech Stack\n\n"
        content+="### Dependencies:\n"
        content+='```json\n'
        content+="$(jq '.dependencies' package.json 2>/dev/null || echo '{}')\n"
        content+='```\n\n'
    fi
    
    printf "%s" "$content"
}

# Function to generate CLAUDE.md
generate_claude_md() {
    local project_type="$1"
    local project_name="${PWD##*/}"
    
    echo -e "${YELLOW}📝 Generating CLAUDE.md for $project_type project: $project_name${NC}"
    
    cat > CLAUDE.md << 'EOF'
# Claude Code Instructions - Project-Specific Configuration

## Project Context
EOF

    echo "**Project Name**: $project_name" >> CLAUDE.md
    echo "**Project Type**: $project_type" >> CLAUDE.md
    echo "**Generated**: $(date)" >> CLAUDE.md
    echo "" >> CLAUDE.md
    
    # Add project-specific content based on type
    case "$project_type" in
        "spec-kit")
            echo "## Spec-Driven Development Project" >> CLAUDE.md
            echo "" >> CLAUDE.md
            read_spec_kit_files >> CLAUDE.md
            ;;
        "multi-agent")
            echo "## Multi-Agent Framework Project" >> CLAUDE.md
            echo "" >> CLAUDE.md
            read_project_files >> CLAUDE.md
            ;;
        *)
            echo "## Standard Project" >> CLAUDE.md
            echo "" >> CLAUDE.md
            read_project_files >> CLAUDE.md
            ;;
    esac
    
    # Add standard Claude instructions
    cat >> CLAUDE.md << 'EOF'

## Development Guidelines

### File Management
- NEVER create temporary test files
- ALWAYS prefer editing existing files over creating new ones
- NEVER create backup copies (rely on git)

### Code Style
- Follow existing patterns in the codebase
- Use the same libraries and frameworks already present
- Maintain consistent naming conventions

### Testing
- Check for existing test patterns before writing tests
- Run `npm test` or equivalent before marking tasks complete
- Never commit failing tests

### Git Workflow
- Create descriptive commit messages
- Reference issue numbers in commits
- Keep commits focused and atomic

## Project-Specific Commands

### Available Slash Commands
Check `.claude/commands/` directory for project-specific commands.

### Build & Test Commands
EOF

    # Add build commands if package.json exists
    if [ -f "package.json" ]; then
        echo '```bash' >> CLAUDE.md
        echo "# Available npm scripts:" >> CLAUDE.md
        npm run 2>/dev/null | grep -E "^  " | head -10 >> CLAUDE.md 2>/dev/null || true
        echo '```' >> CLAUDE.md
    fi
    
    # Add Python commands if detected
    if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        echo '```bash' >> CLAUDE.md
        echo "# Python project commands:" >> CLAUDE.md
        echo "python -m pytest  # Run tests" >> CLAUDE.md
        echo "python -m mypy .  # Type checking" >> CLAUDE.md
        echo '```' >> CLAUDE.md
    fi
    
    echo "" >> CLAUDE.md
    echo "## Notes" >> CLAUDE.md
    echo "This file was auto-generated by claude-init.sh and should be updated as the project evolves." >> CLAUDE.md
}

# Main execution
main() {
    # Check if CLAUDE.md already exists
    if [ -f "CLAUDE.md" ]; then
        echo -e "${YELLOW}⚠️  CLAUDE.md already exists${NC}"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}❌ Aborted${NC}"
            exit 1
        fi
    fi
    
    # Detect project type
    project_type=$(detect_project_type)
    echo -e "${BLUE}📦 Detected project type: ${project_type}${NC}"
    echo ""
    
    # Generate CLAUDE.md
    generate_claude_md "$project_type"
    
    echo ""
    echo -e "${GREEN}✅ CLAUDE.md generated successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review and customize CLAUDE.md for your specific needs"
    echo "2. Add any project-specific rules or patterns"
    echo "3. Update as your project evolves"
    
    # If spec-kit project, suggest integration
    if [ "$project_type" = "spec-kit" ]; then
        echo ""
        echo -e "${YELLOW}💡 Spec-kit Integration Tip:${NC}"
        echo "   Your spec-kit project can now use our enhanced commands:"
        echo "   - /work - to implement tasks"
        echo "   - /create-issue - to create GitHub issues"
        echo "   - /deploy - to deploy to production"
    fi
}

# Run main function
main "$@"