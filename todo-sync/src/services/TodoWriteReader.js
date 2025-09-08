import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';
import { logger } from '../utils/logger.js';
import { v4 as uuidv4 } from 'uuid';

export class TodoWriteReader {
    constructor() {
        this.projectPaths = this.getProjectPaths();
        this.todoCache = new Map();
        this.lastScanTime = 0;
        this.cacheTTL = 60000; // 1 minute cache
    }

    getProjectPaths() {
        // Default project paths based on common Claude Code usage patterns
        const homePath = process.env.HOME || '/home/gotime2022';
        
        return [
            path.join(homePath, 'Projects', 'multi-agent-claude-code'),
            path.join(homePath, 'Projects', 'mcp-kernel-new'),
            path.join(homePath, 'Projects', 'recruitment-ops'),
            path.join(homePath, 'Projects', 'test-todo-app'),
            path.join(homePath, 'multi-agent-observability-system'),
            path.join(homePath, 'synapseai'),
            path.join(homePath, 'project-seed'),
            // Add more project paths as needed
        ];
    }

    async getAllTodos(forceRefresh = false) {
        const now = Date.now();
        
        // Return cached data if it's still valid
        if (!forceRefresh && (now - this.lastScanTime) < this.cacheTTL && this.todoCache.size > 0) {
            return Array.from(this.todoCache.values());
        }

        const allTodos = [];
        
        for (const projectPath of this.projectPaths) {
            try {
                const projectTodos = await this.getProjectTodos(projectPath);
                allTodos.push(...projectTodos);
            } catch (error) {
                // Log but continue - project might not exist or be accessible
                logger.debug(`Could not read todos from ${projectPath}:`, error.message);
            }
        }

        // Update cache
        this.todoCache.clear();
        allTodos.forEach(todo => {
            const key = `${todo.projectPath}-${todo.sessionId}-${todo.content}`;
            this.todoCache.set(key, todo);
        });
        
        this.lastScanTime = now;
        
        logger.info(`Found ${allTodos.length} todos across ${this.projectPaths.length} projects`);
        return allTodos;
    }

    async getProjectTodos(projectPath) {
        const todos = [];
        
        try {
            await fs.access(projectPath);
        } catch (error) {
            // Project doesn't exist or isn't accessible
            return todos;
        }

        // Look for Claude Code workspace files
        const claudePaths = [
            path.join(projectPath, '.claude'),
            path.join(projectPath, '.claude-code'),
            path.join(projectPath, 'claude-workspace')
        ];

        // Check for session files and todo data
        for (const claudePath of claudePaths) {
            try {
                await fs.access(claudePath);
                const sessionTodos = await this.scanClaudeDirectory(claudePath, projectPath);
                todos.push(...sessionTodos);
            } catch (error) {
                // Claude directory doesn't exist, continue
                continue;
            }
        }

        // Also check for standalone todo files in project root
        const standaloneTodos = await this.scanForStandaloneTodos(projectPath);
        todos.push(...standaloneTodos);

        return todos;
    }

    async scanClaudeDirectory(claudePath, projectPath) {
        const todos = [];
        
        try {
            // Look for session directories or files
            const entries = await fs.readdir(claudePath, { withFileTypes: true });
            
            for (const entry of entries) {
                const fullPath = path.join(claudePath, entry.name);
                
                if (entry.isDirectory()) {
                    // Scan subdirectories for todo files
                    const subTodos = await this.scanDirectoryForTodos(fullPath, projectPath);
                    todos.push(...subTodos);
                } else if (entry.isFile()) {
                    // Check if it's a todo-related file
                    if (this.isTodoFile(entry.name)) {
                        const fileTodos = await this.parseTodoFile(fullPath, projectPath);
                        todos.push(...fileTodos);
                    }
                }
            }
        } catch (error) {
            logger.debug(`Error scanning Claude directory ${claudePath}:`, error.message);
        }
        
        return todos;
    }

