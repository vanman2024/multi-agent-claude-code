#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Settings Sync Script
 * Merges template settings with local overrides and applies to VS Code
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

// Deep merge function for objects
const deepMerge = (target, source) => {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
};

// Clean JSON (remove comments)
const cleanJSON = (jsonString) => {
  return jsonString
    .replace(/\/\/.*$/gm, '') // Remove single-line comments
    .replace(/\/\*[\s\S]*?\*\//g, '') // Remove multi-line comments
    .replace(/,(\s*[}\]])/g, '$1'); // Remove trailing commas
};

// Load and parse JSON file with comments
const loadJSONFile = (filePath) => {
  if (!fs.existsSync(filePath)) {
    console.log(`File not found: ${filePath}`);
    return {};
  }
  
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const cleanContent = cleanJSON(content);
    return JSON.parse(cleanContent);
  } catch (error) {
    console.error(`Error parsing ${filePath}:`, error.message);
    return {};
  }
};

// Main sync function
const syncSettings = () => {
  console.log('🔄 Syncing settings...');
  
  const projectRoot = path.resolve(__dirname, '../..');
  const templatesDir = path.join(__dirname, '../templates');
  const overridesDir = path.join(__dirname, '../local-overrides');
  
  // Load template settings
  const templatePath = path.join(templatesDir, 'vscode-settings.template.json');
  const templateSettings = loadJSONFile(templatePath);
  console.log(`📝 Loaded template: ${templatePath}`);
  
  // Load local overrides
  const overridePath = path.join(overridesDir, 'vscode-local.json');
  const localOverrides = loadJSONFile(overridePath);
  if (Object.keys(localOverrides).length > 0) {
    console.log(`🔧 Loaded local overrides: ${overridePath}`);
  }
  
  // Merge settings
  const mergedSettings = deepMerge(templateSettings, localOverrides);
  
  // Create backup of current settings
  const vsCodeSettingsPath = getVSCodeSettingsPath();
  const backupDir = path.join(__dirname, '../backups');
  
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }
  
  if (fs.existsSync(vsCodeSettingsPath)) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(backupDir, `settings-backup-${timestamp}.json`);
    fs.copyFileSync(vsCodeSettingsPath, backupPath);
    console.log(`💾 Backed up current settings to: ${backupPath}`);
  }
  
  // Ensure VS Code settings directory exists
  const vsCodeDir = path.dirname(vsCodeSettingsPath);
  if (!fs.existsSync(vsCodeDir)) {
    fs.mkdirSync(vsCodeDir, { recursive: true });
  }
  
  // Write merged settings
  fs.writeFileSync(vsCodeSettingsPath, JSON.stringify(mergedSettings, null, 2));
  console.log(`✅ Applied settings to: ${vsCodeSettingsPath}`);
  
  // Also update project .vscode/settings.json if it exists
  const projectSettingsPath = path.join(projectRoot, '.vscode', 'settings.json');
  if (fs.existsSync(path.dirname(projectSettingsPath))) {
    fs.writeFileSync(projectSettingsPath, JSON.stringify(mergedSettings, null, 2));
    console.log(`✅ Updated project settings: ${projectSettingsPath}`);
  }
  
  console.log('🎉 Settings sync complete!');
  console.log('\n💡 Tips:');
  console.log('- Restart VS Code to ensure all settings take effect');
  console.log('- Edit local-overrides/vscode-local.json for machine-specific customizations');
  console.log('- Run "npm run backup-settings" before major changes');
};

// CLI handling
if (require.main === module) {
  try {
    syncSettings();
  } catch (error) {
    console.error('❌ Error syncing settings:', error.message);
    process.exit(1);
  }
}

module.exports = { syncSettings, deepMerge, loadJSONFile };