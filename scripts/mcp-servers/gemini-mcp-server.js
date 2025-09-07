#!/usr/bin/env node

/**
 * Gemini 1.5 Pro MCP Server
 * Specialized for testing, documentation, and code analysis
 * Free tier: 1500 requests/day
 */

const { Server } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/index.js');
const { StdioServerTransport } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/types.js');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const API_BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models';
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const DAILY_RATE_LIMIT = 1500; // requests per day
const ALLOWED_EXTENSIONS = ['.js', '.ts', '.py', '.md', '.json', '.yaml', '.yml', '.txt', '.html', '.css'];

class GeminiMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'gemini-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.apiKey = process.env.GOOGLE_API_KEY;
    this.projectRoot = process.cwd();
    this.usageCount = 0;
    this.usageResetDate = this.getDailyResetDate();

    this.setupHandlers();
  }

  getDailyResetDate() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);
    return tomorrow;
  }

  validateApiKey() {
    if (!this.apiKey) {
      throw new Error('GOOGLE_API_KEY environment variable is required');
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
      this.usageResetDate = this.getDailyResetDate();
    }

    if (this.usageCount >= DAILY_RATE_LIMIT) {
      throw new Error(`Daily rate limit exceeded. Resets at ${this.usageResetDate.toLocaleString()}`);
    }
  }

  async makeGeminiRequest(prompt, options = {}) {
    await this.checkRateLimit();
    this.validateApiKey();

    const model = options.model || 'gemini-1.5-pro-latest';
    const requestBody = {
      contents: [{
        parts: [{
          text: prompt
        }]
      }],
      generationConfig: {
        temperature: options.temperature || 0.4,
        maxOutputTokens: options.maxTokens || 4096,
        topP: 0.8,
        topK: 40
      }
    };

    try {
      const url = `${API_BASE_URL}/${model}:generateContent?key=${this.apiKey}`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Gemini API error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      this.usageCount++;
      
      return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    } catch (error) {
      throw new Error(`Gemini request failed: ${error.message}`);
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
            name: 'generate_tests',
            description: 'Generate comprehensive test cases for source code',
            inputSchema: {
              type: 'object',
              properties: {
                sourceFile: {
                  type: 'string',
                  description: 'Path to the source file to test',
                },
                testType: {
                  type: 'string',
                  enum: ['unit', 'integration', 'e2e'],
                  description: 'Type of tests to generate',
                  default: 'unit',
                },
                framework: {
                  type: 'string',
                  description: 'Testing framework (e.g., jest, mocha, pytest)',
                  default: 'jest',
                },
                coverage: {
                  type: 'number',
                  description: 'Target test coverage percentage',
                  default: 80,
                },
              },
              required: ['sourceFile'],
            },
          },
          {
            name: 'generate_documentation',
            description: 'Generate documentation for code or APIs',
            inputSchema: {
              type: 'object',
              properties: {
                source: {
                  type: 'string',
                  description: 'Source file or directory to document',
                },
                format: {
                  type: 'string',
                  enum: ['markdown', 'jsdoc', 'sphinx', 'openapi'],
                  description: 'Documentation format',
                  default: 'markdown',
                },
                audience: {
                  type: 'string',
                  enum: ['developers', 'api-users', 'end-users'],
                  description: 'Target audience for documentation',
                  default: 'developers',
                },
                includeExamples: {
                  type: 'boolean',
                  description: 'Include code examples in documentation',
                  default: true,
                },
              },
              required: ['source'],
            },
          },
          {
            name: 'analyze_code',
            description: 'Analyze code for quality, security, and performance issues',
            inputSchema: {
              type: 'object',
              properties: {
                filename: {
                  type: 'string',
                  description: 'File to analyze',
                },
                analysisType: {
                  type: 'string',
                  enum: ['quality', 'security', 'performance', 'maintainability', 'all'],
                  description: 'Type of analysis to perform',
                  default: 'all',
                },
                standards: {
                  type: 'string',
                  description: 'Coding standards to check against (e.g., eslint, pep8, owasp)',
                },
              },
              required: ['filename'],
            },
          },
          {
            name: 'generate_api_docs',
            description: 'Generate API documentation from source code',
            inputSchema: {
              type: 'object',
              properties: {
                apiFiles: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'List of API endpoint files',
                },
                format: {
                  type: 'string',
                  enum: ['openapi', 'swagger', 'markdown'],
                  description: 'API documentation format',
                  default: 'openapi',
                },
                baseUrl: {
                  type: 'string',
                  description: 'Base URL for the API',
                  default: 'https://api.example.com',
                },
              },
              required: ['apiFiles'],
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
            
            await fs.mkdir(path.dirname(writeFilePath), { recursive: true });
            
            // Backup existing file
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

          case 'generate_tests':
            const sourceFilePath = this.validateFilePath(args.sourceFile);
            const sourceCode = await fs.readFile(sourceFilePath, 'utf-8');
            const projectContext = await this.readProjectContext();

            const testPrompt = `You are an expert test engineer. Generate comprehensive ${args.testType} tests for the following code.

Project Context:
- Tech Stack: ${projectContext.techStack}
- Testing Framework: ${args.framework}
- Target Coverage: ${args.coverage}%

Source Code (${args.sourceFile}):
\`\`\`
${sourceCode}
\`\`\`

Generate ${args.testType} tests that:
1. Cover all functions and methods (aim for ${args.coverage}% coverage)
2. Test both happy path and error cases
3. Include edge cases and boundary conditions
4. Use ${args.framework} syntax and best practices
5. Include setup/teardown if needed
6. Have descriptive test names
7. Test async operations properly
8. Mock external dependencies appropriately

Provide complete, runnable test code:`;

            const testCode = await this.makeGeminiRequest(testPrompt, {
              temperature: 0.3,
              maxTokens: 6000
            });

            return {
              content: [{
                type: 'text',
                text: testCode
              }]
            };

          case 'generate_documentation':
            let sourceContent = '';
            const sourcePath = this.validateFilePath(args.source);
            
            try {
              const stats = await fs.stat(sourcePath);
              if (stats.isFile()) {
                sourceContent = await fs.readFile(sourcePath, 'utf-8');
              } else if (stats.isDirectory()) {
                // Read multiple files from directory
                const files = await fs.readdir(sourcePath);
                const codeFiles = files.filter(f => ALLOWED_EXTENSIONS.includes(path.extname(f)));
                const fileContents = await Promise.all(
                  codeFiles.slice(0, 5).map(async f => {
                    const content = await fs.readFile(path.join(sourcePath, f), 'utf-8');
                    return `File: ${f}\n\`\`\`\n${content}\n\`\`\`\n`;
                  })
                );
                sourceContent = fileContents.join('\n');
              }
            } catch (error) {
              throw new Error(`Could not read source: ${error.message}`);
            }

            const docContext = await this.readProjectContext();

            const docPrompt = `You are a technical documentation expert. Generate ${args.format} documentation for the following code.

Project Context:
- Tech Stack: ${docContext.techStack}
- Target Audience: ${args.audience}
- Include Examples: ${args.includeExamples}

Source Code/Files:
${sourceContent}

Generate comprehensive documentation that:
1. Explains the purpose and functionality
2. Documents all public APIs, functions, and classes
3. Includes parameter and return value descriptions
4. ${args.includeExamples ? 'Provides clear usage examples' : 'Focuses on API reference'}
5. Follows ${args.format} standards and best practices
6. Is appropriate for ${args.audience}
7. Includes installation/setup instructions if applicable
8. Documents error handling and edge cases

Format the output as ${args.format}:`;

            const documentation = await this.makeGeminiRequest(docPrompt, {
              temperature: 0.2,
              maxTokens: 8000
            });

            return {
              content: [{
                type: 'text',
                text: documentation
              }]
            };

          case 'analyze_code':
            const analyzeFilePath = this.validateFilePath(args.filename);
            const analyzeCode = await fs.readFile(analyzeFilePath, 'utf-8');
            const analyzeContext = await this.readProjectContext();

            const analysisPrompt = `You are a senior code reviewer and security expert. Analyze the following code for ${args.analysisType} issues.

Project Context:
- Tech Stack: ${analyzeContext.techStack}
- Standards: ${args.standards || 'Industry best practices'}

Code to Analyze (${args.filename}):
\`\`\`
${analyzeCode}
\`\`\`

Perform a comprehensive ${args.analysisType} analysis focusing on:

${args.analysisType === 'quality' || args.analysisType === 'all' ? `
QUALITY:
- Code structure and organization
- Naming conventions
- Documentation and comments
- Error handling
- Code duplication
- Complexity metrics` : ''}

${args.analysisType === 'security' || args.analysisType === 'all' ? `
SECURITY:
- Input validation vulnerabilities
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Data exposure risks
- Dependency vulnerabilities` : ''}

${args.analysisType === 'performance' || args.analysisType === 'all' ? `
PERFORMANCE:
- Algorithmic complexity
- Memory usage patterns
- Database query efficiency
- Caching opportunities
- Bottlenecks and inefficiencies` : ''}

${args.analysisType === 'maintainability' || args.analysisType === 'all' ? `
MAINTAINABILITY:
- Code modularity
- Coupling and cohesion
- Testability
- Configuration management
- Dependencies and architecture` : ''}

For each issue found, provide:
1. Severity level (Critical, High, Medium, Low)
2. Description of the issue
3. Location in code (line number if possible)
4. Specific fix recommendation
5. Code example of the fix

Format as a structured analysis report:`;

            const analysis = await this.makeGeminiRequest(analysisPrompt, {
              temperature: 0.1,
              maxTokens: 6000
            });

            return {
              content: [{
                type: 'text',
                text: analysis
              }]
            };

          case 'generate_api_docs':
            const apiContents = await Promise.all(
              args.apiFiles.map(async file => {
                const filePath = this.validateFilePath(file);
                const content = await fs.readFile(filePath, 'utf-8');
                return `File: ${file}\n\`\`\`\n${content}\n\`\`\`\n`;
              })
            );

            const apiPrompt = `You are an API documentation specialist. Generate ${args.format} documentation for the following API endpoints.

Base URL: ${args.baseUrl}

API Source Files:
${apiContents.join('\n')}

Generate comprehensive API documentation that includes:
1. Overview and authentication
2. All endpoints with HTTP methods
3. Request/response schemas
4. Parameter descriptions (path, query, body)
5. Response codes and error handling
6. Usage examples with curl/code samples
7. Rate limiting and versioning info
8. Data models and schemas

Format as ${args.format} specification:`;

            const apiDocs = await this.makeGeminiRequest(apiPrompt, {
              temperature: 0.1,
              maxTokens: 8000
            });

            return {
              content: [{
                type: 'text',
                text: apiDocs
              }]
            };

          case 'get_usage_stats':
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  service: 'Gemini 1.5 Pro',
                  usedRequests: this.usageCount,
                  dailyLimit: DAILY_RATE_LIMIT,
                  remainingRequests: DAILY_RATE_LIMIT - this.usageCount,
                  resetTime: this.usageResetDate.toISOString(),
                  percentageUsed: Math.round((this.usageCount / DAILY_RATE_LIMIT) * 100)
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
    console.error('Gemini MCP Server running on stdio');
  }
}

// Run the server
if (require.main === module) {
  const server = new GeminiMCPServer();
  server.run().catch((error) => {
    console.error('Fatal error in Gemini MCP Server:', error);
    process.exit(1);
  });
}

module.exports = { GeminiMCPServer };