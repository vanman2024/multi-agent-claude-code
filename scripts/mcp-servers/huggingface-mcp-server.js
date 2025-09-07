#!/usr/bin/env node

/**
 * HuggingFace Inference MCP Server
 * Provides access to specialized models via HuggingFace Inference API
 * Free tier: 30,000 characters/month
 */

const { Server } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/index.js');
const { StdioServerTransport } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('./../../node_modules/@modelcontextprotocol/sdk/dist/types.js');
const fs = require('fs').promises;
const path = require('path');

// Configuration
const API_BASE_URL = 'https://api-inference.huggingface.co';
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB (smaller due to character limits)
const MONTHLY_CHAR_LIMIT = 30000; // characters per month
const ALLOWED_EXTENSIONS = ['.js', '.ts', '.py', '.md', '.json', '.sql', '.txt'];

// Available models on HuggingFace
const MODELS = {
  'code-generation': 'bigcode/starcoder2-7b',
  'sql-generation': 'defog/sqlcoder-7b-2',
  'code-completion': 'Salesforce/codegen-2B-mono',
  'python-specialist': 'microsoft/DialoGPT-medium',
  'text-to-code': 'microsoft/CodeBERT-base',
  'code-explanation': 'huggingface/CodeBERTa-small-v1'
};

class HuggingFaceMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'huggingface-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.apiToken = process.env.HUGGINGFACE_API_TOKEN;
    this.projectRoot = process.cwd();
    this.charactersUsed = 0;
    this.usageResetDate = this.getMonthlyResetDate();

    this.setupHandlers();
  }

  getMonthlyResetDate() {
    const now = new Date();
    const nextMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1);
    return nextMonth;
  }

  validateApiToken() {
    if (!this.apiToken) {
      throw new Error('HUGGINGFACE_API_TOKEN environment variable is required');
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

  async checkCharacterLimit(inputText) {
    if (new Date() > this.usageResetDate) {
      this.charactersUsed = 0;
      this.usageResetDate = this.getMonthlyResetDate();
    }

    const estimatedChars = inputText.length * 2; // Estimate input + output
    if (this.charactersUsed + estimatedChars > MONTHLY_CHAR_LIMIT) {
      throw new Error(`Character limit exceeded. Used: ${this.charactersUsed}/${MONTHLY_CHAR_LIMIT}. Resets: ${this.usageResetDate.toDateString()}`);
    }
  }

  async makeHuggingFaceRequest(model, inputs, options = {}) {
    await this.checkCharacterLimit(inputs);
    this.validateApiToken();

    const requestBody = {
      inputs: inputs,
      parameters: {
        max_new_tokens: options.maxTokens || 512,
        temperature: options.temperature || 0.7,
        top_p: options.topP || 0.9,
        do_sample: true,
        ...options.parameters
      },
      options: {
        wait_for_model: true,
        use_cache: false
      }
    };

    try {
      const response = await fetch(`${API_BASE_URL}/models/${model}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HuggingFace API error: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      
      // Track character usage
      const responseText = Array.isArray(data) ? data[0]?.generated_text || '' : data.generated_text || '';
      this.charactersUsed += inputs.length + responseText.length;
      
      return responseText;
    } catch (error) {
      throw new Error(`HuggingFace request failed: ${error.message}`);
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
            name: 'generate_sql',
            description: 'Generate SQL queries using SQLCoder specialized model',
            inputSchema: {
              type: 'object',
              properties: {
                description: {
                  type: 'string',
                  description: 'Natural language description of the SQL query needed',
                },
                database: {
                  type: 'string',
                  description: 'Database type (postgresql, mysql, sqlite)',
                  default: 'postgresql',
                },
                schema: {
                  type: 'string',
                  description: 'Database schema information (optional)',
                },
              },
              required: ['description'],
            },
          },
          {
            name: 'generate_specialized_code',
            description: 'Generate code using specialized models for specific domains',
            inputSchema: {
              type: 'object',
              properties: {
                task: {
                  type: 'string',
                  description: 'Description of the code to generate',
                },
                specialty: {
                  type: 'string',
                  enum: ['code-generation', 'python-specialist', 'text-to-code', 'code-completion'],
                  description: 'Specialized model to use',
                  default: 'code-generation',
                },
                language: {
                  type: 'string',
                  description: 'Programming language',
                  default: 'python',
                },
                context: {
                  type: 'string',
                  description: 'Additional context for code generation',
                },
              },
              required: ['task'],
            },
          },
          {
            name: 'explain_code',
            description: 'Explain existing code using code analysis models',
            inputSchema: {
              type: 'object',
              properties: {
                filename: {
                  type: 'string',
                  description: 'File containing code to explain',
                },
                focus: {
                  type: 'string',
                  description: 'What aspect to focus on (algorithm, purpose, optimization)',
                  default: 'purpose',
                },
              },
              required: ['filename'],
            },
          },
          {
            name: 'generate_data_science_code',
            description: 'Generate data science and ML code patterns',
            inputSchema: {
              type: 'object',
              properties: {
                task: {
                  type: 'string',
                  description: 'Data science task description',
                },
                framework: {
                  type: 'string',
                  enum: ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
                  description: 'Framework to use',
                  default: 'pandas',
                },
                dataType: {
                  type: 'string',
                  description: 'Type of data being processed (csv, json, database)',
                  default: 'csv',
                },
              },
              required: ['task'],
            },
          },
          {
            name: 'generate_frontend_component',
            description: 'Generate frontend components using web-specialized models',
            inputSchema: {
              type: 'object',
              properties: {
                component: {
                  type: 'string',
                  description: 'Component description',
                },
                framework: {
                  type: 'string',
                  enum: ['react', 'vue', 'angular', 'vanilla'],
                  description: 'Frontend framework',
                  default: 'react',
                },
                styling: {
                  type: 'string',
                  enum: ['css', 'tailwind', 'styled-components', 'emotion'],
                  description: 'Styling approach',
                  default: 'tailwind',
                },
              },
              required: ['component'],
            },
          },
          {
            name: 'list_available_models',
            description: 'List available specialized models and their use cases',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'get_usage_stats',
            description: 'Get current character usage statistics',
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

          case 'generate_sql':
            const projectContext = await this.readProjectContext();
            
            const sqlPrompt = `Generate a ${args.database} SQL query for the following requirement:

${args.description}

${args.schema ? `Database Schema:\n${args.schema}` : ''}

Generate clean, efficient SQL that:
1. Follows ${args.database} best practices
2. Uses proper indexing considerations
3. Handles edge cases
4. Is optimized for performance

SQL Query:`;

            const sqlResult = await this.makeHuggingFaceRequest(
              MODELS['sql-generation'],
              sqlPrompt,
              {
                maxTokens: 256,
                temperature: 0.1
              }
            );

            return {
              content: [{
                type: 'text',
                text: sqlResult
              }]
            };

          case 'generate_specialized_code':
            const codeContext = await this.readProjectContext();
            
            const codePrompt = `Generate ${args.language} code for the following task:

Task: ${args.task}
Language: ${args.language}
${args.context ? `Context: ${args.context}` : ''}

Project Context: ${codeContext.techStack}

Generate clean, production-ready code that:
1. Follows ${args.language} best practices
2. Includes proper error handling
3. Is well-documented
4. Is modular and reusable

Code:`;

            const codeResult = await this.makeHuggingFaceRequest(
              MODELS[args.specialty],
              codePrompt,
              {
                maxTokens: 512,
                temperature: 0.3
              }
            );

            return {
              content: [{
                type: 'text',
                text: codeResult
              }]
            };

          case 'explain_code':
            const explainFilePath = this.validateFilePath(args.filename);
            const codeToExplain = await fs.readFile(explainFilePath, 'utf-8');

            // Truncate if too long for character limit
            const truncatedCode = codeToExplain.length > 1000 ? 
              codeToExplain.substring(0, 1000) + '\n// ... (truncated)' : 
              codeToExplain;

            const explainPrompt = `Explain the following code, focusing on ${args.focus}:

\`\`\`
${truncatedCode}
\`\`\`

Provide a clear explanation covering:
1. What the code does
2. How it works
3. Key algorithms or patterns used
4. Potential improvements or optimizations

Explanation:`;

            const explanation = await this.makeHuggingFaceRequest(
              MODELS['code-explanation'],
              explainPrompt,
              {
                maxTokens: 300,
                temperature: 0.2
              }
            );

            return {
              content: [{
                type: 'text',
                text: explanation
              }]
            };

          case 'generate_data_science_code':
            const dsPrompt = `Generate Python data science code using ${args.framework} for:

Task: ${args.task}
Framework: ${args.framework}
Data Type: ${args.dataType}

Generate code that:
1. Handles ${args.dataType} data efficiently
2. Uses ${args.framework} best practices
3. Includes proper error handling
4. Has clear documentation
5. Is production-ready

Code:`;

            const dsCode = await this.makeHuggingFaceRequest(
              MODELS['python-specialist'],
              dsPrompt,
              {
                maxTokens: 400,
                temperature: 0.3
              }
            );

            return {
              content: [{
                type: 'text',
                text: dsCode
              }]
            };

          case 'generate_frontend_component':
            const fePrompt = `Generate a ${args.framework} component with ${args.styling} styling:

Component: ${args.component}
Framework: ${args.framework}
Styling: ${args.styling}

Generate a component that:
1. Follows ${args.framework} best practices
2. Uses ${args.styling} for styling
3. Is accessible and responsive
4. Includes proper prop types/interfaces
5. Is reusable and well-documented

Component Code:`;

            const feCode = await this.makeHuggingFaceRequest(
              MODELS['code-generation'],
              fePrompt,
              {
                maxTokens: 400,
                temperature: 0.4
              }
            );

            return {
              content: [{
                type: 'text',
                text: feCode
              }]
            };

          case 'list_available_models':
            const modelList = Object.entries(MODELS).map(([use, model]) => ({
              useCase: use,
              model: model,
              description: this.getModelDescription(use)
            }));

            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  availableModels: modelList,
                  characterLimit: MONTHLY_CHAR_LIMIT,
                  charactersUsed: this.charactersUsed,
                  resetDate: this.usageResetDate.toISOString()
                }, null, 2)
              }]
            };

          case 'get_usage_stats':
            return {
              content: [{
                type: 'text',
                text: JSON.stringify({
                  service: 'HuggingFace Inference',
                  charactersUsed: this.charactersUsed,
                  monthlyLimit: MONTHLY_CHAR_LIMIT,
                  remainingCharacters: MONTHLY_CHAR_LIMIT - this.charactersUsed,
                  resetDate: this.usageResetDate.toISOString(),
                  percentageUsed: Math.round((this.charactersUsed / MONTHLY_CHAR_LIMIT) * 100),
                  estimatedRequestsRemaining: Math.floor((MONTHLY_CHAR_LIMIT - this.charactersUsed) / 500)
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

  getModelDescription(useCase) {
    const descriptions = {
      'code-generation': 'General purpose code generation and completion',
      'sql-generation': 'Specialized SQL query generation and optimization',
      'code-completion': 'Code completion and suggestion',
      'python-specialist': 'Python-focused code generation and data science',
      'text-to-code': 'Natural language to code conversion',
      'code-explanation': 'Code analysis and explanation'
    };
    return descriptions[useCase] || 'Specialized model';
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('HuggingFace MCP Server running on stdio');
  }
}

// Run the server
if (require.main === module) {
  const server = new HuggingFaceMCPServer();
  server.run().catch((error) => {
    console.error('Fatal error in HuggingFace MCP Server:', error);
    process.exit(1);
  });
}

module.exports = { HuggingFaceMCPServer };