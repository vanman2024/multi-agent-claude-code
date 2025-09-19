#!/usr/bin/env bash
# Incrementally update agent context files based on new feature plan
# Supports: CLAUDE.md, GEMINI.md, AGENTS.md, and .github/copilot-instructions.md

set -e

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "001-looking-to-build")
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"
NEW_PLAN="$FEATURE_DIR/plan.md"

# Determine which agent context files to update
CLAUDE_FILE="$REPO_ROOT/CLAUDE.md"
GEMINI_FILE="$REPO_ROOT/GEMINI.md"
AGENTS_FILE="$REPO_ROOT/AGENTS.md"
COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"

# Allow override via argument
AGENT_TYPE="$1"

if [ ! -f "$NEW_PLAN" ]; then
    echo "ERROR: No plan.md found at $NEW_PLAN"
    exit 1
fi

echo "=== Updating agent context files for feature $CURRENT_BRANCH ==="

# Extract tech from new plan safely
NEW_LANG=$(grep "Language/Version" "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/.*: *//' | sed 's/NEEDS CLARIFICATION.*//' || echo "Python 3.11")
NEW_FRAMEWORK=$(grep "Primary Dependencies" "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/.*: *//' | sed 's/NEEDS CLARIFICATION.*//' || echo "Stagehand")
NEW_PROJECT_TYPE=$(grep "Project Type" "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/.*: *//' || echo "CLI tool")

# Function to update a single agent context file
update_agent_file() {
    local target_file="$1"
    local agent_name="$2"
    
    echo "Updating $agent_name context file: $target_file"
    
    # If file doesn't exist, create from template
    if [ ! -f "$target_file" ]; then
        echo "Creating new $agent_name context file..."
        
        # Check if template exists
        if [ -f "$REPO_ROOT/templates/agent-file-template.md" ]; then
            cp "$REPO_ROOT/templates/agent-file-template.md" "$target_file"
            
            # Replace placeholders safely
            sed -i.bak "s/\[PROJECT NAME\]/$(basename "$REPO_ROOT")/" "$target_file"
            sed -i.bak "s/\[DATE\]/$(date +%Y-%m-%d)/" "$target_file"
            sed -i.bak "s/\[EXTRACTED FROM ALL PLAN.MD FILES\]/- $NEW_LANG + $NEW_FRAMEWORK ($CURRENT_BRANCH)/" "$target_file"
            sed -i.bak "s|\[ACTUAL STRUCTURE FROM PLANS\]|src/\ntests/|" "$target_file"
            sed -i.bak "s|\[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES\]|# Add commands for $NEW_LANG|" "$target_file"
            sed -i.bak "s|\[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE\]|$NEW_LANG: Follow standard conventions|" "$target_file"
            sed -i.bak "s|\[LAST 3 FEATURES AND WHAT THEY ADDED\]|- $CURRENT_BRANCH: Added $NEW_LANG + $NEW_FRAMEWORK|" "$target_file"
            
            # Clean up backup files
            rm -f "$target_file.bak"
        else
            # Create basic context file without template
            cat > "$target_file" << EOF
# $(basename "$REPO_ROOT") Development Guidelines

Auto-generated from all feature plans. Last updated: $(date +%Y-%m-%d)

## Active Technologies
- $NEW_LANG + $NEW_FRAMEWORK ($CURRENT_BRANCH)

## Project Structure
\`\`\`
src/
tests/
\`\`\`

## Commands
# Add commands for $NEW_LANG

## Code Style
$NEW_LANG: Follow standard conventions

## Recent Changes
- $CURRENT_BRANCH: Added $NEW_LANG + $NEW_FRAMEWORK

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
EOF
        fi
    else
        # Incremental merge - only do structural updates when targeting specific agent files
        if [ "$target_file" = "$AGENTS_FILE" ] && [ "$AGENT_TYPE" = "agents" -o "$AGENT_TYPE" = "agent" ]; then
            echo "Incrementally updating sections in $target_file ..."

            tmpdir=$(mktemp -d)
            trap 'rm -rf "$tmpdir"' EXIT

            # Helper: replace a section by heading title with new content file
            replace_section() {
                local file="$1"; local heading="$2"; local content_file="$3"
                local start end total
                start=$(grep -n "^${heading}$" "$file" | head -1 | cut -d: -f1 || true)
                total=$(wc -l < "$file")
                if [ -z "$start" ]; then
                    # Append if section not found
                    echo "" >> "$file"
                    cat "$content_file" >> "$file"
                    return 0
                fi
                end=$(awk -v s="$start" 'NR> s && /^## / {print NR; exit}' "$file")
                if [ -z "$end" ]; then end=$((total+1)); fi
                head -n $((start-1)) "$file" > "$file.new"
                cat "$content_file" >> "$file.new"
                tail -n +$end "$file" >> "$file.new"
                mv "$file.new" "$file"
            }

            # Gather repo-aware details
            # Structure bullets
            src_subdirs=$(ls -1 "$REPO_ROOT/src" 2>/dev/null | awk 'BEGIN{ORS=""} { if (NR>1) printf ", "; printf $0 }')
            tests_subdirs=$(ls -1 "$REPO_ROOT/tests" 2>/dev/null | awk 'BEGIN{ORS=""} { if (NR>1) printf ", "; printf $0 }')
            [ -z "$src_subdirs" ] && src_subdirs="cli, models, services, lib"
            [ -z "$tests_subdirs" ] && tests_subdirs="unit, integration, contract, performance"

            # Determine tooling from pyproject
            has_ruff=$(grep -n "^\[tool.ruff\]" "$REPO_ROOT/pyproject.toml" >/dev/null 2>&1 && echo yes || echo no)
            has_black=$(grep -n "^\[tool.black\]" "$REPO_ROOT/pyproject.toml" >/dev/null 2>&1 && echo yes || echo no)
            has_mypy=$(grep -n "^\[tool.mypy\]" "$REPO_ROOT/pyproject.toml" >/dev/null 2>&1 && echo yes || echo no)
            has_cov=$(grep -n "^\[tool.coverage.run\]" "$REPO_ROOT/pyproject.toml" >/dev/null 2>&1 && echo yes || echo no)

            # Extract pytest markers
            markers=$(awk '
                /^\[tool.pytest.ini_options\]/ {inini=1; next}
                inini && /^\[/ {inini=0}
                inini && /^markers *= *\[/ {inm=1; next}
                inm {
                    if ($0 ~ /\]/) {inm=0; next}
                    line=$0
                    gsub(/^[ \t]*"/,"",line)
                    gsub(/",[ \t]*$/, "", line)
                    sub(/:.*/, "", line)
                    if (length(line)>0) print line
                }
            ' "$REPO_ROOT/pyproject.toml")
            [ -z "$markers" ] && markers="unit\nintegration\ncontract\nperformance\nbrowser\nslow"

            # Generate sections
            cat > "$tmpdir/section_structure.md" <<EOF
## Project Structure & Module Organization
- \`src/\`: application code (${src_subdirs}).
- \`tests/\`: test suites (${tests_subdirs}).
- \`scripts/\`: helper scripts (e.g., \`git-commit-helper.sh\`, \`create-new-feature.sh\`).
- \`templates/\`, \`specs/\`, \`memory/\`: support assets and specifications.
- Configuration: \`.env\` for local secrets, \`pyproject.toml\` for tooling.
EOF

            # Conditional fragments for tool presence
            fix_ruff=""; [ "$has_ruff" = "yes" ] && fix_ruff=" (fix: \`ruff check --fix .\`)"
            dot_black=""; [ "$has_black" = "yes" ] && dot_black='.'
            dot_mypy=""; [ "$has_mypy" = "yes" ] && dot_mypy='.'
            dot_cov=""; [ "$has_cov" = "yes" ] && dot_cov='.'

            cat > "$tmpdir/section_commands.md" <<EOF
## Build, Test, and Development Commands
- Setup dev env: \`pip install -e .[dev]\`.
- Lint: \`ruff check .\`$fix_ruff
- Format: \`black .\`$dot_black
- Type-check: \`mypy src\`$dot_mypy
- Tests (all): \`python3 run.py -m pytest\`.
- Tests with coverage: \`python3 run.py -m pytest --cov=src --cov-report=term-missing\`$dot_cov
- Test selection: \`python3 run.py -m pytest -m unit\`, \`python3 run.py -m pytest -m "integration and not slow"\`.
EOF

            cat > "$tmpdir/section_style.md" <<EOF
## Coding Style & Naming Conventions
- Python 3.11+. Use 4-space indentation, line length 88.
- Naming: \`snake_case\` for modules/functions, \`PascalCase\` for classes, \`UPPER_CASE\` for constants.
- Prefer async/await, typed functions, and Pydantic models for data shapes.
- Formatting: Black; Linting: Ruff (rules configured in \`pyproject.toml\`).
- Type safety: MyPy in strict-ish mode (see \`[tool.mypy]\`).
EOF

            markers_line=$(echo "$markers" | awk 'BEGIN{ORS=""} { if (NR>1) printf ", "; printf $0 }')

            cat > "$tmpdir/section_testing.md" <<EOF
## Testing Guidelines
- Framework: \`pytest\` with \`pytest-asyncio\`; markers: ${markers_line}.
- File naming: \`tests/**/test_*.py\`.
- Aim for ≥80% coverage on new/changed code; include negative and async-path tests.
- Browser/slow tests should be marked; default CI path should skip \`-m slow\`.
EOF

            # Replace sections in place
            replace_section "$target_file" "## Project Structure & Module Organization" "$tmpdir/section_structure.md"
            replace_section "$target_file" "## Build, Test, and Development Commands" "$tmpdir/section_commands.md"
            replace_section "$target_file" "## Coding Style & Naming Conventions" "$tmpdir/section_style.md"
            replace_section "$target_file" "## Testing Guidelines" "$tmpdir/section_testing.md"

            echo "Updated sections: structure, commands, style, testing."
        elif [ "$target_file" = "$CLAUDE_FILE" ] && [ "$AGENT_TYPE" = "claude" ]; then
            echo "Incrementally updating sections in $target_file ..."
            # Add structural updates for CLAUDE.md when specifically targeted
            echo "Structural updates available for CLAUDE.md when specifically targeted."
        elif [ "$target_file" = "$GEMINI_FILE" ] && [ "$AGENT_TYPE" = "gemini" ]; then
            echo "Incrementally updating sections in $target_file ..."
            # Add structural updates for GEMINI.md when specifically targeted
            echo "Structural updates available for GEMINI.md when specifically targeted."
        elif [ "$target_file" = "$COPILOT_FILE" ] && [ "$AGENT_TYPE" = "copilot" ]; then
            echo "Incrementally updating sections in $target_file ..."
            # Add structural updates for copilot-instructions.md when specifically targeted
            echo "Structural updates available for copilot-instructions.md when specifically targeted."
        else
            echo "File already exists. No structural updates when using 'all' scope - use specific agent name for structural updates."
        fi
    fi
}

# Update files based on argument or detect existing files
case "$AGENT_TYPE" in
    "claude")
        update_agent_file "$CLAUDE_FILE" "Claude Code"
        ;;
    "gemini") 
        update_agent_file "$GEMINI_FILE" "Gemini CLI"
        ;;
    "agent"|"agents") 
        update_agent_file "$AGENTS_FILE" "Repository Guidelines"
        ;;
    "copilot")
        update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        ;;
    "all")
        # Create all agent context files
        update_agent_file "$CLAUDE_FILE" "Claude Code"
        update_agent_file "$GEMINI_FILE" "Gemini CLI" 
        update_agent_file "$AGENTS_FILE" "Repository Guidelines"
        update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        ;;
    "")
        # Update all existing files, create missing ones if none exist
        updated_any=false
        [ -f "$CLAUDE_FILE" ] && update_agent_file "$CLAUDE_FILE" "Claude Code" && updated_any=true
        [ -f "$GEMINI_FILE" ] && update_agent_file "$GEMINI_FILE" "Gemini CLI" && updated_any=true
        [ -f "$AGENTS_FILE" ] && update_agent_file "$AGENTS_FILE" "Repository Guidelines" && updated_any=true
        [ -f "$COPILOT_FILE" ] && update_agent_file "$COPILOT_FILE" "GitHub Copilot" && updated_any=true
        
        # If no files exist, create all of them
        if [ "$updated_any" = false ]; then
            echo "No agent context files found. Creating all standard agent context files."
            update_agent_file "$CLAUDE_FILE" "Claude Code"
            update_agent_file "$GEMINI_FILE" "Gemini CLI" 
            update_agent_file "$AGENTS_FILE" "Repository Guidelines"
            update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        fi
        ;;
    *)
        echo "ERROR: Unknown agent type '$AGENT_TYPE'. Use: claude, gemini, agents, copilot, all, or leave empty."
        exit 1
        ;;
esac

echo ""
echo "Summary of changes:"
if [ ! -z "$NEW_LANG" ]; then
    echo "- Added language: $NEW_LANG"
fi
if [ ! -z "$NEW_FRAMEWORK" ]; then
    echo "- Added framework: $NEW_FRAMEWORK"
fi

echo ""
echo "Usage: $0 [claude|gemini|agents|copilot|all]"
echo "  - No argument: Update all existing agent context files (create all if none exist)"
echo "  - claude: Update only CLAUDE.md"
echo "  - gemini: Update only GEMINI.md"
echo "  - agents: Update only AGENTS.md (repository guidelines)"
echo "  - copilot: Update only .github/copilot-instructions.md"
echo "  - all: Create/update all agent context files"
