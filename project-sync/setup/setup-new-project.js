#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { syncSettings } = require('./sync-settings');

/**
 * Setup New Project Script  
 * First-time setup for syncing settings in a new coding project
 */

const setupNewProject = () => {
  console.log('🚀 Setting up development settings for new project...');
  
  const overridesDir = path.join(__dirname, '../local-overrides');
  const backupsDir = path.join(__dirname, '../backups');
  
  // Create directories
  if (!fs.existsSync(overridesDir)) {
    fs.mkdirSync(overridesDir, { recursive: true });
    console.log(`📁 Created local-overrides directory: ${overridesDir}`);
  }
  
  if (!fs.existsSync(backupsDir)) {
    fs.mkdirSync(backupsDir, { recursive: true });
    console.log(`📁 Created backups directory: ${backupsDir}`);
  }
  
  // Create example project-specific override files
  const exampleVSCodeOverrides = {
    "// NOTE": "This file contains project-specific VS Code overrides",
    "// Project-specific overrides": "",
    
    "// Python project settings": "",
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    
    "// Project-specific paths": "",
    "// \"files.exclude\": { \"**/build\": true },",
    
    "// Project preferences": "",
    "// \"editor.fontSize\": 14,",
    "// \"workbench.colorTheme\": \"Default Dark+\",",
    
    "// Project-specific spell checker words": "",
    "cSpell.words": [
      "// Add project-specific terms here"
    ]
  };
  
  const vscodeLocalPath = path.join(overridesDir, 'vscode-local.json');
  if (!fs.existsSync(vscodeLocalPath)) {
    fs.writeFileSync(vscodeLocalPath, JSON.stringify(exampleVSCodeOverrides, null, 2));
    console.log(`📝 Created example VS Code overrides: ${vscodeLocalPath}`);
  }
  
  // Create example Claude config overrides  
  const exampleClaudeOverrides = {
    "// NOTE": "This file contains project-specific Claude/MCP configurations",
    "// Project-specific configurations": "",
    
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["@modelcontextprotocol/server-filesystem", "."],
        "env": {}
      }
    },
    
    "// Project-specific settings": "",
    "logLevel": "info",
    "timeout": 30000
  };

  // Create example Docker config overrides
  const exampleDockerOverrides = {
    "// NOTE": "This file contains project-specific Docker configurations",
    "// Project-specific Docker settings": "",
    
    "environment": {
      "PROJECT_NAME": path.basename(path.resolve(__dirname, '../..')),
      "PYTHON_VERSION": "3.12",
      "NODE_VERSION": "18"
    },
    
    "services": {
      "// Custom ports for this project": "",
      "python_dev_port": 8000,
      "frontend_dev_port": 3000,
      "postgres_port": 5432,
      "redis_port": 6379
    },
    
    "volumes": {
      "// Project-specific volume mounts": "",
      "additional_mounts": []
    }
  };
  
  const claudeLocalPath = path.join(overridesDir, 'claude-local.json');
  if (!fs.existsSync(claudeLocalPath)) {
    fs.writeFileSync(claudeLocalPath, JSON.stringify(exampleClaudeOverrides, null, 2));
    console.log(`📝 Created example Claude overrides: ${claudeLocalPath}`);
  }

  const dockerLocalPath = path.join(overridesDir, 'docker-local.json');
  if (!fs.existsSync(dockerLocalPath)) {
    fs.writeFileSync(dockerLocalPath, JSON.stringify(exampleDockerOverrides, null, 2));
    console.log(`🐳 Created example Docker overrides: ${dockerLocalPath}`);
  }
  
  // Create project config file
  const projectConfig = {
    "// NOTE": "Project-specific configuration like paths, build settings, etc.",
    
    "project": {
      "name": path.basename(path.resolve(__dirname, '../..')),
      "type": "multi-agent-framework", 
      "setupDate": new Date().toISOString()
    },
    
    "paths": {
      "projectRoot": ".",
      "pythonVenv": "./venv/bin/python",
      "nodeModules": "./node_modules",
      "buildDir": "./dist"
    },
    
    "preferences": {
      "autoSyncOnPull": true,
      "createBackups": true,
      "verboseLogging": false
    }
  };
  
  const projectConfigPath = path.join(overridesDir, 'project-config.json');
  if (!fs.existsSync(projectConfigPath)) {
    fs.writeFileSync(projectConfigPath, JSON.stringify(projectConfig, null, 2));
    console.log(`⚙️  Created project config: ${projectConfigPath}`);
  }
  
  // Create .gitignore for local-overrides if it doesn't exist
  const gitignorePath = path.join(overridesDir, '.gitignore');
  if (!fs.existsSync(gitignorePath)) {
    const gitignoreContent = `# Local machine-specific overrides - never commit these
*
!.gitignore
!README.md
`;
    fs.writeFileSync(gitignorePath, gitignoreContent);
    console.log(`🔒 Created .gitignore for local overrides`);
  }
  
  // Create README for local-overrides
  const readmePath = path.join(overridesDir, 'README.md');
  if (!fs.existsSync(readmePath)) {
    const readmeContent = `# Local Overrides

This directory contains machine-specific configuration overrides that are never committed to git.

## Files

- **vscode-local.json** - VS Code setting overrides for this machine
- **claude-local.json** - Claude/MCP configuration overrides  
- **machine-config.json** - Machine-specific paths and preferences

## Usage

1. Edit the JSON files to customize settings for this machine
2. Run \`npm run sync-settings\` to apply changes
3. These files override the template settings when syncing

## Examples

### VS Code Font Size Override
\`\`\`json
{
  "editor.fontSize": 16,
  "editor.fontFamily": "JetBrains Mono"
}
\`\`\`

### Python Path Override
\`\`\`json
{
  "python.defaultInterpreterPath": "/usr/local/bin/python3"
}
\`\`\`

### Custom Spell Checker Words
\`\`\`json
{
  "cSpell.words": ["mycompany", "projectname", "customterm"]
}
\`\`\`
`;
    fs.writeFileSync(readmePath, readmeContent);
    console.log(`📖 Created README for local overrides`);
  }
  
  console.log('\n✅ Project setup complete! Next steps:');
  console.log('1. Edit files in local-overrides/ to customize for this project');
  console.log('2. Run "npm run sync-settings" to apply settings to .vscode/');
  console.log('3. Restart VS Code to ensure all settings take effect');
  console.log('\n🔄 Running initial sync...');
  
  // Run initial sync
  try {
    syncSettings();
  } catch (error) {
    console.error('❌ Error during initial sync:', error.message);
    console.log('You can run "npm run sync-settings" manually later');
  }
};

// CLI handling
if (require.main === module) {
  try {
    setupNewProject();
  } catch (error) {
    console.error('❌ Error setting up new project:', error.message);
    process.exit(1);
  }
}

module.exports = { setupNewProject };