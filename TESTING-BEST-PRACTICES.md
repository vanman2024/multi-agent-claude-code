# Testing Best Practices Guide

## 🎯 Overview

This guide provides comprehensive testing strategies and best practices for the Multi-Agent Development Framework. Our unified testing approach ensures code quality, reliability, and maintainability across frontend and backend components.

## 🔍 Testing Philosophy

### Core Principles
1. **Test Early, Test Often** - Write tests alongside code, not after
2. **Automated Everything** - Manual testing should be the exception
3. **Fast Feedback** - Tests should run quickly to maintain developer flow
4. **Clear Failures** - Test failures should immediately indicate what's broken
5. **Deterministic Results** - Tests must be reliable and reproducible

## 🧪 Testing Strategy

### Testing Pyramid
```
         /\          E2E Tests (10%)
        /  \         - Critical user journeys
       /    \        - Cross-browser testing
      /------\       
     /        \      Integration Tests (30%)
    /          \     - API endpoint testing
   /            \    - Component integration
  /--------------\   
 /                \  Unit Tests (60%)
/                  \ - Functions/methods
/__________________\- Component logic
```

### What to Test

#### Always Test
- ✅ Business logic and calculations
- ✅ Data transformations
- ✅ API endpoints (all methods)
- ✅ Authentication/authorization
- ✅ Error handling paths
- ✅ State management
- ✅ User interactions
- ✅ Form validations

#### Consider Testing
- ⚠️ Third-party integrations (with mocks)
- ⚠️ Performance-critical paths
- ⚠️ Complex UI interactions
- ⚠️ Database transactions

#### Don't Test
- ❌ Framework internals
- ❌ Third-party libraries
- ❌ Simple getters/setters
- ❌ Configuration files

## 📝 Writing Good Tests

### Test Structure (AAA Pattern)
```javascript
describe('UserService', () => {
  it('should create a new user with valid data', async () => {
    // Arrange - Set up test data
    const userData = {
      email: 'test@example.com',
      password: 'SecurePass123!'
    };
    
    // Act - Execute the function
    const user = await userService.create(userData);
    
    // Assert - Verify the outcome
    expect(user.email).toBe(userData.email);
    expect(user.id).toBeDefined();
  });
});
```

### Test Naming Conventions
```javascript
// ✅ Good: Descriptive and specific
it('should return 401 when authentication token is invalid')
it('should calculate total price including tax and shipping')
it('should retry failed API calls up to 3 times')

// ❌ Bad: Vague or unclear
it('test user')
it('works correctly')
it('handles errors')
```

### Test Data Management
```javascript
// Use factories for test data
const createTestUser = (overrides = {}) => ({
  id: 'test-id-123',
  email: 'test@example.com',
  role: 'user',
  ...overrides
});

// Use realistic but safe test data
const testCreditCard = '4111111111111111'; // Test Visa number
const testEmail = 'test+{timestamp}@example.com';
```

## 🎭 Mocking Best Practices

### When to Mock
- External API calls
- Database operations (in unit tests)
- Time-dependent functions
- Random number generators
- File system operations

### Mock Examples
```javascript
// Mock external API
jest.mock('../services/payment', () => ({
  processPayment: jest.fn().mockResolvedValue({
    status: 'success',
    transactionId: 'mock-txn-123'
  })
}));

// Mock date/time
const mockDate = new Date('2024-01-01');
jest.spyOn(global, 'Date').mockImplementation(() => mockDate);
```

## 🚀 Frontend Testing

### Component Testing
```javascript
// React Testing Library example
import { render, screen, fireEvent } from '@testing-library/react';

test('increments counter on button click', () => {
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  const counter = screen.getByText('0');
  
  fireEvent.click(button);
  
  expect(screen.getByText('1')).toBeInTheDocument();
});
```

### E2E Testing with Playwright
```javascript
test('user can complete checkout flow', async ({ page }) => {
  // Navigate to product page
  await page.goto('/products/widget-123');
  
  // Add to cart
  await page.click('[data-testid="add-to-cart"]');
  
  // Go to checkout
  await page.click('[data-testid="checkout-button"]');
  
  // Fill payment form
  await page.fill('#email', 'test@example.com');
  await page.fill('#card-number', '4111111111111111');
  
  // Complete purchase
  await page.click('[data-testid="complete-purchase"]');
  
  // Verify success
  await expect(page.locator('.success-message')).toBeVisible();
});
```

## 🔧 Backend Testing

