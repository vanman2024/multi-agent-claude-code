#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

/**
 * Reset Settings Script
 * Restores settings from backup
 */

// Platform-specific VS Code settings paths
const getVSCodeSettingsPath = () => {
  const platform = os.platform();
  const homeDir = os.homedir();
  
  switch (platform) {
    case 'win32':
      return path.join(homeDir, 'AppData', 'Roaming', 'Code', 'User', 'settings.json');
    case 'darwin':
      return path.join(homeDir, 'Library', 'Application Support', 'Code', 'User', 'settings.json');
    case 'linux':
      return path.join(homeDir, '.config', 'Code', 'User', 'settings.json');
    default:
      throw new Error(`Unsupported platform: ${platform}`);
  }
};

const promptUser = (question) => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
};

const resetSettings = async () => {
  console.log('🔄 Reset Settings from Backup');
  
  const backupDir = path.join(__dirname, '../backups');
  
  if (!fs.existsSync(backupDir)) {
    console.log('❌ No backup directory found. Run "npm run backup-settings" first.');
    return;
  }
  
  // List available backups
  const backupFiles = fs.readdirSync(backupDir)
    .filter(file => file.endsWith('.json'))
    .sort()
    .reverse(); // Most recent first
    
  if (backupFiles.length === 0) {
    console.log('❌ No backup files found. Run "npm run backup-settings" first.');
    return;
  }
  
  console.log('\n📋 Available backups:');
  backupFiles.forEach((file, index) => {
    const filePath = path.join(backupDir, file);
    const stats = fs.statSync(filePath);
    const date = stats.mtime.toLocaleDateString();
    const time = stats.mtime.toLocaleTimeString();
    console.log(`  ${index + 1}. ${file} (${date} ${time})`);
  });
  
  // Get user selection
  const selection = await promptUser(`\nSelect backup to restore (1-${backupFiles.length}, or 'q' to quit): `);
  
  if (selection.toLowerCase() === 'q') {
    console.log('Operation cancelled.');
    return;
  }
  
  const index = parseInt(selection) - 1;
  if (isNaN(index) || index < 0 || index >= backupFiles.length) {
    console.log('❌ Invalid selection.');
    return;
  }
  
  const selectedBackup = backupFiles[index];
  const backupPath = path.join(backupDir, selectedBackup);
  
  // Confirm restoration
  const confirm = await promptUser(`\n⚠️  This will overwrite your current settings with: ${selectedBackup}\nContinue? (y/N): `);
  
  if (confirm.toLowerCase() !== 'y' && confirm.toLowerCase() !== 'yes') {
    console.log('Operation cancelled.');
    return;
  }
  
  // Create backup of current settings before restoring
  const { backupSettings } = require('./backup-settings');
  console.log('\n💾 Creating backup of current settings before restore...');
  backupSettings();
  
  // Restore settings
  const vsCodeSettingsPath = getVSCodeSettingsPath();
  
  try {
    // Ensure VS Code settings directory exists
    const vsCodeDir = path.dirname(vsCodeSettingsPath);
    if (!fs.existsSync(vsCodeDir)) {
      fs.mkdirSync(vsCodeDir, { recursive: true });
    }
    
    fs.copyFileSync(backupPath, vsCodeSettingsPath);
    console.log(`\n✅ Restored settings from: ${selectedBackup}`);
    console.log(`📍 Applied to: ${vsCodeSettingsPath}`);
    
    // Also restore to project if it's a project backup
    if (selectedBackup.includes('project-vscode')) {
      const projectRoot = path.resolve(__dirname, '../..');
      const projectSettingsPath = path.join(projectRoot, '.vscode', 'settings.json');
      const projectDir = path.dirname(projectSettingsPath);
      
      if (!fs.existsSync(projectDir)) {
        fs.mkdirSync(projectDir, { recursive: true });
      }
      
      fs.copyFileSync(backupPath, projectSettingsPath);
      console.log(`📍 Also applied to project: ${projectSettingsPath}`);
    }
    
    console.log('\n🎉 Settings restored successfully!');
    console.log('💡 Restart VS Code to ensure all settings take effect.');
    
  } catch (error) {
    console.error('❌ Error restoring settings:', error.message);
  }
};

// CLI handling
if (require.main === module) {
  resetSettings().catch(error => {
    console.error('❌ Error:', error.message);
    process.exit(1);
  });
}

module.exports = { resetSettings };