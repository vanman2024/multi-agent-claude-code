# Conventions - Multi-Agent Development Framework

## Coding Standards & Naming Conventions

### File and Directory Structure
```
project/
├── docs/                          # Documentation files
│   ├── ARCHITECTURE.md           # System design
│   ├── FEATURES.md               # Feature specifications
│   ├── INFRASTRUCTURE.md         # Deployment and hosting
│   └── CONVENTIONS.md            # This file
├── .claude/                      # Claude Code configuration
│   ├── commands/                 # Slash commands
│   ├── agents/                   # Agent configurations
│   └── settings.json            # Claude settings
├── scripts/                      # Automation scripts
│   ├── mcp-servers/             # MCP server implementations
│   ├── automation/              # CI/CD and workflow scripts
│   └── utilities/               # Helper scripts
├── templates/                    # Project templates
│   ├── issues/                  # Issue templates
│   └── guides/                  # Setup and usage guides
└── PROJECT_CONTEXT.md           # Current project state
```

### Naming Conventions

#### Files and Directories
- **Documentation**: `UPPERCASE.md` for major docs, `lowercase.md` for guides
- **Scripts**: `kebab-case.js/py/sh` for all script files
- **Directories**: `lowercase` or `kebab-case` for directory names
- **MCP Servers**: `service-name-mcp-server.js` (e.g., `together-ai-mcp-server.js`)

#### Code Elements
```typescript
// Variables and functions: camelCase
const projectContext = await readProjectContext();
const generateCode = async (task: string) => { ... };

// Constants: SCREAMING_SNAKE_CASE
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const API_RATE_LIMITS = {
  TOGETHER_AI: 3000,
  GEMINI: 1500,
  HUGGINGFACE: 30000
};

// Interfaces and types: PascalCase
interface ProjectContext {
  currentGoals: string[];
  activeFeatures: Feature[];
}

// MCP Server classes: PascalCase with "MCP" suffix
class TogetherAIMCPServer implements EnhancedMCPServer { ... }
```

## Code Quality Standards

### JavaScript/TypeScript Standards
```typescript
// Always use TypeScript for MCP server implementations
// Enable strict mode and all recommended type checking
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "exactOptionalPropertyTypes": true
  }
}

// Use async/await instead of promises
async function readSourceFile(filename: string): Promise<string> {
  try {
    const content = await fs.readFile(filename, 'utf-8');
    return content;
  } catch (error) {
    throw new Error(`Failed to read file ${filename}: ${error.message}`);
  }
}

// Always validate inputs
function validateFilePath(path: string): void {
  if (!path || typeof path !== 'string') {
    throw new Error('File path must be a non-empty string');
  }
  
  if (path.includes('..') || path.startsWith('/')) {
    throw new Error('File path must be relative and within project directory');
  }
}
```

### Python Standards
```python
# Use type hints for all function signatures
from typing import Dict, List, Optional, Union
import asyncio

async def generate_tests(
    source_file: str, 
    context: Dict[str, Union[str, List[str]]]
) -> str:
    """Generate test cases for the given source file.
    
    Args:
        source_file: Path to source file to test
        context: Project context dictionary
        
    Returns:
        Generated test code as string
        
    Raises:
        FileNotFoundError: If source file doesn't exist
        ValidationError: If file is not testable
    """
    # Implementation here
    pass

# Use dataclasses for structured data
from dataclasses import dataclass

@dataclass
class ApiUsage:
    service: str
    requests_used: int
    requests_limit: int
    reset_date: str
```

### Shell Script Standards
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Use functions for reusable code
setup_mcp_server() {
  local server_name="$1"
  local server_command="$2"
  
  echo "Setting up MCP server: $server_name"
  claude mcp add "$server_name" -- $server_command
  
  if ! claude mcp list | grep -q "$server_name"; then
    echo "❌ Failed to add $server_name MCP server"
    exit 1
  fi
  
  echo "✅ $server_name MCP server added successfully"
}

