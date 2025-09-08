#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = process.env.PORT || 8081;
const CLAUDE_TODOS_DIR = path.join(process.env.HOME, '.claude/todos');
const PROJECT_PATH = path.dirname(__dirname); // Get parent directory (project root)

// MIME types for static files
const mimeTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json'
};

// Get all available projects dynamically from .claude/projects
function getAllProjects() {
    try {
        const projectsDir = path.join(process.env.HOME, '.claude/projects');
        if (!fs.existsSync(projectsDir)) {
            return [];
        }
        
        const projects = [];
        const seen = new Set();
        
        fs.readdirSync(projectsDir)
            .filter(dir => fs.statSync(path.join(projectsDir, dir)).isDirectory())
            .forEach(dir => {
                // Convert directory name back to path
                // Directory format: -home-gotime2022-Projects-multi-agent-claude-code
                let projectPath = dir;
                if (projectPath.startsWith('-')) {
                    projectPath = projectPath.substring(1); // Remove leading dash
                }
                
                // Build the path step by step, preserving hyphens in project names
                let reconstructedPath = '/';
                
                // Common patterns to replace
                if (projectPath.startsWith('home-gotime2022-Projects-')) {
                    reconstructedPath = '/home/gotime2022/Projects/';
                    projectPath = projectPath.substring('home-gotime2022-Projects-'.length);
                } else if (projectPath.startsWith('home-gotime2022-')) {
                    // Could be either /home/gotime2022/ or /home/gotime2022/Projects/
                    // We'll check both locations
                    const projectName = projectPath.substring('home-gotime2022-'.length);
                    const pathWithProjects = '/home/gotime2022/Projects/' + projectName;
                    const pathWithoutProjects = '/home/gotime2022/' + projectName;
                    
                    // Check which one actually exists
                    // Always prefer the Projects path if it exists
                    if (fs.existsSync(pathWithProjects)) {
                        reconstructedPath = pathWithProjects;
                    } else if (fs.existsSync(pathWithoutProjects)) {
                        reconstructedPath = pathWithoutProjects;
                    } else {
                        // Default to Projects path even if not found
                        reconstructedPath = pathWithProjects;
                    }
                    projectPath = ''; // Already handled
                }
                
                // Add remaining part if any
                if (projectPath) {
                    reconstructedPath += projectPath;
                }
                
                // Avoid duplicates
                if (!seen.has(reconstructedPath)) {
                    seen.add(reconstructedPath);
                    const projectName = path.basename(reconstructedPath);
                    projects.push({
                        name: projectName,
                        path: reconstructedPath
                    });
                }
            });
        
        return projects;
    } catch (error) {
        console.error('Error reading projects:', error);
        return [];
    }
}

// Function to get ALL todos for this project across all sessions
function getTodos(projectPath = null) {
    try {
        // If projectPath is empty string, null or "all", get todos for all projects
        if (!projectPath || projectPath === '' || projectPath === 'all') {
            return getAllProjectsTodos();
        }
        
        const targetPath = projectPath;
        // Always use the script from main project but run it IN the target directory
        const tableScriptPath = path.join(PROJECT_PATH, '.claude/scripts/project-todos-table.sh');
        
        // Check if the path exists, if not return empty for that project
        if (!fs.existsSync(targetPath)) {
            console.error(`Project path does not exist: ${targetPath}`);
            return {
                todos: [],
                project: targetPath,
                totalSessions: 0,
                lastUpdated: new Date(),
                error: `Project path not found: ${targetPath}`
            };
        }
        
        if (fs.existsSync(tableScriptPath)) {
            // Get raw JSON data from the table script
            const rawData = execSync(`/usr/bin/bash "${tableScriptPath}" json 2>/dev/null || echo '{"todos":[],"sessions":0}'`, {
                encoding: 'utf-8',
                cwd: targetPath,
                maxBuffer: 1024 * 1024 * 10, // 10MB buffer for large todo lists
                shell: '/usr/bin/bash'
            });
            
            try {
                const jsonData = JSON.parse(rawData);
                if (jsonData.todos && jsonData.todos.length > 0) {
                    return {
                        todos: jsonData.todos,
                        project: targetPath, // Return the actual target path, not PROJECT_PATH
                        totalSessions: jsonData.sessions || 1,
                        lastUpdated: new Date()
                    };
                }
                // Even if no todos, return empty result for this project
                return {
                    todos: [],
                    project: targetPath,
                    totalSessions: 0,
                    lastUpdated: new Date()
                };
            } catch (parseError) {
                console.error('Error parsing JSON from table script:', parseError);
            }
        }
        
        // Try the organize script as fallback
        const organizeScriptPath = path.join(PROJECT_PATH, '.claude/scripts/organize-todos-by-project.sh');
        if (fs.existsSync(organizeScriptPath)) {
            // Use the script to get raw data without ANSI codes
            const result = execSync(`bash "${organizeScriptPath}" raw 2>/dev/null || echo ""`, { 
                encoding: 'utf-8',
                cwd: PROJECT_PATH 
            });
            
            // Parse the raw output (format: date|status|content)
            const lines = result.split('\n').filter(line => line.trim());
            const todos = [];
            let currentSession = 'unknown';
            
            lines.forEach(line => {
                // Check for session marker
                if (line.startsWith('SESSION:')) {
                    currentSession = line.replace('SESSION:', '').trim();
                    return;
                }
                
                // Parse todo lines (format: YYYY-MM-DD|status|content)
                const parts = line.split('|');
                if (parts.length >= 3) {
                    const [date, status, ...contentParts] = parts;
                    todos.push({
                        date: date.trim(),
                        status: status.trim(),
                        content: contentParts.join('|').trim(),
                        activeForm: contentParts.join('|').trim(),
                        session: currentSession
                    });
                }
            });
            
            if (todos.length > 0) {
                return {
                    todos: todos,
                    project: PROJECT_PATH,
                    totalSessions: new Set(todos.map(t => t.session)).size,
                    lastUpdated: new Date()
                };
            }
        }
    } catch (error) {
        console.error('Error using scripts:', error);
    }
    
    // Don't fallback to ALL todos - return empty for this specific project
    return {
        todos: [],
        project: projectPath || PROJECT_PATH,
        totalSessions: 0,
        lastUpdated: new Date(),
        error: 'Could not load todos for this project'
    };
}

