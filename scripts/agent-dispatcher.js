#!/usr/bin/env node

/**
 * Agent Dispatcher - Routes issues to appropriate AI agents
 * 
 * This script monitors GitHub issues and dispatches them to:
 * - GitHub Copilot (for simple tasks)
 * - Claude Code agents (for complex tasks)
 * - Human developers (for architecture decisions)
 */

const { execSync } = require('child_process');

class AgentDispatcher {
  constructor(owner, repo) {
    this.owner = owner;
    this.repo = repo;
  }

  /**
   * Analyze issue complexity based on labels and content
   */
  analyzeComplexity(issue) {
    const labels = issue.labels.map(l => l.name);
    const title = issue.title.toLowerCase();
    const body = (issue.body || '').toLowerCase();
    
    // Simple: Good for Copilot
    if (labels.includes('good-first-issue') ||
        labels.includes('documentation') ||
        title.includes('typo') ||
        title.includes('update readme') ||
        body.includes('simple change')) {
      return { complexity: 'simple', agent: 'copilot' };
    }
    
    // Medium: Good for Claude Code
    if (labels.includes('enhancement') ||
        labels.includes('feature') ||
        labels.includes('refactor') ||
        title.includes('[feature]') ||
        title.includes('[enhancement]')) {
      return { complexity: 'medium', agent: 'claude' };
    }
    
    // Complex: Needs human review
    if (labels.includes('architecture') ||
        labels.includes('breaking-change') ||
        labels.includes('security') ||
        title.includes('[rfc]') ||
        title.includes('[design]')) {
      return { complexity: 'complex', agent: 'human' };
    }
    
    // Default to Claude for unknown
    return { complexity: 'unknown', agent: 'claude' };
  }

  /**
   * Assign issue to GitHub Copilot
   */
  async assignToCopilot(issueNumber) {
    console.log(`🤖 Assigning issue #${issueNumber} to GitHub Copilot...`);
    
    try {
      // Using MCP GitHub server to assign Copilot
      const command = `claude-code exec mcp__github__assign_copilot_to_issue \
        --owner ${this.owner} \
        --repo ${this.repo} \
        --issueNumber ${issueNumber}`;
      
      execSync(command, { stdio: 'inherit' });
      
      console.log(`✅ Copilot assigned to issue #${issueNumber}`);
      return true;
    } catch (error) {
      console.error(`❌ Failed to assign Copilot:`, error.message);
      return false;
    }
  }

  /**
   * Create task for Claude Code agent
   */
  async createClaudeTask(issueNumber, branch) {
    console.log(`🧠 Creating Claude Code task for issue #${issueNumber}...`);
    
    const taskConfig = {
      issue: issueNumber,
      branch: branch,
      steps: [
        'git checkout ' + branch,
        'Read issue requirements',
        'Analyze codebase structure',
        'Implement solution',
        'Run tests',
        'Create pull request'
      ]
    };
    
    // This would integrate with Claude Code's agent system
    console.log('Task configuration:', JSON.stringify(taskConfig, null, 2));
    
    // In practice, this would spawn a Claude Code sub-agent
    // that works autonomously on the branch
    return taskConfig;
  }

  /**
   * Monitor and route new issues
   */
  async monitorIssues() {
    console.log(`👀 Monitoring issues for ${this.owner}/${this.repo}...`);
    
    // Get recent issues
    const command = `gh issue list --repo ${this.owner}/${this.repo} \
      --state open --limit 10 --json number,title,labels,body`;
    
    const output = execSync(command, { encoding: 'utf-8' });
    const issues = JSON.parse(output);
    
    for (const issue of issues) {
      const { complexity, agent } = this.analyzeComplexity(issue);
      
      console.log(`\nIssue #${issue.number}: ${issue.title}`);
      console.log(`  Complexity: ${complexity}`);
      console.log(`  Assigned to: ${agent}`);
      
      // Check if already assigned
      const hasAgentLabel = issue.labels.some(l => 
        l.name.includes('copilot-assigned') || 
        l.name.includes('claude-ready')
      );
      
      if (!hasAgentLabel) {
        switch (agent) {
          case 'copilot':
            await this.assignToCopilot(issue.number);
            break;
          case 'claude':
            const branch = `issue-${issue.number}`;
            await this.createClaudeTask(issue.number, branch);
            break;
          case 'human':
            console.log(`  👤 Requires human review`);
            break;
        }
      }
    }
  }
}

// CLI usage
if (require.main === module) {
  const [owner, repo] = process.argv.slice(2);
  
  if (!owner || !repo) {
    console.log('Usage: node agent-dispatcher.js <owner> <repo>');
    process.exit(1);
  }
  
  const dispatcher = new AgentDispatcher(owner, repo);
  
  // Run once or continuously
  if (process.env.CONTINUOUS === 'true') {
    setInterval(() => dispatcher.monitorIssues(), 60000); // Every minute
  } else {
    dispatcher.monitorIssues();
  }
}

module.exports = AgentDispatcher;