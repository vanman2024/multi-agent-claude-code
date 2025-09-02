#!/bin/bash
# Local Pre-Commit Testing Script
# This script runs the SAME checks that GitHub Actions will run
# Run this before creating/updating pull requests to catch issues early

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
WARNINGS=0

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  Local Pre-Commit Testing Suite     ${NC}"
echo -e "${BLUE}  (Mirrors GitHub Actions Pipeline)  ${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Project: $PROJECT_ROOT"
echo "This script runs the same checks as GitHub Actions CI/CD pipeline"
echo ""

# Function to run a test stage
run_stage() {
    local stage_name="$1"
    local stage_function="$2"
    
    echo -e "${YELLOW}🔍 Stage: $stage_name${NC}"
    echo "----------------------------------------"
    
    if $stage_function; then
        echo -e "${GREEN}✅ $stage_name - PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ $stage_name - FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
    echo ""
}

# Function to detect project type
detect_project_type() {
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        echo "javascript"
    elif [ -f "$PROJECT_ROOT/requirements.txt" ] || [ -f "$PROJECT_ROOT/setup.py" ]; then
        echo "python"
    elif [ -f "$PROJECT_ROOT/go.mod" ]; then
        echo "go"
    elif [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
        echo "rust"
    else
        echo "mixed"  # This project is a mixed scripting project
    fi
}

# Stage 1: Code Quality Check (mirrors quality-check job in GitHub Actions)
stage_quality_check() {
    local success=true
    
    echo "📋 Running linter..."
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        if npm run lint 2>/dev/null; then
            echo "  ✓ JavaScript/TypeScript linting passed"
        elif command -v npm >/dev/null 2>&1; then
            echo "  ⚠ No lint script found or linting failed"
            ((WARNINGS++))
        else
            echo "  ⚠ npm not available, skipping JS linting"
            ((WARNINGS++))
        fi
    fi
    
    # For this project, check shell scripts with shellcheck if available
    if command -v shellcheck >/dev/null 2>&1; then
        echo "  Running shellcheck on shell scripts..."
        local shell_issues=0
        while IFS= read -r -d '' script; do
            if ! shellcheck "$script" 2>/dev/null; then
                ((shell_issues++))
            fi
        done < <(find "$PROJECT_ROOT" -name "*.sh" -print0)
        
        if [ "$shell_issues" -eq 0 ]; then
            echo "  ✓ Shell script linting passed"
        else
            echo "  ⚠ Found $shell_issues shell script issues"
            ((WARNINGS++))
        fi
    else
        echo "  ⚠ shellcheck not available, skipping shell linting"
        ((WARNINGS++))
    fi
    
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        if command -v flake8 >/dev/null 2>&1; then
            if flake8 . 2>/dev/null; then
                echo "  ✓ Python linting passed"
            else
                echo "  ⚠ Python linting issues found"
                ((WARNINGS++))
            fi
        else
            echo "  ⚠ flake8 not installed, skipping Python linting"
            ((WARNINGS++))
        fi
    fi
    
    echo "📋 Running type check..."
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        if npm run typecheck 2>/dev/null || npm run type-check 2>/dev/null || npx tsc --noEmit 2>/dev/null; then
            echo "  ✓ TypeScript type checking passed"
        elif grep -q "typescript" "$PROJECT_ROOT/package.json" 2>/dev/null; then
            echo "  ⚠ TypeScript type checking failed"
            ((WARNINGS++))
        else
            echo "  ✓ No TypeScript configuration found"
        fi
    fi
    
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        if command -v mypy >/dev/null 2>&1; then
            if mypy . 2>/dev/null; then
                echo "  ✓ Python type checking passed"
            else
                echo "  ⚠ Python type checking issues found"
                ((WARNINGS++))
            fi
        else
            echo "  ⚠ mypy not installed, skipping Python type checking"
            ((WARNINGS++))
        fi
    fi
    
    echo "📋 Checking code formatting..."
    if [ -f "$PROJECT_ROOT/.prettierrc" ] || [ -f "$PROJECT_ROOT/.prettierrc.json" ]; then
        if npx prettier --check . 2>/dev/null; then
            echo "  ✓ Code formatting is correct"
        else
            echo "  ⚠ Code formatting issues found (run: npx prettier --write .)"
            ((WARNINGS++))
        fi
    else
        echo "  ⚠ No prettier config found, skipping format check"
        ((WARNINGS++))
    fi
    
    # Quality check passes if no critical failures (warnings are OK)
    return 0
}

# Stage 2: Unit Tests (mirrors unit-tests job in GitHub Actions)
stage_unit_tests() {
    local success=true
    
    echo "🧪 Running unit tests..."
    
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        if grep -q '"test"' "$PROJECT_ROOT/package.json"; then
            if npm test -- --coverage --watchAll=false 2>/dev/null || npm test 2>/dev/null; then
                echo "  ✓ JavaScript/TypeScript tests passed"
            else
                echo "  ✗ JavaScript/TypeScript tests failed"
                success=false
            fi
        else
            echo "  ⚠ No test script found in package.json"
            ((WARNINGS++))
        fi
    fi
    
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        if command -v pytest >/dev/null 2>&1; then
            if pytest --cov=. --cov-report=term-missing 2>/dev/null; then
                echo "  ✓ Python tests passed"
            else
                echo "  ✗ Python tests failed"
                success=false
            fi
        else
            echo "  ⚠ pytest not installed, skipping Python tests"
            ((WARNINGS++))
        fi
    fi
    
    # For this project, run existing test suites
    if [ -f "$SCRIPT_DIR/run-all-tests.sh" ]; then
        echo "  Running framework-specific tests..."
        if timeout 60 bash "$SCRIPT_DIR/run-all-tests.sh" >/dev/null 2>&1; then
            echo "  ✓ Framework tests passed"
        else
            echo "  ⚠ Framework tests had issues (non-blocking)"
            ((WARNINGS++))
        fi
    fi
    
    if [ "$success" = true ]; then
        return 0
    else
        return 1
    fi
}

# Stage 3: Integration Tests (mirrors integration-tests job in GitHub Actions)
stage_integration_tests() {
    local success=true
    
    echo "🔗 Running integration tests..."
    
    if [ -f "$PROJECT_ROOT/package.json" ] && grep -q "test:integration" "$PROJECT_ROOT/package.json"; then
        if npm run test:integration 2>/dev/null; then
            echo "  ✓ JavaScript integration tests passed"
        else
            echo "  ✗ JavaScript integration tests failed"
            success=false
        fi
    elif [ -d "$PROJECT_ROOT/tests/integration" ]; then
        if command -v pytest >/dev/null 2>&1; then
            if pytest tests/integration/ 2>/dev/null; then
                echo "  ✓ Python integration tests passed"
            else
                echo "  ✗ Python integration tests failed"
                success=false
            fi
        else
            echo "  ⚠ pytest not installed, skipping integration tests"
            ((WARNINGS++))
        fi
    else
        echo "  ⚠ No integration tests configured"
        ((WARNINGS++))
        # No integration tests is not a failure
        return 0
    fi
    
    if [ "$success" = true ]; then
        return 0
    else
        return 1
    fi
}

# Stage 4: Security Scanning (mirrors security-scan job in GitHub Actions)
stage_security_scan() {
    echo "🔒 Running security scans..."
    
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        if npm audit --audit-level=high 2>/dev/null; then
            echo "  ✓ npm audit passed"
        else
            echo "  ⚠ npm audit found issues (non-blocking)"
            ((WARNINGS++))
        fi
    fi
    
    if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
        if command -v safety >/dev/null 2>&1; then
            if safety check 2>/dev/null; then
                echo "  ✓ Python safety check passed"
            else
                echo "  ⚠ Python safety check found issues (non-blocking)"
                ((WARNINGS++))
            fi
        else
            echo "  ⚠ safety not installed, skipping Python security scan"
            ((WARNINGS++))
        fi
    fi
    
    # Check for common security issues in shell scripts
    echo "  Checking for common security patterns..."
    local security_issues=0
    while IFS= read -r -d '' file; do
        if grep -l "eval\|curl.*http://\|wget.*http://" "$file" >/dev/null 2>&1; then
            ((security_issues++))
        fi
    done < <(find "$PROJECT_ROOT" -name "*.sh" -print0)
    
    if [ "$security_issues" -eq 0 ]; then
        echo "  ✓ No obvious security issues found"
    else
        echo "  ⚠ Found $security_issues potential security issues"
        ((WARNINGS++))
    fi
    
    # Security scans are non-blocking like in GitHub Actions
    return 0
}

# Stage 5: Build Test (mirrors build job in GitHub Actions)
stage_build_test() {
    local success=true
    
    echo "🏗️ Running build test..."
    
    if [ -f "$PROJECT_ROOT/package.json" ] && grep -q '"build"' "$PROJECT_ROOT/package.json"; then
        if npm run build 2>/dev/null; then
            echo "  ✓ Build succeeded"
        else
            echo "  ✗ Build failed"
            success=false
        fi
    elif [ -f "$PROJECT_ROOT/Dockerfile" ]; then
        echo "  ⚠ Docker build test not implemented (requires Docker)"
        ((WARNINGS++))
    else
        echo "  ⚠ No build configuration found (not required for this project)"
        ((WARNINGS++))
    fi
    
    if [ "$success" = true ]; then
        return 0
    else
        return 1
    fi
}

# Stage 6: Git Status Check
stage_git_status() {
    echo "📝 Checking git status..."
    
    # Check if there are uncommitted changes
    if ! git diff --quiet 2>/dev/null; then
        echo "  ⚠ You have uncommitted changes"
        ((WARNINGS++))
    else
        echo "  ✓ No uncommitted changes"
    fi
    
    # Check if we're on a feature branch
    current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
        echo "  ⚠ You're on the main branch - consider using a feature branch"
        ((WARNINGS++))
    else
        echo "  ✓ Working on feature branch: $current_branch"
    fi
    
    return 0
}

# Change to project directory
cd "$PROJECT_ROOT"

# Detect project type
PROJECT_TYPE=$(detect_project_type)
echo "Detected project type: $PROJECT_TYPE"
echo ""

# Install dependencies if needed
echo "📦 Installing dependencies..."
case "$PROJECT_TYPE" in
    javascript)
        if [ -f "package.json" ]; then
            npm ci 2>/dev/null || npm install 2>/dev/null || echo "Failed to install npm dependencies"
        fi
        ;;
    python)
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt >/dev/null 2>&1 || echo "Failed to install Python dependencies"
        fi
        ;;
    mixed)
        echo "Mixed project type - dependencies handled per component"
        ;;
esac
echo ""

# Run all stages
run_stage "Code Quality Check" stage_quality_check || true
run_stage "Unit Tests" stage_unit_tests || true
run_stage "Integration Tests" stage_integration_tests || true
run_stage "Security Scanning" stage_security_scan || true
run_stage "Build Test" stage_build_test || true
run_stage "Git Status Check" stage_git_status || true

# Summary
echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}           SUMMARY                    ${NC}"
echo -e "${BLUE}======================================${NC}"
echo -e "${GREEN}✅ Stages Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Stages Failed: $TESTS_FAILED${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARNINGS${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical stages passed! Ready to create/update PR.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review any warnings above"
    echo "2. Commit your changes: git add . && git commit -m 'Your message'"
    echo "3. Push your changes: git push"
    echo "4. Create or update your pull request"
    
    if [ $WARNINGS -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}⚠️ Consider addressing the $WARNINGS warnings above${NC}"
    fi
    
    exit 0
else
    echo -e "${RED}❌ Some critical stages failed. Fix issues before creating PR.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Run linter and fix issues: npm run lint -- --fix"
    echo "- Fix type errors: npm run typecheck"  
    echo "- Fix failing tests: npm test"
    echo "- Check build issues: npm run build"
    exit 1
fi