    async scanDirectoryForTodos(directory, projectPath) {
        const todos = [];
        
        try {
            // Recursively look for todo files
            const todoFiles = await glob('**/*todo*.json', {
                cwd: directory,
                ignore: ['node_modules/**', '.git/**', '**/dist/**', '**/build/**']
            });

            for (const file of todoFiles) {
                const fullPath = path.join(directory, file);
                const fileTodos = await this.parseTodoFile(fullPath, projectPath);
                todos.push(...fileTodos);
            }

            // Also look for Claude Code session files that might contain todos
            const sessionFiles = await glob('**/session-*.json', {
                cwd: directory,
                ignore: ['node_modules/**', '.git/**']
            });

            for (const file of sessionFiles) {
                const fullPath = path.join(directory, file);
                const sessionTodos = await this.parseSessionFile(fullPath, projectPath);
                todos.push(...sessionTodos);
            }

        } catch (error) {
            logger.debug(`Error scanning directory ${directory}:`, error.message);
        }
        
        return todos;
    }

    async scanForStandaloneTodos(projectPath) {
        const todos = [];
        
        try {
            // Look for todo files in common locations
            const todoPatterns = [
                'todo*.json',
                'todos.json',
                '*-todos.json',
                '.todo/*.json'
            ];

            for (const pattern of todoPatterns) {
                const files = await glob(pattern, {
                    cwd: projectPath,
                    ignore: ['node_modules/**', '.git/**', '**/dist/**', '**/build/**']
                });

                for (const file of files) {
                    const fullPath = path.join(projectPath, file);
                    const fileTodos = await this.parseTodoFile(fullPath, projectPath);
                    todos.push(...fileTodos);
                }
            }
        } catch (error) {
            logger.debug(`Error scanning for standalone todos in ${projectPath}:`, error.message);
        }
        
        return todos;
    }

    isTodoFile(filename) {
        const todoIndicators = [
            'todo',
            'todos',
            'task',
            'tasks',
            'work-journal',
            'session'
        ];
        
        const lowerName = filename.toLowerCase();
        return todoIndicators.some(indicator => 
            lowerName.includes(indicator) && lowerName.endsWith('.json')
        );
    }

    async parseTodoFile(filePath, projectPath) {
        try {
            const content = await fs.readFile(filePath, 'utf8');
            const data = JSON.parse(content);
            
            // Handle different todo file formats
            if (Array.isArray(data)) {
                // Simple array of todos
                return this.processTodoArray(data, filePath, projectPath);
            } else if (data.todos && Array.isArray(data.todos)) {
                // Object with todos array
                return this.processTodoArray(data.todos, filePath, projectPath);
            } else if (data.entries && Array.isArray(data.entries)) {
                // Work journal format (like .claude/work-journal.json)
                return this.processWorkJournalEntries(data.entries, filePath, projectPath);
            } else {
                // Single todo object
                return this.processTodoArray([data], filePath, projectPath);
            }
        } catch (error) {
            logger.debug(`Error parsing todo file ${filePath}:`, error.message);
            return [];
        }
    }

    async parseSessionFile(filePath, projectPath) {
        try {
            const content = await fs.readFile(filePath, 'utf8');
            const data = JSON.parse(content);
            
            const todos = [];
            const sessionId = this.extractSessionId(filePath);
            
            // Look for todo-related data in session
            if (data.todos) {
                todos.push(...this.processTodoArray(data.todos, filePath, projectPath, sessionId));
            }
            
            // Look for todo patterns in session messages or context
            if (data.messages) {
                todos.push(...this.extractTodosFromMessages(data.messages, filePath, projectPath, sessionId));
            }
            
            return todos;
        } catch (error) {
            logger.debug(`Error parsing session file ${filePath}:`, error.message);
            return [];
        }
    }

    processTodoArray(todosArray, filePath, projectPath, sessionId = null) {
        const todos = [];
        const extractedSessionId = sessionId || this.extractSessionId(filePath);
        
        for (const todoItem of todosArray) {
            if (typeof todoItem === 'string') {
                // Simple string todo
                todos.push(this.createTodoObject(todoItem, 'pending', null, extractedSessionId, projectPath, filePath));
            } else if (typeof todoItem === 'object' && todoItem.content) {
                // Structured todo object
                todos.push(this.createTodoObject(
                    todoItem.content,
                    todoItem.status || 'pending',
                    todoItem.activeForm,
                    extractedSessionId,
                    projectPath,
                    filePath,
                    todoItem
                ));
            }
        }
        
        return todos;
    }

