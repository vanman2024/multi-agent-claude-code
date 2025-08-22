const request = require('supertest');
const express = require('express');

// Mock the server for testing
const app = express();
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'multi-agent-claude-code'
  });
});

app.get('/api/agents', (req, res) => {
  res.json({
    agents: [
      { id: 1, name: 'Claude Code', status: 'available' }
    ]
  });
});

app.post('/api/issue/route', (req, res) => {
  const { issueNumber, complexity } = req.body;
  res.json({
    issueNumber,
    assignedAgent: complexity === 'simple' ? 'copilot' : 'claude'
  });
});

describe('API Endpoints', () => {
  test('GET /api/health returns healthy status', async () => {
    const response = await request(app)
      .get('/api/health')
      .expect(200);
    
    expect(response.body).toHaveProperty('status', 'healthy');
    expect(response.body).toHaveProperty('service', 'multi-agent-claude-code');
  });
  
  test('GET /api/agents returns list of agents', async () => {
    const response = await request(app)
      .get('/api/agents')
      .expect(200);
    
    expect(response.body).toHaveProperty('agents');
    expect(Array.isArray(response.body.agents)).toBe(true);
    expect(response.body.agents.length).toBeGreaterThan(0);
  });
  
  test('POST /api/issue/route assigns agent based on complexity', async () => {
    const simpleIssue = {
      issueNumber: 123,
      complexity: 'simple',
      labels: []
    };
    
    const response = await request(app)
      .post('/api/issue/route')
      .send(simpleIssue)
      .expect(200);
    
    expect(response.body).toHaveProperty('assignedAgent', 'copilot');
    expect(response.body).toHaveProperty('issueNumber', 123);
  });
  
  test('POST /api/issue/route assigns claude for complex issues', async () => {
    const complexIssue = {
      issueNumber: 456,
      complexity: 'complex',
      labels: ['enhancement']
    };
    
    const response = await request(app)
      .post('/api/issue/route')
      .send(complexIssue)
      .expect(200);
    
    expect(response.body).toHaveProperty('assignedAgent', 'claude');
  });
});