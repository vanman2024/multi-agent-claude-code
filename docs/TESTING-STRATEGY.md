# Standardized Testing Protocol

## Overview

This document defines the **standardized testing protocol** for the Multi-Agent Development Framework. All agents must follow these standards to prevent testing chaos and ensure consistent behavior across projects.

## 🚨 CRITICAL: Standardized Testing Commands

**Claude Code (slash commands):**
```bash
/test                        # Universal testing (Claude Code only)
/deploy                      # Universal deployment (Claude Code only)
```

**All Other Agents (CLI commands):**
```bash
npm test                     # Standard testing command
npm run lint                 # Standard linting command  
npm run typecheck           # Standard type checking
npm run build               # Standard build command
npm run deploy              # Standard deployment (if available)
```

**NO AGENT may create custom testing frameworks.** All testing MUST use these standardized commands.

## Standardized Testing Protocol

### Technology Stack Detection

The `/test` command automatically detects your project type and runs appropriate commands:

**React/Next.js Projects:**
```bash
npm test                     # or jest
npm run test:unit           # unit tests only  
npm run test:e2e            # playwright tests
npm run lint                # eslint
npm run typecheck           # tsc --noEmit
```

**Python Projects:**
```bash
pytest                      # all tests
pytest tests/unit/          # unit tests only
pytest tests/integration/   # integration tests
ruff check .                # linting  
mypy .                      # type checking
```

**Node.js Backend:**
```bash
npm test                    # jest tests
npm run test:integration    # API tests
npm run lint               # eslint
npm run typecheck          # tsc --noEmit
```

### Agent Compliance Requirements

**Claude Code ONLY:**
- ✅ `/test` - Universal testing slash command
- ✅ `/deploy` - Universal deployment slash command

**ALL OTHER AGENTS must use:**
- ✅ `npm test` - Standard Node.js testing
- ✅ `pytest` - Standard Python testing
- ✅ `npm run lint` - Standard linting
- ✅ `npm run build` - Standard building
- ✅ `npm run deploy` - Standard deployment (if script exists)

**FORBIDDEN - All agents may NOT:**
- ❌ Create custom test frameworks
- ❌ Use non-standard testing commands
- ❌ Bypass the standardized protocol
- ❌ Create project-specific test scripts
- ❌ Use slash commands (only Claude Code has access)

## Why Testing is Mission-Critical

**"Without testing, applications significantly fail in production."**

Testing isn't optional - it's the foundation that:
- **Prevents catastrophic failures** that destroy user trust
- **Catches issues before they cost money** (a production bug costs 100x more to fix)
- **Enables confident deployment** (deploy on Friday without fear)
- **Documents expected behavior** (tests are living documentation)
- **Allows rapid iteration** (change code without breaking everything)

### The Real Cost of No Testing

| Scenario | Without Tests | With Tests |
|----------|--------------|------------|
| Deploy to production | Prayer and panic | Confidence |
| Refactor code | Break 10 things, find 2 | Break 0 things |
| Onboard new developer | "Don't touch that, it might break" | "Run tests to understand" |
| Customer finds bug | Emergency hotfix at 3am | Caught in CI/CD |
| Scale from 100 to 10,000 users | System collapse | Predictable performance |

## Core Testing Philosophy

### Token Optimization First
- **Default behavior**: Run existing tests without agents (~50 tokens)
- **Agent usage**: Only when explicitly requested with `--create` or `--update` flags
- **Smart routing**: Automatic detection prevents unnecessary agent invocation

### Test Organization Structure
```
__tests__/                    # ONLY valid test directory
├── components/              # UI component tests
│   ├── Button.test.tsx
│   └── UserProfile.test.tsx
├── api/                     # API endpoint tests
│   ├── auth.test.ts
│   └── users.test.ts
├── utils/                   # Utility function tests
│   └── validators.test.ts
├── hooks/                   # Custom React hook tests
│   └── useAuth.test.ts
└── e2e/                     # End-to-end tests
    └── checkout.test.ts
```

## Command Reference

### Basic Test Execution
```bash
/test                        # Auto-detect and run tests (uses --quick if tests exist)
/test --quick                # Force quick mode without agents (~50 tokens)
```

### Test Creation & Updates
```bash
/test --create               # Generate all tests using agents (~5000+ tokens)
/test --create --frontend    # Generate only frontend tests
/test --create --backend     # Generate only backend tests
/test --create --e2e         # Generate only E2E tests
/test --update               # Update existing tests (~2000+ tokens)
```

