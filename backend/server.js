const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend')));

// API Routes
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'multi-agent-claude-code',
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development'
  });
});

app.get('/api/agents', (req, res) => {
  res.json({
    agents: [
      { id: 1, name: 'Claude Code', status: 'available', type: 'complex-tasks' },
      { id: 2, name: 'GitHub Copilot', status: 'available', type: 'simple-tasks' },
      { id: 3, name: 'Test Runner', status: 'idle', type: 'testing' }
    ]
  });
});

app.post('/api/issue/route', (req, res) => {
  const { issueNumber, labels, complexity } = req.body;
  
  let assignedAgent = 'human';
  if (complexity === 'simple' || labels.includes('good-first-issue')) {
    assignedAgent = 'copilot';
  } else if (complexity === 'medium' || labels.includes('enhancement')) {
    assignedAgent = 'claude';
  }
  
  res.json({
    issueNumber,
    assignedAgent,
    message: `Issue #${issueNumber} routed to ${assignedAgent}`
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
});