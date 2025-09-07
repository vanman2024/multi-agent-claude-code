#!/usr/bin/env node

/**
 * E2E Integration Tests for Multi-Agent Workflow System
 * Tests complete workflows including routing, fallback, and file operations
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

class E2EWorkflowTester {
  constructor() {
    this.testResults = [];
    this.testDir = './test-workflow-output';
  }

  async runTest(testName, testFn) {
    try {
      console.log(`🧪 Running E2E test: ${testName}`);
      await testFn();
      this.testResults.push({ test: testName, status: 'PASS' });
      console.log(`✅ ${testName}: PASS`);
    } catch (error) {
      this.testResults.push({ test: testName, status: 'FAIL', error: error.message });
      console.log(`❌ ${testName}: FAIL - ${error.message}`);
    }
  }

  async setupTestEnvironment() {
    // Clean up any existing test directory
    try {
      await fs.rm(this.testDir, { recursive: true, force: true });
    } catch (error) {
      // Directory doesn't exist, that's fine
    }

    await fs.mkdir(this.testDir, { recursive: true });
    
    // Create sample files for testing
    await fs.writeFile(path.join(this.testDir, 'sample-auth.js'), `
// Sample authentication module for testing
class AuthService {
  constructor(config) {
    this.config = config;
    this.users = new Map();
  }

  async login(email, password) {
    const user = this.users.get(email);
    if (!user || user.password !== password) {
      throw new Error('Invalid credentials');
    }
    return { token: 'jwt-token', user: { email: user.email, name: user.name } };
  }

  async register(email, password, name) {
    if (this.users.has(email)) {
      throw new Error('User already exists');
    }
    this.users.set(email, { email, password, name });
    return { success: true };
  }

  async validateToken(token) {
    // Simple token validation (in real app, would verify JWT)
    return token === 'jwt-token';
  }
}

module.exports = { AuthService };
`);

    await fs.writeFile(path.join(this.testDir, 'sample-api.js'), `
// Sample API endpoints for testing
const express = require('express');
const { AuthService } = require('./sample-auth');

const app = express();
app.use(express.json());

const authService = new AuthService();

app.post('/api/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const result = await authService.login(email, password);
    res.json(result);
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

app.post('/api/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    const result = await authService.register(email, password, name);
    res.json(result);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

module.exports = app;
`);

    console.log('✅ E2E test environment setup complete');
  }

  async cleanupTestEnvironment() {
    try {
      await fs.rm(this.testDir, { recursive: true, force: true });
      // Clean up usage file
      await fs.rm('.mcp-usage.json', { force: true });
      console.log('✅ E2E test environment cleanup complete');
    } catch (error) {
      console.log('⚠️ Cleanup warning:', error.message);
    }
  }

  async testMCPRouterIntegration() {
    await this.runTest('MCP Router Task Analysis', async () => {
      const output = execSync('node scripts/mcp-router.js analyze "implement user authentication system"', { encoding: 'utf-8' });
      
      if (!output.includes('complexity')) {
        throw new Error('Task analysis output missing complexity field');
      }

      if (!output.includes('type')) {
        throw new Error('Task analysis output missing type field');
      }
    });

    await this.runTest('MCP Router Routing Plan', async () => {
      const output = execSync('node scripts/mcp-router.js route "generate unit tests for authentication"', { encoding: 'utf-8' });
      
      if (!output.includes('primaryService')) {
        throw new Error('Routing plan missing primary service');
      }

      if (!output.includes('fallbacks')) {
        throw new Error('Routing plan missing fallbacks');
      }
    });

    await this.runTest('MCP Router Execution Simulation', async () => {
      const output = execSync('node scripts/mcp-router.js execute "simple bug fix in configuration"', { encoding: 'utf-8' });
      
      if (!output.includes('Successfully completed')) {
        throw new Error('Execution did not complete successfully');
      }

      if (!output.includes('service')) {
        throw new Error('Execution output missing service information');
      }
    });

    await this.runTest('MCP Router Usage Tracking', async () => {
      const output = execSync('node scripts/mcp-router.js usage', { encoding: 'utf-8' });
      
      if (!output.includes('together-ai') || !output.includes('gemini-pro') || !output.includes('huggingface')) {
        throw new Error('Usage report missing expected services');
      }
    });
  }

  async testWorkflowAutomation() {
    await this.runTest('Workflow Automation Help', async () => {
      const output = execSync('./scripts/workflow-automation.sh help', { encoding: 'utf-8' });
      
      if (!output.includes('Available Workflows')) {
        throw new Error('Help output missing workflow information');
      }
    });

    await this.runTest('Component Workflow Simulation', async () => {
      const output = execSync('./scripts/workflow-automation.sh component "TestComponent" "react" "css"', { encoding: 'utf-8' });
      
      if (!output.includes('Component development workflow completed')) {
        throw new Error('Component workflow did not complete');
      }

      if (!output.includes('Phase 1') || !output.includes('Phase 2')) {
        throw new Error('Component workflow missing expected phases');
      }
    });

    await this.runTest('API Workflow Simulation', async () => {
      const output = execSync('./scripts/workflow-automation.sh api "UserAPI" "authentication endpoints"', { encoding: 'utf-8' });
      
      if (!output.includes('API development workflow completed')) {
        throw new Error('API workflow did not complete');
      }
    });

    await this.runTest('Bug Fix Workflow Simulation', async () => {
      const output = execSync(`./scripts/workflow-automation.sh bugfix "authentication error" "${this.testDir}/sample-auth.js"`, { encoding: 'utf-8' });
      
      if (!output.includes('Bug fix workflow completed')) {
        throw new Error('Bug fix workflow did not complete');
      }
    });
  }

  async testMCPServerBasicFunctionality() {
    await this.runTest('Together AI Server Import and Basic Methods', async () => {
      const { TogetherAIMCPServer } = require('../scripts/mcp-servers/together-ai-mcp-server.js');
      const server = new TogetherAIMCPServer();
      
      // Test basic methods exist
      if (typeof server.validateFilePath !== 'function') {
        throw new Error('TogetherAI server missing validateFilePath method');
      }

      if (typeof server.readProjectContext !== 'function') {
        throw new Error('TogetherAI server missing readProjectContext method');
      }

      // Test file path validation works
      try {
        server.validateFilePath('../../../etc/passwd');
        throw new Error('Security validation failed - should have rejected path traversal');
      } catch (error) {
        if (!error.message.includes('path traversal')) {
          throw new Error('Wrong security error message');
        }
      }
    });

    await this.runTest('Gemini Server Import and Basic Methods', async () => {
      const { GeminiMCPServer } = require('../scripts/mcp-servers/gemini-mcp-server.js');
      const server = new GeminiMCPServer();
      
      // Test context reading
      const context = await server.readProjectContext();
      if (!context || typeof context !== 'object') {
        throw new Error('Context reading failed');
      }
    });

    await this.runTest('HuggingFace Server Import and Basic Methods', async () => {
      const { HuggingFaceMCPServer } = require('../scripts/mcp-servers/huggingface-mcp-server.js');
      const server = new HuggingFaceMCPServer();
      
      // Test model description method
      const description = server.getModelDescription('sql-generation');
      if (!description || typeof description !== 'string') {
        throw new Error('Model description method failed');
      }
    });
  }

  async testFileOperationsE2E() {
    await this.runTest('Safe File Reading', async () => {
      const { TogetherAIMCPServer } = require('../scripts/mcp-servers/together-ai-mcp-server.js');
      const server = new TogetherAIMCPServer();
      
      // Change to test directory for safe file operations
      const originalCwd = process.cwd();
      process.chdir(this.testDir);
      
      try {
        const validPath = server.validateFilePath('sample-auth.js');
        if (!validPath.includes('sample-auth.js')) {
          throw new Error('File path validation failed');
        }

        // Test reading the file
        const content = await fs.readFile(validPath, 'utf-8');
        if (!content.includes('AuthService')) {
          throw new Error('File content not read correctly');
        }
      } finally {
        process.chdir(originalCwd);
      }
    });

    await this.runTest('Safe File Writing with Backup', async () => {
      const { GeminiMCPServer } = require('../scripts/mcp-servers/gemini-mcp-server.js');
      const server = new GeminiMCPServer();
      
      const originalCwd = process.cwd();
      process.chdir(this.testDir);
      
      try {
        const testFile = 'write-test.js';
        const initialContent = '// Initial content\nconsole.log("Hello");';
        const newContent = '// Updated content\nconsole.log("Updated");';
        
        // Create initial file
        await fs.writeFile(testFile, initialContent);
        
        // Validate path and write new content
        const validPath = server.validateFilePath(testFile);
        
        // Read existing content (simulating backup)
        const existing = await fs.readFile(validPath, 'utf-8');
        const backupPath = `${validPath}.backup.${Date.now()}`;
        await fs.writeFile(backupPath, existing);
        
        // Write new content
        await fs.writeFile(validPath, newContent);
        
        // Verify new content
        const updatedContent = await fs.readFile(validPath, 'utf-8');
        if (!updatedContent.includes('Updated content')) {
          throw new Error('File update failed');
        }

        // Verify backup exists
        const backupContent = await fs.readFile(backupPath, 'utf-8');
        if (!backupContent.includes('Initial content')) {
          throw new Error('Backup creation failed');
        }
      } finally {
        process.chdir(originalCwd);
      }
    });
  }

  async testUsageTrackingE2E() {
    await this.runTest('Usage Tracking Persistence', async () => {
      const { MCPTaskRouter } = require('../scripts/mcp-router.js');
      const router = new MCPTaskRouter();
      
      // Simulate some usage
      const initialUsage = await router.loadUsage();
      
      // Update usage
      initialUsage['together-ai'].used = 10;
      initialUsage['gemini-pro'].used = 5;
      await router.saveUsage(initialUsage);
      
      // Load usage again and verify persistence
      const loadedUsage = await router.loadUsage();
      if (loadedUsage['together-ai'].used !== 10) {
        throw new Error('Together AI usage not persisted correctly');
      }
      
      if (loadedUsage['gemini-pro'].used !== 5) {
        throw new Error('Gemini usage not persisted correctly');
      }
    });

    await this.runTest('Rate Limit Detection', async () => {
      const { MCPTaskRouter } = require('../scripts/mcp-router.js');
      const router = new MCPTaskRouter();
      
      // Create usage at limit
      const usage = await router.loadUsage();
      usage['together-ai'].used = 3000; // At limit
      await router.saveUsage(usage);
      
      // Test task routing with limits
      const analysis = router.analyzeTask('complex code generation task');
      const candidates = await router.selectOptimalService(analysis, usage);
      
      // Should prefer other services when Together AI is at limit
      const togetherCandidate = candidates.find(c => c.service === 'together-ai');
      if (togetherCandidate && togetherCandidate.available) {
        throw new Error('Rate limit detection failed - Together AI should not be available');
      }
    });
  }

  async testCompleteWorkflowE2E() {
    await this.runTest('Complete Feature Development Simulation', async () => {
      // Test that the complete workflow can be executed without errors
      const output = execSync('./scripts/workflow-automation.sh feature "TestFeature" "Simple test feature"', { encoding: 'utf-8' });
      
      if (!output.includes('Phase 1') || !output.includes('Phase 4')) {
        throw new Error('Complete workflow missing expected phases');
      }

      if (!output.includes('Feature development workflow completed')) {
        throw new Error('Complete workflow did not finish successfully');
      }
    });

    await this.runTest('Multi-Service Task Routing', async () => {
      // Test that different types of tasks get routed to appropriate services
      const testCases = [
        { task: 'simple bug fix', expectedService: 'copilot' },
        { task: 'generate comprehensive unit tests', expectedService: 'gemini-pro' },
        { task: 'generate SQL query for analytics', expectedService: 'huggingface' },
        { task: 'implement complex authentication system', expectedService: 'together-ai' }
      ];

      for (const testCase of testCases) {
        const output = execSync(`node scripts/mcp-router.js route "${testCase.task}"`, { encoding: 'utf-8' });
        
        // Extract JSON from the output (skip the "Routing Plan:" line)
        const lines = output.split('\n');
        const jsonStart = lines.findIndex(line => line.trim().startsWith('{'));
        if (jsonStart === -1) {
          throw new Error(`No JSON found in output for task: ${testCase.task}`);
        }
        
        const jsonString = lines.slice(jsonStart).join('\n').trim();
        const result = JSON.parse(jsonString);
        
        if (result.primaryService.service !== testCase.expectedService) {
          throw new Error(`Task "${testCase.task}" routed to ${result.primaryService.service}, expected ${testCase.expectedService}`);
        }
      }
    });
  }

  printResults() {
    console.log('\n📊 E2E Test Results Summary:');
    console.log('=============================');
    
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
    
    console.log('\n🎯 E2E Test Categories Covered:');
    console.log('   - MCP Router integration and task analysis');
    console.log('   - Workflow automation and multi-phase execution');
    console.log('   - MCP server functionality and security');
    console.log('   - File operations with safety and backup');
    console.log('   - Usage tracking and rate limit detection');
    console.log('   - Complete workflow end-to-end execution');
    console.log('   - Multi-service task routing optimization');
  }

  async runAllTests() {
    console.log('🚀 Starting Multi-Agent Workflow E2E Tests\n');
    
    await this.setupTestEnvironment();
    
    try {
      await this.testMCPRouterIntegration();
      await this.testWorkflowAutomation();
      await this.testMCPServerBasicFunctionality();
      await this.testFileOperationsE2E();
      await this.testUsageTrackingE2E();
      await this.testCompleteWorkflowE2E();
    } finally {
      await this.cleanupTestEnvironment();
    }
    
    this.printResults();
    
    const failed = this.testResults.filter(r => r.status === 'FAIL').length;
    if (failed > 0) {
      console.log('\n⚠️ Some E2E tests failed. Please review the workflow implementations.');
      process.exit(1);
    } else {
      console.log('\n🎉 All E2E tests passed! Multi-Agent Workflow System is fully functional.');
    }
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new E2EWorkflowTester();
  tester.runAllTests().catch(error => {
    console.error('💥 E2E test suite failed:', error);
    process.exit(1);
  });
}

module.exports = { E2EWorkflowTester };