### Targeted Test Runs
```bash
/test --frontend             # Run frontend tests only
/test --backend              # Run backend tests only
/test --unit                 # Run unit tests only
/test --e2e                  # Run E2E tests only
/test --mock                 # Use mock APIs (no DB needed, 10x faster)
/test --ci                   # Trigger CI/CD pipeline
```

## Testing Stack

### Core Framework
- **Jest**: Primary test runner and assertion library
- **Configuration**: `jest.config.js` with TypeScript support via @swc/jest
- **Test Patterns**: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`

### Testing Libraries

| Library | Purpose | Usage |
|---------|---------|-------|
| @testing-library/react | Component testing | DOM queries, user interactions |
| @testing-library/jest-dom | Enhanced matchers | `.toBeInTheDocument()`, etc. |
| node-mocks-http | API testing | Mock HTTP requests/responses |
| @swc/jest | TypeScript transpilation | Fast TS compilation for tests |

## Mock Testing Strategy (Built-in)

### Automatic Mock Detection
When you run `/test --mock` or `/test --create --mock`, the agents automatically:

1. **Check for available tools**:
   - Newman/Postman (preferred)
   - MSW (Mock Service Worker)
   - JSON Server
   - Nock

2. **Use the best available option**:
   - **If Newman exists**: Create Postman collections with mock responses
   - **If MSW exists**: Set up service worker interceptors
   - **Fallback**: Create simple JSON mocks

### Why Mock Testing is Built-in

**Prevents Test Sprawl**:
- No need for complex database setup
- Tests run in milliseconds, not seconds
- No test data pollution between runs
- Deterministic results every time

**Agent Intelligence**:
```bash
/test --create --mock --backend
```
The backend-tester agent will:
1. Analyze your API endpoints
2. Generate mock responses based on TypeScript/schemas
3. Create comprehensive test suites
4. All tests run without any infrastructure

### Performance Comparison

| Test Type | Without Mocks | With Mocks | Improvement |
|-----------|--------------|------------|-------------|
| API Test Suite | 5-10s | 100-500ms | 10-100x faster |
| Database Tests | 2-5s | 50-100ms | 20-50x faster |
| Full Test Run | 30-60s | 2-5s | 10-20x faster |

## Agent-Based Test Generation

### How It Works

When you run `/test --create`, the testing agents:

1. **Analyze Your Codebase**
   - Scan components in `src/components/`
   - Identify API routes in `src/pages/api/` or `src/app/api/`
   - Find utilities in `src/utils/`
   - Detect custom hooks in `src/hooks/`
   - Examine database models/schemas

2. **Generate Appropriate Tests**
   - Match testing patterns to code patterns
   - Create comprehensive test suites
   - Include edge cases and error scenarios
   - Add proper mocking and setup

### Example: Component Test Generation

**Your Component**: `src/components/UserProfile.tsx`

**Generated Test**: `__tests__/components/UserProfile.test.tsx`
```javascript
describe('UserProfile', () => {
  it('renders user information correctly')
  it('displays placeholder for missing avatar')
  it('shows edit button for profile owner')
  it('hides edit button for other users')
  it('handles loading state')
  it('displays error message on fetch failure')
  it('triggers onEdit callback when edit clicked')
})
```

### Example: API Test Generation

**Your Endpoint**: `src/pages/api/auth/login.ts`

**Generated Test**: `__tests__/api/auth/login.test.ts`
```javascript
describe('/api/auth/login', () => {
  it('accepts valid credentials and returns JWT')
  it('rejects incorrect password')
  it('rejects non-existent user')
  it('validates email format')
  it('implements rate limiting after 5 attempts')
  it('handles database connection errors')
  it('returns appropriate error messages')
})
```

## Template vs Real Project Testing

### Template Tests (Placeholder)
The template includes minimal placeholder tests to demonstrate the testing infrastructure:
- `TestComponent.test.tsx` - Shows component testing patterns
- `health.test.ts` - Shows API testing patterns
- `integration.test.ts` - Shows integration testing patterns

### Real Project Tests (Generated)
When you clone the template for a real project:

1. **Initial Setup**
   ```bash
   # After building your features
   /test --create  # Generates tests for all your code
   ```

2. **Ongoing Development**
   ```bash
   # After adding new feature
   /test --create --backend  # If you added API endpoints
   /test --update           # If you modified existing code
   /test                    # Run all tests
   ```

## Token Usage Guidelines

### Optimization Strategy
| Command | Token Usage | When to Use |
|---------|------------|-------------|
| `/test` | ~50 | Daily testing during development |
| `/test --quick` | ~50 | Force quick mode explicitly |
| `/test --mock` | ~50 | Fast testing without database |
| `/test --create` | ~5000+ | Initial project setup only |
| `/test --create --mock` | ~3000+ | Create mock-based tests (faster) |
| `/test --update` | ~2000+ | Major refactoring only |
| `/test --ci` | ~100 | Trigger CI pipeline |

### Best Practices
1. **Use `--create` once** during initial project setup
2. **Default to `/test`** for regular test runs
3. **Use `--update` sparingly** for major changes
4. **Avoid repeated `--create`** commands

## Test Coverage Requirements

### Minimum Coverage Targets
- **Overall**: 80% code coverage
- **Critical paths**: 95% coverage (auth, payments, data operations)
- **UI Components**: 70% coverage
- **Utility functions**: 100% coverage

### Coverage Reports
```bash
/test --coverage            # Generate coverage report
npm run test:coverage       # Direct command
```

## CI/CD Integration

### Automated Testing
The CI/CD pipeline (`ci-cd-pipeline.yml`) automatically:
1. Runs all tests on PR creation
2. Blocks merge if tests fail
3. Generates coverage reports
4. Posts results to PR comments

### Manual CI Trigger
```bash
/test --ci                  # Manually trigger CI pipeline
```

## Common Testing Patterns

### Component Testing Pattern
```javascript
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'

