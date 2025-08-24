// Dashboard JavaScript for Agent Performance Analytics
class AgentDashboard {
    constructor() {
        this.metricsData = null;
        
        this.init();
    }

    async init() {
        await this.loadMetrics();
        this.updateOverviewCards();
        this.createCharts();
        this.updateTimeline();
        this.updateMetricsTable();
        this.setupEventListeners();
    }

    async loadMetrics() {
        try {
            // Try to load from the data endpoint
            const response = await fetch('/data/metrics.json');
            if (response.ok) {
                this.metricsData = await response.json();
            } else {
                throw new Error('Metrics file not found');
            }
        } catch (error) {
            console.warn('Could not load metrics data, using sample data');
            this.metricsData = this.generateSampleData();
        }
    }

    generateSampleData() {
        const now = new Date();
        const assignments = [];
        const completions = [];
        
        // Generate sample assignments over the last 30 days
        for (let i = 30; i > 0; i--) {
            const date = new Date(now.getTime() - (i * 24 * 60 * 60 * 1000));
            const agents = ['copilot', 'claude', 'human'];
            const complexities = ['simple', 'medium', 'complex', 'unknown'];
            
            const numAssignments = Math.floor(Math.random() * 5) + 1;
            for (let j = 0; j < numAssignments; j++) {
                const agent = agents[Math.floor(Math.random() * agents.length)];
                const complexity = complexities[Math.floor(Math.random() * complexities.length)];
                
                assignments.push({
                    timestamp: new Date(date.getTime() + (j * 60 * 60 * 1000)).toISOString(),
                    issueNumber: 100 + assignments.length + j,
                    agent,
                    complexity,
                    status: 'assigned'
                });

                // Some assignments get completed
                if (Math.random() > 0.3) {
                    completions.push({
                        timestamp: new Date(date.getTime() + ((j + 2) * 60 * 60 * 1000)).toISOString(),
                        issueNumber: 100 + assignments.length + j,
                        agent,
                        success: Math.random() > 0.2 // 80% success rate
                    });
                }
            }
        }

        const performance = {
            copilot: { total: 0, completed: 0, failed: 0 },
            claude: { total: 0, completed: 0, failed: 0 },
            human: { total: 0, completed: 0, failed: 0 }
        };

        // Calculate performance metrics
        assignments.forEach(a => performance[a.agent].total++);
        completions.forEach(c => {
            if (c.success) {
                performance[c.agent].completed++;
            } else {
                performance[c.agent].failed++;
            }
        });

        return { assignments, completions, performance };
    }

    updateOverviewCards() {
        const { performance } = this.metricsData;
        
        Object.keys(performance).forEach(agent => {
            const data = performance[agent];
            const total = data.total;
            const successRate = total > 0 ? Math.round((data.completed / total) * 100) : 0;
            
            document.getElementById(`${agent}-total`).textContent = total;
            document.getElementById(`${agent}-rate`).textContent = `${successRate}%`;
        });
    }

    createCharts() {
        this.createPerformanceChart();
        this.createDistributionChart();
    }

    createPerformanceChart() {
        const container = document.getElementById('performanceChart');
        
        // Group assignments by date
        const dailyData = this.groupAssignmentsByDate();
        const labels = Object.keys(dailyData).sort().slice(-7); // Last 7 days
        
        let chart = 'Date        Copilot  Claude  Human\n';
        chart += '────────────────────────────────────\n';
        
        labels.forEach(date => {
            const data = dailyData[date];
            const dateStr = new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            const copilot = (data.copilot || 0).toString().padStart(3);
            const claude = (data.claude || 0).toString().padStart(3);
            const human = (data.human || 0).toString().padStart(3);
            
            chart += `${dateStr.padEnd(12)}${copilot}     ${claude}     ${human}\n`;
        });
        
        container.textContent = chart;
    }

    createDistributionChart() {
        const container = document.getElementById('distributionChart');
        const { performance } = this.metricsData;
        
        const agents = Object.keys(performance);
        const total = agents.reduce((sum, agent) => sum + performance[agent].total, 0);
        
        container.innerHTML = '';
        
        agents.forEach(agent => {
            const data = performance[agent];
            const percentage = total > 0 ? Math.round((data.total / total) * 100) : 0;
            
            const barItem = document.createElement('div');
            barItem.className = 'bar-item';
            
            const label = document.createElement('div');
            label.className = 'bar-label';
            label.innerHTML = `<span>${agent.charAt(0).toUpperCase() + agent.slice(1)}</span><span>${data.total} (${percentage}%)</span>`;
            
            const barContainer = document.createElement('div');
            barContainer.className = 'bar-container';
            
            const barFill = document.createElement('div');
            barFill.className = `bar-fill ${agent}`;
            barFill.style.width = `${percentage}%`;
            if (percentage > 15) {
                barFill.textContent = `${percentage}%`;
            }
            
            barContainer.appendChild(barFill);
            barItem.appendChild(label);
            barItem.appendChild(barContainer);
            container.appendChild(barItem);
        });
    }

