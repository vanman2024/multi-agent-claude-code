#!/bin/bash
# Test Coverage Analyzer - Simple data collector (no AI)
# Analyzes test coverage and testing setup

echo "=== TEST COVERAGE ANALYSIS ==="
echo "Scan Date: $(date)"
echo "Project: $(basename "$(pwd)")"
echo ""

# Count test files
echo "📊 Test files found:"
TEST_COUNT=$(find . -name "*.test.*" -o -name "*.spec.*" | grep -v node_modules | wc -l)
echo "Total test files: $TEST_COUNT"

echo ""
echo "📁 Test structure:"
find . -name "__tests__" -type d | grep -v node_modules
find . -name "test" -type d | grep -v node_modules  
find . -name "tests" -type d | grep -v node_modules

echo ""
echo "🧪 Test file distribution:"
echo "Component tests:"
find . -path "*/__tests__/components/*" -name "*.test.*" | wc -l

echo "API tests:"
find . -path "*/__tests__/api/*" -name "*.test.*" | wc -l

echo "Utils tests:"
find . -path "*/__tests__/utils/*" -name "*.test.*" | wc -l

echo "E2E tests:"
find . -path "*/__tests__/e2e/*" -name "*.test.*" | wc -l

echo ""
echo "⚙️  Testing infrastructure:"
[ -f jest.config.js ] && echo "✓ Jest config found" || echo "⚠️  No Jest config"
[ -f playwright.config.ts ] && echo "✓ Playwright config found" || echo "⚠️  No Playwright config"
grep -q "coverage" package.json 2>/dev/null && echo "✓ Coverage scripts found" || echo "⚠️  No coverage scripts"

echo ""
echo "📈 Coverage artifacts:"
find . -name "coverage" -type d | grep -v node_modules
find . -name "*.lcov" | grep -v node_modules
find . -name "coverage-*.json" | grep -v node_modules

echo ""
echo "🏃 Test scripts in package.json:"
grep -A 10 '"scripts"' package.json 2>/dev/null | grep -E '"test|jest|playwright'

echo ""
echo "=== TEST COVERAGE SCAN COMPLETE ==="