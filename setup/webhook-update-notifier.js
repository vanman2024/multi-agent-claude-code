#!/usr/bin/env node
/**
 * Webhook Update Notifier
 * Sends notifications to deployed projects when template updates are available
 * Can be integrated into template repository CI/CD to notify all deployed projects
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

class WebhookUpdateNotifier {
  constructor() {
    this.templateRepo = 'vanman2024/multi-agent-claude-code';
    this.deployedProjects = [];
    this.webhookSecret = process.env.TEMPLATE_WEBHOOK_SECRET || 'template-update-secret';
  }

  /**
   * Add a deployed project to receive update notifications
   */
  addProject(config) {
    const project = {
      id: config.id || crypto.randomBytes(8).toString('hex'),
      name: config.name,
      webhookUrl: config.webhookUrl,
      owner: config.owner,
      repo: config.repo,
      deployedVersion: config.deployedVersion,
      criticalUpdatesOnly: config.criticalUpdatesOnly || false,
      autoUpdate: config.autoUpdate || false,
      lastNotified: null
    };
    
    this.deployedProjects.push(project);
    this.saveProjectRegistry();
    
    return project.id;
  }

  /**
   * Remove a project from update notifications
   */
  removeProject(projectId) {
    this.deployedProjects = this.deployedProjects.filter(p => p.id !== projectId);
    this.saveProjectRegistry();
  }

  /**
   * Notify all registered projects of template updates
   */
  async notifyProjects(updateInfo) {
    console.log(`📢 Notifying ${this.deployedProjects.length} deployed projects of template updates...`);
    
    const results = {
      successful: [],
      failed: [],
      skipped: []
    };
    
    for (const project of this.deployedProjects) {
      try {
        const shouldNotify = this.shouldNotifyProject(project, updateInfo);
        
        if (!shouldNotify) {
          results.skipped.push({ project: project.name, reason: 'No critical updates' });
          continue;
        }
        
        const notificationPayload = this.createNotificationPayload(project, updateInfo);
        
        if (project.autoUpdate) {
          // Trigger auto-update in the project
          await this.triggerAutoUpdate(project, notificationPayload);
        } else {
          // Send notification webhook
          await this.sendWebhook(project, notificationPayload);
        }
        
        project.lastNotified = new Date().toISOString();
        results.successful.push(project.name);
        
      } catch (error) {
        console.error(`❌ Failed to notify ${project.name}:`, error.message);
        results.failed.push({ project: project.name, error: error.message });
      }
    }
    
    this.saveProjectRegistry();
    
    console.log(`✅ Notification complete: ${results.successful.length} successful, ${results.failed.length} failed, ${results.skipped.length} skipped`);
    return results;
  }

  /**
   * Check if a project should be notified of this update
   */
  shouldNotifyProject(project, updateInfo) {
    // Don't notify if already up to date
    if (project.deployedVersion === updateInfo.latestVersion) {
      return false;
    }
    
    // If project only wants critical updates, check priority
    if (project.criticalUpdatesOnly) {
      const hasCriticalUpdates = updateInfo.changes.some(change => 
        change.priority === 'high' || 
        change.path.includes('devops/') || 
        change.path.includes('agentswarm/')
      );
      return hasCriticalUpdates;
    }
    
    return true;
  }

  /**
   * Create notification payload for a project
   */
  createNotificationPayload(project, updateInfo) {
    return {
      event: 'template_update_available',
      timestamp: new Date().toISOString(),
      template: {
        repository: this.templateRepo,
        currentVersion: updateInfo.currentVersion,
        latestVersion: updateInfo.latestVersion,
        updateUrl: `https://github.com/${this.templateRepo}/compare/${updateInfo.currentVersion}...${updateInfo.latestVersion}`
      },
      project: {
        id: project.id,
        name: project.name,
        deployedVersion: project.deployedVersion
      },
      updates: {
        total: updateInfo.changes.length,
        critical: updateInfo.changes.filter(c => c.priority === 'high').length,
        changes: updateInfo.changes.map(change => ({
          path: change.path,
          type: change.type,
          priority: change.priority
        }))
      },
      actions: {
        checkCommand: '/update-from-template --check',
        previewCommand: '/update-from-template --preview',
        updateCommand: '/update-from-template',
        forceUpdateCommand: '/update-from-template --force'
      }
    };
  }

  /**
   * Send webhook notification to a project
   */
  async sendWebhook(project, payload) {
    return new Promise((resolve, reject) => {
      const payloadString = JSON.stringify(payload);
      const signature = this.createWebhookSignature(payloadString);
      
      const url = new URL(project.webhookUrl);
      const options = {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname + url.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payloadString),
          'X-Template-Signature': signature,
          'X-Template-Event': 'update_available',
          'User-Agent': 'Template-Update-Notifier/1.0'
        }
      };
      
      const req = https.request(options, (res) => {
        let responseData = '';
        
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            console.log(`✅ Notified ${project.name} successfully`);
            resolve({ statusCode: res.statusCode, data: responseData });
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${responseData}`));
          }
        });
      });
      
      req.on('error', (error) => {
        reject(error);
      });
      
      req.write(payloadString);
      req.end();
    });
  }

  /**
   * Trigger auto-update in a project via GitHub Actions
   */
  async triggerAutoUpdate(project, payload) {
    if (!project.owner || !project.repo) {
      throw new Error('Project owner/repo required for auto-update');
    }
    
    // This would trigger a GitHub Actions workflow in the target repository
    // that runs the template update system
    const workflowPayload = {
      ref: 'main',
      inputs: {
        force_update: 'true',
        triggered_by: 'template_webhook',
        template_version: payload.template.latestVersion
      }
    };
    
    console.log(`🔄 Triggering auto-update for ${project.name}...`);
    
    // In a real implementation, this would use GitHub API to trigger the workflow
    // For now, just log the action
    console.log(`Would trigger workflow in ${project.owner}/${project.repo} with:`, workflowPayload);
  }

  /**
   * Create webhook signature for security
   */
  createWebhookSignature(payload) {
    const hmac = crypto.createHmac('sha256', this.webhookSecret);
    hmac.update(payload);
    return `sha256=${hmac.digest('hex')}`;
  }

  /**
   * Verify webhook signature
   */
  verifyWebhookSignature(payload, signature) {
    const expectedSignature = this.createWebhookSignature(payload);
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expectedSignature)
    );
  }

  /**
   * Load project registry from file
   */
  loadProjectRegistry() {
    const registryPath = path.join(__dirname, 'deployed-projects-registry.json');
    
    if (fs.existsSync(registryPath)) {
      try {
        const content = fs.readFileSync(registryPath, 'utf8');
        this.deployedProjects = JSON.parse(content);
      } catch (error) {
        console.warn('Failed to load project registry:', error.message);
        this.deployedProjects = [];
      }
    }
  }

  /**
   * Save project registry to file
   */
  saveProjectRegistry() {
    const registryPath = path.join(__dirname, 'deployed-projects-registry.json');
    
    try {
      fs.writeFileSync(registryPath, JSON.stringify(this.deployedProjects, null, 2));
    } catch (error) {
      console.error('Failed to save project registry:', error.message);
    }
  }

  /**
   * Register a new project deployment
   */
  async registerProject(config) {
    console.log(`📝 Registering project: ${config.name}`);
    
    const projectId = this.addProject(config);
    
    // Send welcome notification
    const welcomePayload = {
      event: 'project_registered',
      timestamp: new Date().toISOString(),
      project: {
        id: projectId,
        name: config.name
      },
      message: 'Your project has been registered for template update notifications',
      actions: {
        checkCommand: '/update-from-template --check',
        unregisterInfo: `Contact admin to unregister project ID: ${projectId}`
      }
    };
    
    if (config.webhookUrl) {
      await this.sendWebhook({ ...config, id: projectId }, welcomePayload);
    }
    
    return projectId;
  }

  /**
   * List all registered projects
   */
  listProjects() {
    return this.deployedProjects.map(project => ({
      id: project.id,
      name: project.name,
      deployedVersion: project.deployedVersion,
      lastNotified: project.lastNotified,
      autoUpdate: project.autoUpdate,
      criticalUpdatesOnly: project.criticalUpdatesOnly
    }));
  }
}

// CLI interface for managing the webhook notifier
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const notifier = new WebhookUpdateNotifier();
  notifier.loadProjectRegistry();
  
  async function runCommand() {
    try {
      switch (command) {
        case 'register':
          const config = JSON.parse(args[1]);
          const projectId = await notifier.registerProject(config);
          console.log(`✅ Project registered with ID: ${projectId}`);
          break;
          
        case 'unregister':
          const projectIdToRemove = args[1];
          notifier.removeProject(projectIdToRemove);
          console.log(`✅ Project ${projectIdToRemove} unregistered`);
          break;
          
        case 'list':
          const projects = notifier.listProjects();
          console.log('📋 Registered Projects:');
          console.table(projects);
          break;
          
        case 'notify':
          const updateInfo = JSON.parse(args[1]);
          const results = await notifier.notifyProjects(updateInfo);
          console.log('Notification results:', results);
          break;
          
        case 'test':
          // Test notification with sample data
          const testUpdate = {
            currentVersion: 'abc123',
            latestVersion: 'def456',
            changes: [
              { path: 'devops/ops/ops', type: 'modified', priority: 'high' },
              { path: 'agentswarm/coordinator.py', type: 'modified', priority: 'high' },
              { path: 'template-agents/CLAUDE.md', type: 'modified', priority: 'medium' }
            ]
          };
          await notifier.notifyProjects(testUpdate);
          break;
          
        default:
          console.log('Webhook Update Notifier');
          console.log('');
          console.log('Commands:');
          console.log('  register <config>  - Register a project for notifications');
          console.log('  unregister <id>    - Unregister a project');
          console.log('  list              - List registered projects');
          console.log('  notify <updates>   - Send notifications to all projects');
          console.log('  test              - Test notifications with sample data');
          console.log('');
          console.log('Example config:');
          console.log('  {');
          console.log('    "name": "My Project",');
          console.log('    "webhookUrl": "https://api.github.com/repos/user/repo/dispatches",');
          console.log('    "owner": "user",');
          console.log('    "repo": "repo",');
          console.log('    "deployedVersion": "abc123",');
          console.log('    "autoUpdate": false,');
          console.log('    "criticalUpdatesOnly": true');
          console.log('  }');
          break;
      }
    } catch (error) {
      console.error('❌ Command failed:', error.message);
      process.exit(1);
    }
  }
  
  runCommand();
}

module.exports = WebhookUpdateNotifier;