#!/bin/bash

# This script mimics what the /test slash command should do
# It follows the logic from .claude/commands/test.md

echo "🔍 Detecting project type..."

# Step 1: Check recent changes
echo "📝 Checking recent changes..."
RECENT_CHANGES=$(git diff --name-only HEAD~1 2>/dev/null | head -5)
if [ -n "$RECENT_CHANGES" ]; then
    echo "Recent changes in:"
    echo "$RECENT_CHANGES"
fi

# Step 2: Detect project type
FRONTEND=false
BACKEND=false

# Check for frontend indicators
if [ -f "package.json" ] && grep -q -E '"react"|"vue"|"angular"|"svelte"|"next"' package.json 2>/dev/null; then
    FRONTEND=true
    echo "✅ Frontend project detected (React/Next.js)"
fi

# Check for backend indicators  
if [ -f "requirements.txt" ]; then
    BACKEND=true
    echo "✅ Python backend detected"
elif [ -f "package.json" ] && grep -q -E '"express"|"fastify"|"nestjs"' package.json 2>/dev/null; then
    BACKEND=true
    echo "✅ Node.js backend detected"
fi

# Determine test type
if [ "$FRONTEND" = true ] && [ "$BACKEND" = true ]; then
    echo "✅ Project type: Full-stack"
    TEST_TYPE="full-stack"
elif [ "$FRONTEND" = true ]; then
    echo "✅ Project type: Frontend"
    TEST_TYPE="frontend"
elif [ "$BACKEND" = true ]; then
    echo "✅ Project type: Backend"
    TEST_TYPE="backend"
else
    echo "⚠️  Could not detect project type"
    TEST_TYPE="unknown"
fi

echo ""
echo "🧪 Running $TEST_TYPE tests..."
echo "⏱️  Estimated time: 2-5 minutes"
echo ""

# Step 3: Run appropriate tests
case $TEST_TYPE in
    frontend|full-stack)
        echo "=== Frontend Testing ==="
        echo "📋 What the frontend-playwright-tester agent SHOULD do:"
        echo "  1. Check for Vercel deployment URL"
        echo "  2. Open Firefox browser via Playwright MCP"
        echo "  3. Navigate to the deployment or localhost:3002"
        echo "  4. Run E2E tests in the browser"
        echo "  5. Take screenshots of key pages"
        echo ""
        
        # Check if we can find a Vercel URL
        echo "🔍 Checking for Vercel deployment..."
        
        # Try to get Vercel URL from recent deployments
        VERCEL_URL=$(gh pr view --json url -q '.url' 2>/dev/null | sed 's/github.com/vercel.app/g' | sed 's/pull\//pr-/g')
        
        if [ -n "$VERCEL_URL" ]; then
            echo "🌐 Found Vercel preview: $VERCEL_URL"
            echo "❌ PROBLEM: Agent should open Firefox and test this URL"
        else
            echo "🏠 No Vercel URL found, would use localhost:3002"
            echo "❌ PROBLEM: Agent should start local dev server and test"
        fi
        
        echo ""
        echo "📝 To properly invoke the agent, the /test command should:"
        echo "   Use Task tool with subagent_type: frontend-playwright-tester"
        echo ""
        
        # Run local Jest tests as fallback
        echo "📦 Running local Jest tests instead..."
        npm test
        ;;
        
    backend)
        echo "=== Backend Testing ==="
        echo "📋 What the backend-tester agent SHOULD do:"
        echo "  1. Detect testing framework (Jest/Pytest/Go test)"
        echo "  2. Run unit tests"
        echo "  3. Run integration tests"
        echo "  4. Check coverage"
        echo ""
        
        # Run actual tests
        if [ -f "package.json" ]; then
            echo "Running Node.js tests..."
            npm test
        elif [ -f "requirements.txt" ]; then
            echo "Would run: pytest"
        fi
        ;;
        
    *)
        echo "❌ Cannot determine which tests to run"
        echo "💡 Use: /test --frontend or /test --backend"
        ;;
esac

echo ""
echo "📊 Test Results Summary"
echo "======================"
echo "This script shows what SHOULD happen when /test is run."
echo "The actual /test command needs to invoke agents via Task tool."