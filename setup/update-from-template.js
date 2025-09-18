#!/usr/bin/env node

/**
 * Template Update System
 * Updates existing projects with latest template changes
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class TemplateUpdater {
  constructor() {
    this.templateRepo = 'https://github.com/vanman2024/multi-agent-claude-code.git';
    this.tempDir = '/tmp/template-update';
    this.projectRoot = process.cwd();
    this.templateVersionFile = '.template-version';
    
    // Safe-to-update paths (won't overwrite user code)
    this.safeUpdatePaths = [
      'devops/',
      'agentswarm/', 
      'agents/',
      'template-agents/',
      '.github/workflows/version-management.yml',
      'scripts/ops',
      'automation/',
      '.gitmessage',
      'VERSIONING.md'
    ];
    
    // Preserve user files (never overwrite)
    this.preservePaths = [
      'src/',
      'app/',
      'components/',
      'pages/',
      'api/',
      'lib/',
      '.env*',
      'package.json',
      'pyproject.toml',
      'requirements.txt',
      'README.md'  // User's project README
    ];
  }

  async checkCurrentVersion() {
    const versionFile = path.join(this.projectRoot, this.templateVersionFile);
    if (fs.existsSync(versionFile)) {
      return fs.readFileSync(versionFile, 'utf8').trim();
    }
    return null;
  }

  async getLatestTemplateVersion() {
    try {
      // Clone template to temp directory
      if (fs.existsSync(this.tempDir)) {
        execSync(`rm -rf ${this.tempDir}`);
      }
      
      console.log('🔍 Checking latest template version...');
      execSync(`git clone --depth 1 ${this.templateRepo} ${this.tempDir}`, { stdio: 'pipe' });
      
      const versionFile = path.join(this.tempDir, 'VERSION');
      if (fs.existsSync(versionFile)) {
        const content = fs.readFileSync(versionFile, 'utf8');
        const match = content.match(/version:\s*(.+)/);
        return match ? match[1].trim() : null;
      }
      
      return null;
    } catch (error) {
      console.error('❌ Failed to check template version:', error.message);
      return null;
    }
  }

  async showAvailableUpdates() {
    const currentVersion = await this.checkCurrentVersion();
    const latestVersion = await this.getLatestTemplateVersion();
    
    console.log('\n📊 Template Version Status:');
    console.log(`   Current: ${currentVersion || 'Unknown'}`);
    console.log(`   Latest:  ${latestVersion || 'Unknown'}`);
    
    if (!currentVersion) {
      console.log('\n⚠️  No template version tracking found. Run with --force to initialize.');
      return false;
    }
    
    if (currentVersion === latestVersion) {
      console.log('\n✅ Project is up to date with latest template!');
      return false;
    }
    
    console.log('\n🔄 Updates available!');
    return true;
  }

  async updateProject(options = {}) {
    const { force = false, preview = false } = options;
    
    if (!force) {
      const hasUpdates = await this.showAvailableUpdates();
      if (!hasUpdates && !force) {
        return;
      }
    }

    console.log('\n🚀 Starting template update...');
    
    // Ensure we have latest template
    await this.getLatestTemplateVersion();
    
    const changes = [];
    
    // Process safe update paths
    for (const safePath of this.safeUpdatePaths) {
      const templatePath = path.join(this.tempDir, safePath);
      const projectPath = path.join(this.projectRoot, safePath);
      
      if (fs.existsSync(templatePath)) {
        const stat = fs.statSync(templatePath);
        
        if (stat.isDirectory()) {
          await this.updateDirectory(templatePath, projectPath, changes, preview);
        } else {
          await this.updateFile(templatePath, projectPath, changes, preview);
        }
      }
    }
    
    if (preview) {
      console.log('\n📋 Preview of changes:');
      changes.forEach(change => console.log(`   ${change}`));
      console.log('\nRun without --preview to apply changes.');
      return;
    }
    
    if (changes.length === 0) {
      console.log('\n✅ No changes needed.');
      return;
    }
    
    // Update template version
    const latestVersion = await this.getLatestTemplateVersion();
    if (latestVersion) {
      fs.writeFileSync(
        path.join(this.projectRoot, this.templateVersionFile), 
        `TEMPLATE_VERSION=${latestVersion}\n`
      );
      changes.push('Updated .template-version');
    }
    
    console.log('\n✅ Template update completed!');
    console.log(`📝 Applied ${changes.length} changes:`);
    changes.forEach(change => console.log(`   • ${change}`));
    
    // Cleanup
    execSync(`rm -rf ${this.tempDir}`);
  }

  async updateDirectory(templateDir, projectDir, changes, preview) {
    if (!fs.existsSync(templateDir)) return;
    
    const files = fs.readdirSync(templateDir);
    
    for (const file of files) {
      const templateFile = path.join(templateDir, file);
      const projectFile = path.join(projectDir, file);
      
      const stat = fs.statSync(templateFile);
      
      if (stat.isDirectory()) {
        await this.updateDirectory(templateFile, projectFile, changes, preview);
      } else {
        await this.updateFile(templateFile, projectFile, changes, preview);
      }
    }
  }

  async updateFile(templateFile, projectFile, changes, preview) {
    const templateContent = fs.readFileSync(templateFile, 'utf8');
    
    // Check if file exists and is different
    if (fs.existsSync(projectFile)) {
      const projectContent = fs.readFileSync(projectFile, 'utf8');
      if (templateContent === projectContent) {
        return; // No changes needed
      }
    }
    
    const relativePath = path.relative(this.projectRoot, projectFile);
    
    if (!preview) {
      // Ensure directory exists
      const dir = path.dirname(projectFile);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      fs.writeFileSync(projectFile, templateContent);
    }
    
    changes.push(fs.existsSync(projectFile) ? `Updated ${relativePath}` : `Created ${relativePath}`);
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const options = {
    force: args.includes('--force'),
    preview: args.includes('--preview'),
    check: args.includes('--check')
  };
  
  const updater = new TemplateUpdater();
  
  if (options.check) {
    await updater.showAvailableUpdates();
  } else {
    await updater.updateProject(options);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { TemplateUpdater };