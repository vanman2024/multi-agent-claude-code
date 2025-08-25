#!/usr/bin/env node

/**
 * Notification Integration Script
 * Integrates the notification system with the existing multi-agent system
 */

const NotificationServer = require('./app/server');
const AgentDispatcher = require('./scripts/agent-dispatcher');
const { execSync } = require('child_process');

class NotificationIntegration {
  constructor() {
    this.notificationServer = null;
    this.isServerRunning = false;
  }

  /**
   * Start the notification server
   */
  async startNotificationServer(port = 3000) {
    if (this.isServerRunning) {
      console.log('📱 Notification server already running');
      return;
    }

    console.log('🚀 Starting notification server...');
    this.notificationServer = new NotificationServer(port);
    this.notificationServer.start();
    this.isServerRunning = true;
    
    // Wait for server to start
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log('✅ Notification server ready');
  }

  /**
   * Send notification via API
   */
  async sendNotification(userId, title, message, type = 'info', priority = 'normal') {
    if (!this.isServerRunning) {
      console.log('⚠️ Notification server not running, starting...');
      await this.startNotificationServer();
    }

    try {
      const response = await fetch('http://localhost:3000/api/v1/notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId,
          title,
          message,
          type,
          priority
        })
      });

      if (response.ok) {
        const notification = await response.json();
        console.log(`📬 Notification sent to ${userId}: ${title}`);
        return notification;
      } else {
        const error = await response.json();
        console.error('❌ Failed to send notification:', error);
        return null;
      }
    } catch (error) {
      console.error('❌ Notification error:', error.message);
      return null;
    }
  }

  /**
   * Enhanced agent dispatcher with notifications
   */
  async enhanceAgentDispatcher() {
    console.log('🔧 Enhancing agent dispatcher with notifications...');

    // Extend the existing AgentDispatcher class
    const originalAssignToCopilot = AgentDispatcher.prototype.assignToCopilot;
    const originalCreateClaudeTask = AgentDispatcher.prototype.createClaudeTask;

    // Override assignToCopilot to send notifications
    AgentDispatcher.prototype.assignToCopilot = async function(issueNumber) {
      const result = await originalAssignToCopilot.call(this, issueNumber);
      
      if (result) {
        await integration.sendNotification(
          'developer',
          'Task Assigned',
          `Issue #${issueNumber} has been assigned to GitHub Copilot`,
          'info',
          'normal'
        );
      }
      
      return result;
    };

    // Override createClaudeTask to send notifications
    AgentDispatcher.prototype.createClaudeTask = async function(issueNumber, branch) {
      const result = await originalCreateClaudeTask.call(this, issueNumber, branch);
      
      await integration.sendNotification(
        'developer',
        'Claude Agent Started',
        `Claude Code agent is working on issue #${issueNumber} in branch ${branch}`,
        'info',
        'high'
      );
      
      return result;
    };

    console.log('✅ Agent dispatcher enhanced with notifications');
  }

  /**
   * Add GitHub webhook integration
   */
  setupGitHubWebhooks() {
    console.log('🔗 Setting up GitHub webhook integration...');
    
    // This would typically be a separate webhook server
    // For now, we'll just create the notification endpoints

    const express = require('express');
    const app = express();
    app.use(express.json());

    // Issue events
    app.post('/webhook/github/issues', async (req, res) => {
      const { action, issue, repository } = req.body;
      const userId = 'developer'; // Would be determined from issue assignee

      switch (action) {
        case 'opened':
          await this.sendNotification(
            userId,
            'New Issue Created',
            `Issue #${issue.number}: ${issue.title}`,
            'info',
            'normal'
          );
          break;
          
        case 'closed':
          await this.sendNotification(
            userId,
            'Issue Completed',
            `Issue #${issue.number} has been closed`,
            'success',
            'normal'
          );
          break;
      }

      res.status(200).json({ status: 'processed' });
    });

    // Pull request events
    app.post('/webhook/github/pulls', async (req, res) => {
      const { action, pull_request, repository } = req.body;
      const userId = 'developer';

      switch (action) {
        case 'opened':
          await this.sendNotification(
            userId,
            'Pull Request Created',
            `PR #${pull_request.number}: ${pull_request.title}`,
            'info',
            'normal'
          );
          break;
          
        case 'merged':
          await this.sendNotification(
            userId,
            'Pull Request Merged',
            `PR #${pull_request.number} has been merged`,
            'success',
            'high'
          );
          break;
      }

      res.status(200).json({ status: 'processed' });
    });

    // Start webhook server on different port
    app.listen(3001, () => {
      console.log('🎣 GitHub webhook server running on port 3001');
    });
  }

  /**
   * Create notification helpers for common scenarios
   */
  async notifyAgentStart(issueNumber, agentType) {
    return await this.sendNotification(
      'developer',
      `${agentType} Agent Started`,
      `Working on issue #${issueNumber}`,
      'info',
      'normal'
    );
  }

  async notifyAgentComplete(issueNumber, agentType, success = true) {
    return await this.sendNotification(
      'developer',
      `${agentType} Agent ${success ? 'Completed' : 'Failed'}`,
      `Issue #${issueNumber} ${success ? 'resolved' : 'needs attention'}`,
      success ? 'success' : 'error',
      success ? 'normal' : 'high'
    );
  }

  async notifySystemError(error, context) {
    return await this.sendNotification(
      'developer',
      'System Error',
      `Error in ${context}: ${error.message}`,
      'error',
      'urgent'
    );
  }

  async notifyTestResults(passed, total, context) {
    const success = passed === total;
    return await this.sendNotification(
      'developer',
      `Tests ${success ? 'Passed' : 'Failed'}`,
      `${passed}/${total} tests passed in ${context}`,
      success ? 'success' : 'warning',
      success ? 'normal' : 'high'
    );
  }

  /**
   * Run a demo of the integrated system
   */
  async runDemo() {
    console.log('🎬 Running notification system demo...\n');

    await this.startNotificationServer();
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Demo scenario: Agent workflow
    await this.notifyAgentStart(123, 'Claude Code');
    await new Promise(resolve => setTimeout(resolve, 2000));

    await this.sendNotification(
      'developer',
      'Code Analysis Complete',
      'Found 3 files to modify for issue #123',
      'info',
      'normal'
    );
    await new Promise(resolve => setTimeout(resolve, 2000));

    await this.sendNotification(
      'developer',
      'Tests Running',
      'Running automated tests for changes...',
      'info',
      'normal'
    );
    await new Promise(resolve => setTimeout(resolve, 3000));

    await this.notifyTestResults(8, 8, 'notification system');
    await new Promise(resolve => setTimeout(resolve, 1000));

    await this.notifyAgentComplete(123, 'Claude Code', true);

    console.log('\n🎯 Demo complete! Check http://localhost:3000 to see the notifications');
  }
}

// Create global integration instance
const integration = new NotificationIntegration();

// Add fetch polyfill for Node.js
if (typeof fetch === 'undefined') {
  global.fetch = require('node-fetch');
}

// CLI usage
if (require.main === module) {
  const command = process.argv[2];

  switch (command) {
    case 'start':
      integration.startNotificationServer();
      break;
      
    case 'demo':
      integration.runDemo();
      break;
      
    case 'webhook':
      integration.startNotificationServer();
      integration.setupGitHubWebhooks();
      break;
      
    default:
      console.log(`
🔔 Notification Integration Commands:

  node notification-integration.js start   - Start notification server
  node notification-integration.js demo    - Run integration demo
  node notification-integration.js webhook - Start with GitHub webhooks

Examples:
  # Start notification server
  node notification-integration.js start

  # Run demo with sample notifications  
  node notification-integration.js demo
      `);
  }
}

module.exports = NotificationIntegration;