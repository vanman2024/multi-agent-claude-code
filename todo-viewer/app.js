// Todo Dashboard Application
class TodoDashboard {
    constructor() {
        this.todos = [];
        this.currentFilter = 'all';
        this.searchTerm = '';
        this.selectedProject = null;
        this.availableProjects = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTodos();
        // Auto-refresh every 5 seconds
        setInterval(() => this.loadTodos(), 5000);
    }

    setupEventListeners() {
        // Project filter dropdown
        document.getElementById('projectFilter').addEventListener('change', (e) => {
            this.selectedProject = e.target.value;
            // Reload todos with the selected project filter from server
            this.loadTodos();
        });

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentFilter = e.target.dataset.filter;
                this.renderTodos();
            });
        });

        // Search box
        document.getElementById('searchBox').addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.renderTodos();
        });

        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadTodos();
            document.getElementById('refreshBtn').classList.add('loading');
            setTimeout(() => {
                document.getElementById('refreshBtn').classList.remove('loading');
            }, 1000);
        });
    }

    async loadTodos() {
        try {
            // Build API URL with project parameter if selected
            let apiUrl = '/api/todos';
            if (this.selectedProject) {
                // selectedProject already contains the full path from the dropdown
                apiUrl = `/api/todos?project=${encodeURIComponent(this.selectedProject)}`;
            }
            
            const response = await fetch(apiUrl);
            const data = await response.json();
            
            // Store ALL todos
            this.allTodos = data.todos || [];
            this.todos = this.allTodos;
            
            // Update available projects from server
            if (data.availableProjects) {
                this.availableProjects = data.availableProjects;
            }
            
            // Extract unique project paths from todo content if not available from server
            if (!this.availableProjects || this.availableProjects.length === 0) {
                this.projectList = this.extractProjectsFromTodos();
            }
            
            // Update dropdown with available projects
            this.updateSimpleProjectDropdown();
            
            document.getElementById('projectPath').textContent = data.project || '/home/gotime2022/Projects/multi-agent-claude-code';
            
            // No need for client-side filtering anymore - server handles it
            this.updateStats();
            this.renderTodos();
            this.updateLastUpdated();
        } catch (error) {
            console.error('Error loading todos:', error);
            this.todos = [];
            this.updateStats();
            this.renderTodos();
        }
    }
    
    extractProjectsFromTodos() {
        const projectMap = new Map();
        
        // Known project mappings
        const projectKeywords = [
            { keywords: ['multi-agent', 'claude-code', 'multi-agent-claude-code'], name: 'multi-agent-claude-code', fullPath: '/home/gotime2022/Projects/multi-agent-claude-code' },
            { keywords: ['mcp-kernel', 'kernel-new'], name: 'mcp-kernel-new', fullPath: '/home/gotime2022/Projects/mcp-kernel-new' },
            { keywords: ['recruitment', 'recruitment-ops'], name: 'recruitment-ops', fullPath: '/home/gotime2022/Projects/recruitment-ops' },
            { keywords: ['test-todo', 'todo-app'], name: 'test-todo-app', fullPath: '/home/gotime2022/Projects/test-todo-app' },
            { keywords: ['observability', 'monitoring'], name: 'multi-agent-observability-system', fullPath: '/home/gotime2022/multi-agent-observability-system' },
            { keywords: ['synapseai', 'synapse'], name: 'synapseai', fullPath: '/home/gotime2022/synapseai' },
            { keywords: ['project-seed'], name: 'project-seed', fullPath: '/home/gotime2022/project-seed' }
        ];
        
        // Count todos per project
        this.allTodos.forEach(todo => {
            if (todo.content) {
                const contentLower = todo.content.toLowerCase();
                
                // Check each project's keywords
                projectKeywords.forEach(project => {
                    const matches = project.keywords.some(keyword => 
                        contentLower.includes(keyword.toLowerCase())
                    );
                    
                    if (matches) {
                        if (!projectMap.has(project.name)) {
                            projectMap.set(project.name, { 
                                name: project.name, 
                                fullPath: project.fullPath,
                                count: 0 
                            });
                        }
                        projectMap.get(project.name).count++;
                    }
                });
            }
        });
        
        // Return projects sorted by todo count
        return Array.from(projectMap.values())
            .sort((a, b) => b.count - a.count)
            .map(p => p.name);
    }
    
    updateSimpleProjectDropdown() {
        const dropdown = document.getElementById('projectFilter');
        const currentValue = this.selectedProject || dropdown.value; // Preserve current selection
        dropdown.innerHTML = '';
        
        // Add "All Projects" option
        const allOption = document.createElement('option');
        allOption.value = '';
        allOption.textContent = `📁 All Projects`;
        dropdown.appendChild(allOption);
        
        // Add separator
        if (this.availableProjects && this.availableProjects.length > 0) {
            const separator = document.createElement('option');
            separator.disabled = true;
            separator.textContent = '──────────────';
            dropdown.appendChild(separator);
            
            // Add each project from server data
            this.availableProjects.forEach(project => {
                const option = document.createElement('option');
                option.value = project.path || project.name;
                option.textContent = `📁 ${project.name}`;
                dropdown.appendChild(option);
            });
        } else if (this.projectList && this.projectList.length > 0) {
            // Fallback to extracted project list
            const separator = document.createElement('option');
            separator.disabled = true;
            separator.textContent = '──────────────';
            dropdown.appendChild(separator);
            
            // Add each project
            this.projectList.forEach(project => {
                const option = document.createElement('option');
                option.value = project;
                option.textContent = `📁 ${project}`;
                dropdown.appendChild(option);
            });
        }
        
        // Restore the previously selected value
        if (currentValue) {
            dropdown.value = currentValue;
        }
    }
    
    applyProjectFilter() {
        if (!this.selectedProject) {
            // Show all todos
            this.todos = this.allTodos;
        } else {
            // Filter todos that mention the selected project
            this.todos = this.allTodos.filter(todo => 
                todo.content && todo.content.toLowerCase().includes(this.selectedProject.toLowerCase())
            );
        }
    }
    
    updateProjectDropdown(currentProject) {
        const dropdown = document.getElementById('projectFilter');
        dropdown.innerHTML = '';
        
        // Add current project as default
        const currentOption = document.createElement('option');
        currentOption.value = currentProject;
        currentOption.textContent = `📁 Current: ${currentProject.split('/').pop()}`;
        currentOption.selected = true;
        dropdown.appendChild(currentOption);
        
        // Add separator
        const separator = document.createElement('option');
        separator.disabled = true;
        separator.textContent = '──────────────';
        dropdown.appendChild(separator);
        
        // Add all projects
        this.availableProjects.forEach(project => {
            const option = document.createElement('option');
            option.value = project.path;
            option.textContent = `${project.name} (${project.path})`;
            dropdown.appendChild(option);
        });
    }

    loadSampleData() {
        // Sample data structure matching Claude Code's todo format
        this.todos = [
            {
                content: "Create web-based todo viewer app",
                status: "in_progress",
                activeForm: "Creating web-based todo viewer",
                date: new Date().toISOString(),
                session: "current"
            },
            {
                content: "Design HTML/CSS/JS interface for todo visualization",
                status: "pending",
                activeForm: "Designing todo visualization interface",
                date: new Date().toISOString(),
                session: "current"
            },
            {
                content: "Implement live reload/auto-refresh for todo updates",
                status: "pending",
                activeForm: "Implementing live todo updates",
                date: new Date().toISOString(),
                session: "current"
            },
            {
                content: "Add hook to trigger TodoWrite on task starts",
                status: "pending",
                activeForm: "Adding TodoWrite trigger hook",
                date: new Date().toISOString(),
                session: "current"
            },
            {
                content: "Build todo API endpoint for web app",
                status: "pending",
                activeForm: "Building todo API endpoint",
                date: new Date().toISOString(),
                session: "current"
            },
            {
                content: "Analyze why TodoWrite tool is underutilized",
                status: "completed",
                activeForm: "Analyzing TodoWrite tool usage patterns",
                date: new Date().toISOString(),
                session: "current"
            }
        ];
        this.updateStats();
        this.renderTodos();
        this.updateLastUpdated();
    }

    updateStats() {
        const stats = {
            completed: this.todos.filter(t => t.status === 'completed').length,
            inProgress: this.todos.filter(t => t.status === 'in_progress').length,
            pending: this.todos.filter(t => t.status === 'pending').length,
            total: this.todos.length
        };

        document.getElementById('completedCount').textContent = stats.completed;
        document.getElementById('inProgressCount').textContent = stats.inProgress;
        document.getElementById('pendingCount').textContent = stats.pending;
        document.getElementById('totalCount').textContent = stats.total;
    }

    renderTodos() {
        const container = document.getElementById('todosContainer');
        const filteredTodos = this.filterTodos();
        
        // Group todos by status
        const grouped = {
            in_progress: filteredTodos.filter(t => t.status === 'in_progress'),
            pending: filteredTodos.filter(t => t.status === 'pending'),
            completed: filteredTodos.filter(t => t.status === 'completed')
        };

        let html = '';

        // Render In Progress section
        if (grouped.in_progress.length > 0) {
            html += this.renderSection('🔄 In Progress', grouped.in_progress, 'in-progress');
        }

        // Render Pending section
        if (grouped.pending.length > 0) {
            html += this.renderSection('⏳ Pending', grouped.pending, 'pending');
        }

        // Render Completed section
        if (grouped.completed.length > 0) {
            html += this.renderSection('✅ Completed', grouped.completed, 'completed');
        }

        container.innerHTML = html || '<div class="todo-section"><p>No todos found</p></div>';
    }

    renderSection(title, todos, statusClass) {
        let html = `
            <div class="todo-section">
                <h2 class="section-title">${title} (${todos.length})</h2>
                <div class="todos-list">
        `;

        // Group by session for better organization
        const bySession = {};
        todos.forEach(todo => {
            const session = todo.session || 'unknown';
            if (!bySession[session]) bySession[session] = [];
            bySession[session].push(todo);
        });

        // Render todos grouped by session
        Object.entries(bySession).forEach(([session, sessionTodos]) => {
            if (sessionTodos.length > 0) {
                html += `<div style="margin-bottom: 15px;">`;
                html += `<div style="font-size: 0.85rem; color: #666; margin-bottom: 5px;">Session: ${session.substring(0, 8)}...</div>`;
                
                sessionTodos.forEach(todo => {
                    // Use timestamp for both date and time if available, otherwise fall back to date field
                    let dateStr = 'No date';
                    let timeStr = '';
                    
                    if (todo.timestamp) {
                        // Use timestamp for both date and time
                        const timestamp = new Date(todo.timestamp);
                        dateStr = timestamp.toLocaleDateString();
                        timeStr = timestamp.toLocaleTimeString('en-US', { 
                            hour: 'numeric', 
                            minute: '2-digit',
                            hour12: true 
                        });
                    } else if (todo.date) {
                        // Fall back to date field if no timestamp
                        const date = new Date(todo.date);
                        dateStr = date.toLocaleDateString();
                    }
                    
                    html += `
                        <div class="todo-item ${statusClass}">
                            <div class="todo-content">${this.escapeHtml(todo.content)}</div>
                            <div class="todo-meta">
                                <span>📅 ${dateStr}</span>
                                ${timeStr ? `<span>🕐 ${timeStr}</span>` : ''}
                                ${todo.activeForm && todo.activeForm !== todo.content ? 
                                    `<span style="font-style: italic;">🎯 ${this.escapeHtml(todo.activeForm)}</span>` : ''}
                            </div>
                        </div>
                    `;
                });
                html += `</div>`;
            }
        });

        html += `
                </div>
            </div>
        `;

        return html;
    }

    filterTodos() {
        let filtered = this.todos;

        // Apply status filter
        if (this.currentFilter !== 'all') {
            filtered = filtered.filter(t => t.status === this.currentFilter.replace('-', '_'));
        }

        // Apply search filter
        if (this.searchTerm) {
            filtered = filtered.filter(t => 
                t.content.toLowerCase().includes(this.searchTerm) ||
                (t.activeForm && t.activeForm.toLowerCase().includes(this.searchTerm))
            );
        }

        return filtered;
    }

    updateLastUpdated() {
        const now = new Date().toLocaleString();
        document.getElementById('lastUpdated').textContent = `Last updated: ${now}`;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TodoDashboard();
});