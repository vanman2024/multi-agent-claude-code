#!/bin/bash

# implement-tasks.sh
# Simple script to load and display spec-kit tasks
# Claude Code decides the execution order

set -e

# Find the tasks file
if [ -n "$1" ]; then
    TASK_FILE="specs/$1/tasks.md"
else
    TASK_FILE=$(ls -t specs/*/tasks.md 2>/dev/null | head -1)
fi

if [ ! -f "$TASK_FILE" ]; then
    echo "❌ No spec-kit tasks found!"
    echo ""
    echo "Run these commands first:"
    echo "  /specify     # Define requirements"
    echo "  /plan        # Choose tech stack"
    echo "  /tasks       # Generate task list"
    exit 1
fi

echo "📋 Tasks file: $TASK_FILE"
echo ""

# Count task phases
INFRA=$(grep -c "^- \[ \] T00[0-9]\|^- \[ \] T010" "$TASK_FILE" 2>/dev/null || echo "0")
TESTS=$(grep -c "^- \[ \] T0[12][0-9]" "$TASK_FILE" 2>/dev/null | grep -v "T010" || echo "0")
CORE=$(grep -c "^- \[ \] T03[0-7]" "$TASK_FILE" 2>/dev/null || echo "0")
FEATURES=$(grep -c "^- \[ \] T0[3-9][8-9]\|^- \[ \] T[1-9][0-9][0-9]" "$TASK_FILE" 2>/dev/null || echo "0")

echo "📊 Task Summary:"
echo "  Infrastructure (T001-T010): $INFRA tasks"
echo "  Tests (T011-T028): $TESTS tasks"
echo "  Core (T029-T037): $CORE tasks"
echo "  Features (T038+): $FEATURES tasks"
echo ""
echo "✅ Ready for implementation!"