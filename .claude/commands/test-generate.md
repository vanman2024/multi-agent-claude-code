---
allowed-tools: Read(*), Write(*), Glob(*), Bash(*), Task(*)
description: Generate comprehensive test suites by analyzing entire project (run AFTER setup)
argument-hint: [--unit | --integration | --e2e | --all] [--domain domain-type]
---

# Generate Test Suites

<!--
WHEN TO USE THIS COMMAND:
- After project structure is set up (frontend/, backend/, docs/)
- After /project-setup and /plan:generate are complete
- When you need comprehensive test coverage (90% from day 1)
- To generate Postman collections for API testing
- Before starting development (tests ready upfront)

WHEN NOT TO USE:
- Before project documentation exists
- If comprehensive tests already exist
- For adding single test (use /test --create instead)

FLAGS:
--all           : Generate all test types (default)
--unit          : Only unit tests
--integration   : Only API tests (Postman collections)
--api           : Same as --integration
--e2e           : Only end-to-end tests
--domain [type] : Domain-specific tests (e-commerce, saas, etc.)

WORKFLOW:
1. /project-setup        # Create foundation docs
2. /plan:generate        # Create vision document  
3. /test:generate --all  # Generate comprehensive tests
4. npm test             # Run generated tests
5. /test --create       # Add specific tests as needed

TESTING APPROACH:
- Uses Newman/Postman for API testing (no database needed)
- Mock-first with MSW for frontend
- Fixtures instead of real data
- Contract testing over integration testing
-->

## 📋 Prerequisites
**This command should be run AFTER:**
1. `/project-setup` - Project requirements gathered
2. `/plan:generate` - Project plan created
3. Basic project structure exists (frontend/, backend/, docs/)
4. Core infrastructure is configured

**Why?** This command analyzes your ENTIRE project to generate relevant tests.

## Context
- Current directory: !`pwd`
- Project docs: !`ls -la docs/*.md 2>/dev/null | grep -E "PLAN|FEATURES|ARCHITECTURE"`
- Existing tests: !`find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l`

## Your Task

When user runs `/test:generate $ARGUMENTS`:

First, check for spec-kit integration:
!`./scripts/integrate-test-with-speckit.sh`

Then analyze the ENTIRE project and create comprehensive test suites.

### Step 1: Deep Project Analysis

**This command runs AFTER project setup is complete.** It analyzes everything:

```bash
# 1. Check all documentation
echo "📚 Analyzing project documentation..."
if [ -f "docs/PROJECT_PLAN.md" ]; then
  echo "✅ Found PROJECT_PLAN.md - extracting features and roadmap"
fi
if [ -f "docs/FEATURES.md" ]; then
  echo "✅ Found FEATURES.md - extracting user journeys and workflows"
fi
if [ -f "docs/ARCHITECTURE.md" ]; then
  echo "✅ Found ARCHITECTURE.md - extracting API design and structure"
fi
if [ -f "docs/INFRASTRUCTURE.md" ]; then
  echo "✅ Found INFRASTRUCTURE.md - extracting services and deployment"
fi
if [ -f "docs/DESIGN_SYSTEM.md" ]; then
  echo "✅ Found DESIGN_SYSTEM.md - extracting UI components"
fi

# 2. Analyze existing code structure
echo "🔍 Analyzing code structure..."
ls -la frontend/src 2>/dev/null && echo "✅ Found frontend code"
ls -la backend/app 2>/dev/null && echo "✅ Found backend code"
ls -la database/migrations 2>/dev/null && echo "✅ Found database schemas"

# 3. Check package files for tech stack
echo "📦 Detecting tech stack..."
[ -f "package.json" ] && echo "✅ Found package.json - analyzing dependencies"
[ -f "requirements.txt" ] && echo "✅ Found requirements.txt - Python project"
[ -f "pyproject.toml" ] && echo "✅ Found pyproject.toml - Modern Python"

# 4. Check for existing tests to avoid duplication
echo "🧪 Checking existing tests..."
find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | wc -l
```

