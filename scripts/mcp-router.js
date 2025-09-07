#!/usr/bin/env node

/**
 * MCP Task Router - Intelligent task delegation with fallback chains
 * Automatically routes tasks to optimal AI models with fallback handling
 */

const fs = require('fs').promises;
const path = require('path');

class MCPTaskRouter {
  constructor() {
    this.services = {
      'together-ai': {
        limit: 3000,
        period: 'month',
        specialty: 'complex-code-generation',
        cost: 'free',
        priority: 1
      },
      'gemini-pro': {
        limit: 1500,
        period: 'day', 
        specialty: 'testing-documentation',
        cost: 'free',
        priority: 2
      },
      'huggingface': {
        limit: 30000,
        period: 'month',
        specialty: 'specialized-models',
        cost: 'free',
        priority: 3,
        unit: 'characters'
      },
      'claude-code': {
        limit: null,
        period: null,
        specialty: 'orchestration-complex',
        cost: 'paid',
        priority: 999
      },
      'copilot': {
        limit: null,
        period: null,
        specialty: 'simple-tasks',
        cost: 'free',
        priority: 0
      }
    };

    this.usageFile = '.mcp-usage.json';
  }

  async loadUsage() {
    try {
      const data = await fs.readFile(this.usageFile, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      return {
        'together-ai': { used: 0, resetDate: this.getNextReset('month') },
        'gemini-pro': { used: 0, resetDate: this.getNextReset('day') },
        'huggingface': { used: 0, resetDate: this.getNextReset('month') },
        lastUpdated: new Date().toISOString()
      };
    }
  }

  async saveUsage(usage) {
    usage.lastUpdated = new Date().toISOString();
    await fs.writeFile(this.usageFile, JSON.stringify(usage, null, 2));
  }

  getNextReset(period) {
    const now = new Date();
    if (period === 'day') {
      const tomorrow = new Date(now);
      tomorrow.setDate(tomorrow.getDate() + 1);
      tomorrow.setHours(0, 0, 0, 0);
      return tomorrow.toISOString();
    } else if (period === 'month') {
      const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      return nextMonth.toISOString();
    }
    return null;
  }

  analyzeTask(taskDescription) {
    const analysis = {
      complexity: 1,
      size: 'XS',
      type: 'unknown',
      language: 'javascript',
      isTestingRelated: false,
      isDocumentationRelated: false,
      isCodeGeneration: false,
      isSQLRelated: false,
      estimatedTokens: 100
    };

    const lowerTask = taskDescription.toLowerCase();

    // Complexity analysis
    const complexityKeywords = {
      5: ['architecture', 'system design', 'microservice', 'distributed', 'algorithm', 'optimization'],
      4: ['authentication', 'authorization', 'security', 'encryption', 'oauth', 'api design'],
      3: ['database', 'integration', 'async', 'performance', 'refactor', 'framework'],
      2: ['function', 'component', 'validation', 'parsing', 'formatting'],
      1: ['fix', 'typo', 'import', 'export', 'variable', 'simple']
    };

    for (const [level, keywords] of Object.entries(complexityKeywords)) {
      if (keywords.some(keyword => lowerTask.includes(keyword))) {
        analysis.complexity = parseInt(level);
        break;
      }
    }

    // Size estimation
    const sizeKeywords = {
      'XL': ['system', 'application', 'full', 'complete', 'entire'],
      'L': ['module', 'service', 'component', 'multiple'],
      'M': ['function', 'class', 'feature'],
      'S': ['method', 'utility', 'helper', 'single'],
      'XS': ['fix', 'typo', 'rename', 'import']
    };

    for (const [size, keywords] of Object.entries(sizeKeywords)) {
      if (keywords.some(keyword => lowerTask.includes(keyword))) {
        analysis.size = size;
        break;
      }
    }

    // Type analysis
    if (lowerTask.includes('test') || lowerTask.includes('spec') || lowerTask.includes('unit') || lowerTask.includes('integration')) {
      analysis.isTestingRelated = true;
      analysis.type = 'testing';
      analysis.complexity = Math.max(analysis.complexity, 3); // Testing is generally complex
    }

    if (lowerTask.includes('doc') || lowerTask.includes('api') || lowerTask.includes('readme') || lowerTask.includes('guide')) {
      analysis.isDocumentationRelated = true;
      analysis.type = 'documentation';
    }

    if (lowerTask.includes('generate') || lowerTask.includes('create') || lowerTask.includes('implement') || lowerTask.includes('build')) {
      analysis.isCodeGeneration = true;
      analysis.type = 'code-generation';
    }

    if (lowerTask.includes('sql') || lowerTask.includes('query') || lowerTask.includes('database') || lowerTask.includes('select')) {
      analysis.isSQLRelated = true;
      analysis.type = 'sql';
    }

    // Language detection
    const languages = ['javascript', 'typescript', 'python', 'sql', 'java', 'go', 'rust', 'c++'];
    for (const lang of languages) {
      if (lowerTask.includes(lang)) {
        analysis.language = lang;
        break;
      }
    }

    // Token estimation
    analysis.estimatedTokens = Math.max(100, taskDescription.length * 2);

    return analysis;
  }

  async selectOptimalService(taskAnalysis, usage) {
    const candidates = [];

    // Reset usage if needed
    for (const [service, data] of Object.entries(usage)) {
      if (data.resetDate && new Date() > new Date(data.resetDate)) {
        data.used = 0;
        data.resetDate = this.getNextReset(this.services[service]?.period);
      }
    }

    // GitHub Copilot for simple tasks
    if (taskAnalysis.complexity <= 2 && ['XS', 'S'].includes(taskAnalysis.size)) {
      candidates.push({
        service: 'copilot',
        score: 100,
        rationale: 'Simple task suitable for GitHub Copilot',
        available: true
      });
    }

    // Gemini for testing and documentation
    if (taskAnalysis.isTestingRelated || taskAnalysis.isDocumentationRelated) {
      const geminiUsage = usage['gemini-pro'] || { used: 0 };
      const available = geminiUsage.used < this.services['gemini-pro'].limit;
      
      candidates.push({
        service: 'gemini-pro',
        score: available ? 90 : 10,
        rationale: `Specialized in ${taskAnalysis.type}`,
        available,
        usageInfo: `${geminiUsage.used}/${this.services['gemini-pro'].limit}`
      });
    }

    // HuggingFace for SQL and specialized models
    if (taskAnalysis.isSQLRelated || taskAnalysis.type === 'specialized') {
      const hfUsage = usage['huggingface'] || { used: 0 };
      const estimatedChars = taskAnalysis.estimatedTokens * 4; // Rough estimate
      const available = hfUsage.used + estimatedChars < this.services['huggingface'].limit;
      
      candidates.push({
        service: 'huggingface',
        score: available ? 85 : 5,
        rationale: `Specialized models for ${taskAnalysis.type}`,
        available,
        usageInfo: `${hfUsage.used}/${this.services['huggingface'].limit} chars`
      });
    }

    // Together AI for complex code generation
    if (taskAnalysis.isCodeGeneration && taskAnalysis.complexity >= 3) {
      const togetherUsage = usage['together-ai'] || { used: 0 };
      const available = togetherUsage.used < this.services['together-ai'].limit;
      
      candidates.push({
        service: 'together-ai',
        score: available ? 95 : 15,
        rationale: 'Complex code generation specialist',
        available,
        usageInfo: `${togetherUsage.used}/${this.services['together-ai'].limit}`
      });
    }

    // Claude Code as fallback for complex tasks
    if (taskAnalysis.complexity > 2 || ['L', 'XL'].includes(taskAnalysis.size)) {
      candidates.push({
        service: 'claude-code',
        score: 80,
        rationale: 'Complex task requiring orchestration',
        available: true,
        cost: 'paid'
      });
    }

    // Sort by score and availability
    candidates.sort((a, b) => {
      if (a.available !== b.available) return b.available - a.available;
      return b.score - a.score;
    });

    return candidates;
  }

  async createFallbackChain(taskDescription) {
    const taskAnalysis = this.analyzeTask(taskDescription);
    const usage = await this.loadUsage();
    const candidates = await this.selectOptimalService(taskAnalysis, usage);

    const chain = {
      task: taskDescription,
      analysis: taskAnalysis,
      primaryService: candidates[0],
      fallbacks: candidates.slice(1, 4), // Top 3 fallbacks
      createdAt: new Date().toISOString()
    };

    return chain;
  }

  async executeWithFallback(taskDescription, options = {}) {
    const chain = await this.createFallbackChain(taskDescription);
    const results = [];

    console.log(`🎯 Task: ${taskDescription}`);
    console.log(`📊 Analysis: Complexity ${chain.analysis.complexity}, Size ${chain.analysis.size}, Type ${chain.analysis.type}`);
    console.log(`🚀 Primary service: ${chain.primaryService.service} (${chain.primaryService.rationale})`);

    // Try primary service
    try {
      if (chain.primaryService.available) {
        const result = await this.executeTask(chain.primaryService.service, taskDescription, options);
        await this.updateUsage(chain.primaryService.service, chain.analysis);
        
        results.push({
          service: chain.primaryService.service,
          status: 'success',
          result: result
        });
        
        console.log(`✅ Successfully completed with ${chain.primaryService.service}`);
        return { success: true, service: chain.primaryService.service, result, chain };
      }
    } catch (error) {
      console.log(`❌ Primary service ${chain.primaryService.service} failed: ${error.message}`);
      results.push({
        service: chain.primaryService.service,
        status: 'failed',
        error: error.message
      });
    }

    // Try fallbacks
    for (const fallback of chain.fallbacks) {
      if (!fallback.available) {
        console.log(`⏭️ Skipping ${fallback.service} (not available: ${fallback.usageInfo || 'rate limited'})`);
        continue;
      }

      try {
        console.log(`🔄 Trying fallback: ${fallback.service} (${fallback.rationale})`);
        const result = await this.executeTask(fallback.service, taskDescription, options);
        await this.updateUsage(fallback.service, chain.analysis);
        
        results.push({
          service: fallback.service,
          status: 'success',
          result: result
        });
        
        console.log(`✅ Successfully completed with fallback ${fallback.service}`);
        return { success: true, service: fallback.service, result, chain, fallbackUsed: true };
      } catch (error) {
        console.log(`❌ Fallback ${fallback.service} failed: ${error.message}`);
        results.push({
          service: fallback.service,
          status: 'failed',
          error: error.message
        });
      }
    }

    console.log(`💥 All services failed for task: ${taskDescription}`);
    return { success: false, allResults: results, chain };
  }

  async executeTask(service, taskDescription, options) {
    const commands = {
      'copilot': () => this.executeGitHubCopilot(taskDescription, options),
      'together-ai': () => this.executeMCPServer('together-ai', 'generate-code', { task: taskDescription, ...options }),
      'gemini-pro': () => this.executeMCPServer('gemini-pro', this.getGeminiOperation(taskDescription), { task: taskDescription, ...options }),
      'huggingface': () => this.executeMCPServer('huggingface', this.getHuggingFaceOperation(taskDescription), { task: taskDescription, ...options }),
      'claude-code': () => this.executeClaudeCode(taskDescription, options)
    };

    const executor = commands[service];
    if (!executor) {
      throw new Error(`Unknown service: ${service}`);
    }

    return await executor();
  }

  getGeminiOperation(taskDescription) {
    const lower = taskDescription.toLowerCase();
    if (lower.includes('test')) return 'generate-tests';
    if (lower.includes('doc')) return 'generate-documentation';
    if (lower.includes('analyze')) return 'analyze-code';
    return 'generate-documentation';
  }

  getHuggingFaceOperation(taskDescription) {
    const lower = taskDescription.toLowerCase();
    if (lower.includes('sql')) return 'generate-sql';
    if (lower.includes('frontend') || lower.includes('component')) return 'generate-frontend-component';
    if (lower.includes('data') || lower.includes('analysis')) return 'generate-data-science-code';
    return 'generate-specialized-code';
  }

  async executeMCPServer(server, operation, params) {
    // This would execute the actual MCP server command
    const command = `/mcp ${server} ${operation} ${Object.entries(params).map(([k,v]) => `--${k} "${v}"`).join(' ')}`;
    
    // For now, return a simulation
    return {
      command: command,
      status: 'simulated',
      message: `Would execute: ${command}`
    };
  }

  async executeGitHubCopilot(taskDescription, options) {
    // This would create a GitHub issue assigned to Copilot
    return {
      action: 'github-issue',
      title: `Copilot Task: ${taskDescription}`,
      assignee: 'copilot',
      labels: ['copilot-task', 'auto-assigned'],
      status: 'simulated'
    };
  }

  async executeClaudeCode(taskDescription, options) {
    // This would start a Claude Code work session
    return {
      action: 'claude-work',
      command: `/work ${taskDescription}`,
      status: 'simulated'
    };
  }

  async updateUsage(service, taskAnalysis) {
    const usage = await this.loadUsage();
    
    if (!usage[service]) {
      usage[service] = { used: 0, resetDate: this.getNextReset(this.services[service]?.period) };
    }

    // Update usage based on service type
    if (service === 'huggingface') {
      usage[service].used += taskAnalysis.estimatedTokens * 4; // Rough character estimate
    } else if (['together-ai', 'gemini-pro'].includes(service)) {
      usage[service].used += 1; // Request count
    }

    await this.saveUsage(usage);
  }

  async getUsageReport() {
    const usage = await this.loadUsage();
    const report = {};

    for (const [service, serviceInfo] of Object.entries(this.services)) {
      const serviceUsage = usage[service] || { used: 0, resetDate: null };
      
      report[service] = {
        specialty: serviceInfo.specialty,
        used: serviceUsage.used,
        limit: serviceInfo.limit,
        available: serviceInfo.limit ? serviceUsage.used < serviceInfo.limit : true,
        resetDate: serviceUsage.resetDate,
        cost: serviceInfo.cost,
        unit: serviceInfo.unit || 'requests'
      };

      if (serviceInfo.limit) {
        report[service].percentageUsed = Math.round((serviceUsage.used / serviceInfo.limit) * 100);
        report[service].remaining = serviceInfo.limit - serviceUsage.used;
      }
    }

    return report;
  }
}

// CLI interface
async function main() {
  const router = new MCPTaskRouter();
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'analyze':
      const taskDesc = args[1];
      if (!taskDesc) {
        console.log('Usage: node mcp-router.js analyze "task description"');
        process.exit(1);
      }
      
      const analysis = router.analyzeTask(taskDesc);
      console.log('Task Analysis:');
      console.log(JSON.stringify(analysis, null, 2));
      break;

    case 'route':
      const routeTask = args[1];
      if (!routeTask) {
        console.log('Usage: node mcp-router.js route "task description"');
        process.exit(1);
      }
      
      const chain = await router.createFallbackChain(routeTask);
      console.log('Routing Plan:');
      console.log(JSON.stringify(chain, null, 2));
      break;

    case 'execute':
      const executeTask = args[1];
      if (!executeTask) {
        console.log('Usage: node mcp-router.js execute "task description"');
        process.exit(1);
      }
      
      const result = await router.executeWithFallback(executeTask);
      console.log('\nExecution Result:');
      console.log(JSON.stringify(result, null, 2));
      break;

    case 'usage':
      const report = await router.getUsageReport();
      console.log('Usage Report:');
      console.log(JSON.stringify(report, null, 2));
      break;

    case 'help':
    default:
      console.log(`
MCP Task Router - Intelligent task delegation with fallback chains

Commands:
  analyze "task"    - Analyze task complexity and requirements
  route "task"      - Show optimal service routing plan
  execute "task"    - Execute task with automatic fallback
  usage            - Show current API usage across all services
  help             - Show this help message

Examples:
  node mcp-router.js analyze "implement OAuth2 authentication"
  node mcp-router.js route "generate unit tests for auth.js"
  node mcp-router.js execute "create SQL query for user analytics"
  node mcp-router.js usage
      `);
  }
}

// Run CLI if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}

module.exports = { MCPTaskRouter };