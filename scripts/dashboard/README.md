# Agent Performance Dashboard

A comprehensive dashboard for monitoring and analyzing AI agent performance in the multi-agent Claude Code system.

## Features

✅ **Agent Activity Timeline** - Real-time view of agent assignments and completions
✅ **Task Completion Rate Metrics** - Success rates for each agent type (Copilot, Claude, Human)
✅ **Performance Graphs Over Time** - Visual representation of agent workload distribution
✅ **Export Functionality** - JSON report generation for detailed analysis

## Quick Start

### 1. Generate Sample Data (Optional)
```bash
node scripts/generate-sample-data.js
```

### 2. Start the Dashboard Server
```bash
node scripts/dashboard/server.js
```

### 3. Access the Dashboard
Open your browser to: http://localhost:3000

## Dashboard Sections

### 📊 Overview Cards
- Total assignments per agent
- Success rates and completion statistics
- Real-time performance indicators

### 📈 Performance Over Time
- Text-based chart showing daily assignment trends
- 7-day rolling view of agent activity
- Comparative analysis across agent types

### 📊 Task Distribution
- Visual breakdown of work allocation
- Percentage distribution with progress bars
- Color-coded by agent type

### ⏰ Activity Timeline
- Chronological view of recent assignments
- Filterable by time range (24h, 7d, 30d, all time)
- Shows issue numbers, agents, and complexity levels

### 📋 Detailed Metrics Table
- Complete assignment history
- Status tracking (assigned, completed, failed)
- Complexity classification with color coding
- Sortable and paginated view

## Metrics Collection

The dashboard automatically collects metrics from the AgentDispatcher:

```javascript
// Records when an issue is assigned to an agent
dispatcher.recordAssignment(issueNumber, agent, complexity);

// Records when a task is completed (success/failure)
dispatcher.recordCompletion(issueNumber, agent, success);
```

## Export Reports

Click the "📊 Export Report" button to download a JSON report containing:
- Summary statistics
- Agent performance breakdown
- Recent activity data
- Timestamp of report generation

## Data Storage

Metrics are stored in `data/metrics.json` with the following structure:
```json
{
  "assignments": [...],
  "completions": [...], 
  "performance": {
    "copilot": { "total": 0, "completed": 0, "failed": 0 },
    "claude": { "total": 0, "completed": 0, "failed": 0 },
    "human": { "total": 0, "completed": 0, "failed": 0 }
  }
}
```

## Configuration

### Server Port
```bash
node scripts/dashboard/server.js [port]
# Default: 3000
```

### Data Location
The dashboard looks for metrics in `data/metrics.json` relative to the project root. If not found, it generates sample data for demonstration.

## Architecture

The dashboard follows a minimal, no-dependency approach:
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: Node.js HTTP server
- **Storage**: File-based JSON (easily replaceable with database)
- **Charts**: Text-based visualization (no external libraries)

## Integration with Agent Dispatcher

The dashboard seamlessly integrates with the existing AgentDispatcher class:

1. **Metrics Collection**: Automatic recording during agent assignments
2. **Real-time Updates**: Refresh button syncs with latest data
3. **Historical Analysis**: Tracks performance trends over time
4. **Export Capability**: Generate reports for stakeholder review

## Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Development

### Adding New Metrics
Extend the metrics collection in `AgentDispatcher`:

```javascript
// Custom metric recording
recordCustomMetric(type, data) {
  const metrics = JSON.parse(fs.readFileSync(this.metricsPath, 'utf8'));
  metrics.custom = metrics.custom || [];
  metrics.custom.push({ type, data, timestamp: new Date().toISOString() });
  fs.writeFileSync(this.metricsPath, JSON.stringify(metrics, null, 2));
}
```

### Customizing Dashboard
Modify `scripts/dashboard/dashboard.js` to add new visualizations or change the UI layout in `index.html`.

## Troubleshooting

**Dashboard not loading?**
- Ensure the server is running on port 3000
- Check for any firewall restrictions

**No data showing?**
- Run the sample data generator first
- Verify `data/metrics.json` exists and contains data

**Export not working?**
- Modern browsers required for download functionality
- Check browser's download permissions

## License

This dashboard is part of the multi-agent Claude Code project and follows the same license terms.