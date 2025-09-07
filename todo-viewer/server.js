#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

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

// Function to get ALL todos for this project across all sessions
function getTodos() {
    try {
        // Try using the project-todos-table script which gives us clean data
        const tableScriptPath = path.join(PROJECT_PATH, '.claude/scripts/project-todos-table.sh');
        if (fs.existsSync(tableScriptPath)) {
            // Get raw JSON data from the table script
            const rawData = execSync(`bash "${tableScriptPath}" json 2>/dev/null || echo '{}'`, {
                encoding: 'utf-8',
                cwd: PROJECT_PATH,
                maxBuffer: 1024 * 1024 * 10 // 10MB buffer for large todo lists
            });
            
            try {
                const jsonData = JSON.parse(rawData);
                if (jsonData.todos && jsonData.todos.length > 0) {
                    return {
                        todos: jsonData.todos,
                        project: PROJECT_PATH,
                        totalSessions: jsonData.sessions || 1,
                        lastUpdated: new Date()
                    };
                }
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
    
    // Fallback to reading all todo files directly
    return getAllProjectTodos();
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

    if (req.url === '/api/todos') {
        // API endpoint for todos
        res.writeHead(200, { 
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify(getTodos()));
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