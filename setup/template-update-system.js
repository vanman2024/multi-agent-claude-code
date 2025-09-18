#!/usr/bin/env node
/**
 * Template Auto-Update System
 * Detects changes in template repository and provides update mechanisms
 * for deployed projects to stay synchronized with template improvements
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

class TemplateUpdateSystem {
  constructor(projectRoot = process.cwd()) {
    this.projectRoot = projectRoot;
    this.templateRepo = 'https://github.com/vanman2024/multi-agent-claude-code.git';
    this.templateVersionFile = path.join(projectRoot, '.template-version');
    this.updateCacheDir = path.join(projectRoot, '.template-cache');
    this.criticalPaths = [
      'devops/',
      'agentswarm/', 
      'template-agents/',
      'scripts/ops',
      '.github/workflows/',
      '.claude/hooks/',
      'setup/sync-project.js'
    ];
  }

  /**
   * Check if updates are available from template repository
   */
  async checkForUpdates(options = {}) {
    console.log('🔍 Checking for template updates...');
    
    try {
      const currentVersion = this.getCurrentTemplateVersion();
      const latestVersion = await this.getLatestTemplateVersion();
      
      if (currentVersion === latestVersion) {
        console.log('✅ Project is up to date with template');
        return { hasUpdates: false, currentVersion, latestVersion };
      }
      
      const changes = await this.getChangesSince(currentVersion);
      const criticalChanges = this.filterCriticalChanges(changes);
      
      console.log(`📦 Template updates available:`);
      console.log(`   Current: ${currentVersion}`);
      console.log(`   Latest: ${latestVersion}`);
      console.log(`   Changes in critical paths: ${criticalChanges.length}`);
      
      if (options.details) {
        this.showUpdateDetails(criticalChanges);
      }
      
      return {
        hasUpdates: true,
        currentVersion,
        latestVersion,
        changes: criticalChanges,
        allChanges: changes
      };
      
    } catch (error) {
      console.error('❌ Failed to check for updates:', error.message);
      return { hasUpdates: false, error: error.message };
    }
  }

  /**
   * Preview what would be updated without applying changes
   */
  async previewUpdates() {
    console.log('👀 Previewing template updates...');
    
    const updateInfo = await this.checkForUpdates({ details: true });
    if (!updateInfo.hasUpdates) {
      return updateInfo;
    }
    
    // Clone template to temporary directory for comparison
    const tempDir = await this.cloneTemplateToTemp();
    
    try {
      const preview = {
        filesToUpdate: [],
        filesToAdd: [],
        conflictingFiles: [],
        backupRequired: []
      };
      
      for (const change of updateInfo.changes) {
        const analysis = await this.analyzeFileChange(change, tempDir);
        
        if (analysis.hasConflict) {
          preview.conflictingFiles.push(analysis);
        } else if (analysis.isNew) {
          preview.filesToAdd.push(analysis);
        } else {
          preview.filesToUpdate.push(analysis);
        }
        
        if (analysis.needsBackup) {
          preview.backupRequired.push(analysis);
        }
      }
      
      this.showPreviewSummary(preview);
      return { ...updateInfo, preview };
      
    } finally {
      this.cleanupTempDir(tempDir);
    }
  }

  /**
   * Apply template updates to current project
   */
  async applyUpdates(options = {}) {
    console.log('🔄 Applying template updates...');
    
    const previewInfo = await this.previewUpdates();
    if (!previewInfo.hasUpdates) {
      return previewInfo;
    }
    
    // Create backup before applying changes
    const backupDir = await this.createBackup();
    console.log(`💾 Created backup at: ${backupDir}`);
    
    try {
      const results = {
        updated: [],
        added: [],
        conflicts: [],
        errors: []
      };
      
      // Apply non-conflicting updates first
      for (const file of previewInfo.preview.filesToUpdate) {
        try {
          await this.updateFile(file);
          results.updated.push(file.path);
          console.log(`  ✅ Updated ${file.path}`);
        } catch (error) {
          results.errors.push({ path: file.path, error: error.message });
          console.log(`  ❌ Failed to update ${file.path}: ${error.message}`);
        }
      }
      
      // Add new files
      for (const file of previewInfo.preview.filesToAdd) {
        try {
          await this.addFile(file);
          results.added.push(file.path);
          console.log(`  ✅ Added ${file.path}`);
        } catch (error) {
          results.errors.push({ path: file.path, error: error.message });
          console.log(`  ❌ Failed to add ${file.path}: ${error.message}`);
        }
      }
      
      // Handle conflicts
      for (const file of previewInfo.preview.conflictingFiles) {
        if (options.autoResolve) {
          try {
            await this.autoResolveConflict(file);
            results.updated.push(file.path);
            console.log(`  ✅ Auto-resolved conflict in ${file.path}`);
          } catch (error) {
            results.conflicts.push(file.path);
            console.log(`  ⚠️  Manual resolution needed for ${file.path}`);
          }
        } else {
          results.conflicts.push(file.path);
          console.log(`  ⚠️  Skipped conflicting file ${file.path} (use --auto-resolve to force)`);
        }
      }
      
      // Update template version
      await this.updateTemplateVersion(previewInfo.latestVersion);
      
      console.log('\n📊 Update Summary:');
      console.log(`   Files updated: ${results.updated.length}`);
      console.log(`   Files added: ${results.added.length}`);
      console.log(`   Conflicts: ${results.conflicts.length}`);
      console.log(`   Errors: ${results.errors.length}`);
      
      if (results.conflicts.length > 0) {
        console.log('\n⚠️  Manual Resolution Needed:');
        results.conflicts.forEach(path => console.log(`   - ${path}`));
        console.log('   Review these files and manually merge changes');
      }
      
      if (results.errors.length === 0 && results.conflicts.length === 0) {
        console.log('\n✅ Template update completed successfully!');
        
        // Optionally run project sync to ensure everything is current
        if (options.runSync) {
          console.log('\n🔄 Running project sync to apply updates...');
          execSync('node setup/sync-project.js', { 
            cwd: this.projectRoot, 
            stdio: 'inherit' 
          });
        }
      }
      
      return { ...previewInfo, results, backupDir };
      
    } catch (error) {
      console.error('❌ Update failed, restoring from backup...');
      await this.restoreFromBackup(backupDir);
      throw error;
    }
  }

  getCurrentTemplateVersion() {
    if (!fs.existsSync(this.templateVersionFile)) {
      return 'unknown';
    }
    
    const content = fs.readFileSync(this.templateVersionFile, 'utf8');
    const match = content.match(/TEMPLATE_VERSION=(.+)/);
    return match ? match[1].trim() : 'unknown';
  }

  async getLatestTemplateVersion() {
    // Get latest commit hash from remote template repository
    try {
      const result = execSync(
        `git ls-remote ${this.templateRepo} HEAD`,
        { encoding: 'utf8' }
      );
      return result.split('\t')[0].substring(0, 8);
    } catch (error) {
      throw new Error(`Failed to get latest template version: ${error.message}`);
    }
  }

  async getChangesSince(version) {
    // This is a simplified version - in production you'd query the git API
    // or maintain a changes manifest in the template repository
    try {
      const tempDir = await this.cloneTemplateToTemp();
      
      // Get list of changed files since version
      const changes = [];
      
      for (const criticalPath of this.criticalPaths) {
        const sourcePath = path.join(tempDir, criticalPath);
        if (fs.existsSync(sourcePath)) {
          if (fs.statSync(sourcePath).isDirectory()) {
            const files = this.getAllFilesInDir(sourcePath);
            files.forEach(file => {
              const relativePath = path.relative(tempDir, file);
              changes.push({
                path: relativePath,
                type: 'modified',
                priority: this.getChangePriority(relativePath)
              });
            });
          } else {
            changes.push({
              path: criticalPath,
              type: 'modified',
              priority: this.getChangePriority(criticalPath)
            });
          }
        }
      }
      
      this.cleanupTempDir(tempDir);
      return changes;
      
    } catch (error) {
      throw new Error(`Failed to get changes: ${error.message}`);
    }
  }

  filterCriticalChanges(changes) {
    return changes.filter(change => 
      this.criticalPaths.some(path => change.path.startsWith(path))
    );
  }

  getChangePriority(filePath) {
    if (filePath.includes('devops/') || filePath.includes('agentswarm/')) {
      return 'high';
    } else if (filePath.includes('.github/workflows/') || filePath.includes('scripts/')) {
      return 'medium';
    }
    return 'low';
  }

  async cloneTemplateToTemp() {
    const tempDir = path.join(this.updateCacheDir, `template-${Date.now()}`);
    fs.mkdirSync(tempDir, { recursive: true });
    
    execSync(`git clone --depth 1 ${this.templateRepo} ${tempDir}`, {
      stdio: 'pipe'
    });
    
    return tempDir;
  }

  async analyzeFileChange(change, tempDir) {
    const tempFilePath = path.join(tempDir, change.path);
    const projectFilePath = path.join(this.projectRoot, change.path);
    
    const analysis = {
      path: change.path,
      priority: change.priority,
      isNew: !fs.existsSync(projectFilePath),
      hasConflict: false,
      needsBackup: false,
      tempPath: tempFilePath,
      projectPath: projectFilePath
    };
    
    if (!analysis.isNew) {
      // Check for conflicts by comparing content
      if (fs.existsSync(tempFilePath) && fs.existsSync(projectFilePath)) {
        const tempHash = this.getFileHash(tempFilePath);
        const projectHash = this.getFileHash(projectFilePath);
        
        if (tempHash !== projectHash) {
          // Further analysis could check if the file was modified locally
          analysis.hasConflict = this.hasLocalModifications(projectFilePath);
          analysis.needsBackup = true;
        }
      }
    }
    
    return analysis;
  }

  hasLocalModifications(filePath) {
    // Simplified check - in production you'd track original hashes
    // or use git to detect local modifications
    return true; // Assume all existing files might have local modifications
  }

  getFileHash(filePath) {
    const content = fs.readFileSync(filePath);
    return crypto.createHash('md5').update(content).digest('hex');
  }

  getAllFilesInDir(dir) {
    const files = [];
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      if (fs.statSync(fullPath).isDirectory()) {
        files.push(...this.getAllFilesInDir(fullPath));
      } else {
        files.push(fullPath);
      }
    }
    
    return files;
  }

  showUpdateDetails(changes) {
    console.log('\n📋 Critical changes detected:');
    
    const grouped = changes.reduce((acc, change) => {
      if (!acc[change.priority]) acc[change.priority] = [];
      acc[change.priority].push(change);
      return acc;
    }, {});
    
    ['high', 'medium', 'low'].forEach(priority => {
      if (grouped[priority]) {
        console.log(`\n🔴 ${priority.toUpperCase()} priority:`);
        grouped[priority].forEach(change => {
          console.log(`   - ${change.path}`);
        });
      }
    });
  }

  showPreviewSummary(preview) {
    console.log('\n📋 Update Preview:');
    
    if (preview.filesToUpdate.length > 0) {
      console.log(`\n🔄 Files to update (${preview.filesToUpdate.length}):`);
      preview.filesToUpdate.forEach(file => {
        console.log(`   - ${file.path} (${file.priority} priority)`);
      });
    }
    
    if (preview.filesToAdd.length > 0) {
      console.log(`\n➕ Files to add (${preview.filesToAdd.length}):`);
      preview.filesToAdd.forEach(file => {
        console.log(`   - ${file.path}`);
      });
    }
    
    if (preview.conflictingFiles.length > 0) {
      console.log(`\n⚠️  Conflicting files (${preview.conflictingFiles.length}):`);
      preview.conflictingFiles.forEach(file => {
        console.log(`   - ${file.path} (has local modifications)`);
      });
    }
    
    if (preview.backupRequired.length > 0) {
      console.log(`\n💾 Files requiring backup (${preview.backupRequired.length}):`);
      preview.backupRequired.forEach(file => {
        console.log(`   - ${file.path}`);
      });
    }
  }

  async createBackup() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupDir = path.join(this.updateCacheDir, `backup-${timestamp}`);
    
    fs.mkdirSync(backupDir, { recursive: true });
    
    // Copy critical files to backup
    for (const criticalPath of this.criticalPaths) {
      const sourcePath = path.join(this.projectRoot, criticalPath);
      const backupPath = path.join(backupDir, criticalPath);
      
      if (fs.existsSync(sourcePath)) {
        fs.mkdirSync(path.dirname(backupPath), { recursive: true });
        
        if (fs.statSync(sourcePath).isDirectory()) {
          this.copyDirectoryRecursive(sourcePath, backupPath);
        } else {
          fs.copyFileSync(sourcePath, backupPath);
        }
      }
    }
    
    return backupDir;
  }

  async updateFile(fileAnalysis) {
    if (!fs.existsSync(fileAnalysis.tempPath)) {
      throw new Error(`Template file not found: ${fileAnalysis.tempPath}`);
    }
    
    fs.mkdirSync(path.dirname(fileAnalysis.projectPath), { recursive: true });
    fs.copyFileSync(fileAnalysis.tempPath, fileAnalysis.projectPath);
  }

  async addFile(fileAnalysis) {
    return this.updateFile(fileAnalysis);
  }

  async autoResolveConflict(fileAnalysis) {
    // Simple strategy: take template version but preserve critical local settings
    // In production, this would be more sophisticated
    console.log(`   🔧 Auto-resolving conflict in ${fileAnalysis.path}`);
    
    // For now, just update with template version
    await this.updateFile(fileAnalysis);
  }

  async updateTemplateVersion(newVersion) {
    const versionContent = `TEMPLATE_VERSION=${newVersion}
TEMPLATE_REPO=${this.templateRepo}
SYNC_DATE=${new Date().toISOString().split('T')[0]}
LAST_UPDATE=${new Date().toISOString()}

# Template Update Commands:
# /update-from-template --check     # Check for updates
# /update-from-template --preview   # Preview changes  
# /update-from-template             # Apply updates
# /update-from-template --force     # Force update with auto-resolve
`;
    
    fs.writeFileSync(this.templateVersionFile, versionContent);
  }

  async restoreFromBackup(backupDir) {
    if (!fs.existsSync(backupDir)) {
      throw new Error(`Backup directory not found: ${backupDir}`);
    }
    
    console.log('🔄 Restoring from backup...');
    
    for (const criticalPath of this.criticalPaths) {
      const backupPath = path.join(backupDir, criticalPath);
      const projectPath = path.join(this.projectRoot, criticalPath);
      
      if (fs.existsSync(backupPath)) {
        if (fs.statSync(backupPath).isDirectory()) {
          this.copyDirectoryRecursive(backupPath, projectPath);
        } else {
          fs.copyFileSync(backupPath, projectPath);
        }
      }
    }
    
    console.log('✅ Restored from backup');
  }

  copyDirectoryRecursive(source, target) {
    if (!fs.existsSync(target)) {
      fs.mkdirSync(target, { recursive: true });
    }
    
    const items = fs.readdirSync(source);
    for (const item of items) {
      const sourcePath = path.join(source, item);
      const targetPath = path.join(target, item);
      
      if (fs.statSync(sourcePath).isDirectory()) {
        this.copyDirectoryRecursive(sourcePath, targetPath);
      } else {
        fs.copyFileSync(sourcePath, targetPath);
      }
    }
  }

  cleanupTempDir(tempDir) {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';
  const projectRoot = process.cwd();
  
  const updateSystem = new TemplateUpdateSystem(projectRoot);
  
  async function runCommand() {
    try {
      switch (command) {
        case 'check':
        case '--check':
          await updateSystem.checkForUpdates({ details: true });
          break;
          
        case 'preview':
        case '--preview':
          await updateSystem.previewUpdates();
          break;
          
        case 'apply':
        case 'update':
          const autoResolve = args.includes('--force') || args.includes('--auto-resolve');
          const runSync = args.includes('--sync');
          await updateSystem.applyUpdates({ autoResolve, runSync });
          break;
          
        default:
          console.log('Template Update System');
          console.log('');
          console.log('Commands:');
          console.log('  check     - Check for template updates');
          console.log('  preview   - Preview what would be updated');
          console.log('  apply     - Apply template updates');
          console.log('');
          console.log('Options:');
          console.log('  --force   - Auto-resolve conflicts during apply');
          console.log('  --sync    - Run project sync after applying updates');
          break;
      }
    } catch (error) {
      console.error('❌ Command failed:', error.message);
      process.exit(1);
    }
  }
  
  runCommand();
}

module.exports = TemplateUpdateSystem;