// Get todos from ALL projects combined
function getAllProjectsTodos() {
    try {
        const allProjects = getAllProjects();
        const allTodos = [];
        let totalSessions = 0;
        
        // Collect todos from each project
        for (const project of allProjects) {
            if (fs.existsSync(project.path)) {
                const projectTodos = getTodosSingleProject(project.path);
                if (projectTodos && projectTodos.todos) {
                    // Add project info to each todo
                    projectTodos.todos.forEach(todo => {
                        allTodos.push({
                            ...todo,
                            projectName: project.name,
                            projectPath: project.path
                        });
                    });
                    totalSessions += projectTodos.totalSessions || 0;
                }
            }
        }
        
        // Sort by status priority
        const statusOrder = { 'in_progress': 0, 'pending': 1, 'completed': 2 };
        allTodos.sort((a, b) => {
            const orderDiff = statusOrder[a.status] - statusOrder[b.status];
            if (orderDiff !== 0) return orderDiff;
            return new Date(b.date) - new Date(a.date);
        });
        
        return {
            todos: allTodos,
            project: 'All Projects',
            totalSessions: totalSessions,
            lastUpdated: new Date()
        };
    } catch (error) {
        console.error('Error getting all projects todos:', error);
        return { todos: [], project: 'All Projects' };
    }
}

// Helper to get todos from a single project
function getTodosSingleProject(projectPath) {
    try {
        const tableScriptPath = path.join(PROJECT_PATH, '.claude/scripts/project-todos-table.sh');
        if (fs.existsSync(tableScriptPath) && fs.existsSync(projectPath)) {
            const rawData = execSync(`/usr/bin/bash "${tableScriptPath}" json 2>/dev/null || echo '{"todos":[],"sessions":0}'`, {
                encoding: 'utf-8',
                cwd: projectPath,
                maxBuffer: 1024 * 1024 * 10,
                shell: '/usr/bin/bash'
            });
            
            const jsonData = JSON.parse(rawData);
            return jsonData;
        }
    } catch (error) {
        console.error(`Error getting todos for ${projectPath}:`, error.message);
    }
    return { todos: [], sessions: 0 };
}

function getAllProjectTodos() {
    try {
        const allTodos = [];
        const sessions = new Set();
        
        // Read all todo files
        const files = fs.readdirSync(CLAUDE_TODOS_DIR)
            .filter(f => f.endsWith('.json'))
            .map(f => ({
                name: f,
                path: path.join(CLAUDE_TODOS_DIR, f),
                mtime: fs.statSync(path.join(CLAUDE_TODOS_DIR, f)).mtime
            }));

        // Read each file and collect todos
        files.forEach(file => {
            try {
                const content = fs.readFileSync(file.path, 'utf-8');
                const data = JSON.parse(content);
                
                // The todos are stored as an array directly in the file
                let todos = Array.isArray(data) ? data : (data.todos || []);
                const sessionId = file.name.split('-')[0];
                
                // Add metadata to each todo
                todos.forEach(todo => {
                    allTodos.push({
                        ...todo,
                        date: file.mtime,
                        session: sessionId
                    });
                });
                
                sessions.add(sessionId);
            } catch (e) {
                // Skip files that can't be parsed
            }
        });
        
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
            project: PROJECT_PATH,
            totalSessions: sessions.size,
            lastUpdated: new Date()
        };
    } catch (error) {
        console.error('Error reading todo files:', error);
        return { todos: [], project: PROJECT_PATH };
    }
}

// Create HTTP server
const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);

    if (req.url.startsWith('/api/todos')) {
        // Parse query parameters
        const url = new URL(req.url, `http://${req.headers.host}`);
        const projectPath = url.searchParams.get('project');
        
        // API endpoint for todos with project list
        const todosData = getTodos(projectPath);
        const response = {
            ...todosData,
            availableProjects: getAllProjects()
        };
        res.writeHead(200, { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(response));
    } else if (req.url === '/api/projects') {
        // API endpoint for projects list
        res.writeHead(200, { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(getAllProjects()));
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
║  🚀 Claude Code Todo Dashboard Server                 ║
╠════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:${PORT}            ║
║  Project: ${PROJECT_PATH.substring(0, 40)}${PROJECT_PATH.length > 40 ? '...' : ''}
║                                                        ║
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