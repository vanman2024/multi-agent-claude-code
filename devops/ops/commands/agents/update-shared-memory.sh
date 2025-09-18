#!/usr/bin/env bash
# Update Shared Memory - Agent Context & Constitution Slash Command
#
# This script updates both agent context files and the constitution.md
# to keep shared memory synchronized across all AI agents.
#
# Usage:
#   /update-memory [message] [scope] [--force]
#   
# Examples:
#   /update-memory                                          # Update all (agent context + constitution)
#   /update-memory "Update pytest to python3 run.py" agent # Update agent files with specific message
#   /update-memory constitution                             # Update only constitution.md
#   /update-memory "Add new commands" all --force           # Force update with message

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 2>/dev/null || SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENT_CONTEXT_SCRIPT="$SCRIPT_DIR/update-agent-context-simple.sh"
CONSTITUTION_FILE="$REPO_ROOT/memory/constitution.md"
COORDINATION_PLAN="$REPO_ROOT/AI_COORDINATION_PLAN.md"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

usage() {
    echo -e "${CYAN}📚 Update Shared Memory - Agent Context & Constitution${NC}"
    echo ""
    echo "This slash command updates shared memory for all AI agents:"
    echo "  • Agent context files (CLAUDE.md, GEMINI.md, AGENTS.md, etc.)"
    echo "  • Constitution.md with latest project information"  
    echo "  • Coordination system documentation"
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo "  /update-memory [MESSAGE] [SCOPE] [OPTIONS]"
    echo ""
    echo -e "${BLUE}MESSAGE:${NC}"
    echo "  \"Update message\"   Specific update to apply across agent files"
    echo "                     Example: \"Update pytest commands to python3 run.py\""
    echo ""
    echo -e "${BLUE}SCOPE:${NC}"
    echo "  agent         Update only agent context files (all agents)"
    echo "  claude        Update only CLAUDE.md"
    echo "  gemini        Update only GEMINI.md" 
    echo "  agents        Update only AGENTS.md"
    echo "  copilot       Update only .github/copilot-instructions.md"
    echo "  constitution  Update only constitution.md" 
    echo "  coordination  Update only coordination documentation"
    echo "  all           Update everything (default)"
    echo ""
    echo -e "${BLUE}OPTIONS:${NC}"
    echo "  --force       Force update even if no changes detected"
    echo "  --dry-run     Show what would be updated without making changes"
    echo "  --help        Show this help"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  /update-memory                                          # Update all shared memory"
    echo "  /update-memory claude                                   # Update only CLAUDE.md"
    echo "  /update-memory gemini                                   # Update only GEMINI.md"
    echo "  /update-memory \"Update pytest to python3 run.py\" agent # Apply specific update to all agent files"
    echo "  /update-memory constitution                             # Update only constitution"
    echo "  /update-memory \"Add new commands\" all --force           # Force update with message"
}

check_prerequisites() {
    if [[ ! -f "$AGENT_CONTEXT_SCRIPT" ]]; then
        echo -e "${RED}❌ Agent context script not found: $AGENT_CONTEXT_SCRIPT${NC}"
        exit 1
    fi
    
    if [[ ! -f "$CONSTITUTION_FILE" ]]; then
        echo -e "${YELLOW}⚠️  Constitution file not found, will be created${NC}"
    fi
    
    echo -e "${GREEN}✅ Prerequisites checked${NC}"
}

update_agent_context() {
    local dry_run="$1"
    local message="$2"
    local agent="$3"
    
    # Default to 'all' if no specific agent provided
    if [[ -z "$agent" ]]; then
        agent="all"
    fi
    
    echo -e "${BLUE}🤖 Updating Agent Context Files...${NC}"
    
    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}[DRY RUN] Would run: $AGENT_CONTEXT_SCRIPT $agent${NC}"
        if [[ -n "$message" ]]; then
            echo -e "${YELLOW}[DRY RUN] Would apply message: $message${NC}"
        fi
        return 0
    fi
    
    # Use the existing update-agent-context.sh script
    if bash "$AGENT_CONTEXT_SCRIPT" "$agent"; then
        echo -e "${GREEN}✅ Agent context files updated successfully${NC}"
        
        # Apply custom message if provided
        if [[ -n "$message" ]]; then
            apply_message_to_agent_files "$message"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Failed to update agent context files${NC}"
        return 1
    fi
}

