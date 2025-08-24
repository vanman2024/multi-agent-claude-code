#!/usr/bin/env node

/**
 * Test script to generate sample metrics data
 */

const AgentDispatcher = require('./agent-dispatcher');
const fs = require('fs');
const path = require('path');

async function generateSampleMetrics() {
  console.log('🧪 Generating sample metrics data for dashboard testing...');
  
  const dispatcher = new AgentDispatcher('vanman2024', 'multi-agent-claude-code');
  
  // Generate sample assignments
  const sampleAssignments = [
    { issue: 101, agent: 'copilot', complexity: 'simple' },
    { issue: 102, agent: 'claude', complexity: 'medium' },
    { issue: 103, agent: 'human', complexity: 'complex' },
    { issue: 104, agent: 'copilot', complexity: 'simple' },
    { issue: 105, agent: 'claude', complexity: 'medium' },
    { issue: 106, agent: 'claude', complexity: 'unknown' },
    { issue: 107, agent: 'copilot', complexity: 'simple' },
    { issue: 108, agent: 'human', complexity: 'complex' }
  ];
  
  // Record assignments with delays to create realistic timestamps
  for (let i = 0; i < sampleAssignments.length; i++) {
    const { issue, agent, complexity } = sampleAssignments[i];
    dispatcher.recordAssignment(issue, agent, complexity);
    
    // Simulate some completions
    if (Math.random() > 0.3) {
      const success = Math.random() > 0.2; // 80% success rate
      dispatcher.recordCompletion(issue, agent, success);
    }
    
    // Small delay to create different timestamps
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  console.log('✅ Sample metrics data generated successfully!');
  console.log('📊 You can now view the dashboard at: http://localhost:3000');
  console.log('');
  console.log('Run the dashboard server with:');
  console.log('   node scripts/dashboard/server.js');
}

if (require.main === module) {
  generateSampleMetrics().catch(console.error);
}

module.exports = { generateSampleMetrics };