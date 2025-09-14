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
      
      // Check if file is in project-sync first (like .github files)
      if (agentFile.startsWith('.github/')) {
        sourcePath = path.join(__dirname, '..', agentFile);
      } else if (agentFile.startsWith('agents/')) {
        // Agent files are in project-sync/agents/
        sourcePath = path.join(__dirname, '..', agentFile);
      } else {
        sourcePath = path.join(__dirname, '..', '..', agentFile);
      }
      
      const targetPath = path.join(this.projectRoot, agentFile);
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        syncCount++;
        console.log(`  ✅ Synced ${agentFile}`);
      } else {
        console.log(`  ⚠️  Source not found: ${agentFile}`);
      }
    }

    // Sync optional agent files if they exist
    for (const agentFile of agentFiles.optional || []) {
      const sourcePath = agentFile.startsWith('agents/') ? 
        path.join(__dirname, '..', agentFile) : 
        path.join(__dirname, '..', '..', agentFile);
      const targetPath = path.join(this.projectRoot, agentFile);
      
      if (fs.existsSync(sourcePath)) {
        this.ensureDirectoryExists(path.dirname(targetPath));
        fs.copyFileSync(sourcePath, targetPath);
        syncCount++;
        console.log(`  ✅ Synced optional ${agentFile}`);
      }
    }

    console.log(`📁 Synced ${syncCount} agent files`);
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
    
    // Make hook files executable
    const hooksDir = path.join(targetClaudeDir, 'hooks');
    if (fs.existsSync(hooksDir)) {
      const hookFiles = fs.readdirSync(hooksDir);
      for (const hookFile of hookFiles) {
        if (hookFile.endsWith('.sh')) {
          const hookPath = path.join(hooksDir, hookFile);
          fs.chmodSync(hookPath, '755');
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
    
    // Copy Docker files to project root (not in docker subdirectory)
    const dockerFiles = [
      { src: 'docker-dev.template.yml', dest: 'docker-compose.dev.yml' },
      { src: 'Dockerfile.dev.template', dest: 'Dockerfile.dev' },
      { src: '.env.docker.example', dest: '.env.docker.example' },
      { src: '.dockerignore', dest: '.dockerignore' },
      { src: 'docker-scripts.sh', dest: 'docker-scripts.sh' }
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
    
    // Create .devcontainer directory if it doesn't exist
    const devcontainerDir = path.join(this.projectRoot, '.devcontainer');
    if (!fs.existsSync(devcontainerDir)) {
      fs.mkdirSync(devcontainerDir, { recursive: true });
      
      // Copy devcontainer.json
      const devcontainerSrc = path.join(sourceDockerDir, 'devcontainer.json.template');
      const devcontainerDest = path.join(devcontainerDir, 'devcontainer.json');
      
      if (fs.existsSync(devcontainerSrc)) {
        fs.copyFileSync(devcontainerSrc, devcontainerDest);
        console.log('  ✅ Created .devcontainer/devcontainer.json for VS Code');
      }
    }
    
    if (copiedCount > 0) {
      console.log(`  ✅ Docker development environment ready!`);
      console.log(`     Run: ./docker-scripts.sh dev-up`);
    } else {
      console.log('  ℹ️  Docker files already exist');
    }
  }
  

  syncSetupTemplates() {
    console.log('📋 Syncing setup templates...');
    
    // These templates from setup/ directory are used for project configuration
    const setupTemplates = [
      { source: 'vscode-settings.template.json', target: '.vscode/settings.template.json' },
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

  async run() {
    console.log('🚀 Starting comprehensive project sync...\n');
    
    try {
      // 1. Detect technology stack
      this.detectTechStack();
      console.log('');

      // 2. Sync all components
      this.syncVSCodeSettings();
      this.syncAgentFiles();
      this.syncClaudeDirectory();
      this.syncSpecKit();
      this.syncDockerTemplates();
      this.syncSetupTemplates();
      this.syncMcpConfigurations();
      this.syncProjectEssentials();

      console.log('\n✅ Project sync completed successfully!');
      console.log('\n📋 Next steps:');
      console.log('  1. Review synced agent files in agents/ directory');
      console.log('  2. Add MCP servers: /add-mcp all');
      console.log('  3. Review .env file and update API keys as needed');
      console.log('  4. Run testing commands to verify setup');
      
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