apply_message_to_agent_files() {
    local message="$1"
    
    echo -e "${BLUE}📝 Applying custom message to agent files...${NC}"
    
    # Check if message contains WSL screenshot instruction
    if [[ "$message" == *"wsl"* && "$message" == *"screenshot"* ]]; then
        echo -e "${CYAN}🖼️  Adding WSL screenshot path instruction to agent files${NC}"
        
        # Add WSL instruction to all agent files
        for agent_file in "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/GEMINI.md" "$REPO_ROOT/AGENTS.md" "$REPO_ROOT/.github/copilot-instructions.md"; do
            if [[ -f "$agent_file" ]]; then
                # Check if WSL section already exists
                if ! grep -q "WSL Environment Notes" "$agent_file"; then
                    # Find the manual additions section and add WSL notes
                    if grep -q "<!-- MANUAL ADDITIONS START -->" "$agent_file"; then
                        # Replace manual additions section with WSL notes
                        sed -i '/<!-- MANUAL ADDITIONS START -->/,/<!-- MANUAL ADDITIONS END -->/c\
<!-- MANUAL ADDITIONS START -->\
\
## WSL Environment Notes\
- When reading screenshots or working with Windows paths, always use WSL-compatible paths (e.g., `/mnt/c/` instead of `C:\`)\
- Screenshots saved by Windows applications should be accessed via WSL path format\
\
<!-- MANUAL ADDITIONS END -->' "$agent_file"
                        echo -e "${GREEN}  ✅ Updated $(basename "$agent_file")${NC}"
                    else
                        # Add WSL section at the end
                        echo -e "\n## WSL Environment Notes\n- When reading screenshots or working with Windows paths, always use WSL-compatible paths (e.g., \`/mnt/c/\` instead of \`C:\\\`)\n- Screenshots saved by Windows applications should be accessed via WSL path format" >> "$agent_file"
                        echo -e "${GREEN}  ✅ Added WSL notes to $(basename "$agent_file")${NC}"
                    fi
                else
                    echo -e "${YELLOW}  ⚠️  WSL notes already exist in $(basename "$agent_file")${NC}"
                fi
            fi
        done
    else
        # Generic message handling - add to all agent files
        echo -e "${BLUE}📝 Adding custom message to all agent files: $message${NC}"
        
        for agent_file in "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/GEMINI.md" "$REPO_ROOT/AGENTS.md" "$REPO_ROOT/.github/copilot-instructions.md"; do
            if [[ -f "$agent_file" ]]; then
                # Check if manual additions section exists
                if grep -q "<!-- MANUAL ADDITIONS START -->" "$agent_file"; then
                    # Add to existing manual additions section (before the END marker)
                    sed -i "/<!-- MANUAL ADDITIONS END -->/i\\
- $message" "$agent_file"
                    echo -e "${GREEN}  ✅ Added to $(basename "$agent_file")${NC}"
                else
                    # Create new manual additions section at the end
                    cat >> "$agent_file" << EOF

<!-- MANUAL ADDITIONS START -->

## Custom Instructions
- $message

<!-- MANUAL ADDITIONS END -->
EOF
                    echo -e "${GREEN}  ✅ Created manual additions section in $(basename "$agent_file")${NC}"
                fi
            else
                echo -e "${YELLOW}  ⚠️  $(basename "$agent_file") not found${NC}"
            fi
        done
    fi
}

