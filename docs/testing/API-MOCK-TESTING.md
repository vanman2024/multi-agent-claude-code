# API Mock Testing Strategy

## Overview

Test APIs without requiring real databases, external services, or complex infrastructure setup. This approach uses mock responses and contract testing to validate API behavior.

## Why Mock Testing?

### Traditional Testing Problems
- **Database dependency**: Need to setup/teardown test DB
- **Data pollution**: Tests can contaminate each other
- **Slow execution**: Database operations are slow
- **External dependencies**: Can't test offline
- **Flaky tests**: Network/timing issues

### Mock Testing Solutions
- **No infrastructure**: Just JavaScript objects
- **Isolated tests**: Each test gets fresh data
- **Fast execution**: Milliseconds per test
- **Offline capable**: No network required
- **Deterministic**: Same result every time

## Implementation Options

### Option 1: MSW (Mock Service Worker)

**Installation**:
```bash
npm install --save-dev msw
```

**Setup** (`__tests__/mocks/server.ts`):
```typescript
import { setupServer } from 'msw/node'
import { rest } from 'msw'

export const server = setupServer(
  // Mock user endpoints
  rest.get('/api/users', (req, res, ctx) => {
    return res(ctx.json({
      users: [
        { id: 1, name: 'Alice', email: 'alice@example.com' },
        { id: 2, name: 'Bob', email: 'bob@example.com' }
      ]
    }))
  }),
  
  rest.post('/api/users', (req, res, ctx) => {
    const { name, email } = req.body as any
    return res(ctx.json({
      id: 3,
      name,
      email,
      createdAt: new Date().toISOString()
    }))
  }),
  
  // Mock authentication
  rest.post('/api/auth/login', (req, res, ctx) => {
    const { email, password } = req.body as any
    
    if (email === 'test@example.com' && password === 'password') {
      return res(ctx.json({
        token: 'mock-jwt-token',
        user: { id: 1, email }
      }))
    }
    
    return res(
      ctx.status(401),
      ctx.json({ error: 'Invalid credentials' })
    )
  })
)

// Enable request interception
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

**Test Example**:
```typescript
describe('User API', () => {
  it('fetches users successfully', async () => {
    const response = await fetch('/api/users')
    const data = await response.json()
    
    expect(data.users).toHaveLength(2)
    expect(data.users[0].name).toBe('Alice')
  })
  
  it('handles authentication failure', async () => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: 'wrong@example.com',
        password: 'wrong'
      })
    })
    
    expect(response.status).toBe(401)
    const error = await response.json()
    expect(error.error).toBe('Invalid credentials')
  })
})
```

### Option 2: JSON Server for Development

**Setup** (`db.json`):
```json
{
  "users": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ],
  "posts": [
    { "id": 1, "userId": 1, "title": "First Post" }
  ]
}
```

**Run mock server**:
```bash
npx json-server --watch db.json --port 3001
```

### Option 3: Postman/Newman Contract Testing

**Collection** (`postman-collection.json`):
```json
{
  "info": {
    "name": "API Tests"
  },
  "item": [
    {
      "name": "Get Users",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/users"
      },
      "test": [
        "pm.test('Status is 200', () => {",
        "  pm.response.to.have.status(200);",
        "});",
        "pm.test('Returns array', () => {",
        "  const users = pm.response.json().users;",
        "  pm.expect(users).to.be.an('array');",
        "});"
      ]
    }
  ]
}
```

**Run tests**:
```bash
newman run postman-collection.json \
  --environment test-env.json \
  --reporters cli,json
```

### Option 4: Fixture-Based Testing

**Fixtures** (`__tests__/fixtures/users.ts`):
```typescript
export const mockUsers = {
  valid: [
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' }
  ],
  invalid: {
    missingEmail: { id: 3, name: 'Charlie' },
    invalidEmail: { id: 4, name: 'Dave', email: 'not-an-email' }
  }
}

export const mockApiResponses = {
  success: {
    status: 200,
    data: { users: mockUsers.valid }
  },
  notFound: {
    status: 404,
    data: { error: 'User not found' }
  },
  serverError: {
    status: 500,
    data: { error: 'Internal server error' }
  }
}
```

## Integration with Our Testing Framework

### Add to `/test` Command

```bash
/test --mock           # Run tests with mock APIs
/test --mock --create  # Generate mock-based tests
```

### Mock Test Generation

When agents create tests with `--mock` flag:

1. **Analyze API endpoints**
2. **Generate mock responses** based on:
   - TypeScript interfaces
   - OpenAPI/Swagger specs
   - Existing API responses
3. **Create comprehensive tests** for:
   - Success scenarios
   - Error handling
   - Edge cases
   - Rate limiting
   - Authentication

### Example Generated Mock Test

```typescript
// __tests__/api/orders.mock.test.ts
import { server } from '../mocks/server'
import { rest } from 'msw'