    groupAssignmentsByDate() {
        const dailyData = {};
        
        this.metricsData.assignments.forEach(assignment => {
            const date = assignment.timestamp.split('T')[0];
            if (!dailyData[date]) {
                dailyData[date] = { copilot: 0, claude: 0, human: 0 };
            }
            dailyData[date][assignment.agent]++;
        });
        
        return dailyData;
    }

    updateTimeline() {
        const container = document.getElementById('timelineContainer');
        const timeRange = document.getElementById('timeRange').value;
        
        let filteredAssignments = this.filterByTimeRange(this.metricsData.assignments, timeRange);
        filteredAssignments = filteredAssignments.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        container.innerHTML = '';
        
        filteredAssignments.slice(0, 50).forEach(assignment => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            
            const dot = document.createElement('div');
            dot.className = `timeline-dot ${assignment.agent}`;
            
            const content = document.createElement('div');
            content.className = 'timeline-content';
            
            const time = document.createElement('div');
            time.className = 'timeline-time';
            time.textContent = new Date(assignment.timestamp).toLocaleString();
            
            const description = document.createElement('div');
            description.className = 'timeline-description';
            description.textContent = `Issue #${assignment.issueNumber} assigned to ${assignment.agent} (${assignment.complexity})`;
            
            content.appendChild(time);
            content.appendChild(description);
            
            item.appendChild(dot);
            item.appendChild(content);
            
            container.appendChild(item);
        });
    }

    updateMetricsTable() {
        const tbody = document.getElementById('metricsTableBody');
        const assignments = this.metricsData.assignments
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, 100); // Show last 100 entries
        
        tbody.innerHTML = '';
        
        assignments.forEach(assignment => {
            const row = document.createElement('tr');
            
            const completion = this.metricsData.completions.find(c => c.issueNumber === assignment.issueNumber);
            const status = completion ? (completion.success ? 'completed' : 'failed') : 'assigned';
            
            row.innerHTML = `
                <td>${new Date(assignment.timestamp).toLocaleString()}</td>
                <td>#${assignment.issueNumber}</td>
                <td>${assignment.agent.charAt(0).toUpperCase() + assignment.agent.slice(1)}</td>
                <td><span class="complexity-${assignment.complexity}">${assignment.complexity}</span></td>
                <td><span class="status-${status}">${status}</span></td>
            `;
            
            tbody.appendChild(row);
        });
    }

    filterByTimeRange(data, range) {
        const now = new Date();
        let cutoff;
        
        switch (range) {
            case '24h':
                cutoff = new Date(now.getTime() - (24 * 60 * 60 * 1000));
                break;
            case '7d':
                cutoff = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000));
                break;
            case '30d':
                cutoff = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
                break;
            case 'all':
            default:
                return data;
        }
        
        return data.filter(item => new Date(item.timestamp) >= cutoff);
    }

    setupEventListeners() {
        document.getElementById('timeRange').addEventListener('change', () => {
            this.updateTimeline();
        });
    }

    async refresh() {
        await this.loadMetrics();
        this.updateOverviewCards();
        this.createCharts();
        this.updateTimeline();
        this.updateMetricsTable();
    }

    exportReport() {
        const { performance, assignments, completions } = this.metricsData;
        
        const report = {
            generatedAt: new Date().toISOString(),
            summary: {
                totalAssignments: assignments.length,
                totalCompletions: completions.length,
                successRate: completions.length > 0 ? 
                    Math.round((completions.filter(c => c.success).length / completions.length) * 100) : 0
            },
            agentPerformance: performance,
            recentActivity: assignments.slice(-50)
        };
        
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `agent-performance-report-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
    }
}

// Global functions for button handlers
async function refreshData() {
    if (window.dashboard) {
        await window.dashboard.refresh();
    }
}

function exportReport() {
    if (window.dashboard) {
        window.dashboard.exportReport();
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AgentDashboard();
});