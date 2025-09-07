#!/usr/bin/env node

/**
 * Basic validation tests for Enhanced MCP Servers
 * Tests file access, security validation, and basic functionality
 */

const fs = require('fs').promises;
const path = require('path');

// Test configuration
const TEST_DIR = './test-files';
const SERVERS = [
  { name: 'Together AI', module: '../../scripts/mcp-servers/together-ai-mcp-server.js' },
  { name: 'Gemini', module: '../../scripts/mcp-servers/gemini-mcp-server.js' },
  { name: 'HuggingFace', module: '../../scripts/mcp-servers/huggingface-mcp-server.js' }
];

class MCPServerTester {
  constructor() {
    this.testResults = [];
  }

  async runTest(testName, testFn) {
    try {
      console.log(`🧪 Running test: ${testName}`);
      await testFn();
      this.testResults.push({ test: testName, status: 'PASS' });
      console.log(`✅ ${testName}: PASS`);
    } catch (error) {
      this.testResults.push({ test: testName, status: 'FAIL', error: error.message });
      console.log(`❌ ${testName}: FAIL - ${error.message}`);
    }
  }

  async setupTestEnvironment() {
    // Create test directory and files
    await fs.mkdir(TEST_DIR, { recursive: true });
    
    // Create a sample source file
    await fs.writeFile(path.join(TEST_DIR, 'sample.js'), `
function add(a, b) {
  return a + b;
}

function multiply(a, b) {
  return a * b;
}

module.exports = { add, multiply };
`);

    // Create a sample SQL file
    await fs.writeFile(path.join(TEST_DIR, 'sample.sql'), `
SELECT users.id, users.name, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.name;
`);

    console.log('✅ Test environment setup complete');
  }

  async cleanupTestEnvironment() {
    try {
      await fs.rm(TEST_DIR, { recursive: true, force: true });
      console.log('✅ Test environment cleanup complete');
    } catch (error) {
      console.log('⚠️ Cleanup warning:', error.message);
    }
  }

  async testServerImports() {
    for (const server of SERVERS) {
      await this.runTest(`Import ${server.name} MCP Server`, async () => {
        const serverModule = require(server.module);
        if (!serverModule) {
          throw new Error(`Failed to import ${server.name} server module`);
        }
      });
    }
  }

  async testFilePathValidation() {
    const { TogetherAIMCPServer } = require('../../scripts/mcp-servers/together-ai-mcp-server.js');
    const server = new TogetherAIMCPServer();

    await this.runTest('Valid file path validation', async () => {
      const validPath = server.validateFilePath('src/test.js');
      if (!validPath.includes('src/test.js')) {
        throw new Error('Valid path validation failed');
      }
    });

    await this.runTest('Path traversal security check', async () => {
      try {
        server.validateFilePath('../../../etc/passwd');
        throw new Error('Security check failed - path traversal allowed');
      } catch (error) {
        if (!error.message.includes('path traversal')) {
          throw new Error('Wrong error type for path traversal');
        }
      }
    });

    await this.runTest('Sensitive file protection', async () => {
      try {
        server.validateFilePath('.env');
        throw new Error('Security check failed - sensitive file access allowed');
      } catch (error) {
        if (!error.message.includes('sensitive')) {
          throw new Error('Wrong error type for sensitive file access');
        }
      }
    });
  }

  async testProjectContextReading() {
    const { GeminiMCPServer } = require('../../scripts/mcp-servers/gemini-mcp-server.js');
    const server = new GeminiMCPServer();

    await this.runTest('Project context reading', async () => {
      const context = await server.readProjectContext();
      if (!context || typeof context !== 'object') {
        throw new Error('Project context reading failed');
      }
      
      // Should have basic structure - check for object properties
      const expectedKeys = ['status', 'goals', 'milestone', 'techStack', 'architecture'];
      const hasRequiredStructure = expectedKeys.every(key => key in context);
      
      if (!hasRequiredStructure) {
        throw new Error('Project context missing expected structure');
      }
      
      // Should have at least milestone from fallback
      if (!context.milestone) {
        throw new Error('Project context missing fallback values');
      }
    });
  }

  async testFileOperations() {
    const { HuggingFaceMCPServer } = require('../../scripts/mcp-servers/huggingface-mcp-server.js');
    const server = new HuggingFaceMCPServer();

    await this.runTest('File reading operation', async () => {
      const testFile = path.join(TEST_DIR, 'sample.js');
      const content = await fs.readFile(server.validateFilePath(testFile), 'utf-8');
      
      if (!content.includes('function add')) {
        throw new Error('File content not read correctly');
      }
    });

    await this.runTest('File writing operation', async () => {
      const testFile = path.join(TEST_DIR, 'write-test.js');
      const testContent = '// Test file content\nconsole.log("Hello, World!");';
      
      // Simulate file writing (without actually calling API)
      const validatedPath = server.validateFilePath(testFile);
      await fs.writeFile(validatedPath, testContent);
      
      // Verify content was written
      const writtenContent = await fs.readFile(validatedPath, 'utf-8');
      if (!writtenContent.includes('Test file content')) {
        throw new Error('File writing failed');
      }
    });
  }

