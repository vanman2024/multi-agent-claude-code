#!/bin/bash

# integrate-test-with-speckit.sh
# Bridges spec-kit TDD tasks (T011-T028) with our test generation

set -e

echo "🔗 Integrating spec-kit TDD tasks with test generation..."

# Find the most recent spec-kit tasks file
TASK_FILE=$(ls -t specs/*/tasks.md 2>/dev/null | head -1)

if [ -z "$TASK_FILE" ]; then
    echo "❌ No spec-kit tasks found. Run /specify, /plan, /tasks first."
    exit 1
fi

echo "📋 Found tasks file: $TASK_FILE"

# Extract TDD tasks (T011-T028)
echo "🧪 Extracting TDD tasks..."
TDD_TASKS=$(grep -E "^- T0(1[1-9]|2[0-8]):" "$TASK_FILE" || true)

if [ -z "$TDD_TASKS" ]; then
    echo "⚠️ No TDD tasks found (T011-T028). Spec-kit may not have generated test tasks."
    echo "💡 Running general test generation instead..."
    
    # Fall back to analyzing project for test generation
    echo "📊 Analyzing project structure for test needs..."
    
    # Check what exists
    HAS_FRONTEND=$([ -d "frontend" ] && echo "true" || echo "false")
    HAS_BACKEND=$([ -d "backend" ] && echo "true" || echo "false")
    HAS_API=$(grep -l "api" package.json 2>/dev/null || grep -l "express\|fastapi" requirements.txt 2>/dev/null || echo "")
    
    echo "Frontend: $HAS_FRONTEND"
    echo "Backend: $HAS_BACKEND"
    echo "API: $([ -n "$HAS_API" ] && echo "true" || echo "false")"
    
    # Generate tests based on what exists
    TEST_TYPES=""
    [ "$HAS_FRONTEND" = "true" ] && TEST_TYPES="$TEST_TYPES --unit"
    [ -n "$HAS_API" ] && TEST_TYPES="$TEST_TYPES --integration"
    [ "$HAS_FRONTEND" = "true" ] && TEST_TYPES="$TEST_TYPES --e2e"
    
    echo "🚀 Triggering test generation: $TEST_TYPES"
    echo "Run: /test:generate $TEST_TYPES"
else
    echo "✅ Found TDD tasks:"
    echo "$TDD_TASKS"
    
    # Parse TDD tasks and map to test types
    HAS_UNIT=$(echo "$TDD_TASKS" | grep -i "unit test" || true)
    HAS_INTEGRATION=$(echo "$TDD_TASKS" | grep -i "integration\|api test" || true)
    HAS_E2E=$(echo "$TDD_TASKS" | grep -i "e2e\|end-to-end" || true)
    
    # Build test generation command
    TEST_FLAGS=""
    [ -n "$HAS_UNIT" ] && TEST_FLAGS="$TEST_FLAGS --unit"
    [ -n "$HAS_INTEGRATION" ] && TEST_FLAGS="$TEST_FLAGS --integration"
    [ -n "$HAS_E2E" ] && TEST_FLAGS="$TEST_FLAGS --e2e"
    
    if [ -z "$TEST_FLAGS" ]; then
        TEST_FLAGS="--all"
    fi
    
    echo "🚀 Mapped to test types: $TEST_FLAGS"
    echo "Run: /test:generate $TEST_FLAGS"
    
    # Create test tracking file
    SPEC_DIR=$(dirname "$TASK_FILE")
    echo "# Test Implementation Status" > "$SPEC_DIR/test-status.md"
    echo "" >> "$SPEC_DIR/test-status.md"
    echo "## TDD Tasks from spec-kit:" >> "$SPEC_DIR/test-status.md"
    echo "$TDD_TASKS" >> "$SPEC_DIR/test-status.md"
    echo "" >> "$SPEC_DIR/test-status.md"
    echo "## Generated Tests:" >> "$SPEC_DIR/test-status.md"
    echo "- [ ] Unit tests" >> "$SPEC_DIR/test-status.md"
    echo "- [ ] Integration tests" >> "$SPEC_DIR/test-status.md"
    echo "- [ ] E2E tests" >> "$SPEC_DIR/test-status.md"
    
    echo "📝 Created test tracking: $SPEC_DIR/test-status.md"
fi

echo ""
echo "✅ Integration complete!"
echo ""
echo "Next steps:"
echo "1. Run the test generation command shown above"
echo "2. Implement tests for each TDD task"
echo "3. Mark tasks complete as you go"