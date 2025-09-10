#!/bin/bash

# import-spec-kit-tasks.sh - Import spec-kit tasks into Claude Code's TodoWrite
# This reads tasks.md from spec-kit and loads them into Claude's todo system

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Spec-Kit Task Importer for Claude Code${NC}"
echo ""

# Function to find latest spec with tasks
find_tasks_file() {
    local latest_spec=""
    local latest_time=0
    
    # Find all tasks.md files
    for task_file in specs/*/tasks.md; do
        if [ -f "$task_file" ]; then
            mod_time=$(stat -c %Y "$task_file" 2>/dev/null || stat -f %m "$task_file" 2>/dev/null)
            if [ "$mod_time" -gt "$latest_time" ]; then
                latest_time=$mod_time
                latest_spec=$task_file
            fi
        fi
    done
    
    echo "$latest_spec"
}

# Function to parse tasks from tasks.md
parse_tasks() {
    local tasks_file="$1"
    local tasks_json="[]"
    local current_phase=""
    
    echo -e "${YELLOW}📖 Reading tasks from: $tasks_file${NC}"
    
    # Extract task lines (format: "- [ ] T001 Description")
    while IFS= read -r line; do
        # Check for phase headers
        if [[ "$line" =~ ^##.*Phase.*:(.*)$ ]]; then
            current_phase="${BASH_REMATCH[1]}"
            continue
        fi
        
        # Parse task lines
        if [[ "$line" =~ ^-\ \[\ \]\ (T[0-9]+)\ (\[P\]\ )?(.*)$ ]]; then
            task_id="${BASH_REMATCH[1]}"
            parallel="${BASH_REMATCH[2]}"
            description="${BASH_REMATCH[3]}"
            
            # Clean up description
            description="${description//\"/\\\"}"  # Escape quotes
            
            # Determine if it's infrastructure (T001-T010 usually)
            task_num="${task_id#T}"
            task_num="${task_num#0}"  # Remove leading zeros
            
            if [ "$task_num" -le 10 ]; then
                status="pending"
                priority="[INFRA]"
            else
                status="pending"
                priority=""
            fi
            
            # Add parallel marker if present
            if [ -n "$parallel" ]; then
                priority="$priority[P]"
            fi
            
            # Format for TodoWrite
            content="$task_id: $priority $description"
            activeForm="Working on $task_id: $description"
            
            echo "  Found: $task_id - $description"
            
            # Add to JSON array (simplified - in real script would use jq)
            tasks_json="${tasks_json%]},{\"content\":\"$content\",\"status\":\"$status\",\"activeForm\":\"$activeForm\"}]"
        fi
    done < "$tasks_file"
    
    # Fix JSON format
    tasks_json="${tasks_json/[,/[}"
    
    echo "$tasks_json"
}

# Function to create TodoWrite command
create_todo_command() {
    local tasks_json="$1"
    local output_file=".claude/temp-todo-import.json"
    
    mkdir -p .claude
    
    cat > "$output_file" << EOF
{
  "todos": $tasks_json
}
EOF
    
    echo -e "${GREEN}✅ Tasks prepared for import${NC}"
    echo ""
    echo "To import into Claude Code's TodoWrite, Claude should run:"
    echo ""
    echo "TodoWrite with contents from: $output_file"
    echo ""
    echo "This will load all spec-kit tasks into Claude's todo system."
}

# Function to analyze task distribution
analyze_tasks() {
    local tasks_file="$1"
    
    echo -e "${BLUE}📊 Task Analysis:${NC}"
    
    # Count different types
    local infra_count=$(grep -c "T00[0-9]" "$tasks_file" || true)
    local test_count=$(grep -c "T01[0-9]\|T02[0-3]" "$tasks_file" || true)
    local impl_count=$(grep -c "T0[2-9][4-9]\|T0[3-9][0-9]\|T05[0-2]" "$tasks_file" || true)
    local total_count=$(grep -c "^- \[ \] T" "$tasks_file" || true)
    
    echo "  🏗️  Infrastructure tasks (T001-T010): $infra_count"
    echo "  🧪 Test tasks (T011-T023): $test_count"
    echo "  ✨ Implementation tasks (T024+): $impl_count"
    echo "  📋 Total tasks: $total_count"
    echo ""
    
    # Check for CI/CD tasks
    if grep -q "CI\|CD\|pipeline\|GitHub Actions\|deploy" "$tasks_file"; then
        echo -e "${GREEN}✓${NC} CI/CD pipeline tasks found"
    else
        echo -e "${YELLOW}⚠️${NC} No CI/CD tasks found - may need supplementation"
    fi
    
    # Check for Docker/containerization
    if grep -q "Docker\|container\|compose" "$tasks_file"; then
        echo -e "${GREEN}✓${NC} Containerization tasks found"
    else
        echo -e "${YELLOW}⚠️${NC} No containerization tasks found"
    fi
}

# Main execution
main() {
    # Find tasks file
    TASKS_FILE=$(find_tasks_file)
    
    if [ -z "$TASKS_FILE" ] || [ ! -f "$TASKS_FILE" ]; then
        echo -e "${RED}❌ No tasks.md file found in specs/*/tasks.md${NC}"
        echo "Run 'tasks' command in spec-kit first to generate tasks"
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Found tasks file: $TASKS_FILE"
    echo ""
    
    # Analyze task distribution
    analyze_tasks "$TASKS_FILE"
    
    # Parse tasks and create JSON
    TASKS_JSON=$(parse_tasks "$TASKS_FILE")
    
    # Create TodoWrite command
    create_todo_command "$TASKS_JSON"
    
    # Summary
    echo -e "${BLUE}📋 Import Summary:${NC}"
    echo "1. Spec-kit tasks parsed from: $TASKS_FILE"
    echo "2. JSON prepared for TodoWrite import"
    echo "3. Claude can now execute tasks sequentially"
    echo ""
    echo -e "${YELLOW}💡 Execution Order:${NC}"
    echo "1. Start with T001-T010 (infrastructure) - MUST complete first!"
    echo "2. Then T011-T023 (tests) for TDD approach"
    echo "3. Finally T024+ (features) building on infrastructure"
    echo ""
    echo -e "${GREEN}✅ Ready for Claude Code to import and execute!${NC}"
}

# Run main function
main "$@"