// Test structure
describe('ComponentName', () => {
  it('renders without crashing', () => {})
  it('handles user interactions', () => {})
  it('updates state correctly', () => {})
  it('passes props properly', () => {})
})
```

### API Testing Pattern
```javascript
import { createMocks } from 'node-mocks-http'

// Test structure
describe('/api/endpoint', () => {
  it('returns correct status code', () => {})
  it('validates input data', () => {})
  it('handles errors gracefully', () => {})
  it('implements proper authentication', () => {})
})
```

### E2E Testing Pattern
```javascript
// Test structure
describe('User Flow', () => {
  it('completes full user journey', () => {})
  it('handles network failures', () => {})
  it('maintains data consistency', () => {})
  it('provides proper feedback', () => {})
})
```

## Security in Testing

### Never Expose Secrets
- Use `.env.test` for test credentials
- Mock external API calls
- Sanitize test output
- Never commit real user data

### Test Data Management
```bash
# Before running tests
cp .env.test.example .env.test
# Add test-specific credentials
```

## Troubleshooting

### Common Issues

| Issue | Solution | Command |
|-------|----------|---------|
| No tests found | Create tests | `/test --create` |
| Tests failing | Check recent changes | `git diff` |
| Module not found | Install dependencies | `npm install` |
| Port in use | Kill process | `lsof -ti:3000 \| xargs kill` |
| Out of memory | Increase heap | `NODE_OPTIONS=--max-old-space-size=4096` |

### Debug Mode
```bash
npm test -- --verbose       # Detailed test output
npm test -- --watch        # Watch mode for development
npm test -- --detectOpenHandles  # Find hanging processes
```

## Migration from Other Test Structures

If you have existing tests in other locations:

1. **Move to __tests__/**
   ```bash
   mv src/**/*.test.* __tests__/
   mv src/**/*.spec.* __tests__/
   ```

2. **Update imports**
   ```javascript
   // Old: import Component from './Component'
   // New: import Component from '../../src/components/Component'
   ```

3. **Run tests to verify**
   ```bash
   /test --quick
   ```

## Performance Monitoring

### Target Metrics
- **Detection time**: <500ms
- **Test execution**: <5s for unit tests
- **Total overhead**: <10% of runtime
- **Memory usage**: <100MB for detection

### Monitoring Commands
```bash
time npm test               # Measure execution time
npm test -- --logHeapUsage # Monitor memory usage
```

## Next Steps for Projects

1. **Clone template**
2. **Build your features**
3. **Run `/test --create`** to generate comprehensive tests
4. **Set up CI/CD** with test requirements
5. **Maintain tests** with `/test --update` when needed
6. **Run `/test`** regularly during development

---

Remember: The template provides the testing **infrastructure** - you provide the **business logic** tests through agent-based generation.