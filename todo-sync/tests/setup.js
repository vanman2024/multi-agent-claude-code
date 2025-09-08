// Jest setup file
import { jest } from '@jest/globals';

// Mock console methods to reduce noise during tests
const originalError = console.error;
const originalWarn = console.warn;
const originalLog = console.log;

beforeAll(() => {
    // Mock console methods but allow important test output
    console.error = jest.fn((message, ...args) => {
        if (message.includes('ENOENT') || message.includes('Test error')) {
            // Silent for expected errors
            return;
        }
        originalError(message, ...args);
    });
    
    console.warn = jest.fn((message, ...args) => {
        if (message.includes('Rate limit') || message.includes('Mock')) {
            return;
        }
        originalWarn(message, ...args);
    });
    
    console.log = jest.fn((message, ...args) => {
        if (typeof message === 'string' && message.includes('Test')) {
            return;
        }
        originalLog(message, ...args);
    });
});

afterAll(() => {
    // Restore original console methods
    console.error = originalError;
    console.warn = originalWarn;
    console.log = originalLog;
});

// Global test helpers
global.testUtils = {
    createMockTodo: (overrides = {}) => ({
        id: 1,
        content: 'Test todo',
        status: 'pending',
        activeForm: 'Testing todo functionality',
        sessionId: 'test-session-123',
        projectPath: '/test/project',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        ...overrides
    }),
    
    createMockGitHubIssue: (overrides = {}) => ({
        number: 123,
        id: 456,
        title: 'Test issue',
        body: 'Test description',
        state: 'open',
        labels: [{ name: 'todo-sync' }],
        assignees: [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ...overrides
    }),
    
    delay: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
    
    expectEventuallyResolved: async (promise, timeout = 5000) => {
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error(`Promise did not resolve within ${timeout}ms`)), timeout)
        );
        
        return Promise.race([promise, timeoutPromise]);
    }
};

// Mock environment variables for tests
process.env.NODE_ENV = 'test';
process.env.DB_PATH = './test-data/test.db';
process.env.LOG_LEVEL = 'error';
process.env.SYNC_INTERVAL_MS = '1000';
process.env.RATE_LIMIT_PER_HOUR = '1000';
process.env.BATCH_SIZE = '10';