# Always validate prerequisites
check_prerequisites() {
  command -v claude >/dev/null 2>&1 || {
    echo "❌ Claude Code CLI not found. Please install first."
    exit 1
  }
  
  command -v gh >/dev/null 2>&1 || {
    echo "❌ GitHub CLI not found. Please install first."
    exit 1
  }
}
```

## Documentation Standards

### Markdown Conventions
```markdown
# Use H1 for main title only
## H2 for major sections
### H3 for subsections
#### H4 for details (avoid deeper nesting)

<!-- Always include status indicators -->
**Status**: ✅ Complete | 🔄 In Progress | 📋 Planned | ❌ Blocked

<!-- Use emoji for visual clarity -->
- ✅ Completed items
- 🔄 In progress items
- 📋 Planned items
- ⚠️ Warnings or important notes
- 💡 Tips or suggestions
- 🔒 Security considerations

<!-- Code blocks with language specification -->
```typescript
// Always specify language for syntax highlighting
interface Example {
  property: string;
}
```

<!-- Use tables for structured data -->
| Service | Free Tier | Paid Tier | Use Case |
|---------|-----------|-----------|----------|
| Together AI | 3000/month | $0.20/1M | Code generation |
```

### API Documentation
```typescript
/**
 * Enhanced MCP Server interface for AI model integration
 * 
 * @interface EnhancedMCPServer
 * @description Provides standardized methods for AI model interaction with file access
 */
interface EnhancedMCPServer {
  /**
   * Read current project context from PROJECT_CONTEXT.md
   * 
   * @returns Promise<ProjectContext> Current project state and goals
   * @throws {Error} If PROJECT_CONTEXT.md cannot be read
   */
  readProjectContext(): Promise<ProjectContext>;
  
  /**
   * Read source file content with security validation
   * 
   * @param filename - Relative path to file within project directory
   * @returns Promise<string> File content as UTF-8 string
   * @throws {SecurityError} If file is outside project scope
   * @throws {FileNotFoundError} If file doesn't exist
   */
  readSourceFile(filename: string): Promise<string>;
}
```

## Version Control Conventions

### Branch Naming
```bash
# Feature branches
feature/mcp-server-integration
feature/together-ai-integration

# Bug fixes
fix/rate-limit-handling
fix/file-access-security

# Agent-specific branches (for Copilot)
copilot/feature-name
copilot/fix-description

# Documentation updates
docs/update-architecture
docs/add-conventions
```

### Commit Message Format
```
type: brief description (50 chars max)

Longer explanation if needed (wrap at 72 chars)
- Use bullet points for multiple changes
- Reference issues with #123 format

Types:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- refactor: code refactoring
- test: adding tests
- chore: maintenance tasks
- mcp: MCP server related changes
```

### Commit Examples
```bash
feat: add Together AI MCP server with file access

- Implement TogetherAIMCPServer class with enhanced interface
- Add file read/write capabilities with security validation
- Include rate limiting and usage tracking
- Add comprehensive error handling

Fixes #152

---

mcp: add Gemini 1.5 Pro server for test generation

- Create GeminiMCPServer with specialized test generation
- Implement project context reading
- Add documentation generation capabilities
- Include 1500/day rate limit tracking

Related to #152

---

docs: update CONVENTIONS.md with MCP server standards

