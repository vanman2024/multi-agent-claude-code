#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Backup Settings Script
 * Creates backups of current VS Code and other settings
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

const backupSettings = () => {
  console.log('💾 Creating settings backup...');
  
  const backupDir = path.join(__dirname, '../backups');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  
  // Ensure backup directory exists
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }
  
  // Backup VS Code settings
  const vsCodeSettingsPath = getVSCodeSettingsPath();
  if (fs.existsSync(vsCodeSettingsPath)) {
    const backupPath = path.join(backupDir, `vscode-settings-${timestamp}.json`);
    fs.copyFileSync(vsCodeSettingsPath, backupPath);
    console.log(`✅ Backed up VS Code settings: ${backupPath}`);
  } else {
    console.log('⚠️  VS Code settings file not found, skipping backup');
  }
  
  // Backup project .vscode/settings.json if it exists
  const projectRoot = path.resolve(__dirname, '../..');
  const projectSettingsPath = path.join(projectRoot, '.vscode', 'settings.json');
  if (fs.existsSync(projectSettingsPath)) {
    const backupPath = path.join(backupDir, `project-vscode-settings-${timestamp}.json`);
    fs.copyFileSync(projectSettingsPath, backupPath);
    console.log(`✅ Backed up project VS Code settings: ${backupPath}`);
  }
  
  // List all backups
  console.log('\n📋 Available backups:');
  const backupFiles = fs.readdirSync(backupDir)
    .filter(file => file.endsWith('.json'))
    .sort()
    .reverse(); // Most recent first
    
  backupFiles.slice(0, 10).forEach((file, index) => {
    const filePath = path.join(backupDir, file);
    const stats = fs.statSync(filePath);
    const date = stats.mtime.toLocaleDateString();
    const time = stats.mtime.toLocaleTimeString();
    console.log(`  ${index + 1}. ${file} (${date} ${time})`);
  });
  
  if (backupFiles.length > 10) {
    console.log(`  ... and ${backupFiles.length - 10} more`);
  }
  
  console.log('\n💡 Tip: Use "npm run reset-settings" to restore from backup');
};

// CLI handling
if (require.main === module) {
  try {
    backupSettings();
  } catch (error) {
    console.error('❌ Error creating backup:', error.message);
    process.exit(1);
  }
}

module.exports = { backupSettings };