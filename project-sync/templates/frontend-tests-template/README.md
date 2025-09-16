# Frontend Testing Suite Template

A universal, battle-tested frontend testing suite built with Playwright for solo founders and development teams working across multiple full-stack projects.

## 🎯 Why This Template?

- **Framework Agnostic**: Works with React, Vue, Angular, Svelte, or vanilla JavaScript
- **Cross-Platform**: Tests across Chrome, Firefox, Safari, Edge, and mobile browsers
- **Multi-Layer Testing**: E2E, API, Visual, and Accessibility testing in one suite
- **Agent-Friendly**: Designed for collaboration with AI agents and human developers
- **CI/CD Ready**: Pre-configured for GitHub Actions and other CI platforms
- **Solo Founder Optimized**: Simple setup, clear documentation, easy maintenance

## 🚀 Quick Start

### 1. Scaffold into a project (solo/agent friendly)

```bash
# From your project root (with package.json)
./frontend-testing-suite-template/setup-testing.sh --yes --skip-install

# Install deps when ready (choose your PM)
npm i -D @playwright/test @types/node eslint typescript \
  @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier \
  axe-playwright playwright-visual-regression

# Install browsers (Chromium first for speed/stability)
npx playwright install chromium
# On Linux/WSL: system libs for Chromium
npx playwright install-deps chromium

# Run fast smoke tests
./tests/run-smoke.sh
# Or via npm: npm run test:smoke
```

### 2. Configure for Your Project

Edit `playwright.config.ts`:
```typescript
export default defineConfig({
  // Update baseURL for your development server
  use: {
    baseURL: 'http://localhost:3000', // Change this to your dev server
  },

  // Update webServer command for your framework
  webServer: process.env.SKIP_WEBSERVER ? undefined : {
    command: 'npm run dev', // Change to your dev command
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 📁 Project Structure

```
frontend-testing-suite-template/
├── package.json                 # Dependencies and scripts
├── playwright.config.ts         # Playwright configuration
├── tests/
│   ├── global-setup.ts          # Global test setup
│   ├── global-teardown.ts       # Global test cleanup
│   ├── utils/
│   │   └── test-utils.ts        # Shared utilities and page objects
│   ├── e2e/                     # End-to-end tests
│   ├── api/                     # API tests
│   ├── visual/                  # Visual regression tests
│   └── accessibility/           # Accessibility tests
└── README.md                    # This file
```

## 🧪 Test Types

### E2E Tests (`tests/e2e/`)
User journey tests that simulate real user interactions.

```typescript
import { test, expect } from '@playwright/test';
import { BasePage } from '../utils/test-utils';

test('user can sign up and log in', async ({ page }) => {
  const homePage = new BasePage(page);

  await homePage.goto('/');
  await homePage.clickSafely('[data-testid="signup-button"]');
  // ... test implementation
});
```

### API Tests (`tests/api/`)
Backend API testing without UI.

```typescript
import { test, expect } from '@playwright/test';
import { ApiUtils } from '../utils/test-utils';

test('GET /api/users returns user list', async () => {
  const response = await ApiUtils.get('/api/users');
  expect(response.status).toBe(200);

  const users = await response.json();
  expect(Array.isArray(users)).toBe(true);
});
```

### Visual Tests (`tests/visual/`)
Screenshot comparison for UI consistency.

```typescript
import { test, expect } from '@playwright/test';