### API Endpoint Testing
```javascript
// Supertest example for Express
const request = require('supertest');
const app = require('../app');

describe('POST /api/users', () => {
  it('creates a new user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'new@example.com',
        password: 'SecurePass123!'
      })
      .expect(201);
    
    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('new@example.com');
  });
  
  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid-email',
        password: 'SecurePass123!'
      })
      .expect(400);
    
    expect(response.body.error).toContain('email');
  });
});
```

### Database Testing
```javascript
// Use transactions for test isolation
describe('UserRepository', () => {
  let transaction;
  
  beforeEach(async () => {
    transaction = await db.transaction();
  });
  
  afterEach(async () => {
    await transaction.rollback();
  });
  
  it('finds user by email', async () => {
    // Create test user within transaction
    await UserModel.create({
      email: 'test@example.com'
    }, { transaction });
    
    // Test the find method
    const user = await userRepo.findByEmail(
      'test@example.com',
      { transaction }
    );
    
    expect(user).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });
});
```

## 📊 Test Coverage

### Coverage Goals
- **Overall**: >80%
- **Critical Paths**: >95%
- **New Code**: 100%
- **API Endpoints**: 100%
- **Business Logic**: >90%

### Coverage Commands
```bash
# JavaScript/TypeScript
npm test -- --coverage
npm run test:coverage

# Python
pytest --cov=src --cov-report=html
coverage run -m pytest && coverage report

# Go
go test -cover ./...
go test -coverprofile=coverage.out && go tool cover -html=coverage.out
```

## 🏃 Performance Testing

### Load Testing Example
```javascript
// Using k6
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 100 }, // Ramp up
    { duration: '1m', target: 100 },  // Stay at 100
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
  },
};

export default function () {
  const response = http.get('https://api.example.com/users');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

## 🐛 Debugging Failed Tests

### Debugging Strategies
1. **Read the error message carefully** - Often contains the solution
2. **Run single test in isolation** - `npm test -- --testNamePattern="specific test"`
3. **Add console.logs temporarily** - But remove before committing
4. **Use debugger** - `node --inspect-brk` or IDE breakpoints
5. **Check test data** - Ensure it's valid and complete
6. **Verify mocks** - Ensure they match actual behavior
7. **Check timing issues** - Add appropriate waits for async operations

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Flaky tests | Use explicit waits, avoid time-dependent logic |
| Slow tests | Mock external calls, use test database |
| False positives | Add more specific assertions |
| Test pollution | Use proper setup/teardown, isolate tests |
| Memory leaks | Clean up listeners, close connections |

## 🔄 CI/CD Integration

### Pre-commit Checks
```bash
# Run before every commit
npm test -- --onlyChanged  # Test only changed files
npm run lint               # Code quality
npm run typecheck          # Type safety
```

### CI Pipeline Tests
```yaml
# Example GitHub Actions workflow
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-node@v2
    - run: npm ci
    - run: npm run lint
    - run: npm run typecheck
    - run: npm test -- --coverage
    - run: npm run test:e2e
```

## 📚 Testing Resources

### Recommended Tools
- **Frontend**: Jest, React Testing Library, Playwright
- **Backend**: Jest/Mocha (Node.js), pytest (Python), testing package (Go)
- **API Testing**: Supertest, Postman, REST Client
- **Load Testing**: k6, JMeter, Locust
- **Mocking**: Jest mocks, Sinon, MSW (Mock Service Worker)

### Learning Resources
- [Testing Library Documentation](https://testing-library.com/)
- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)
- [pytest Documentation](https://docs.pytest.org/)

## 🎖️ Testing Checklist

Before marking any feature as complete:

- [ ] Unit tests written and passing
- [ ] Integration tests for API endpoints
- [ ] E2E tests for critical user paths
- [ ] Error scenarios tested
- [ ] Edge cases covered
- [ ] Performance validated
- [ ] Security considerations tested
- [ ] Documentation updated
- [ ] Code coverage meets standards
- [ ] Tests run in CI/CD pipeline
- [ ] No console.logs or debug code
- [ ] Test data cleaned up properly

## 🚨 Emergency Procedures

### When Tests Fail in Production
1. **Don't panic** - Check if it's a test issue or actual bug
2. **Rollback if needed** - Use feature flags or revert deployment
3. **Reproduce locally** - Isolate the issue
4. **Fix forward** - Create hotfix with tests
5. **Post-mortem** - Document what happened and prevent recurrence

### Test Environment Issues
```bash
# Reset test database
npm run db:reset:test

# Clear test cache
npm test -- --clearCache

# Run with verbose output
npm test -- --verbose

# Skip cache and run fresh
npm test -- --no-cache
```

---

*Remember: Testing is not about finding bugs, it's about building confidence in your code. Write tests that give you and your team the confidence to ship fast and sleep well.*# Test trigger
