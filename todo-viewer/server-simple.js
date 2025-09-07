#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const CLAUDE_TODOS_DIR = path.join(process.env.HOME, '.claude/todos');
const PROJECT_PATH = path.dirname(__dirname); // Get parent directory (project root)

// MIME types for static files
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json'
};

// Get project-specific session IDs
function getProjectSessions(projectPath) {
    const projectKey = projectPath.replace(/\//g, '-').replace(/^-/, '');
    const projectDir = path.join(process.env.HOME, '.claude/projects', projectKey);
    const sessionIds = new Set();
    
    if (fs.existsSync(projectDir)) {
        const files = fs.readdirSync(projectDir);
        files.forEach(file => {
            if (file.endsWith('.jsonl')) {
                const sessionId = file.replace('.jsonl', '');
                sessionIds.add(sessionId);
            }
        });
    }
    
    return sessionIds;
}

// Get all available projects
function getAllProjects() {
    const projectsDir = path.join(process.env.HOME, '.claude/projects');
    const projects = [];
    
    if (fs.existsSync(projectsDir)) {
        const dirs = fs.readdirSync(projectsDir);
        dirs.forEach(dir => {
            // Convert directory name back to path
            const projectPath = '/' + dir.replace(/^-/, '').replace(/-/g, '/');
            projects.push({
                key: dir,
                path: projectPath,
                name: path.basename(projectPath)
            });
        });
    }
    
    return projects;
}

// Function to get todos - optionally filtered by project
function getAllTodos(filterProject = null) {
    try {
        const { execSync } = require('child_process');
        
        // If filtering by project, use the project-todos-table script
        if (filterProject) {
            // Change to the project directory and run the script
            const scriptPath = path.join(filterProject, '.claude/scripts/project-todos-table.sh');
            
            // Check if script exists
            if (!fs.existsSync(scriptPath)) {
                // Fallback to reading all todos if script doesn't exist
                return getAllTodosDirectly(null);
            }
            
            try {
                // Run the script with JSON output
                const jsonOutput = execSync(`cd "${filterProject}" && bash .claude/scripts/project-todos-table.sh json 2>/dev/null || echo '{}'`, {
                    encoding: 'utf-8',
                    maxBuffer: 1024 * 1024 * 10
                });
                
                const result = JSON.parse(jsonOutput);
                if (result.todos && result.todos.length > 0) {
                    return {
                        todos: result.todos,
                        project: filterProject,
                        currentProject: PROJECT_PATH,
                        availableProjects: getAllProjects(),
                        totalSessions: result.sessions || 1,
                        totalTodos: result.todos.length,
                        lastUpdated: new Date()
                    };
                }
            } catch (e) {
                console.error('Error running project script:', e);
            }
        }
        
        // Fallback or when no filter - read all todos
        return getAllTodosDirectly(filterProject);
    } catch (error) {
        console.error('Error getting todos:', error);
        return { 
            todos: [], 
            project: filterProject || PROJECT_PATH,
            availableProjects: getAllProjects(),
            error: error.message 
        };
    }
}

// Direct reading function (fallback)
function getAllTodosDirectly(filterProject = null) {
    try {
        const allTodos = [];
        const sessions = new Set();
        let totalFound = 0;
        
        // Get project sessions if filtering
        const projectSessions = filterProject ? getProjectSessions(filterProject) : null;
        
        // Read all todo files
        const files = fs.readdirSync(CLAUDE_TODOS_DIR);
        console.log(`Found ${files.length} files in todo directory`);
        if (projectSessions) {
            console.log(`Filtering for project: ${filterProject} (${projectSessions.size} sessions)`);
        }
        
        files.forEach(file => {
            if (!file.endsWith('.json')) return;
            
            const sessionId = file.split('-')[0];
            
            // If filtering by project, skip non-project sessions
            if (projectSessions && !projectSessions.has(sessionId)) {
                return;
            }
            
            const filePath = path.join(CLAUDE_TODOS_DIR, file);
            try {
                const content = fs.readFileSync(filePath, 'utf-8');
                const data = JSON.parse(content);
                
                // The todos are stored as an array directly in the file
                let todos = Array.isArray(data) ? data : (data.todos || []);
                
                if (todos.length > 0) {
                    const stats = fs.statSync(filePath);
                    
                    // Add metadata to each todo
                    todos.forEach(todo => {
                        allTodos.push({
                            ...todo,
                            date: stats.mtime,
                            session: sessionId
                        });
                        totalFound++;
                    });
                    
                    sessions.add(sessionId);
                    console.log(`  File ${file}: ${todos.length} todos`);
                }
            } catch (e) {
                // Skip files that can't be parsed
                console.log(`  Skipping ${file}: ${e.message}`);
            }
        });
        
        console.log(`Total todos found: ${totalFound} across ${sessions.size} sessions`);
        
        // Sort todos by status (in_progress first, then pending, then completed)
        const statusOrder = { 'in_progress': 0, 'pending': 1, 'completed': 2 };
        allTodos.sort((a, b) => {
            const orderDiff = statusOrder[a.status] - statusOrder[b.status];
            if (orderDiff !== 0) return orderDiff;
            // Within same status, sort by date (newest first)
            return new Date(b.date) - new Date(a.date);
        });
        
        return {
            todos: allTodos,
            project: filterProject || PROJECT_PATH,
            currentProject: PROJECT_PATH,
            availableProjects: getAllProjects(),
            totalSessions: sessions.size,
            totalTodos: totalFound,
            lastUpdated: new Date()
        };
    } catch (error) {
        console.error('Error reading todo files:', error);
        return { 
            todos: [], 
            project: PROJECT_PATH,
            availableProjects: getAllProjects(),
            error: error.message 
        };
    }
}

// Create HTTP server
const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    if (req.url.startsWith('/api/todos')) {
        // Parse query parameters for project filter
        const url = new URL(req.url, `http://${req.headers.host}`);
        const projectPath = url.searchParams.get('project');
        
        // API endpoint for todos - filter by project if specified
        const data = getAllTodos(projectPath);
        
        res.writeHead(200, { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(data, null, 2));
    } else if (req.url === '/' || req.url === '/index.html') {
        // Serve index.html
        const filePath = path.join(__dirname, 'index.html');
        fs.readFile(filePath, (err, content) => {
            if (err) {
                res.writeHead(500);
                res.end('Error loading page');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content);
        });
    } else {
        // Serve static files
        let filePath = path.join(__dirname, req.url);
        const extname = path.extname(filePath);
        const contentType = mimeTypes[extname] || 'text/plain';

        fs.readFile(filePath, (err, content) => {
            if (err) {
                if (err.code === 'ENOENT') {
                    res.writeHead(404);
                    res.end('File not found');
                } else {
                    res.writeHead(500);
                    res.end('Server error');
                }
                return;
            }
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        });
    }
});

server.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════════════════╗
║  🚀 Claude Code Todo Dashboard Server (Simple)        ║
╠════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:${PORT}            ║
║  Project: ${PROJECT_PATH.substring(0, 40)}${PROJECT_PATH.length > 40 ? '...' : ''}
║                                                        ║
║  This version reads ALL todos from ALL sessions       ║
║  Open your browser to view the dashboard              ║
║  Press Ctrl+C to stop the server                      ║
╚════════════════════════════════════════════════════════╝
    `);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\nShutting down todo dashboard server...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});