Extract comprehensive context:
- **Tech stack**: From package.json, requirements.txt, actual code
- **Project structure**: From directory layout and file organization
- **Features**: From FEATURES.md and PROJECT_PLAN.md
- **API design**: From ARCHITECTURE.md and actual route files
- **Database schema**: From migrations and models
- **UI components**: From frontend/src/components
- **Business logic**: From backend services and utilities
- **User workflows**: From FEATURES.md user journeys
- **External services**: From INFRASTRUCTURE.md and .env.example

### Step 2: Determine Test Framework & Strategy

Based on tech stack and your testing infrastructure:

#### API Testing (Primary Focus):
- **Newman/Postman MCP** → API contract testing (PREFERRED)
- **No database setup needed** → Use mock responses
- **Fast execution** → No infrastructure dependencies
- **Contract-first** → Define API contracts in Postman collections

#### Frontend Testing:
- **Next.js/React** → Jest + React Testing Library + MSW for mocks
- **Playwright** → E2E testing with mocked backends

#### Backend Testing:
- **FastAPI** → Pytest with fixture-based mocking
- **Express** → Jest with Newman for API testing
- **NO direct database testing** → Always use mocks/fixtures

### Step 3: Generate Test Categories

#### If `--all` or no flags (default):
Generate all three categories

#### If `--unit`:
Generate unit tests for:
- Business logic functions
- Data validators
- Utility functions
- Service methods
- Component rendering (frontend)

#### If `--integration` or `--api`:
Generate API contract tests using Postman/Newman:

1. **Create Postman Collection** (`postman-collection.json`):
   - Define all API endpoints from ARCHITECTURE.md
   - Add request examples with mock data
   - Include pre-request scripts for setup
   - Add test scripts for validation
   - Set up environment variables

2. **Create Newman Test Scripts**:
   ```json
   // postman-collection.json
   {
     "info": { "name": "API Contract Tests" },
     "item": [/* Generated endpoint tests */],
     "variable": [/* Environment configs */]
   }
   ```

3. **NO Database Operations**:
   - Use mock responses defined in collection
   - Test API contracts, not database state
   - Validate response shapes and status codes

#### If `--e2e`:
Generate end-to-end tests for:
- Critical user journeys
- Multi-step workflows
- Cross-browser scenarios
- Mobile responsiveness

### Step 4: Generate Domain-Specific Tests

Based on business domain detected or specified:

#### E-commerce Domain:
```javascript
// __tests__/unit/cart.test.js
describe('Shopping Cart', () => {
  test('calculates total with tax correctly')
  test('applies discount codes')
  test('handles inventory limits')
  test('validates payment methods')
  test('calculates shipping costs')
})

// __tests__/integration/checkout.test.js
describe('Checkout API', () => {
  test('POST /api/checkout validates cart items')
  test('POST /api/checkout processes payment')
  test('POST /api/checkout sends confirmation email')
})

// __tests__/e2e/purchase-flow.test.js
describe('Customer Purchase Journey', () => {
  test('Browse → Add to Cart → Checkout → Confirmation')
  test('Apply coupon during checkout')
  test('Handle out-of-stock during checkout')
})
```

#### SaaS/B2B Domain:
```javascript
// __tests__/unit/subscription.test.js
describe('Subscription Management', () => {
  test('calculates prorated billing')
  test('handles plan upgrades/downgrades')
  test('enforces usage limits')
  test('manages team seats')
})

// __tests__/integration/team.test.js
describe('Team API', () => {
  test('POST /api/team/invite sends invitations')
  test('PUT /api/team/member updates permissions')
  test('DELETE /api/team/member revokes access')
})

// __tests__/e2e/onboarding-flow.test.js
describe('Team Onboarding', () => {
  test('Sign up → Create team → Invite members → Setup')
  test('SSO authentication flow')
  test('Permission management workflow')
})
```