test('homepage looks correct', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

### Accessibility Tests (`tests/accessibility/`)
WCAG compliance and accessibility checks.

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage is accessible', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## 🛠️ Available Commands

```bash
# Run all tests
npm test

# Run tests in headed mode (see browser)
npm run test:headed

# Debug tests
npm run test:debug

# Open test UI
npm run test:ui

# Run specific test types
npm run test:e2e        # E2E tests only
npm run test:api        # API tests only
npm run test:visual     # Visual tests only
npm run test:accessibility  # Accessibility tests only

# Run tagged tests
npm run test:smoke      # Tests tagged with @smoke
npm run test:regression # Tests tagged with @regression

# Code quality
npm run lint           # Lint code
npm run lint:fix       # Fix linting issues
npm run type-check     # TypeScript type checking

# Setup
npm run setup          # Install browsers and dependencies
npm run install:browsers    # Install Playwright browsers
npm run install:deps        # Install system dependencies

# CI/CD
npm run ci             # Full CI pipeline (lint + type-check + test)
npm run test:parallel  # Run tests in parallel
npm run test:shard     # Run tests in shards (for CI distribution)

# Utilities
npm run codegen        # Generate tests from user interactions
npm run report         # View test reports

# Local smoke runner (script)
./tests/run-smoke.sh [--headed] [--debug]
```

## ⚙️ Configuration

### Environment Variables

```bash
# Base URL for tests
BASE_URL=http://localhost:3000

# Skip web server startup (for CI or when dev server is already running)
SKIP_WEBSERVER=true

# Enable other browsers beyond Chromium
ALL_BROWSERS=1

# Disable Chromium sandbox (CI/WSL friendly)
PW_NO_SANDBOX=1

# Browser installation
INSTALL_BROWSERS=true

# Test data setup/cleanup
SETUP_TEST_DB=true
SETUP_TEST_DATA=true
CLEANUP_TEST_DB=true
CLEANUP_TEST_DATA=true
CLEANUP_TEMP_FILES=true
```

### Custom Configuration

Create `tests/config/custom.config.ts`:

```typescript
export const customConfig = {
  // Your custom test configuration
  apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:3001',
  testUser: {
    email: 'test@example.com',
    password: 'password123'
  },
  timeouts: {
    pageLoad: 30000,
    apiCall: 10000,
  }
};
```

## 🤖 Agent Collaboration

This template is designed for seamless collaboration between AI agents and human developers:

### For AI Agents:
- Clear, consistent code patterns
- Comprehensive type definitions
- Extensive documentation
- Modular, reusable components

### For Human Developers:
- Simple setup and maintenance
- Clear naming conventions
- Comprehensive test coverage
- Easy debugging and extension

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Frontend Tests
on: [push, pull_request]

jobs:
  test-chromium:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install deps
        run: npm ci
      - name: Setup Playwright (cached)
        uses: microsoft/playwright-github-action@v1
        with:
          browsers: 'chromium'
      - name: Run smoke tests (Chromium)
        env:
          BASE_URL: http://localhost:3000
          SKIP_WEBSERVER: true
          PW_NO_SANDBOX: '1'
        run: ./tests/run-smoke.sh

  # Optional nightly full matrix
  nightly-all-browsers:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - uses: microsoft/playwright-github-action@v1
        with:
          browsers: 'all'
      - name: Run full suite
        env:
          BASE_URL: http://localhost:3000
          ALL_BROWSERS: '1'
          SKIP_WEBSERVER: true
        run: npm test
```

## 📊 Test Reporting

### HTML Reports
```bash
npm run report  # Opens HTML test report in browser
```

### JSON Reports
Test results are automatically saved to `test-results.json` for CI integration.

### JUnit Reports
XML reports available at `test-results.xml` for CI tools like Jenkins.

## 🎨 Extending the Template

### Adding New Page Objects

```typescript
// tests/utils/pages/LoginPage.ts
import { BasePage } from '../test-utils';

export class LoginPage extends BasePage {
  async login(email: string, password: string) {
    await this.fillSafely('[data-testid="email"]', email);
    await this.fillSafely('[data-testid="password"]', password);
    await this.clickSafely('[data-testid="login-button"]');
  }
}
```

### Adding Custom Test Utilities

```typescript
// tests/utils/custom-utils.ts
import { TestUtils } from './test-utils';

export class CustomUtils extends TestUtils {
  static randomUser() {
    return {
      name: this.randomString(10),
      email: this.randomEmail(),
      age: this.randomNumber(18, 65)
    };
  }
}
```

## 🚨 Best Practices

### Test Organization
- Group related tests in describe blocks
- Use clear, descriptive test names
- Tag tests appropriately (`@smoke`, `@regression`, etc.)

### Page Objects
- Create one page object per page/component
- Keep selectors in constants at the top
- Use data-testid attributes for reliable selection

### Test Data
- Use factories for test data creation
- Clean up after tests
- Avoid dependencies between tests

### Performance
- Use `test.describe.parallel` for independent test groups
- Keep tests focused and fast
- Use retries sparingly

## 🐛 Troubleshooting

### Common Issues

**Tests failing intermittently?**
- Add proper waits using `waitForVisible()`
- Use `TestUtils.retry()` for flaky operations
- Check for race conditions

**Chromium fails to launch (CI/WSL/Linux)?**
```bash
# Install Chromium only (faster)
npx playwright install chromium

# Install required system libraries
npx playwright install-deps chromium

# Disable sandbox (common in CI/WSL)
PW_NO_SANDBOX=1 ./tests/run-smoke.sh

# Still failing? Check missing libs from the error and install via apt/yum.
```

**TypeScript errors?**
```bash
npm run type-check
npm run lint:fix
```

**Tests too slow?**
- Use `test.describe.parallel`
- Reduce browser count in config
- Use `test.skip()` for slow tests in development

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/)
- [Testing Best Practices](https://playwright.dev/docs/best-practices)
- [Visual Testing Guide](https://playwright.dev/docs/test-screenshots)
- [Accessibility Testing](https://playwright.dev/docs/accessibility-testing)

## 🤝 Contributing

When adding new tests or utilities:

1. Follow the existing patterns
2. Add TypeScript types
3. Include JSDoc comments
4. Update this README if needed
5. Test across all browsers

---

**Happy Testing!** 🎭

*Built for solo founders and development teams who value quality, reliability, and maintainability.*