- Add coding standards for TypeScript MCP servers
- Document naming conventions for server files
- Include error handling patterns
- Add API documentation templates
```

## Testing Standards

### Unit Test Conventions
```typescript
// Use descriptive test names
describe('TogetherAIMCPServer', () => {
  describe('readSourceFile', () => {
    it('should read valid project file successfully', async () => {
      // Arrange
      const server = new TogetherAIMCPServer();
      const filename = 'src/example.js';
      
      // Act
      const content = await server.readSourceFile(filename);
      
      // Assert
      expect(content).toContain('function example()');
    });
    
    it('should throw SecurityError for path traversal attempt', async () => {
      // Arrange
      const server = new TogetherAIMCPServer();
      const filename = '../../../etc/passwd';
      
      // Act & Assert
      await expect(server.readSourceFile(filename))
        .rejects.toThrow(SecurityError);
    });
  });
});
```

### Integration Test Standards
```typescript
// Test complete workflows, not just individual functions
describe('MCP Server Integration', () => {
  it('should complete code generation workflow end-to-end', async () => {
    // Arrange
    const context = await readProjectContext();
    const task = 'Generate a user authentication function';
    
    // Act
    const generatedCode = await mcpServer.generateCode(task, context);
    await mcpServer.writeFile('src/auth.js', generatedCode);
    
    // Assert
    const writtenFile = await mcpServer.readSourceFile('src/auth.js');
    expect(writtenFile).toContain('function authenticate');
    expect(writtenFile).toContain('password');
    expect(writtenFile).toContain('token');
  });
});
```

## Security Conventions

### API Key Management
```typescript
// Always use environment variables for API keys
const TOGETHER_AI_API_KEY = process.env.TOGETHER_AI_API_KEY;
if (!TOGETHER_AI_API_KEY) {
  throw new Error('TOGETHER_AI_API_KEY environment variable is required');
}

// Never log API keys or sensitive data
logger.info(`Making request to Together AI API`, {
  endpoint: '/completions',
  // Do NOT log: apiKey, token, or other sensitive data
});
```

### File Access Security
```typescript
// Always validate file paths
function validateFilePath(path: string): void {
  // Block path traversal
  if (path.includes('..') || path.includes('~')) {
    throw new SecurityError('Path traversal not allowed');
  }
  
  // Block absolute paths
  if (path.startsWith('/') || /^[a-zA-Z]:/.test(path)) {
    throw new SecurityError('Absolute paths not allowed');
  }
  
  // Block sensitive files
  const sensitiveFiles = ['.env', '.git', 'node_modules'];
  if (sensitiveFiles.some(pattern => path.includes(pattern))) {
    throw new SecurityError('Access to sensitive files not allowed');
  }
}
```

## Performance Standards

### Response Time Targets
```typescript
interface PerformanceTargets {
  mcpServerResponse: 500; // milliseconds
  fileOperation: 100;     // milliseconds
  apiCall: 2000;         // milliseconds
  contextLoad: 200;      // milliseconds
}

// Implement timeouts for all operations
const generateCodeWithTimeout = async (task: string): Promise<string> => {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Operation timeout')), 2000);
  });
  
  return Promise.race([
    generateCode(task),
    timeoutPromise
  ]);
};
```

### Memory Management
```typescript
// Use streaming for large files
async function readLargeFile(filename: string): Promise<string> {
  const maxSize = 10 * 1024 * 1024; // 10MB limit
  const stats = await fs.stat(filename);
  
  if (stats.size > maxSize) {
    throw new Error(`File too large: ${stats.size} bytes (max: ${maxSize})`);
  }
  
  return fs.readFile(filename, 'utf-8');
}
```

## Error Handling Conventions

### Structured Error Types
```typescript
// Define specific error types for different failure modes
class SecurityError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'SecurityError';
  }
}

class RateLimitError extends Error {
  constructor(service: string, resetTime: Date) {
    super(`Rate limit exceeded for ${service}. Resets at ${resetTime}`);
    this.name = 'RateLimitError';
  }
}

class FileAccessError extends Error {
  constructor(filename: string, operation: string, cause: Error) {
    super(`Failed to ${operation} file ${filename}: ${cause.message}`);
    this.name = 'FileAccessError';
    this.cause = cause;
  }
}
```

### Error Recovery Patterns
```typescript
// Implement retry logic with exponential backoff
async function withRetry<T>(
  operation: () => Promise<T>,
  maxAttempts: number = 3
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      
      const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw new Error('Retry logic failed'); // This should never be reached
}
```

---

These conventions ensure consistency, maintainability, and security across the entire Multi-Agent Development Framework. All contributors should follow these standards to maintain code quality and system reliability.