#### Skilled Trades Domain:
```javascript
// __tests__/unit/certification.test.js
describe('Certification Validation', () => {
  test('validates Red Seal certification format')
  test('checks certification expiry dates')
  test('verifies apprenticeship hours')
  test('calculates skill match scores')
})

// __tests__/integration/trades-api.test.js
describe('Trades Directory API', () => {
  test('GET /api/trades filters by location')
  test('GET /api/trades/match returns ranked results')
  test('POST /api/certification/verify validates documents')
})

// __tests__/e2e/job-matching.test.js
describe('Job Matching Flow', () => {
  test('Create profile → Add skills → Get matched → Apply')
  test('Employer posts job → Reviews candidates → Contacts')
  test('Apprentice finds program → Applies → Gets accepted')
})
```

### Step 5: Create Test Structure

Generate appropriate directory structure:

```bash
# Create test directories
mkdir -p __tests__/{unit,integration,e2e}
mkdir -p tests/{fixtures,mocks,helpers}

# For Next.js projects
mkdir -p __tests__/components
mkdir -p __tests__/pages
mkdir -p __tests__/api

# For FastAPI projects  
mkdir -p tests/{unit,integration,e2e}
mkdir -p tests/conftest
```

### Step 6: Generate Test Files

For each category, create actual test files:

#### API Testing with Newman/Postman (PRIMARY APPROACH):
```json
// postman-collection.json
{
  "info": {
    "name": "{{PROJECT_NAME}} API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "User Login",
          "request": {
            "method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"test@example.com\", \"password\": \"testpass123\"}"
            },
            "url": "{{baseUrl}}/api/auth/login"
          },
          "response": [],
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status code is 200', () => {",
                  "    pm.response.to.have.status(200);",
                  "});",
                  "pm.test('Response has token', () => {",
                  "    const jsonData = pm.response.json();",
                  "    pm.expect(jsonData).to.have.property('token');",
                  "});",
                  "pm.test('Response time is less than 500ms', () => {",
                  "    pm.expect(pm.response.responseTime).to.be.below(500);",
                  "});"
                ]
              }
            }
          ]
        }
      ]
    },
    {
      "name": "User Management",
      "item": [
        {
          "name": "Get User Profile",
          "request": {
            "method": "GET",
            "header": [{"key": "Authorization", "value": "Bearer {{token}}"}],
            "url": "{{baseUrl}}/api/users/profile"
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Returns user data', () => {",
                  "    const user = pm.response.json();",
                  "    pm.expect(user).to.have.property('id');",
                  "    pm.expect(user).to.have.property('email');",
                  "});",
                  "pm.test('No sensitive data exposed', () => {",
                  "    const user = pm.response.json();",
                  "    pm.expect(user).to.not.have.property('password');",
                  "});"
                ]
              }
            }
          ]
        }
      ]
    }
  ],
  "variable": [
    {"key": "baseUrl", "value": "http://localhost:8891", "type": "string"},
    {"key": "token", "value": "", "type": "string"}
  ]
}
```

#### Newman Test Runner Script:
```bash
#!/bin/bash
# run-api-tests.sh

# Run tests with Newman
newman run postman-collection.json \
  --environment test-env.json \
  --reporters cli,json,html \
  --reporter-json-export results.json \
  --reporter-html-export results.html

# Check if MCP Postman server is available for advanced testing
if command -v mcp__postman &> /dev/null; then
  echo "Using MCP Postman server for enhanced testing..."
  # MCP server provides additional capabilities
fi
```

