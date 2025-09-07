#!/usr/bin/env node

/**
 * Together AI MCP Server
 * Provides enhanced AI code generation capabilities with file access
 * Free tier: 3000 requests/month
 */

const { Server } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/index.js');
const { StdioServerTransport } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/types.js');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const API_BASE_URL = 'https://api.together.xyz';
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const RATE_LIMIT = 3000; // requests per month
const ALLOWED_EXTENSIONS = ['.js', '.ts', '.py', '.md', '.json', '.yaml', '.yml', '.txt'];

class TogetherAIMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'together-ai-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.apiKey = process.env.TOGETHER_AI_API_KEY;
    this.projectRoot = process.cwd();
    this.usageCount = 0;
    this.usageResetDate = this.getMonthlyResetDate();

    this.setupHandlers();
  }

  getMonthlyResetDate() {
    const now = new Date();
    const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
    return nextMonth;
  }

  validateApiKey() {
    if (!this.apiKey) {
      throw new Error('TOGETHER_AI_API_KEY environment variable is required');
    }
  }

  validateFilePath(filePath) {
    // Security validation
    if (!filePath || typeof filePath !== 'string') {
      throw new Error('File path must be a non-empty string');
    }

    // Block path traversal
    if (filePath.includes('..') || filePath.includes('~') || path.isAbsolute(filePath)) {
      throw new Error('Invalid file path: path traversal or absolute paths not allowed');
    }

    // Block sensitive files/directories
    const sensitivePatterns = ['.env', '.git', 'node_modules', '.ssh', 'credentials'];
    if (sensitivePatterns.some(pattern => filePath.includes(pattern))) {
      throw new Error('Access to sensitive files not allowed');
    }

    // Check file extension
    const ext = path.extname(filePath).toLowerCase();
    if (ext && !ALLOWED_EXTENSIONS.includes(ext)) {
      throw new Error(`File extension ${ext} not allowed`);
    }

    return path.resolve(this.projectRoot, filePath);
  }

  async readProjectContext() {
    try {
      const contextPath = path.join(this.projectRoot, 'PROJECT_CONTEXT.md');
      const content = await fs.readFile(contextPath, 'utf-8');
      
      // Parse basic project information
      const lines = content.split('\n');
      const context = {
        status: this.extractValue(lines, 'Status'),
        goals: this.extractValue(lines, 'Current Goals'),
        milestone: this.extractValue(lines, 'Current Milestone'),
        techStack: this.extractValue(lines, 'Technology Stack'),
        architecture: this.extractValue(lines, 'Architecture Overview'),
      };

      return context;
    } catch (error) {
      console.warn('Could not read PROJECT_CONTEXT.md:', error.message);
      return {
        status: 'Unknown',
        goals: 'Multi-agent development framework',
        milestone: 'Development',
        techStack: 'Node.js, TypeScript, Python',
        architecture: 'Multi-agent with GitHub coordination'
      };
    }
  }

  extractValue(lines, key) {
    const line = lines.find(l => l.includes(key + ':'));
    return line ? line.split(':')[1]?.trim() || '' : '';
  }

  async checkRateLimit() {
    if (new Date() > this.usageResetDate) {
      this.usageCount = 0;
      this.usageResetDate = this.getMonthlyResetDate();
    }

    if (this.usageCount >= RATE_LIMIT) {
      throw new Error(`Rate limit exceeded. Resets on ${this.usageResetDate.toDateString()}`);
    }
  }

  async makeTogetherAIRequest(messages, options = {}) {
    await this.checkRateLimit();
    this.validateApiKey();

    const requestBody = {
      model: options.model || 'meta-llama/Llama-2-7b-chat-hf',
      messages: messages,
      max_tokens: options.maxTokens || 2048,
      temperature: options.temperature || 0.7,
      ...options
    };

    try {
      const response = await fetch(`${API_BASE_URL}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`Together AI API error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      this.usageCount++;
      
      return data.choices[0]?.message?.content || '';
    } catch (error) {
      throw new Error(`Together AI request failed: ${error.message}`);
    }
  }

  setupHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'read_project_context',
            description: 'Read current project context from PROJECT_CONTEXT.md',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'read_source_file',
            description: 'Read a source file from the project directory',
            inputSchema: {
              type: 'object',
              properties: {
                filename: {
                  type: 'string',
                  description: 'Relative path to the file within the project directory',
                },
              },
              required: ['filename'],
            },
          },
          {
            name: 'write_file',
            description: 'Write content to a file in the project directory',
            inputSchema: {
              type: 'object',
              properties: {
                filename: {
                  type: 'string',
                  description: 'Relative path to the file within the project directory',
                },
                content: {
                  type: 'string',
                  description: 'Content to write to the file',
                },
              },
              required: ['filename', 'content'],
            },
          },
          {
            name: 'generate_code',
            description: 'Generate code using Together AI with project context',
            inputSchema: {
              type: 'object',
              properties: {
                task: {
                  type: 'string',
                  description: 'Description of the code to generate',
                },
                language: {
                  type: 'string',
                  description: 'Programming language (e.g., javascript, python, typescript)',
                  default: 'javascript',
                },
                framework: {
                  type: 'string',
                  description: 'Framework or library context (e.g., react, fastapi, express)',
                },
                complexity: {
                  type: 'string',
                  enum: ['simple', 'medium', 'complex'],
                  description: 'Complexity level of the code to generate',
                  default: 'medium',
                },
              },
              required: ['task'],
            },
          },
          {
            name: 'refactor_code',
            description: 'Refactor existing code using Together AI',
            inputSchema: {
              type: 'object',
              properties: {
                filename: {
                  type: 'string',
                  description: 'File containing code to refactor',
                },
                focus: {
                  type: 'string',
                  description: 'What to focus on (e.g., performance, readability, maintainability)',
                  default: 'readability',
                },
                preserveAPI: {
                  type: 'boolean',
                  description: 'Whether to preserve the existing API/interface',
                  default: true,
                },
              },
              required: ['filename'],
            },
          },
          {
            name: 'get_usage_stats',
            description: 'Get current API usage statistics',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'read_project_context':
            const context = await this.readProjectContext();
            return {
              content: [{
                type: 'text',
                text: JSON.stringify(context, null, 2)
              }]
            };

          case 'read_source_file':
            const filePath = this.validateFilePath(args.filename);
            
            // Check file size
            const stats = await fs.stat(filePath);
            if (stats.size > MAX_FILE_SIZE) {
              throw new Error(`File too large: ${stats.size} bytes (max: ${MAX_FILE_SIZE})`);
            }

            const content = await fs.readFile(filePath, 'utf-8');
            return {
              content: [{
                type: 'text',
                text: content
              }]
            };

          case 'write_file':
            const writeFilePath = this.validateFilePath(args.filename);
            
            // Create directory if it doesn't exist
            await fs.mkdir(path.dirname(writeFilePath), { recursive: true });
            
            // Backup existing file if it exists
            try {
              const existing = await fs.readFile(writeFilePath, 'utf-8');
              const backupPath = `${writeFilePath}.backup.${Date.now()}`;
              await fs.writeFile(backupPath, existing);
            } catch (error) {
              // File doesn't exist, no backup needed
            }

            await fs.writeFile(writeFilePath, args.content, 'utf-8');
            return {
              content: [{
                type: 'text',
                text: `File written successfully: ${args.filename}`
              }]
            };

          case 'generate_code':
            const projectContext = await this.readProjectContext();
            
            const prompt = `You are an expert software engineer working on a ${projectContext.techStack} project.

Project Context:
- Status: ${projectContext.status}
- Current Goals: ${projectContext.goals}
- Milestone: ${projectContext.milestone}
- Architecture: ${projectContext.architecture}

Task: ${args.task}
Language: ${args.language || 'javascript'}
${args.framework ? `Framework: ${args.framework}` : ''}
Complexity: ${args.complexity || 'medium'}

Generate high-quality, production-ready code that:
1. Follows best practices for ${args.language || 'javascript'}
2. Includes proper error handling
3. Has clear documentation/comments
4. Is modular and maintainable
5. Fits the project architecture

Provide only the code without explanation:`;

            const messages = [
              { role: 'system', content: 'You are an expert software engineer. Generate clean, production-ready code.' },
              { role: 'user', content: prompt }
            ];

            const generatedCode = await this.makeTogetherAIRequest(messages, {
              model: 'codellama/CodeLlama-7b-Instruct-hf',
              maxTokens: 4096,
              temperature: 0.3
            });

            return {
              content: [{
                type: 'text',
                text: generatedCode
              }]
            };

          case 'refactor_code':
            const refactorFilePath = this.validateFilePath(args.filename);
            const originalCode = await fs.readFile(refactorFilePath, 'utf-8');
            const refactorContext = await this.readProjectContext();

            const refactorPrompt = `You are an expert software engineer refactoring code.

Project Context:
- Tech Stack: ${refactorContext.techStack}
- Architecture: ${refactorContext.architecture}

Original Code:
\`\`\`
${originalCode}
\`\`\`

Refactoring Focus: ${args.focus}
Preserve API: ${args.preserveAPI}

Refactor this code to improve ${args.focus} while:
1. Maintaining functionality
2. ${args.preserveAPI ? 'Preserving the existing API/interface' : 'Optimizing the interface if needed'}
3. Following modern best practices
4. Adding clear documentation
5. Improving error handling

Provide only the refactored code:`;

            const refactorMessages = [
              { role: 'system', content: 'You are an expert at code refactoring. Improve code quality while maintaining functionality.' },
              { role: 'user', content: refactorPrompt }
            ];

            const refactoredCode = await this.makeTogetherAIRequest(refactorMessages, {
              model: 'codellama/CodeLlama-7b-Instruct-hf',
              maxTokens: 4096,
              temperature: 0.2
            });

            return {
              content: [{
                type: 'text',
                text: refactoredCode
              }]
            };

          case 'get_usage_stats':
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  service: 'Together AI',
                  usedRequests: this.usageCount,
                  monthlyLimit: RATE_LIMIT,
                  remainingRequests: RATE_LIMIT - this.usageCount,
                  resetDate: this.usageResetDate.toISOString(),
                  percentageUsed: Math.round((this.usageCount / RATE_LIMIT) * 100)
                }, null, 2)
              }]
            };

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: `Error: ${error.message}`
          }],
          isError: true
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Together AI MCP Server running on stdio');
  }
}

// Run the server
if (require.main === module) {
  const server = new TogetherAIMCPServer();
  server.run().catch((error) => {
    console.error('Fatal error in Together AI MCP Server:', error);
    process.exit(1);
  });
}

module.exports = { TogetherAIMCPServer };