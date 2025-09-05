# Test Directory Structure

This directory contains all test files for the project. Tests are organized by type and must follow the structure below.

## Directory Structure

```
__tests__/
├── api/                    # Backend API endpoint tests
│   ├── health.test.ts     # Health check endpoint tests
│   └── users.test.ts      # User API tests
├── components/             # React component tests
│   └── Button.test.tsx    # Button component tests
├── e2e/                   # End-to-end tests
│   └── user-flow.e2e.ts   # Complete user journey tests
├── hooks/                 # React hook tests
│   └── useAuth.test.ts    # Authentication hook tests
├── pages/                 # Next.js page tests
│   └── index.test.tsx     # Homepage tests
├── utils/                 # Utility function tests
│   └── validators.test.ts # Validation utility tests
└── services/              # Service layer tests
    └── api-client.test.ts # API client service tests
```

## Naming Conventions

- **API tests**: `[endpoint-name].test.ts`
- **Component tests**: `[ComponentName].test.tsx`
- **E2E tests**: `[feature-name].e2e.test.ts`
- **Hook tests**: `[hookName].test.ts`
- **Page tests**: `[page-name].test.tsx`
- **Utility tests**: `[utility-name].test.ts`
- **Service tests**: `[service-name].test.ts`

## Important Rules

1. **ALL tests MUST be placed in this `__tests__` directory**
2. **NEVER place test files next to source files**
3. **Use the appropriate subdirectory based on test type**
4. **Follow the naming conventions strictly**
5. **Do not create additional test directories elsewhere**

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Run specific test directory
npm test -- __tests__/api

# Run specific test file
npm test -- __tests__/api/health.test.ts
```

## Test Creation

When creating new tests:
1. Identify the type of test (API, component, E2E, etc.)
2. Place it in the corresponding subdirectory
3. Follow the naming convention for that type
4. Import the source file using relative paths from this location

Example:
```typescript
// In __tests__/components/Button.test.tsx
import { Button } from '../../src/components/Button';
```

## Coverage Reports

Coverage reports are generated in the `coverage/` directory at the root of the project.