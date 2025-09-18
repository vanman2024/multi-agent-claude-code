#!/bin/bash
# Frontend Testing Suite Setup Script
#
# PURPOSE: Scaffold a fast, agent‑friendly Playwright testing suite for local development
# USAGE: ./frontend-tests-template/setup-testing.sh [--yes] [--skip-install] [--skip-browsers] [--pm npm|pnpm|yarn] [--force]
# PART OF: Frontend testing template for solo/local development
# CONNECTS TO: playwright.config.ts, frontend-tests/, GitHub Actions workflow (frontend tests)

set -euo pipefail

echo "🚀 Setting up Frontend Testing Suite..."

# Flags
YES=${YES:-0}
SKIP_INSTALL=0
SKIP_BROWSERS=0
PM=""
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes|-y) YES=1; shift ;;
    --skip-install) SKIP_INSTALL=1; shift ;;
    --skip-browsers) SKIP_BROWSERS=1; shift ;;
    --pm) PM="${2:-}"; shift 2 ;;
    --force) FORCE=1; shift ;;
    -h|--help)
      grep -E '^# (PURPOSE|USAGE|PART OF|CONNECTS TO):' "$0" | sed 's/^# //'
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Guard: project root
if [ ! -f "package.json" ]; then
    echo "❌ Error: No package.json found. Run from your project root."
    exit 1
fi

# Detect package manager if not specified
if [ -z "$PM" ]; then
  if [ -f "pnpm-lock.yaml" ]; then PM=pnpm; elif [ -f "yarn.lock" ]; then PM=yarn; else PM=npm; fi
fi

run_pm() {
  case "$PM" in
    npm) npm "$@" ;;
    pnpm) pnpm "$@" ;;
    yarn) yarn "$@" ;;
    *) echo "❌ Unknown package manager: $PM"; exit 1 ;;
  esac
}

# Backup existing frontend-tests unless --force
if [ -d "frontend-tests" ] && [ "$FORCE" -ne 1 ]; then
  echo "⚠️  Frontend-tests directory exists. Creating backup..."
  mv frontend-tests "frontend-tests.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy the testing suite
echo "📋 Copying frontend testing suite template..."
mkdir -p frontend-tests
cp -r frontend-tests-template/tests/* ./frontend-tests/

# Copy GitHub Actions workflow
mkdir -p .github/workflows
cp -f frontend-tests-template/.github/workflows/ci.yml .github/workflows/frontend-tests.yml

# Ensure .gitignore entries
{ echo "playwright-report/"; echo "test-results/"; echo "tests/screenshots/"; } | while read -r line; do
  grep -qxF "$line" .gitignore 2>/dev/null || echo "$line" >> .gitignore
done

# Update package.json scripts using jq (safer than sed) - NAMESPACED
echo "📦 Updating package.json scripts (namespaced)..."
if ! command -v jq >/dev/null 2>&1; then
  echo "⚠️  jq not found; installing via $PM to modify package.json safely"
  run_pm add -D jq || true
fi

tmp_pkg=$(mktemp)
jq '.scripts = (.scripts // {}) + {
  "test:frontend": "playwright test frontend-tests/",
  "test:frontend:headed": "playwright test --headed frontend-tests/",
  "test:frontend:debug": "playwright test --debug frontend-tests/",
  "test:frontend:ui": "playwright test --ui frontend-tests/",
  "test:frontend:e2e": "playwright test frontend-tests/e2e/",
  "test:frontend:api": "playwright test frontend-tests/api/",
  "test:frontend:visual": "playwright test frontend-tests/visual/",
  "test:frontend:accessibility": "playwright test frontend-tests/accessibility/",
  "test:frontend:smoke": "playwright test --grep @smoke frontend-tests/",
  "test:frontend:regression": "playwright test --grep @regression frontend-tests/",
  "frontend:report": "playwright show-report",
  "frontend:install-browsers": "playwright install",
  "frontend:install-deps": "playwright install-deps",
  "frontend:codegen": "playwright codegen",
  "lint:frontend": "eslint frontend-tests/ --ext .js,.ts",
  "lint:frontend:fix": "eslint frontend-tests/ --ext .js,.ts --fix",
  "typecheck:frontend": "tsc --noEmit",
  "frontend:setup": "npm run frontend:install-browsers && npm run frontend:install-deps",
  "ci:frontend": "npm run lint:frontend && npm run typecheck:frontend && npm run test:frontend",
  "test:frontend:parallel": "playwright test --workers=4 frontend-tests/",
  "test:frontend:shard": "playwright test --shard=1/4 frontend-tests/"
}' package.json > "$tmp_pkg" && mv "$tmp_pkg" package.json

# Create playwright config if it doesn't exist
if [ ! -f "playwright.config.ts" ]; then
    echo "⚙️  Creating Playwright configuration..."
    cp frontend-tests-template/playwright.config.ts ./
fi

# Create smoke runner script
cp -f frontend-tests-template/tests/run-smoke.sh ./frontend-tests/
chmod +x ./frontend-tests/run-smoke.sh

# Create screenshots directory
mkdir -p frontend-tests/screenshots

# Create .env.example for test configuration
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# Test Configuration
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3001
API_TOKEN=your-api-token-here

# Test Data Setup
SETUP_TEST_DB=false
SETUP_TEST_DATA=false
CLEANUP_TEST_DB=false
CLEANUP_TEST_DATA=false
CLEANUP_TEMP_FILES=false

# Browser Installation
INSTALL_BROWSERS=false
EOF
fi

if [ "$SKIP_INSTALL" -eq 0 ]; then
  echo "📥 Installing testing dependencies via $PM..."
  case "$PM" in
    npm) npm install --save-dev @playwright/test @types/node eslint typescript @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier axe-playwright playwright-visual-regression ;;
    pnpm) pnpm add -D @playwright/test @types/node eslint typescript @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier axe-playwright playwright-visual-regression ;;
    yarn) yarn add -D @playwright/test @types/node eslint typescript @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier axe-playwright playwright-visual-regression ;;
  esac

  if [ "$SKIP_BROWSERS" -eq 0 ]; then
    echo "🌐 Installing Playwright browsers..."
    npx playwright install
    if [[ "${OSTYPE:-}" == linux* ]]; then
      echo "🐧 Installing system dependencies..."
      npx playwright install-deps chromium || true
    fi
  else
    echo "⏭️  Skipping browser installation (use later with: npx playwright install)"
  fi
else
  echo "⏭️  Skipping dependency installation per flag"
fi

echo ""
echo "✅ Frontend Testing Suite setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Update playwright.config.ts baseURL (or set BASE_URL in .env)"
echo "2. Run tests: ./frontend-tests/run-smoke.sh or $PM run test:frontend:smoke"
echo "3. Install browsers when ready: npx playwright install"
echo "4. Open the test UI: $PM run test:frontend:ui"
echo ""
echo "🎯 Happy testing!"
