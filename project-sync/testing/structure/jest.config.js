/**
 * Jest configuration for PROJECT_NAME
 * 
 * This configuration provides standardized testing setup
 * for Node.js/TypeScript projects.
 */

module.exports = {
  // Test environment
  testEnvironment: 'node',
  
  // Test file patterns
  testMatch: [
    '**/tests/**/*.test.{js,ts}',
    '**/tests/**/*.spec.{js,ts}'
  ],
  
  // Setup files
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  
  // Module resolution
  moduleFileExtensions: ['js', 'ts', 'json'],
  
  // Transform files
  transform: {
    '^.+\\.ts$': 'ts-jest',
    '^.+\\.js$': 'babel-jest'
  },
  
  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{js,ts}',
    '!src/**/*.spec.{js,ts}'
  ],
  
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  
  // Test timeout
  testTimeout: 30000,
  
  // Custom test categories using projects
  projects: [
    {
      displayName: 'smoke',
      testMatch: ['**/tests/smoke/**/*.test.{js,ts}'],
      testTimeout: 5000
    },
    {
      displayName: 'unit',
      testMatch: ['**/tests/unit/**/*.test.{js,ts}'],
      testTimeout: 10000
    },
    {
      displayName: 'integration',
      testMatch: ['**/tests/integration/**/*.test.{js,ts}'],
      testTimeout: 60000
    },
    {
      displayName: 'contract',
      testMatch: ['**/tests/contract/**/*.test.{js,ts}'],
      testTimeout: 30000
    },
    {
      displayName: 'performance',
      testMatch: ['**/tests/performance/**/*.test.{js,ts}'],
      testTimeout: 300000
    },
    {
      displayName: 'e2e',
      testMatch: ['**/tests/e2e/**/*.test.{js,ts}'],
      testTimeout: 120000
    }
  ],
  
  // Global variables
  globals: {
    'ts-jest': {
      useESM: true
    }
  },
  
  // Mock configuration
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true
};