  async testRateLimitChecking() {
    await this.runTest('Rate limit initialization', async () => {
      const { TogetherAIMCPServer } = require('../../scripts/mcp-servers/together-ai-mcp-server.js');
      const server = new TogetherAIMCPServer();
      
      // Should not throw error for initial rate limit check
      await server.checkRateLimit();
    });

    await this.runTest('Character limit checking (HuggingFace)', async () => {
      const { HuggingFaceMCPServer } = require('../../scripts/mcp-servers/huggingface-mcp-server.js');
      const server = new HuggingFaceMCPServer();
      
      // Should not throw error for reasonable input
      await server.checkCharacterLimit('This is a test input');
    });
  }

  async testErrorHandling() {
    await this.runTest('Invalid file extension handling', async () => {
      const { GeminiMCPServer } = require('../../scripts/mcp-servers/gemini-mcp-server.js');
      const server = new GeminiMCPServer();
      
      try {
        server.validateFilePath('malicious.exe');
        throw new Error('Should have rejected invalid file extension');
      } catch (error) {
        if (!error.message.includes('not allowed')) {
          throw new Error('Wrong error type for invalid extension');
        }
      }
    });

    await this.runTest('Missing API key handling', async () => {
      // Save original env var
      const originalKey = process.env.TOGETHER_AI_API_KEY;
      delete process.env.TOGETHER_AI_API_KEY;
      
      try {
        const { TogetherAIMCPServer } = require('../../scripts/mcp-servers/together-ai-mcp-server.js');
        const server = new TogetherAIMCPServer();
        
        try {
          server.validateApiKey();
          throw new Error('Should have thrown error for missing API key');
        } catch (error) {
          if (!error.message.includes('required')) {
            throw new Error('Wrong error type for missing API key');
          }
        }
      } finally {
        // Restore original env var
        if (originalKey) {
          process.env.TOGETHER_AI_API_KEY = originalKey;
        }
      }
    });
  }

  async testModelSpecificFeatures() {
    await this.runTest('HuggingFace model list', async () => {
      const { HuggingFaceMCPServer } = require('../../scripts/mcp-servers/huggingface-mcp-server.js');
      const server = new HuggingFaceMCPServer();
      
      const description = server.getModelDescription('sql-generation');
      if (!description || typeof description !== 'string') {
        throw new Error('Model description not available');
      }
    });

    await this.runTest('Context value extraction', async () => {
      const { GeminiMCPServer } = require('../../scripts/mcp-servers/gemini-mcp-server.js');
      const server = new GeminiMCPServer();
      
      const testLines = ['Status: Active Development', 'Goals: Testing framework'];
      const status = server.extractValue(testLines, 'Status');
      
      if (status !== 'Active Development') {
        throw new Error('Context value extraction failed');
      }
    });
  }

  printResults() {
    console.log('\n📊 Test Results Summary:');
    console.log('========================');
    
    const passed = this.testResults.filter(r => r.status === 'PASS').length;
    const failed = this.testResults.filter(r => r.status === 'FAIL').length;
    
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📈 Success Rate: ${Math.round((passed / this.testResults.length) * 100)}%`);
    
    if (failed > 0) {
      console.log('\n❌ Failed Tests:');
      this.testResults
        .filter(r => r.status === 'FAIL')
        .forEach(r => console.log(`   - ${r.test}: ${r.error}`));
    }
    
    console.log('\n🎯 Test Categories Covered:');
    console.log('   - Server module imports');
    console.log('   - File path security validation');
    console.log('   - Project context reading');
    console.log('   - File operations (read/write)');
    console.log('   - Rate limit checking');
    console.log('   - Error handling');
    console.log('   - Model-specific features');
  }

  async runAllTests() {
    console.log('🚀 Starting Enhanced MCP Servers Validation Tests\n');
    
    await this.setupTestEnvironment();
    
    try {
      await this.testServerImports();
      await this.testFilePathValidation();
      await this.testProjectContextReading();
      await this.testFileOperations();
      await this.testRateLimitChecking();
      await this.testErrorHandling();
      await this.testModelSpecificFeatures();
    } finally {
      await this.cleanupTestEnvironment();
    }
    
    this.printResults();
    
    const failed = this.testResults.filter(r => r.status === 'FAIL').length;
    if (failed > 0) {
      console.log('\n⚠️ Some tests failed. Please review the MCP server implementations.');
      process.exit(1);
    } else {
      console.log('\n🎉 All tests passed! MCP servers are ready for use.');
    }
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new MCPServerTester();
  tester.runAllTests().catch(error => {
    console.error('💥 Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = { MCPServerTester };