#### Example Unit Test Generation:
```javascript
// __tests__/unit/auth.test.js
import { hashPassword, verifyPassword, generateToken } from '@/lib/auth'

describe('Authentication Utilities', () => {
  describe('hashPassword', () => {
    test('hashes password with bcrypt', async () => {
      const password = 'TestPass123!'
      const hash = await hashPassword(password)
      expect(hash).not.toBe(password)
      expect(hash).toMatch(/^\$2[aby]\$/)
    })

    test('generates unique hash for same password', async () => {
      const password = 'TestPass123!'
      const hash1 = await hashPassword(password)
      const hash2 = await hashPassword(password)
      expect(hash1).not.toBe(hash2)
    })
  })

  describe('verifyPassword', () => {
    test('verifies correct password', async () => {
      const password = 'TestPass123!'
      const hash = await hashPassword(password)
      const isValid = await verifyPassword(password, hash)
      expect(isValid).toBe(true)
    })

    test('rejects incorrect password', async () => {
      const password = 'TestPass123!'
      const hash = await hashPassword(password)
      const isValid = await verifyPassword('WrongPass', hash)
      expect(isValid).toBe(false)
    })
  })
})
```

### Step 7: Generate Test Helpers

Create common test utilities:

```javascript
// tests/helpers/test-utils.js
export const createMockUser = (overrides = {}) => ({
  id: 'test-user-123',
  email: 'test@example.com',
  name: 'Test User',
  role: 'user',
  ...overrides
})

export const createMockProduct = (overrides = {}) => ({
  id: 'prod-123',
  name: 'Test Product',
  price: 99.99,
  stock: 10,
  ...overrides
})

// tests/helpers/api-helper.js
export const apiClient = {
  get: (url) => fetch(`http://localhost:8891${url}`),
  post: (url, data) => fetch(`http://localhost:8891${url}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}
```

### Step 8: Generate Test Configuration

Create or update test configuration files:

#### For Jest (package.json):
```json
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest __tests__/unit",
    "test:integration": "jest __tests__/integration",
    "test:e2e": "playwright test",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch"
  }
}
```

#### For Pytest (pyproject.toml):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests"
]
```

### Step 9: Output Summary

After generation, provide summary:

```
✅ Generated comprehensive test suites:

📁 Test Structure Created:
__tests__/
├── unit/           (25 test files, 150+ test cases)
├── integration/    (15 test files, 80+ test cases)
├── e2e/           (8 test files, 30+ scenarios)
└── helpers/       (Common utilities and mocks)

🧪 Test Coverage:
- Unit Tests: All business logic and utilities
- Integration Tests: All API endpoints
- E2E Tests: Critical user journeys

📊 By Feature:
- Authentication: 15 tests
- [Feature 1]: 20 tests
- [Feature 2]: 18 tests
- [Feature 3]: 12 tests

🚀 Next Steps:
1. Run 'npm test' to execute all tests
2. Run '/test --quick' for fast feedback
3. Run '/test --create' to add specific tests
4. Tests will run automatically on git push

Generated tests provide ~90% coverage from day 1.
Add remaining 10% as you build with '/test --create'.
```

## Important Guidelines

### Test Quality Principles:
- **Isolated**: Each test should be independent
- **Repeatable**: Same result every time
- **Fast**: Unit tests < 50ms, Integration < 500ms
- **Clear**: Test names describe what and why
- **Comprehensive**: Cover happy path and edge cases

### Domain Awareness:
- Healthcare → HIPAA compliance tests
- Fintech → Security and precision tests
- E-commerce → Payment and inventory tests
- B2B → Multi-tenancy and permissions tests

### Framework Consistency:
- Match existing test patterns if found
- Use same assertion style throughout
- Follow project naming conventions
- Respect existing test structure

## Integration with Existing Commands

This command generates the test foundation, then:
- `/test --quick` runs the generated tests
- `/test --create` adds new tests as needed
- `/test --ci` triggers full test suite in CI/CD

## Usage Examples

```bash
# Generate all tests after project setup
/test:generate --all

# Generate only unit tests
/test:generate --unit

# Generate with specific domain knowledge
/test:generate --all --domain e-commerce

# Generate E2E tests only
/test:generate --e2e
```