describe('Orders API (Mocked)', () => {
  it('creates order with valid data', async () => {
    const orderData = {
      userId: 1,
      items: [{ productId: 1, quantity: 2 }],
      total: 29.99
    }
    
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    })
    
    expect(response.status).toBe(201)
    const order = await response.json()
    expect(order).toMatchObject({
      id: expect.any(Number),
      ...orderData,
      status: 'pending',
      createdAt: expect.any(String)
    })
  })
  
  it('validates required fields', async () => {
    const invalidOrder = { userId: 1 } // Missing items
    
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(invalidOrder)
    })
    
    expect(response.status).toBe(400)
    const error = await response.json()
    expect(error.error).toContain('items required')
  })
  
  it('handles inventory shortage', async () => {
    server.use(
      rest.post('/api/orders', (req, res, ctx) => {
        return res(
          ctx.status(409),
          ctx.json({ error: 'Insufficient inventory' })
        )
      })
    )
    
    const response = await fetch('/api/orders', {
      method: 'POST',
      body: JSON.stringify({ /* order data */ })
    })
    
    expect(response.status).toBe(409)
  })
})
```

## Best Practices

### 1. Separate Mock and Integration Tests
```
__tests__/
├── mocks/           # Mock tests (fast, isolated)
│   └── api/
└── integration/     # Real API tests (slower, comprehensive)
    └── api/
```

### 2. Use Mock Tests For
- **Rapid development**: Test while building
- **CI/CD pipelines**: Fast feedback
- **Edge cases**: Error scenarios
- **External APIs**: Third-party services

### 3. Use Integration Tests For
- **Final validation**: Before deployment
- **Data flow**: End-to-end scenarios
- **Performance**: Real database queries
- **Security**: Authentication flows

### 4. Mock Data Management
```typescript
// Centralized mock data
const mockDatabase = {
  users: new Map(),
  posts: new Map(),
  
  reset() {
    this.users.clear()
    this.posts.clear()
    this.seed()
  },
  
  seed() {
    this.users.set(1, { id: 1, name: 'Test User' })
  }
}

// Use in tests
beforeEach(() => mockDatabase.reset())
```

## Performance Comparison

| Test Type | Setup Time | Execution | Teardown | Total |
|-----------|------------|-----------|----------|-------|
| Mock API | 0ms | 5ms | 0ms | 5ms |
| In-Memory DB | 50ms | 20ms | 30ms | 100ms |
| Test DB | 500ms | 100ms | 400ms | 1000ms |
| Real DB | 2000ms | 200ms | 1000ms | 3200ms |

## Migration Strategy

### Phase 1: Add Mock Layer
1. Install MSW or similar
2. Create mock handlers for existing APIs
3. Run existing tests against mocks

### Phase 2: Parallel Testing
1. Keep integration tests
2. Add mock tests for rapid development
3. Run both in CI/CD

### Phase 3: Optimize
1. Move slow tests to mock layer
2. Keep critical paths in integration
3. Balance speed vs confidence

## Troubleshooting

### Common Issues

**Issue**: Mocks don't match reality
**Solution**: Generate mocks from OpenAPI spec or actual responses

**Issue**: Tests pass but production fails
**Solution**: Run integration tests before deployment

**Issue**: Mock data gets complex
**Solution**: Use factories or builders pattern

**Issue**: External API changes
**Solution**: Version your mocks, update regularly

## Tools & Libraries

### Recommended Stack
- **MSW**: Best for React/Next.js apps
- **Nock**: Good for Node.js backends
- **Mirage JS**: Full fake backend
- **JSON Server**: Quick REST API
- **Postman/Newman**: Contract testing

### Installation Commands
```bash
# MSW
npm install --save-dev msw

# Nock
npm install --save-dev nock

# JSON Server
npm install --save-dev json-server

# Newman (Postman CLI)
npm install --save-dev newman
```

## Conclusion

Mock testing provides:
- **Speed**: 10-100x faster than database tests
- **Reliability**: No flaky network issues
- **Isolation**: Tests don't affect each other
- **Portability**: Run anywhere, anytime
- **Control**: Test any scenario easily

Combine with integration tests for comprehensive coverage while maintaining fast feedback loops during development.