#!/usr/bin/env node
/**
 * Comprehensive Project Sync Script
 * Syncs agent files, MCP configs, settings, and project essentials
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_FILE = path.join(__dirname, '..', 'project', 'project-sync-config.template.json');
const TEMPLATES_DIR = path.join(__dirname, '..', 'docker');

class ProjectSync {
  constructor(projectRoot = process.cwd()) {
    this.projectRoot = projectRoot;
    this.config = this.loadConfig();
    this.detectedTechStack = null;
  }

  loadConfig() {
    try {
      const configContent = fs.readFileSync(CONFIG_FILE, 'utf8');
      return JSON.parse(configContent);
    } catch (error) {
      console.error('❌ Failed to load project sync config:', error.message);
      process.exit(1);
    }
  }

  detectTechStack() {
    console.log('🔍 Detecting technology stack...');
    
    const patterns = this.config.techStackDetection.patterns;
    const detected = {};

    // Check for frontend frameworks
    if (this.fileExists('package.json')) {
      const packageJson = this.readJsonFile('package.json');
      const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
      
      if (deps.react || deps.next || deps['@types/react']) {
        detected.frontend = 'react';
        if (deps.next) detected.framework = 'nextjs';
      }
    }

    // Check for backend frameworks
    if (this.fileExists('requirements.txt') || this.fileExists('pyproject.toml')) {
      detected.backend = 'python';
      
      const reqContent = this.fileExists('requirements.txt') ? 
        fs.readFileSync(path.join(this.projectRoot, 'requirements.txt'), 'utf8') : '';
      const pyprojectContent = this.fileExists('pyproject.toml') ?
        fs.readFileSync(path.join(this.projectRoot, 'pyproject.toml'), 'utf8') : '';
      
      if (reqContent.includes('fastapi') || pyprojectContent.includes('fastapi')) {
        detected.framework = 'fastapi';
      } else if (reqContent.includes('django') || pyprojectContent.includes('django')) {
        detected.framework = 'django';
      } else if (reqContent.includes('flask') || pyprojectContent.includes('flask')) {
        detected.framework = 'flask';
      }
    }

    // Check for Node.js backend
    if (this.fileExists('package.json') && !detected.backend) {
      const packageJson = this.readJsonFile('package.json');
      const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
      
      if (deps.express || deps.fastify || deps['@nestjs/core']) {
        detected.backend = 'node';
        if (deps.express) detected.framework = 'express';
        if (deps.fastify) detected.framework = 'fastify';
        if (deps['@nestjs/core']) detected.framework = 'nestjs';
      }
    }

    // Determine project type
    if (detected.frontend && detected.backend) {
      detected.type = 'full-stack';
    } else if (detected.frontend) {
      detected.type = 'frontend';
    } else if (detected.backend) {
      detected.type = 'backend';
    } else {
      detected.type = 'unknown';
    }

    this.detectedTechStack = detected;
    console.log('✅ Detected tech stack:', detected);
    return detected;
  }

  syncAgentFiles() {
    console.log('👥 Syncing agent files...');
    
    const agentFiles = this.config.agentFiles;
    let syncCount = 0;

    // Sync required agent files
    for (const agentFile of agentFiles.required) {
      let sourcePath;
      let targetPath;

      // Check if file is in project-sync first (like .github files)
      if (agentFile.startsWith('.github/')) {
        sourcePath = path.join(__dirname, '..', agentFile);
        targetPath = path.join(this.projectRoot, agentFile);
      } else if (agentFile.startsWith('template-agents/')) {
        // Agent template files are in project-sync/template-agents/ but go to agents/ in project
        sourcePath = path.join(__dirname, '..', agentFile);
        // Extract just the filename and place in agents/ directory
        const fileName = path.basename(agentFile);
        targetPath = path.join(this.projectRoot, 'agents', fileName);
      } else if (agentFile.startsWith('scripts/')) {
        // Scripts are in project-sync/scripts/
        sourcePath = path.join(__dirname, '..', agentFile);
        targetPath = path.join(this.projectRoot, agentFile);
      } else if (agentFile.startsWith('automation/')) {
        // Automation config template
        sourcePath = path.join(__dirname, '..', agentFile);
        if (agentFile.endsWith('.template')) {
          // Remove .template extension for target
          const targetFile = agentFile.replace('.template', '');
          targetPath = path.join(this.projectRoot, '.automation', path.basename(targetFile));
        } else {
          targetPath = path.join(this.projectRoot, '.automation', path.basename(agentFile));
        }
      } else if (agentFile.startsWith('docs/')) {
        // Documentation files
        sourcePath = path.join(__dirname, '..', agentFile);
        targetPath = path.join(this.projectRoot, agentFile);
      } else {
        sourcePath = path.join(__dirname, '..', '..', agentFile);
        targetPath = path.join(this.projectRoot, agentFile);
      }
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        
        // Make scripts executable
        if (agentFile.startsWith('scripts/')) {
          try {
            fs.chmodSync(targetPath, 0o755);
          } catch (error) {
            console.log(`  ⚠️  Could not make ${agentFile} executable: ${error.message}`);
          }
        }
        
        syncCount++;
        const displayPath = agentFile.startsWith('template-agents/') ? 'agents/' + path.basename(agentFile) : agentFile;
        console.log(`  ✅ Synced ${displayPath}`);
      } else {
        console.log(`  ⚠️  Source not found: ${agentFile}`);
      }
    }

    // Sync optional agent files if they exist
    for (const agentFile of agentFiles.optional || []) {
      let sourcePath;
      let targetPath;

      if (agentFile.startsWith('template-agents/')) {
        sourcePath = path.join(__dirname, '..', agentFile);
        // Extract just the filename and place in agents/ directory
        const fileName = path.basename(agentFile);
        targetPath = path.join(this.projectRoot, 'agents', fileName);
      } else {
        sourcePath = path.join(__dirname, '..', '..', agentFile);
        targetPath = path.join(this.projectRoot, agentFile);
      }
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        syncCount++;
        const displayPath = agentFile.startsWith('template-agents/') ? 'agents/' + path.basename(agentFile) : agentFile;
        console.log(`  ✅ Synced optional ${displayPath}`);
      }
    }

    // Sync agentswarm directory if it exists
    for (const agentSwarmDir of agentFiles.agentSwarm || []) {
      const sourcePath = path.join(__dirname, '..', agentSwarmDir);
      const targetPath = path.join(this.projectRoot, agentSwarmDir);
      
      if (fs.existsSync(sourcePath)) {
        this.copyDirectoryRecursively(sourcePath, targetPath, false);
        syncCount++;
        console.log(`  ✅ Synced ${agentSwarmDir} directory`);
      }
    }

    console.log(`📁 Synced ${syncCount} agent files`);

    // Ensure agents directory exists
    const agentsDir = path.join(this.projectRoot, 'agents');
    this.ensureDirectoryExists(agentsDir);
    console.log('  📁 Agent files synced to agents/ directory');
  }

  syncGitHubWorkflows() {
    console.log('⚙️  Syncing GitHub workflows...');
    
    const workflows = this.config.githubWorkflows?.essential || [];
    let workflowCount = 0;
    
    for (const workflow of workflows) {
      const sourcePath = path.join(__dirname, '..', workflow);
      const targetPath = path.join(this.projectRoot, workflow);
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        workflowCount++;
        console.log(`  ✅ Synced ${workflow}`);
      } else {
        console.log(`  ⚠️  Workflow not found: ${workflow}`);
      }
    }
    
    if (workflowCount > 0) {
      console.log(`🔄 Synced ${workflowCount} GitHub workflows`);
    }
  }

  syncGitHubIssueTemplates() {
    console.log('📋 Syncing GitHub issue templates...');
    
    const issueTemplates = [
      '.github/ISSUE_TEMPLATE/bug_report.yml',
      '.github/ISSUE_TEMPLATE/feature_request.yml',
      '.github/ISSUE_TEMPLATE/task.yml',
      '.github/ISSUE_TEMPLATE/hotfix.yml',
      '.github/ISSUE_TEMPLATE/config.yml'
    ];
    
    let templateCount = 0;
    
    for (const template of issueTemplates) {
      const sourcePath = path.join(__dirname, '..', template);
      const targetPath = path.join(this.projectRoot, template);
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        templateCount++;
        console.log(`  ✅ Synced ${path.basename(template)}`);
      } else {
        console.log(`  ⚠️  Template not found: ${template}`);
      }
    }
    
    if (templateCount > 0) {
      console.log(`📋 Synced ${templateCount} issue templates`);
    }
  }

  syncVersioningSystem() {
    console.log('🏷️  Syncing versioning system...');
    
    const versioningSource = path.join(__dirname, '..', 'templates', 'versioning');
    
    if (!fs.existsSync(versioningSource)) {
      console.log('  ⚠️  Versioning templates not found');
      return;
    }
    
    let syncCount = 0;
    
    // Copy .gitmessage to project root
    const gitmessageSource = path.join(versioningSource, '.gitmessage');
    const gitmessageTarget = path.join(this.projectRoot, '.gitmessage');
    
    if (fs.existsSync(gitmessageSource)) {
      if (!fs.existsSync(gitmessageTarget)) {
        fs.copyFileSync(gitmessageSource, gitmessageTarget);
        syncCount++;
        console.log('  ✅ Synced .gitmessage template');
      } else {
        console.log('  ℹ️  .gitmessage already exists, skipping');
      }
    }
    
    
    // Configure git to use the commit template
    try {
      execSync(`cd "${this.projectRoot}" && git config commit.template .gitmessage`, {
        stdio: 'pipe',
        cwd: this.projectRoot
      });
      console.log('  ✅ Configured git commit template');
    } catch (error) {
      console.log('  ⚠️  Could not configure git commit template:', error.message);
    }
    
    // Create initial VERSION file if it doesn't exist
    const versionFile = path.join(this.projectRoot, 'VERSION');
    if (!fs.existsSync(versionFile)) {
      const initialVersion = {
        version: 'v0.1.0',
        commit: 'initial',
        build_date: new Date().toISOString(),
        build_type: 'production'
      };
      fs.writeFileSync(versionFile, JSON.stringify(initialVersion, null, 2));
      console.log('  ✅ Created initial VERSION file');
      syncCount++;
    }
    
    if (syncCount > 0) {
      console.log(`  ✅ Synced ${syncCount} versioning components`);
      console.log('  📋 Versioning system configured:');
      console.log('     • .gitmessage - Conventional commit template with multi-agent signatures');
      console.log('     • VERSION file - Tracks project version and build metadata');
      console.log('     • Git commit template configured for conventional commits');
      console.log('     • Workflow: version-management.yml synced via GitHub workflows');
    } else {
      console.log('  ℹ️  Versioning system already configured');
    }
  }

  syncMcpConfigurations() {
    console.log('🔧 MCP Server Management...');
    
    console.log('  ℹ️  MCP servers are now managed by Claude Code directly');
    console.log('  ℹ️  Use the /add-mcp slash command to configure servers:');
    console.log('     • /add-mcp github    - GitHub repository management');
    console.log('     • /add-mcp vercel    - Deployment and hosting');
    console.log('     • /add-mcp playwright - Browser automation and testing');
    console.log('     • /add-mcp memory    - Persistent context storage');
    console.log('     • /add-mcp all       - Add all essential servers');
    console.log('  ✅ MCP guidance provided');
  }

  syncVSCodeSettings() {
    console.log('⚙️  Syncing VS Code settings...');
    
    // Sync project-level .vscode/settings.json from project-sync template
    const sourceVSCodeDir = path.join(__dirname, '..', '.vscode');
    const targetVSCodeDir = path.join(this.projectRoot, '.vscode');
    
    if (fs.existsSync(sourceVSCodeDir)) {
      this.ensureDirectoryExists(targetVSCodeDir);
      
      // Copy or update settings.json
      const sourceSettings = path.join(sourceVSCodeDir, 'settings.json');
      const targetSettings = path.join(targetVSCodeDir, 'settings.json');
      
      if (fs.existsSync(sourceSettings)) {
        if (!fs.existsSync(targetSettings)) {
          // New file - copy directly
          fs.copyFileSync(sourceSettings, targetSettings);
          console.log('  ✅ Synced .vscode/settings.json');
        } else {
          // Existing file - apply critical updates
          this.updateVSCodeSettings(sourceSettings, targetSettings);
        }
      }
      
      // Copy other VS Code files like extensions.json, launch.json etc
      const vscodeFiles = fs.readdirSync(sourceVSCodeDir);
      for (const file of vscodeFiles) {
        if (file !== 'settings.json') { // We handled settings.json above
          const sourceFile = path.join(sourceVSCodeDir, file);
          const targetFile = path.join(targetVSCodeDir, file);
          
          if (!fs.existsSync(targetFile) && fs.lstatSync(sourceFile).isFile()) {
            fs.copyFileSync(sourceFile, targetFile);
            console.log(`  ✅ Synced .vscode/${file}`);
          }
        }
      }
    } else {
      console.log('  ⚠️  Source .vscode directory not found');
    }
    
    console.log('  ✅ Synced VS Code settings');
  }

  updateVSCodeSettings(sourceSettings, targetSettings) {
    try {
      // Read both files
      const sourceContent = JSON.parse(fs.readFileSync(sourceSettings, 'utf8'));
      const targetContent = JSON.parse(fs.readFileSync(targetSettings, 'utf8'));
      
      // Critical updates to apply to existing files
      const criticalUpdates = {
        'workbench.iconTheme': 'vs-seti'  // Fix file icons disappearing
      };
      
      let updated = false;
      for (const [key, value] of Object.entries(criticalUpdates)) {
        if (targetContent[key] !== value) {
          targetContent[key] = value;
          updated = true;
        }
      }
      
      if (updated) {
        // Write back the updated settings
        fs.writeFileSync(targetSettings, JSON.stringify(targetContent, null, 2));
        console.log('  🔄 Updated .vscode/settings.json with critical fixes (file icons)');
      } else {
        console.log('  ↪️  .vscode/settings.json already up to date');
      }
      
    } catch (error) {
      console.log('  ⚠️  Could not update VS Code settings:', error.message);
    }
  }

  syncProjectEssentials() {
    console.log('📋 Syncing project essentials...');

    // Don't copy README.md - each project should have its own README
    // The agents/README.md provides the multi-agent documentation

    // Copy .env file directly (not just example)
    const envTarget = path.join(this.projectRoot, '.env');
    const envSource = path.join(__dirname, '..', '.env');

    if (!fs.existsSync(envTarget) && fs.existsSync(envSource)) {
      fs.copyFileSync(envSource, envTarget);
      console.log('  ✅ Created .env with API keys');
    }

    // Copy .gitignore if it doesn't exist
    const gitignoreTarget = path.join(this.projectRoot, '.gitignore');
    const gitignoreSource = path.join(__dirname, '..', '.gitignore');

    if (!fs.existsSync(gitignoreTarget) && fs.existsSync(gitignoreSource)) {
      fs.copyFileSync(gitignoreSource, gitignoreTarget);
      console.log('  ✅ Created .gitignore');
    }

    // Sync production readiness tools
    this.syncProductionReadinessTools();
    
    // Sync hooks  
    this.syncHooks();
    
    // Sync documentation
    this.syncDocumentation();

    // Update .gitignore with additional entries
    this.updateGitignore();
    
    // Add testing commands to package.json if applicable
    this.updatePackageJsonScripts();
  }

  syncProductionReadinessTools() {
    console.log('🔍 Syncing production readiness tools...');
    
    // Create scripts directory
    const scriptsDir = path.join(this.projectRoot, 'scripts', 'helpers');
    this.ensureDirectoryExists(scriptsDir);
    
    // Copy helper scripts
    const helperScripts = ['scan-mocks.sh', 'check-apis.sh', 'test-coverage.sh', 'security-scan.sh'];
    let scriptCount = 0;
    
    for (const script of helperScripts) {
      const sourceScript = path.join(__dirname, 'helpers', script);
      const targetScript = path.join(scriptsDir, script);
      if (fs.existsSync(sourceScript)) {
        fs.copyFileSync(sourceScript, targetScript);
        fs.chmodSync(targetScript, '755');
        scriptCount++;
      }
    }
    
    if (scriptCount > 0) {
      console.log(`  ✅ Synced ${scriptCount} production readiness helper scripts`);
    }
    
    // Now sync all main scripts directories
    this.syncMainScripts();
  }
  
  syncMainScripts() {
    console.log('📜 Syncing project scripts...');
    
    // Copy from project-sync/project/ and project-sync/docker/
    const sourceProjectDir = path.join(__dirname, '..', 'project');
    const sourceDockerDir = path.join(__dirname, '..', 'docker');
    const targetScriptsDir = path.join(this.projectRoot, 'scripts');
    
    let scriptCount = 0;
    
    // Copy Docker scripts from the dedicated docker directory
    if (fs.existsSync(sourceDockerDir)) {
      // Copy docker-scripts.sh to project root
      const dockerScript = path.join(sourceDockerDir, 'docker-scripts.sh');
      if (fs.existsSync(dockerScript)) {
        const targetDockerScript = path.join(this.projectRoot, 'docker-scripts.sh');
        if (!fs.existsSync(targetDockerScript)) {
          fs.copyFileSync(dockerScript, targetDockerScript);
          fs.chmodSync(targetDockerScript, '755');
          scriptCount++;
          console.log(`  ✅ Synced docker-scripts.sh`);
        }
      }
      
      // Copy sync-docker.js to scripts directory
      const syncDockerScript = path.join(sourceDockerDir, 'sync-docker.js');
      if (fs.existsSync(syncDockerScript)) {
        const targetSyncDockerScript = path.join(targetScriptsDir, 'sync-docker.js');
        this.ensureDirectoryExists(targetScriptsDir);
        if (!fs.existsSync(targetSyncDockerScript)) {
          fs.copyFileSync(syncDockerScript, targetSyncDockerScript);
          fs.chmodSync(targetSyncDockerScript, '755');
          scriptCount++;
          console.log(`  ✅ Synced sync-docker.js`);
        }
      }
    }
    
    // Copy other project scripts if the project directory exists
    if (fs.existsSync(sourceProjectDir)) {
      // Copy helpers directory if it exists
      const helpersSourceDir = path.join(sourceProjectDir, 'helpers');
      const helpersTargetDir = path.join(targetScriptsDir, 'helpers');
      if (fs.existsSync(helpersSourceDir)) {
        this.copyDirectoryRecursively(helpersSourceDir, helpersTargetDir, false);
        // Make helper scripts executable
        if (fs.existsSync(helpersTargetDir)) {
          const helperFiles = fs.readdirSync(helpersTargetDir);
          for (const file of helperFiles) {
            if (file.endsWith('.sh')) {
              fs.chmodSync(path.join(helpersTargetDir, file), '755');
            }
          }
        }
        scriptCount++;
        console.log(`  ✅ Synced helpers directory`);
      }
    }
    
    console.log(`  ✅ Synced ${scriptCount} project-useful scripts (no bloat)`);
  }

  syncHooks() {
    console.log('🪝 Syncing hooks...');
    
    // Create .claude/hooks directory
    const hooksDir = path.join(this.projectRoot, '.claude', 'hooks');
    this.ensureDirectoryExists(hooksDir);
    
    // Copy essential hooks
    const hooks = ['load-context.sh', 'save-work-state.sh'];
    let hookCount = 0;
    
    for (const hook of hooks) {
      const sourceHook = path.join(__dirname, '..', 'hooks', hook);
      const targetHook = path.join(hooksDir, hook);
      if (fs.existsSync(sourceHook)) {
        fs.copyFileSync(sourceHook, targetHook);
        fs.chmodSync(targetHook, '755');
        hookCount++;
      }
    }
    
    if (hookCount > 0) {
      console.log(`  ✅ Synced ${hookCount} hooks`);
    }
  }

  syncDocumentation() {
    console.log('📚 Syncing documentation...');
    
    // Create docs directory
    const docsDir = path.join(this.projectRoot, 'docs');
    this.ensureDirectoryExists(docsDir);
    
    // Copy essential docs
    const docs = ['TESTING-STRATEGY.md', 'AI-AGENT-MOCK-TO-PRODUCTION-GUIDE.md', 'API-MOCK-TESTING.md', 'AI-DEVELOPMENT-WORKFLOW.md'];
    let docCount = 0;
    
    for (const doc of docs) {
      const sourceDoc = path.join(__dirname, '..', 'docs', doc);
      const targetDoc = path.join(docsDir, doc);
      if (fs.existsSync(sourceDoc)) {
        fs.copyFileSync(sourceDoc, targetDoc);
        docCount++;
      }
    }
    
    if (docCount > 0) {
      console.log(`  ✅ Synced ${docCount} documentation files`);
    }
  }

  syncClaudeDirectory() {
    console.log('🤖 Syncing .claude directory...');
    
    const sourceClaudeDir = path.join(__dirname, '..', '.claude');
    const targetClaudeDir = path.join(this.projectRoot, '.claude');
    
    if (!fs.existsSync(sourceClaudeDir)) {
      console.log('  ⚠️  Source .claude directory not found');
      return;
    }
    
    this.copyDirectoryRecursively(sourceClaudeDir, targetClaudeDir, false); // Don't overwrite existing
    
    // Now merge settings properly - keep hooks from project, add permissions from global
    const globalSettingsPath = path.join(require('os').homedir(), '.claude', 'settings.json');
    const targetSettingsPath = path.join(targetClaudeDir, 'settings.json');
    const sourceSettingsPath = path.join(sourceClaudeDir, 'settings.json');
    
    try {
      // Start with the project template settings (has hooks)
      let settings = {};
      if (fs.existsSync(sourceSettingsPath)) {
        settings = JSON.parse(fs.readFileSync(sourceSettingsPath, 'utf8'));
      }
      
      // Convert relative hook paths to absolute paths for this specific project
      if (settings.hooks) {
        for (const eventType in settings.hooks) {
          const eventHooks = settings.hooks[eventType];
          for (const hookGroup of eventHooks) {
            if (hookGroup.hooks) {
              for (const hook of hookGroup.hooks) {
                if (hook.type === 'command' && hook.command) {
                  // Replace relative .claude/hooks/ paths with absolute paths
                  if (hook.command.includes('.claude/hooks/')) {
                    const scriptName = hook.command.split('.claude/hooks/')[1];
                    const commandPrefix = hook.command.split(' ')[0]; // bash or python3
                    hook.command = `${commandPrefix} ${path.join(this.projectRoot, '.claude', 'hooks', scriptName)}`;
                  }
                }
              }
            }
          }
        }
        console.log('  ✅ Converted hook paths to absolute for current project');
      }
      
      // Add permissions from global settings if they exist
      if (fs.existsSync(globalSettingsPath)) {
        const globalSettings = JSON.parse(fs.readFileSync(globalSettingsPath, 'utf8'));
        
        // Merge in permissions and MCP settings from global, but keep hooks from project
        if (globalSettings.permissions) {
          settings.permissions = globalSettings.permissions;
        }
        if (globalSettings.mcpServers) {
          settings.mcpServers = globalSettings.mcpServers;
        }
        // Keep the hooks from the project template, don't overwrite them!
      }
      
      // Write the merged settings
      fs.writeFileSync(targetSettingsPath, JSON.stringify(settings, null, 2));
      console.log('  ✅ Merged Claude settings (project hooks + global permissions)');
      
    } catch (error) {
      console.log('  ⚠️  Could not merge Claude settings:', error.message);
      // Fall back to copying source if merge fails
      if (fs.existsSync(sourceSettingsPath)) {
        fs.copyFileSync(sourceSettingsPath, targetSettingsPath);
      }
    }
    
    // Make hook and script files executable
    const executableDirs = ['hooks', 'scripts'];
    for (const dir of executableDirs) {
      const dirPath = path.join(targetClaudeDir, dir);
      if (fs.existsSync(dirPath)) {
        const files = fs.readdirSync(dirPath);
        for (const file of files) {
          if (file.endsWith('.sh') || file.endsWith('.py')) {
            const filePath = path.join(dirPath, file);
            fs.chmodSync(filePath, '755');
          }
        }
      }
    }
    
    console.log('  ✅ Synced complete .claude directory with commands, agents, and hooks');
  }
  
  syncSpecKit() {
    console.log('📋 Syncing spec-kit files...');
    
    const sourceSpecKitDir = path.join(__dirname, '..', 'spec-kit');
    const targetSpecKitDir = path.join(this.projectRoot, 'spec-kit');
    
    if (!fs.existsSync(sourceSpecKitDir)) {
      console.log('  ⚠️  Source spec-kit directory not found');
      return;
    }
    
    this.copyDirectoryRecursively(sourceSpecKitDir, targetSpecKitDir, false); // Don't overwrite existing
    
    // Make scripts executable
    const updateScript = path.join(targetSpecKitDir, 'update-agent-context.sh');
    if (fs.existsSync(updateScript)) {
      fs.chmodSync(updateScript, '755');
    }
    
    console.log('  ✅ Synced spec-kit templates and scripts');
  }

  syncDockerTemplates() {
    console.log('🐳 Syncing Docker development environment...');

    const sourceDockerDir = path.join(__dirname, '..', 'docker');

    if (!fs.existsSync(sourceDockerDir)) {
      console.log('  ⚠️  Docker templates not found');
      return;
    }

    // Create docker directory
    const targetDockerDir = path.join(this.projectRoot, 'docker');
    this.ensureDirectoryExists(targetDockerDir);

    // Copy Docker files to docker/ subdirectory and some to root
    const dockerFiles = [
      { src: 'docker-dev.template.yml', dest: 'docker/docker-compose.dev.yml' },
      { src: 'Dockerfile.dev.template', dest: 'docker/Dockerfile.dev' },
      { src: '.env.docker.example', dest: 'docker/.env.docker.example' },
      { src: '.dockerignore', dest: '.dockerignore' },  // Keep in root
      { src: 'docker-scripts.sh', dest: 'docker-scripts.sh' }  // Keep in root for easy access
    ];
    
    let copiedCount = 0;
    for (const file of dockerFiles) {
      const sourcePath = path.join(sourceDockerDir, file.src);
      const targetPath = path.join(this.projectRoot, file.dest);
      
      if (fs.existsSync(sourcePath) && !fs.existsSync(targetPath)) {
        fs.copyFileSync(sourcePath, targetPath);
        
        // Make shell scripts executable
        if (file.dest.endsWith('.sh')) {
          fs.chmodSync(targetPath, '755');
        }
        
        copiedCount++;
        console.log(`  ✅ Created ${file.dest}`);
      }
    }

    const includeDevcontainer = process.argv.includes('--devcontainer');
    if (includeDevcontainer) {
      const devcontainerDir = path.join(this.projectRoot, '.devcontainer');
      if (!fs.existsSync(devcontainerDir)) {
        fs.mkdirSync(devcontainerDir, { recursive: true });

        const devcontainerSrc = path.join(sourceDockerDir, 'devcontainer.json.template');
        const devcontainerDest = path.join(devcontainerDir, 'devcontainer.json');

        if (fs.existsSync(devcontainerSrc)) {
          fs.copyFileSync(devcontainerSrc, devcontainerDest);
          console.log('  ✅ Created .devcontainer/devcontainer.json for VS Code');
        }
      }
    } else {
      console.log('  ℹ️  Dev container setup skipped (enable with --devcontainer)');
    }

    if (copiedCount > 0) {
      console.log(`  ✅ Docker development environment ready!`);
      console.log(`     Run: ./docker-scripts.sh dev-up`);
    } else {
      console.log('  ℹ️  Docker files already exist');
    }
  }
  

  updateConstitution() {
    console.log('📜 Updating project constitution with multi-agent rules...');

    const constitutionPath = path.join(this.projectRoot, '.specify', 'memory', 'constitution.md');
    const addonPath = path.join(__dirname, 'constitution-multi-agent-addon.md');

    // Check if constitution.md exists (created by spec-kit)
    if (fs.existsSync(constitutionPath)) {
      // Read existing constitution
      let constitutionContent = fs.readFileSync(constitutionPath, 'utf8');

      // Check if multi-agent rules already added
      if (!constitutionContent.includes('Multi-Agent Coordination Principles')) {
        // Read addon content
        const addonContent = fs.readFileSync(addonPath, 'utf8');

        // Find where to insert (before governance section or at end)
        const governanceIndex = constitutionContent.indexOf('## Governance');

        if (governanceIndex > -1) {
          // Insert before governance section
          constitutionContent =
            constitutionContent.slice(0, governanceIndex) +
            '\n' + addonContent + '\n\n' +
            constitutionContent.slice(governanceIndex);
        } else {
          // Append at end before version info
          const versionIndex = constitutionContent.lastIndexOf('**Version**:');
          if (versionIndex > -1) {
            constitutionContent =
              constitutionContent.slice(0, versionIndex) +
              '\n' + addonContent + '\n\n' +
              constitutionContent.slice(versionIndex);
          } else {
            // Just append at end
            constitutionContent += '\n\n' + addonContent;
          }
        }

        // Write updated constitution
        fs.writeFileSync(constitutionPath, constitutionContent);
        console.log('  ✅ Added multi-agent coordination principles to constitution.md');
      } else {
        console.log('  ℹ️  Multi-agent rules already in constitution.md');
      }
    } else {
      console.log('  ⚠️  No constitution.md found. Run spec-kit init first.');
    }
  }

  syncSetupTemplates() {
    console.log('📋 Syncing setup templates...');

    // These templates from setup/ directory are used for project configuration
    const setupTemplates = [
      // Removed vscode-settings.template.json since we already copy settings.json
      { source: 'wsl-setup.template.sh', target: 'scripts/wsl-setup.sh' }
    ];
    
    let templateCount = 0;
    
    for (const template of setupTemplates) {
      const sourcePath = path.join(__dirname, template.source);
      const targetPath = path.join(this.projectRoot, template.target);
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        if (!fs.existsSync(targetPath)) {
          fs.copyFileSync(sourcePath, targetPath);
          if (template.source.endsWith('.sh')) {
            fs.chmodSync(targetPath, '755');
          }
          templateCount++;
          console.log(`  ✅ Synced ${template.target}`);
        }
      }
    }
    
    if (templateCount > 0) {
      console.log(`  ✅ Synced ${templateCount} setup templates`);
    }
  }

  copyDirectoryRecursively(source, target, overwrite = false) {
    if (!fs.existsSync(source)) return;
    
    this.ensureDirectoryExists(target);
    
    const items = fs.readdirSync(source);
    for (const item of items) {
      const sourcePath = path.join(source, item);
      const targetPath = path.join(target, item);
      
      if (fs.lstatSync(sourcePath).isDirectory()) {
        this.copyDirectoryRecursively(sourcePath, targetPath, overwrite);
      } else {
        // Only copy if target doesn't exist or overwrite is true
        if (!fs.existsSync(targetPath) || overwrite) {
          fs.copyFileSync(sourcePath, targetPath);
        }
      }
    }
  }

  updateGitignore() {
    const gitignorePath = path.join(this.projectRoot, '.gitignore');
    const additions = this.config.projectEssentials.gitignoreAdditions;
    
    if (fs.existsSync(gitignorePath)) {
      const currentContent = fs.readFileSync(gitignorePath, 'utf8');
      const newEntries = additions.filter(entry => !currentContent.includes(entry.replace('# ', '')));
      
      if (newEntries.length > 0) {
        fs.appendFileSync(gitignorePath, '\n' + newEntries.join('\n') + '\n');
        console.log(`  ✅ Added ${newEntries.length} entries to .gitignore`);
      }
    }
  }

  updatePackageJsonScripts() {
    const packageJsonPath = path.join(this.projectRoot, 'package.json');
    if (!fs.existsSync(packageJsonPath)) return;

    const packageJson = this.readJsonFile('package.json');
    const techStack = this.detectedTechStack;
    
    if (!techStack) return;

    // Get testing standards for detected tech stack
    const testingKey = this.getTestingKey(techStack);
    const testingStandards = this.config.testingStandards.commandsByTechStack[testingKey];
    
    if (testingStandards) {
      let updated = false;
      packageJson.scripts = packageJson.scripts || {};
      
      for (const [script, command] of Object.entries(testingStandards)) {
        if (!packageJson.scripts[script]) {
          packageJson.scripts[script] = command;
          updated = true;
        }
      }
      
      if (updated) {
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('  ✅ Added testing scripts to package.json');
      }
    }
  }

  getTestingKey(techStack) {
    if (techStack.frontend === 'react' && techStack.framework === 'nextjs') {
      return 'react-nextjs';
    }
    if (techStack.backend === 'python' && techStack.framework === 'fastapi') {
      return 'python-fastapi';
    }
    if (techStack.backend === 'python' && techStack.framework === 'django') {
      return 'python-django';
    }
    if (techStack.backend === 'node' && techStack.framework === 'express') {
      return 'node-express';
    }
    return 'react-nextjs'; // default
  }

  // Utility methods
  fileExists(filePath) {
    return fs.existsSync(path.join(this.projectRoot, filePath));
  }

  readJsonFile(filePath) {
    try {
      const content = fs.readFileSync(path.join(this.projectRoot, filePath), 'utf8');
      return JSON.parse(content);
    } catch (error) {
      return {};
    }
  }

  ensureDirectoryExists(dirPath) {
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  }

  syncTestingStructure() {
    console.log('🧪 Syncing testing structure...');
    
    let syncCount = 0;
    const packageJsonPath = path.join(this.projectRoot, 'package.json');
    const pyprojectPath = path.join(this.projectRoot, 'pyproject.toml');
    const requirementsPath = path.join(this.projectRoot, 'requirements.txt');
    
    // Check for skip flags
    const skipBackend = process.argv.includes('--frontend-only') || process.argv.includes('--no-testing');
    const skipFrontend = process.argv.includes('--backend-only') || process.argv.includes('--no-testing');
    
    // Auto-detect project type
    const isPython = fs.existsSync(pyprojectPath) || fs.existsSync(requirementsPath);
    const isNode = fs.existsSync(packageJsonPath);
    
    console.log(`  🔍 Project detection: Python=${isPython}, Node.js=${isNode}`);
    
    // Always sync complete backend testing structure (language-agnostic)
    if (!skipBackend) {
      const backendTestsSource = path.join(__dirname, '..', 'tests', 'backend');
      const backendTestsTarget = path.join(this.projectRoot, 'tests', 'backend');
      
      if (fs.existsSync(backendTestsSource)) {
        console.log('  📋 Syncing backend testing structure (language-agnostic)...');
        this.copyDirectoryRecursive(backendTestsSource, backendTestsTarget);
        syncCount++;
      }
      
      // Also copy conftest.py and helpers regardless of project type
      const conftestSource = path.join(__dirname, '..', 'tests', 'conftest.py');
      const conftestTarget = path.join(this.projectRoot, 'tests', 'conftest.py');
      if (fs.existsSync(conftestSource)) {
        fs.copyFileSync(conftestSource, conftestTarget);
        console.log('  ✅ Synced conftest.py (testing configuration)');
      }
      
      const helpersSource = path.join(__dirname, '..', 'tests', 'helpers');
      const helpersTarget = path.join(this.projectRoot, 'tests', 'helpers');
      if (fs.existsSync(helpersSource)) {
        this.copyDirectoryRecursive(helpersSource, helpersTarget);
        console.log('  ✅ Synced tests/helpers/ (testing utilities)');
      }
    }
    
    // Always sync complete frontend testing structure (language-agnostic)
    if (!skipFrontend) {
      const frontendTestsSource = path.join(__dirname, '..', 'tests', 'frontend');
      const frontendTemplateTarget = path.join(this.projectRoot, 'tests', 'frontend');
      
      if (fs.existsSync(frontendTestsSource)) {
        console.log('  🎭 Syncing frontend testing structure (Playwright/TypeScript)...');
        
        // Copy frontend tests but exclude .github folder (we'll merge it separately)
        this.copyDirectoryRecursiveWithExclusions(frontendTestsSource, frontendTemplateTarget, ['.github']);
        
        // Merge frontend CI workflow into root .github folder
        const frontendGithubSource = path.join(frontendTestsSource, '.github');
        const rootGithubTarget = path.join(this.projectRoot, '.github');
        
        if (fs.existsSync(frontendGithubSource)) {
          this.ensureDirectoryExists(rootGithubTarget);
          this.ensureDirectoryExists(path.join(rootGithubTarget, 'workflows'));
          
          // Copy CI workflow with descriptive name
          const frontendCiSource = path.join(frontendGithubSource, 'workflows', 'ci.yml');
          const frontendCiTarget = path.join(rootGithubTarget, 'workflows', 'frontend-tests.yml');
          
          if (fs.existsSync(frontendCiSource)) {
            fs.copyFileSync(frontendCiSource, frontendCiTarget);
            console.log('  📋 Merged frontend CI workflow to .github/workflows/frontend-tests.yml');
          }
        }
        
        console.log('  📋 Frontend testing ready - tests/frontend/ configured');
        syncCount++;
      }
    } else if (!skipFrontend && !isNode) {
      console.log('  ⚠️  Frontend testing skipped (no Node.js project detected)');
    }
    
    // Show skip messages
    if (skipBackend && isPython) {
      console.log('  ⏭️  Backend testing skipped (--frontend-only or --no-testing flag)');
    }
    if (skipFrontend && isNode) {
      console.log('  ⏭️  Frontend testing skipped (--backend-only or --no-testing flag)');
    }
    
    if (syncCount > 0) {
      console.log(`  ✅ Synced ${syncCount} testing suites`);
      console.log('  📁 Created dual testing architecture:');
      
      if (!skipBackend && isPython) {
        console.log('     • tests/backend/ - Python/pytest backend testing');
        console.log('       • tests/backend/smoke/ - Quick validation tests');
        console.log('       • tests/backend/unit/ - Individual component tests');
        console.log('       • tests/backend/integration/ - External service tests');
        console.log('       • tests/backend/contract/ - API contract tests');
        console.log('       • tests/backend/performance/ - Performance benchmarks');
        console.log('       • Run: ./devops/ops/ops qa --backend');
      }
      
      if (!skipFrontend && isNode) {
        console.log('     • tests/frontend/ - Playwright/TypeScript frontend testing');
        console.log('       • Smart E2E strategy (5-10% critical journeys)');
        console.log('       • Visual regression, accessibility, API testing');
        console.log('       • Run: ./devops/ops/ops qa --frontend');
      }
      
      if (!skipBackend && !skipFrontend && isPython && isNode) {
        console.log('     • Full-stack testing: ./devops/ops/ops qa --all');
      }
    } else if (process.argv.includes('--no-testing')) {
      console.log('  ⏭️  Testing setup skipped (--no-testing flag)');
    } else {
      console.log('  ⚠️  No matching project types detected for testing templates');
    }
  }

  syncDevOpsSystem() {
    console.log('🔧 Syncing DevOps system...');
    
    try {
      // Sync the entire devops directory
      const devopsSource = path.join(__dirname, '..', 'devops');
      const devopsTarget = path.join(this.projectRoot, 'devops');
      
      if (fs.existsSync(devopsSource)) {
        this.copyDirectoryRecursive(devopsSource, devopsTarget);
        
        console.log('  ✅ DevOps system files synced');
        console.log('    • devops/ops/ - Operations scripts');
        console.log('    • devops/deploy/ - Deployment scripts');
        console.log('    • devops/ci/ - CI/CD workflows');
        
        // Make scripts executable
        const scriptsToMakeExecutable = [
          path.join(devopsTarget, 'ops', 'ops'),
          path.join(devopsTarget, 'deploy', 'deploy')
        ];
        
        scriptsToMakeExecutable.forEach(scriptPath => {
          if (fs.existsSync(scriptPath)) {
            fs.chmodSync(scriptPath, '755');
          }
        });
        
        console.log('  ✅ Made DevOps scripts executable');
      } else {
        console.log('  ⚠️  DevOps source directory not found');
      }
      
    } catch (error) {
      console.log('  ⚠️  DevOps system sync failed:', error.message);
    }
  }
  
  copyDirectoryRecursive(source, target) {
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    
    const items = fs.readdirSync(source);
    
    for (const item of items) {
      const sourcePath = path.join(source, item);
      const targetPath = path.join(target, item);
      
      const stat = fs.statSync(sourcePath);
      
      if (stat.isDirectory()) {
        this.copyDirectoryRecursive(sourcePath, targetPath);
      } else {
        // Handle template files
        if (item.includes('PROJECT_NAME')) {
          const projectName = path.basename(this.projectRoot);
          let content = fs.readFileSync(sourcePath, 'utf8');
          content = content.replace(/PROJECT_NAME/g, projectName);
          fs.writeFileSync(targetPath, content);
        } else {
          fs.copyFileSync(sourcePath, targetPath);
        }
        
        // Preserve executable permissions
        if (stat.mode & parseInt('111', 8)) {
          fs.chmodSync(targetPath, '755');
        }
      }
    }
  }

  copyDirectoryRecursiveWithExclusions(source, target, exclusions = []) {
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    
    const items = fs.readdirSync(source);
    
    for (const item of items) {
      // Skip excluded items
      if (exclusions.includes(item)) {
        continue;
      }
      
      const sourcePath = path.join(source, item);
      const targetPath = path.join(target, item);
      
      const stat = fs.statSync(sourcePath);
      
      if (stat.isDirectory()) {
        this.copyDirectoryRecursiveWithExclusions(sourcePath, targetPath, exclusions);
      } else {
        // Handle template files
        if (item.includes('PROJECT_NAME')) {
          const projectName = path.basename(this.projectRoot);
          let content = fs.readFileSync(sourcePath, 'utf8');
          content = content.replace(/PROJECT_NAME/g, projectName);
          fs.writeFileSync(targetPath, content);
        } else {
          fs.copyFileSync(sourcePath, targetPath);
        }
        
        // Preserve executable permissions
        if (stat.mode & parseInt('111', 8)) {
          fs.chmodSync(targetPath, '755');
        }
      }
    }
  }

  runDevOpsSetup() {
    console.log('\n🔧 Setting up DevOps system...');
    
    const projectName = path.basename(this.projectRoot);
    const setupBackend = !process.argv.includes('--frontend-only');
    const setupFrontend = !process.argv.includes('--backend-only');
    const setupTesting = !process.argv.includes('--no-testing');
    const setupAgents = !process.argv.includes('--no-agents');
    
    try {
      // Create project configuration
      this.createDevOpsConfig(projectName, setupBackend, setupFrontend, setupTesting, setupAgents);
      
      // Setup development environment files
      this.setupDevEnvironment();
      
      // Make DevOps scripts executable
      this.makeDevOpsExecutable();
      
      // Initialize DevOps system if available
      this.initializeDevOpsSystem();
      
      // Create setup summary
      this.createDevOpsSetupSummary(projectName, setupBackend, setupFrontend, setupTesting, setupAgents);
      
      console.log('  ✅ DevOps system setup completed');
      
    } catch (error) {
      console.log('  ⚠️  DevOps setup completed with warnings:', error.message);
    }
  }

  createDevOpsConfig(projectName, setupBackend, setupFrontend, setupTesting, setupAgents) {
    const devopsDir = path.join(this.projectRoot, 'devops');
    if (!fs.existsSync(devopsDir)) return;
    
    // Look for pyproject.toml.template in devops directory
    const templateFile = path.join(devopsDir, 'pyproject.toml.template');
    const projectConfigFile = path.join(this.projectRoot, 'pyproject.toml');
    
    if (!fs.existsSync(templateFile)) {
      console.log('  ⚠️  pyproject.toml.template not found, skipping DevOps config');
      return;
    }
    
    try {
      // Read template
      let templateContent = fs.readFileSync(templateFile, 'utf8');
      
      // Replace template variables
      const projectType = setupBackend && setupFrontend ? 'fullstack' : (setupBackend ? 'backend' : 'frontend');
      const projectDescription = `${projectType.charAt(0).toUpperCase() + projectType.slice(1)} project with AI agent coordination`;
      
      templateContent = templateContent
        .replace(/\{\{PROJECT_NAME\}\}/g, projectName)
        .replace(/\{\{PROJECT_DESCRIPTION\}\}/g, projectDescription)
        .replace(/\{\{AUTHOR_NAME\}\}/g, 'Developer')
        .replace(/\{\{AUTHOR_EMAIL\}\}/g, 'developer@example.com');
      
      // Write transformed pyproject.toml
      fs.writeFileSync(projectConfigFile, templateContent);
      console.log('  ✅ Created pyproject.toml from template');
      
      // Remove template file after use
      fs.unlinkSync(templateFile);
      console.log('  🗑️  Removed pyproject.toml.template');
      
    } catch (error) {
      console.log('  ⚠️  Failed to create pyproject.toml from template:', error.message);
    }
  }

  setupDevEnvironment() {
    // Create .env.example if it doesn't exist
    const envExamplePath = path.join(this.projectRoot, '.env.example');
    if (!fs.existsSync(envExamplePath)) {
      const envTemplate = `# Environment Variables Template
# Copy to .env and fill in your values

# API Keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Database
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Application
# NODE_ENV=development
# PORT=3000

# Add your project-specific environment variables here
`;
      fs.writeFileSync(envExamplePath, envTemplate);
      console.log('  ✅ Created .env.example template');
    }

    // Update .gitignore with DevOps entries
    const gitignorePath = path.join(this.projectRoot, '.gitignore');
    if (fs.existsSync(gitignorePath)) {
      const currentContent = fs.readFileSync(gitignorePath, 'utf8');
      if (!currentContent.includes('# DevOps System')) {
        const devopsIgnores = `
# DevOps System
devops/ops/.venv/
devops/ops/logs/
devops/deploy/logs/
devops/ci/logs/

# Testing
testing/*/logs/
testing/*/screenshots/
testing/*/videos/
testing/*/reports/
test-results/
playwright-report/

# Agent Configuration
agents/logs/
agents/temp/
`;
        fs.appendFileSync(gitignorePath, devopsIgnores);
        console.log('  ✅ Updated .gitignore with DevOps entries');
      }
    }
  }

  makeDevOpsExecutable() {
    const devopsScripts = [
      path.join(this.projectRoot, 'devops', 'ops', 'ops'),
      path.join(this.projectRoot, 'devops', 'deploy', 'deploy')
    ];
    
    devopsScripts.forEach(scriptPath => {
      if (fs.existsSync(scriptPath)) {
        fs.chmodSync(scriptPath, '755');
      }
    });
    
    console.log('  ✅ Made DevOps scripts executable');
  }

  initializeDevOpsSystem() {
    const opsScript = path.join(this.projectRoot, 'devops', 'ops', 'ops');
    if (fs.existsSync(opsScript)) {
      try {
        execSync(`cd "${this.projectRoot}" && "${opsScript}" setup`, {
          stdio: 'pipe',
          cwd: this.projectRoot
        });
        console.log('  ✅ Initialized DevOps system');
      } catch (error) {
        console.log('  ⚠️  DevOps system initialization completed with warnings');
      }
    }
  }

  createDevOpsSetupSummary(projectName, setupBackend, setupFrontend, setupTesting, setupAgents) {
    const summaryPath = path.join(this.projectRoot, 'DEVOPS_SETUP.md');
    const projectType = setupBackend && setupFrontend ? 'Full-stack' : (setupBackend ? 'Backend' : 'Frontend');
    
    const summary = `# DevOps Setup Summary - ${projectName}

**Setup completed on**: ${new Date().toDateString()}

## Project Configuration
- **Name**: ${projectName}
- **Type**: ${projectType}
- **Python Version**: 3.11 (backend)
- **Node Version**: 18 (frontend)

## Features Enabled
- Backend Development: ${setupBackend}
- Frontend Development: ${setupFrontend}  
- Testing Framework: ${setupTesting}
- AI Agents: ${setupAgents}

## Quick Start Commands

### Development Workflow
\`\`\`bash
# Run quality checks (lint, test, typecheck)
./devops/ops/ops qa

# Build for production
./devops/ops/ops build

# Check project status
./devops/ops/ops status

# Deploy to production
./devops/deploy/deploy production
\`\`\`

### Testing
\`\`\`bash
${setupBackend ? `# Backend tests
./devops/ops/ops qa --backend
pytest testing/backend/

` : ''}${setupFrontend ? `# Frontend tests  
./devops/ops/ops qa --frontend
npx playwright test

` : ''}# All tests
./devops/ops/ops qa --all
\`\`\`

## Directory Structure
\`\`\`
${projectName}/
├── devops/                 # DevOps system
│   ├── ops/               # Operations scripts
│   ├── deploy/            # Deployment scripts  
│   └── ci/                # CI/CD workflows
${setupTesting ? `├── testing/               # Testing framework
${setupBackend ? '│   ├── backend/           # Backend tests' : ''}
${setupFrontend ? '│   └── frontend/          # Frontend tests' : ''}` : ''}
${setupAgents ? '├── agents/                # AI agent config' : ''}
└── [your project files]
\`\`\`

## Next Steps
1. Copy \`.env.example\` to \`.env\` and configure
2. Install dependencies for your project type
3. Run \`./devops/ops/ops qa\` to verify setup
4. Start developing with AI agents as your partners!

## Getting Help
- DevOps system: \`./devops/ops/ops --help\`
- Deployment: \`./devops/deploy/deploy --help\`  
- Testing: Check \`testing/*/README.md\`
- AI Agents: See \`agents/README.md\`

Generated by sync-project.js v1.0
`;

    fs.writeFileSync(summaryPath, summary);
    console.log('  ✅ Created DevOps setup summary');
  }

  createTemplateVersionTracking() {
    console.log('🏷️  Setting up template version tracking...');
    
    try {
      // Read current template version from VERSION file
      const versionFile = path.join(__dirname, '..', 'VERSION');
      let templateVersion = 'unknown';
      
      if (fs.existsSync(versionFile)) {
        const versionContent = fs.readFileSync(versionFile, 'utf8');
        const match = versionContent.match(/version:\s*(.+)/);
        templateVersion = match ? match[1].trim() : 'unknown';
      }
      
      // Create .template-version file in project
      const templateVersionFile = path.join(this.projectRoot, '.template-version');
      const versionInfo = `TEMPLATE_VERSION=${templateVersion}
TEMPLATE_REPO=https://github.com/vanman2024/multi-agent-claude-code
SYNC_DATE=${new Date().toISOString().split('T')[0]}

# Template Update Commands:
# /update-from-template --check     # Check for updates
# /update-from-template --preview   # Preview changes  
# /update-from-template             # Apply updates
`;
      
      fs.writeFileSync(templateVersionFile, versionInfo);
      console.log(`  ✅ Created .template-version (${templateVersion})`);
      
      // Copy update script to project
      const updateScriptSource = path.join(__dirname, 'update-from-template.js');
      const updateScriptTarget = path.join(this.projectRoot, 'setup', 'update-from-template.js');
      
      this.ensureDirectoryExists(path.dirname(updateScriptTarget));
      fs.copyFileSync(updateScriptSource, updateScriptTarget);
      console.log('  ✅ Copied template update script');
      
      // Copy slash command template
      const slashCommandSource = path.join(__dirname, '..', 'templates', 'slash-commands', 'update-from-template.md');
      const slashCommandTarget = path.join(this.projectRoot, 'templates', 'slash-commands', 'update-from-template.md');
      
      this.ensureDirectoryExists(path.dirname(slashCommandTarget));
      if (fs.existsSync(slashCommandSource)) {
        fs.copyFileSync(slashCommandSource, slashCommandTarget);
        console.log('  ✅ Copied template update slash command');
      }
      
      // Add update commands to next steps
      this.updateCommands = [
        'Check for template updates: /update-from-template --check',
        'Preview template updates: /update-from-template --preview', 
        'Apply template updates: /update-from-template'
      ];
      
    } catch (error) {
      console.log(`  ⚠️  Failed to set up template version tracking: ${error.message}`);
    }
  }

  async run() {
    console.log('🚀 Starting comprehensive project sync...\n');
    
    // Show available flags
    if (process.argv.includes('--help')) {
      console.log('📁 Available flags:');
      console.log('  --backend-only    : Skip frontend testing setup');
      console.log('  --frontend-only   : Skip backend testing setup');
      console.log('  --no-testing      : Skip all testing setup');
      console.log('  --devcontainer    : Include VS Code dev container configuration');
      console.log('  --help           : Show this help');
      console.log('');
      return;
    }
    
    try {
      // 1. Detect technology stack
      this.detectTechStack();
      console.log('');

      // 2. Sync all components
      this.syncVSCodeSettings();
      this.syncAgentFiles();
      this.syncClaudeDirectory();
      this.syncSpecKit();
      this.updateConstitution();  // Update constitution after spec-kit creates it
      this.syncDockerTemplates();
      this.syncSetupTemplates();
      this.syncMcpConfigurations();
      this.syncTestingStructure();
      this.syncDevOpsSystem();  // Sync DevOps system files
      this.syncProjectEssentials();
      this.syncGitHubIssueTemplates();  // Sync GitHub issue templates
      this.syncVersioningSystem();  // Sync versioning system (templates/versioning)
      this.createTemplateVersionTracking();  // Track template version for future updates
      this.runDevOpsSetup();  // Run DevOps setup after all syncing

      console.log('\n✅ Project sync completed successfully!');
      console.log('\n📋 Next steps:');
      console.log('  1. Review synced agent files in agents/ directory');
      console.log('  2. Add MCP servers: /add-mcp all');
      console.log('  3. Review .env file and update API keys as needed');
      console.log('  4. Run testing commands to verify setup');
      
      if (this.updateCommands && this.updateCommands.length > 0) {
        console.log('\n🔄 Template update commands:');
        this.updateCommands.forEach((cmd, i) => {
          console.log(`  ${i + 5}. ${cmd}`);
        });
      }
      
      if (this.detectedTechStack) {
        const testKey = this.getTestingKey(this.detectedTechStack);
        const commands = this.config.testingStandards.commandsByTechStack[testKey];
        if (commands) {
          console.log('\n🧪 Available testing commands:');
          Object.entries(commands).forEach(([script, cmd]) => {
            console.log(`    ${script}: ${cmd}`);
          });
        }
      }
      
    } catch (error) {
      console.error('\n❌ Project sync failed:', error.message);
      process.exit(1);
    }
  }
}

// Run if called directly
if (require.main === module) {
  const projectRoot = process.argv[2] || process.cwd();
  const sync = new ProjectSync(projectRoot);
  sync.run();
}

module.exports = ProjectSync;