    processWorkJournalEntries(entries, filePath, projectPath) {
        // Work journal entries don't directly contain todos but might have todo-related info
        // This is mainly for future enhancement if work journal starts tracking todos
        return [];
    }

    extractTodosFromMessages(messages, filePath, projectPath, sessionId) {
        const todos = [];
        
        // Look for messages that contain TodoWrite tool usage
        for (const message of messages) {
            if (message.tool_calls) {
                for (const toolCall of message.tool_calls) {
                    if (toolCall.name === 'TodoWrite' && toolCall.arguments) {
                        try {
                            const args = typeof toolCall.arguments === 'string' 
                                ? JSON.parse(toolCall.arguments) 
                                : toolCall.arguments;
                            
                            if (args.todos && Array.isArray(args.todos)) {
                                todos.push(...this.processTodoArray(args.todos, filePath, projectPath, sessionId));
                            }
                        } catch (error) {
                            logger.debug(`Error parsing TodoWrite arguments:`, error.message);
                        }
                    }
                }
            }
        }
        
        return todos;
    }

    createTodoObject(content, status, activeForm, sessionId, projectPath, filePath, originalData = null) {
        return {
            content: content.trim(),
            status: status || 'pending',
            activeForm: activeForm || null,
            sessionId: sessionId || this.generateSessionId(filePath),
            projectPath: projectPath,
            sourceFile: filePath,
            createdAt: originalData?.createdAt || this.getFileCreationTime(filePath),
            updatedAt: originalData?.updatedAt || new Date().toISOString(),
            
            // Additional metadata that might be useful
            originalData: originalData ? {
                ...originalData,
                sourceFile: filePath
            } : null
        };
    }

    extractSessionId(filePath) {
        // Try to extract session ID from file path or name
        const basename = path.basename(filePath);
        
        // Look for session-<id> pattern
        const sessionMatch = basename.match(/session-([a-f0-9-]+)/i);
        if (sessionMatch) {
            return sessionMatch[1];
        }
        
        // Look for timestamp-based session IDs
        const timestampMatch = basename.match(/(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})/);
        if (timestampMatch) {
            return timestampMatch[1];
        }
        
        // Generate a deterministic session ID based on file path
        return this.generateSessionId(filePath);
    }

    generateSessionId(filePath) {
        // Generate a consistent session ID based on the file path
        const crypto = require('crypto');
        return crypto.createHash('md5').update(filePath).digest('hex').substring(0, 8);
    }

    async getFileCreationTime(filePath) {
        try {
            const stats = await fs.stat(filePath);
            return stats.birthtime.toISOString();
        } catch (error) {
            return new Date().toISOString();
        }
    }

    // Monitoring and utilities
    getCacheStats() {
        return {
            cacheSize: this.todoCache.size,
            lastScanTime: new Date(this.lastScanTime),
            cacheTTL: this.cacheTTL,
            projectPaths: this.projectPaths
        };
    }

    clearCache() {
        this.todoCache.clear();
        this.lastScanTime = 0;
        logger.info('TodoWrite cache cleared');
    }

    async validateProjectPaths() {
        const validPaths = [];
        const invalidPaths = [];
        
        for (const projectPath of this.projectPaths) {
            try {
                await fs.access(projectPath);
                validPaths.push(projectPath);
            } catch (error) {
                invalidPaths.push(projectPath);
            }
        }
        
        return { validPaths, invalidPaths };
    }

    // Real-time file watching (for future implementation)
    async startWatching() {
        // This could be implemented to watch todo files for changes
        // and emit events when todos are added/modified/removed
        logger.info('File watching not yet implemented');
    }

    stopWatching() {
        // Stop file watching
        logger.info('File watching stopped');
    }
}