extract_project_intelligence() {
    # Extract real project state and content for updates
    local intelligence_file=$(mktemp)
    
    echo "# Project Intelligence Report - $(date)" > "$intelligence_file"
    
    # 1. Git and branch information
    echo "## Git Status" >> "$intelligence_file"
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    echo "BRANCH=$current_branch" >> "$intelligence_file"
    local last_commit_raw=$(git log -1 --oneline 2>/dev/null || echo "Initial setup")
    # Escape special characters in commit message for bash variable assignment
    local last_commit_escaped=$(echo "$last_commit_raw" | sed 's/["\\]/\\&/g')
    echo "LAST_COMMIT=\"$last_commit_escaped\"" >> "$intelligence_file"
    local repo_changes=$(git status --porcelain 2>/dev/null | wc -l || echo "0")
    echo "REPO_STATUS=\"$repo_changes uncommitted changes\"" >> "$intelligence_file"
    
    # 2. Find active specs directory - look for any specs with tasks.md
    local active_spec_dir=""
    local tasks_file=""
    
    # First try current branch
    if [[ -d "$REPO_ROOT/specs/$current_branch" && -f "$REPO_ROOT/specs/$current_branch/tasks.md" ]]; then
        active_spec_dir="$REPO_ROOT/specs/$current_branch"
        tasks_file="$active_spec_dir/tasks.md"
    else
        # Look for any spec directory with tasks.md
        for spec_dir in "$REPO_ROOT/specs"/*; do
            if [[ -d "$spec_dir" && -f "$spec_dir/tasks.md" ]]; then
                active_spec_dir="$spec_dir"
                tasks_file="$spec_dir/tasks.md"
                break
            fi
        done
    fi
    
    # 2. Task analysis from any available tasks.md
    if [[ -n "$tasks_file" && -f "$tasks_file" ]]; then
        echo "## Task Analysis" >> "$intelligence_file"
        echo "ACTIVE_SPEC=\"$(basename "$active_spec_dir")\"" >> "$intelligence_file"
        
        local total_tasks=$(grep -c "^- \[" "$tasks_file" 2>/dev/null | tr -d '\n' || echo "0")
        local completed_tasks=$(grep -c "^- \[x\]" "$tasks_file" 2>/dev/null | tr -d '\n' || echo "0")
        
        # Ensure variables are numeric (fallback to 0) and clean
        total_tasks=$(echo "${total_tasks:-0}" | tr -d ' \n\r\t')
        completed_tasks=$(echo "${completed_tasks:-0}" | tr -d ' \n\r\t')
        
        # Validate they are actually numbers
        if ! [[ "$total_tasks" =~ ^[0-9]+$ ]]; then
            total_tasks=0
        fi
        if ! [[ "$completed_tasks" =~ ^[0-9]+$ ]]; then
            completed_tasks=0
        fi
        
        # Avoid division by zero
        local pending_tasks=$((total_tasks - completed_tasks))
        local progress_percent=0
        if [[ $total_tasks -gt 0 ]]; then
            progress_percent=$(( completed_tasks * 100 / total_tasks ))
        fi
        
        echo "TOTAL_TASKS=$total_tasks" >> "$intelligence_file"
        echo "COMPLETED_TASKS=$completed_tasks" >> "$intelligence_file"
        echo "PENDING_TASKS=$pending_tasks" >> "$intelligence_file"
        echo "PROGRESS_PERCENT=$progress_percent" >> "$intelligence_file"
        
        # Get current phase (generic approach)
        local current_phase="In Progress"
        if [[ $total_tasks -eq 0 ]]; then
            current_phase="No Tasks"
        elif [[ $completed_tasks -eq $total_tasks ]]; then
            current_phase="Complete"
        elif [[ $completed_tasks -eq 0 ]]; then
            current_phase="Starting"
        else
            current_phase="In Progress ($progress_percent% complete)"
        fi
        # Escape special characters in current phase for bash variable assignment
        local current_phase_escaped=$(echo "$current_phase" | sed 's/["\\(%)]/\\&/g')
        echo "CURRENT_PHASE=\"$current_phase_escaped\"" >> "$intelligence_file"
        
        # Get agent task distribution - use simple approach
        echo "## Agent Task Distribution" >> "$intelligence_file"
        
        # Count pending tasks for each agent (disable exit on error temporarily)
        set +e
        local claude_pending=$(grep -c "^- \[ \].*@claude" "$tasks_file" 2>/dev/null)
        [[ $? -ne 0 ]] && claude_pending=0
        
        local copilot_pending=$(grep -c "^- \[ \].*@copilot" "$tasks_file" 2>/dev/null)
        [[ $? -ne 0 ]] && copilot_pending=0
        
        local codex_pending=$(grep -c "^- \[ \].*@codex" "$tasks_file" 2>/dev/null)
        [[ $? -ne 0 ]] && codex_pending=0
        
        local gemini_pending=$(grep -c "^- \[ \].*@gemini" "$tasks_file" 2>/dev/null)
        [[ $? -ne 0 ]] && gemini_pending=0
        set -e
        echo "CLAUDE_PENDING=$claude_pending" >> "$intelligence_file"
        echo "COPILOT_PENDING=$copilot_pending" >> "$intelligence_file"
        echo "CODEX_PENDING=$codex_pending" >> "$intelligence_file"
        echo "GEMINI_PENDING=$gemini_pending" >> "$intelligence_file"
    else
        echo "## Task Analysis" >> "$intelligence_file"
        echo "ACTIVE_SPEC=\"None found\"" >> "$intelligence_file"
        echo "TOTAL_TASKS=0" >> "$intelligence_file"
        echo "COMPLETED_TASKS=0" >> "$intelligence_file"
        echo "PENDING_TASKS=0" >> "$intelligence_file"
        echo "PROGRESS_PERCENT=0" >> "$intelligence_file"
        echo "CURRENT_PHASE=\"No active specifications\"" >> "$intelligence_file"
        echo "## Agent Task Distribution" >> "$intelligence_file"
        echo "CLAUDE_PENDING=0" >> "$intelligence_file"
        echo "COPILOT_PENDING=0" >> "$intelligence_file"
        echo "CODEX_PENDING=0" >> "$intelligence_file"
        echo "GEMINI_PENDING=0" >> "$intelligence_file"
    fi
    
    # 3. Technology stack from any available plan.md
    local plan_file=""
    if [[ -n "$active_spec_dir" && -f "$active_spec_dir/plan.md" ]]; then
        plan_file="$active_spec_dir/plan.md"
    else
        # Look for any plan.md in specs
        for spec_dir in "$REPO_ROOT/specs"/*; do
            if [[ -d "$spec_dir" && -f "$spec_dir/plan.md" ]]; then
                plan_file="$spec_dir/plan.md"
                break
            fi
        done
    fi
    
    if [[ -n "$plan_file" && -f "$plan_file" ]]; then
        echo "## Technology Stack" >> "$intelligence_file"
        echo "TECH_STACK=\"$(grep -A 5 "Tech Stack\|Language\|Technologies" "$plan_file" 2>/dev/null | head -10 | tr '\n' ' ' | sed 's/[^a-zA-Z0-9.,+ ()-]/ /g' || echo "Not specified")\"" >> "$intelligence_file"
    else
        echo "## Technology Stack" >> "$intelligence_file"
        echo "TECH_STACK=\"Not specified\"" >> "$intelligence_file"
    fi
    
    # 4. Actual implemented features (check src/ directory)
    echo "## Implemented Features" >> "$intelligence_file"
    if [[ -d "$REPO_ROOT/src" ]]; then
        local src_structure=$(find "$REPO_ROOT/src" -name "*.py" -type f | head -20 | sed 's|.*src/||' | tr '\n' ', ')
        local model_count=$(find "$REPO_ROOT/src/models" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        local service_count=$(find "$REPO_ROOT/src/services" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        local cli_count=$(find "$REPO_ROOT/src/cli" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        local lib_count=$(find "$REPO_ROOT/src/lib" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        echo "SRC_STRUCTURE=$src_structure" >> "$intelligence_file"
        echo "MODEL_COUNT=$model_count" >> "$intelligence_file"
        echo "SERVICE_COUNT=$service_count" >> "$intelligence_file"
        echo "CLI_COUNT=$cli_count" >> "$intelligence_file"
        echo "LIB_COUNT=$lib_count" >> "$intelligence_file"
    fi
    
    # 5. Test coverage analysis
    if [[ -d "$REPO_ROOT/tests" ]]; then
        echo "## Test Coverage" >> "$intelligence_file"
        local contract_tests=$(find "$REPO_ROOT/tests/contract" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        local integration_tests=$(find "$REPO_ROOT/tests/integration" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        local unit_tests=$(find "$REPO_ROOT/tests/unit" -name "*.py" -type f 2>/dev/null | wc -l || echo "0")
        echo "CONTRACT_TESTS=$contract_tests" >> "$intelligence_file"
        echo "INTEGRATION_TESTS=$integration_tests" >> "$intelligence_file"
        echo "UNIT_TESTS=$unit_tests" >> "$intelligence_file"
    fi
    
    # 6. Coordination system status
    echo "## Coordination System" >> "$intelligence_file"
    local coordinator_available=$([[ -f "$REPO_ROOT/scripts/agent-coordinator.py" ]] && echo "true" || echo "false")
    local coordination_plan_exists=$([[ -f "$REPO_ROOT/AI_COORDINATION_PLAN.md" ]] && echo "true" || echo "false")
    echo "COORDINATOR_AVAILABLE=$coordinator_available" >> "$intelligence_file"
    echo "COORDINATION_PLAN_EXISTS=$coordination_plan_exists" >> "$intelligence_file"
    
    # 7. Dependencies and environment
    if [[ -f "$REPO_ROOT/pyproject.toml" ]]; then
        echo "## Dependencies" >> "$intelligence_file"
        local python_version=$(grep 'python' "$REPO_ROOT/pyproject.toml" | sed 's/.*=\s*//; s/["><=]//g; s/\s//g' | head -1 || echo "3.11")
        local main_deps=$(grep -A 10 '^\[project.dependencies\]' "$REPO_ROOT/pyproject.toml" | grep -E '^".*"' | head -5 | tr '\n' ', ' | sed 's/,$//g' || echo "httpx, pydantic, fastapi")
        echo "PYTHON_VERSION=$python_version" >> "$intelligence_file"
        echo "MAIN_DEPS=$main_deps" >> "$intelligence_file"
    fi
    
    echo "$intelligence_file"
}

update_constitution() {
    local dry_run="$1"
    local force="$2"
    
    echo -e "${BLUE}📜 Updating Constitution.md...${NC}"
    
    # Extract current project intelligence
    local intelligence_file=$(extract_project_intelligence)
    if [[ -f "$intelligence_file" ]]; then
        source "$intelligence_file"
    else
        echo "Warning: Could not extract project intelligence" >&2
        return 1
    fi
    
    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}[DRY RUN] Would update constitution.md with:${NC}"
        echo "  • Branch: $BRANCH ($PROGRESS_PERCENT% complete)"
        echo "  • Current Phase: $CURRENT_PHASE"
        echo "  • Tech Stack: $(echo "$TECH_STACK" | cut -c1-50)..."
        echo "  • Agent Tasks: @claude($CLAUDE_PENDING), @copilot($COPILOT_PENDING), @codex($CODEX_PENDING), @gemini($GEMINI_PENDING)"
        echo "  • Implementation: $MODEL_COUNT models, $SERVICE_COUNT services, $CLI_COUNT CLI files"
        rm -f "$intelligence_file"
        return 0
    fi
    
    # Update constitution with current project state
    if [[ -f "$CONSTITUTION_FILE" ]]; then
        # Update existing sections
        local temp_file=$(mktemp)
        
        # Generate constitution with real project intelligence
        cat > "$temp_file" << EOF
# AI Agent Development Constitution

## Current Project Status (Auto-Generated)
- **Active Branch**: $BRANCH  
- **Last Commit**: $LAST_COMMIT
- **Active Specification**: ${ACTIVE_SPEC:-"None"}
- **Task Progress**: $COMPLETED_TASKS/$TOTAL_TASKS completed ($PROGRESS_PERCENT%)
- **Current Phase**: $CURRENT_PHASE
- **Implementation Status**: $MODEL_COUNT models, $SERVICE_COUNT services, $CLI_COUNT CLI files, $LIB_COUNT libraries
- **Test Coverage**: $CONTRACT_TESTS contract, $INTEGRATION_TESTS integration, $UNIT_TESTS unit tests
- **Last Updated**: $(date '+%Y-%m-%d %H:%M:%S')

## Agent Task Distribution (Current)
- **@claude**: $CLAUDE_PENDING pending tasks (integration & architecture)
- **@copilot**: $COPILOT_PENDING pending tasks (implementation & models)  
- **@codex**: $CODEX_PENDING pending tasks (testing & debugging)
- **@gemini**: $GEMINI_PENDING pending tasks (documentation & research)

## Active Technology Stack
$TECH_STACK

## Current Implementation Structure
\`\`\`
src/
$(ls -la "$REPO_ROOT/src" 2>/dev/null | tail -n +2 | head -10 | awk '{print "├── " $9}' || echo "├── [Not yet implemented]")

tests/  
$(ls -la "$REPO_ROOT/tests" 2>/dev/null | tail -n +2 | head -5 | awk '{print "├── " $9}' || echo "├── [Not yet implemented]")
\`\`\`

## Core Development Principles

### I. Spec-Driven Development (ACTIVE)
- ✅ Specifications become executable and drive implementation
- ✅ Follow the spec-kit methodology for all new features  
- ✅ Reference specs/\${ACTIVE_SPEC:-current}/ for current feature requirements
- ✅ Use contracts/ directory for API and interface specifications
- **Status**: $([ "$COORDINATION_PLAN_EXISTS" = "true" ] && echo "Coordination system active" || echo "Coordination system pending")

### II. Multi-Agent Coordination (IMPLEMENTED)
- ✅ Use @ assignments in tasks.md for agent coordination
- ✅ Coordinator Claude manages programmatic agent execution (scripts/agent-coordinator.py)
- ✅ Worker Claude handles complex integration tasks  
- ✅ Respect agent capabilities and limitations
- **Status**: $([ "$COORDINATOR_AVAILABLE" = "true" ] && echo "Agent coordinator ready" || echo "Agent coordinator pending")

### III. Test-First Development ($([ "$CONTRACT_TESTS" -gt 0 ] && echo "ACTIVE" || echo "PENDING"))
- $([ "$CONTRACT_TESTS" -gt 0 ] && echo "✅" || echo "⏳") All contract and integration tests must be written first
- $([ "$INTEGRATION_TESTS" -gt 0 ] && echo "✅" || echo "⏳") Tests must fail before implementation begins
- ✅ Follow TDD red-green-refactor cycle strictly
- ✅ Use `python3 run.py -m pytest` with appropriate markers (unit, integration, contract, browser, slow)
- **Current**: $CONTRACT_TESTS contract tests, $INTEGRATION_TESTS integration tests implemented

### IV. Architecture & Integration Focus ($([ "$SERVICE_COUNT" -gt 0 ] && echo "IN PROGRESS" || echo "PENDING"))
- ✅ Prefer async/await patterns for I/O operations
- $([ "$LIB_COUNT" -gt 0 ] && echo "✅" || echo "⏳") Use structured logging with JSON format  
- ✅ Implement proper error handling and rate limiting
- ✅ Follow existing code patterns and conventions
- **Current**: $SERVICE_COUNT services, $LIB_COUNT libraries implemented

### V. Documentation & Shared Memory (ACTIVE)
- ✅ Keep agent context files synchronized (use /update-memory)
- ✅ Update constitution.md when processes change (auto-generated)
- ✅ Document coordination decisions in AI_COORDINATION_PLAN.md  
- ✅ Use memory/ directory for shared knowledge

EOF

        # Preserve existing spec-kit section if it exists
        if grep -q "## Spec-Kit Development Workflow" "$CONSTITUTION_FILE"; then
            echo "" >> "$temp_file"
            sed -n '/## Spec-Kit Development Workflow/,$p' "$CONSTITUTION_FILE" >> "$temp_file"
        else
            # Add spec-kit section if missing
            cat >> "$temp_file" << 'EOF'

## Spec-Kit Development Workflow

### What is Spec-Kit?
Spec-Kit is a toolkit for **Spec-Driven Development** - an approach where specifications become executable and drive the implementation process instead of being discarded after initial coding.

### Core Philosophy
- **"Specifications become executable"** - specs are living documents, not throwaway artifacts
- **Intent-driven development** - focus on "what" before "how"
- **Specifications drive implementation** - plans and contracts guide code generation

### Available Commands
```bash
# Check spec-kit installation and requirements
uvx --from git+https://github.com/github/spec-kit.git specify check

# Initialize new specification (if needed for new features)
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

# Access spec-kit help
uvx --from git+https://github.com/github/spec-kit.git specify --help
```

### Project Structure (Already Generated)
This project was initialized with spec-kit and follows its structure:
```
specs/001-looking-to-build/    # Current feature specification
├── spec.md                    # Feature specification
├── plan.md                    # Technical implementation plan  
├── tasks.md                   # Detailed task breakdown (T001-T040)
├── quickstart.md             # User workflows
├── research.md               # Research and decisions
├── data-model.md             # Data entities and relationships
└── contracts/                # API and interface contracts
    ├── search-api.md
    ├── person-api.md
    ├── credits-api.md
    ├── cli-interface.md
    ├── stagehand-automation.md
    └── scroll-search-api.md

templates/                     # Spec-kit templates
memory/                       # Shared knowledge (this file)
```

### Agent Usage Guidelines
**All AI agents should:**
- Reference `specs/001-looking-to-build/tasks.md` for current task breakdown
- Follow the contracts in `specs/001-looking-to-build/contracts/` 
- Implement according to `specs/001-looking-to-build/plan.md`
- Update task completion status in `tasks.md` as work progresses

**For new features:**
- Use spec-kit to generate new spec directories
- Follow the established spec-driven workflow
- Generate tasks, contracts, and implementation plans before coding

### Integration with AI Coordination
Spec-kit specifications work with our AI coordination strategy:
- **@claude**: Handles architecture and multi-component integration per specs
- **@copilot**: Implements individual components following contract specifications
- **@codex**: Develops tests based on contract specifications (TDD approach)
- **@gemini**: Creates documentation and researches implementation approaches

## Governance
**Constitution supersedes all other practices**
- Amendments require documentation in this file
- All agents must verify compliance with these principles
- Use AI_COORDINATION_PLAN.md for runtime coordination guidance
- Complexity must be justified against these core principles

**Version**: 1.0.0 | **Ratified**: $(date '+%Y-%m-%d') | **Last Amended**: $(date '+%Y-%m-%d')
EOF
        fi
        
        mv "$temp_file" "$CONSTITUTION_FILE"
        echo -e "${GREEN}✅ Constitution.md updated with current project status${NC}"
        echo -e "${BLUE}📊 Updated with real-time project intelligence:${NC}"
        echo -e "  • Progress: $COMPLETED_TASKS/$TOTAL_TASKS tasks ($PROGRESS_PERCENT%)"
        echo -e "  • Phase: $CURRENT_PHASE"
        echo -e "  • Implementation: $MODEL_COUNT models, $SERVICE_COUNT services"
        echo -e "  • Agent workload: Claude($CLAUDE_PENDING), Copilot($COPILOT_PENDING), Codex($CODEX_PENDING), Gemini($GEMINI_PENDING)"
    else
        echo -e "${YELLOW}⚠️  Constitution.md not found, creating new one...${NC}"
        update_constitution "$dry_run" true
    fi
    
    # Cleanup intelligence file
    rm -f "$intelligence_file"
}

update_coordination_docs() {
    local dry_run="$1"
    
    echo -e "${BLUE}🔄 Updating Coordination Documentation...${NC}"
    
    if [[ "$dry_run" == "true" ]]; then
        echo -e "${YELLOW}[DRY RUN] Would update AI_COORDINATION_PLAN.md status${NC}"
        return 0
    fi
    
    # Update the system status in coordination plan
    if [[ -f "$COORDINATION_PLAN" ]]; then
        # Update last modified date
        local temp_file=$(mktemp)
        sed "s/Last updated: [0-9-]*/Last updated: $(date '+%Y-%m-%d')/" "$COORDINATION_PLAN" > "$temp_file"
        mv "$temp_file" "$COORDINATION_PLAN"
        echo -e "${GREEN}✅ Coordination documentation updated${NC}"
    else
        echo -e "${YELLOW}⚠️  AI_COORDINATION_PLAN.md not found${NC}"
    fi
}

# Parse arguments
MESSAGE=""
SCOPE="all"
FORCE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        agent|claude|gemini|agents|copilot|constitution|coordination|all)
            SCOPE="$1"
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            # First unknown argument is treated as the message
            if [[ -z "$MESSAGE" ]]; then
                MESSAGE="$1"
                shift
            else
                echo -e "${RED}❌ Unknown option: $1${NC}"
                usage
                exit 1
            fi
            ;;
    esac
done

# Main execution
echo -e "${CYAN}📚 Updating Shared Memory for AI Agents${NC}"
echo -e "${CYAN}=======================================${NC}"

check_prerequisites

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
fi

case $SCOPE in
    "agent")
        update_agent_context "$DRY_RUN" "$MESSAGE" "all"
        ;;
    "claude")
        update_agent_context "$DRY_RUN" "$MESSAGE" "claude"
        ;;
    "gemini")
        update_agent_context "$DRY_RUN" "$MESSAGE" "gemini"
        ;;
    "agents")
        update_agent_context "$DRY_RUN" "$MESSAGE" "agents"
        ;;
    "copilot")
        update_agent_context "$DRY_RUN" "$MESSAGE" "copilot"
        ;;
    "constitution") 
        update_constitution "$DRY_RUN" "$FORCE"
        ;;
    "coordination")
        update_coordination_docs "$DRY_RUN"
        ;;
    "all")
        echo -e "${BLUE}📋 Updating all shared memory components...${NC}"
        update_agent_context "$DRY_RUN" "$MESSAGE" "all"
        echo ""
        update_constitution "$DRY_RUN" "$FORCE"  
        echo ""
        update_coordination_docs "$DRY_RUN"
        ;;
esac

echo ""
echo -e "${GREEN}✅ Shared memory update complete!${NC}"
echo -e "${CYAN}📌 All AI agents now have synchronized context and constitution${NC}"
