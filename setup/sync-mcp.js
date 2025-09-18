#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { loadJSONFile, deepMerge } = require('./sync-settings');

/**
 * Shared MCP Configuration Sync Script
 * Ensures all AI tools use the same MCP server configurations locally
 */

// Platform-specific Claude Code MCP config paths
const getClaudeMCPConfigPath = () => {
  const platform = os.platform();
  const homeDir = os.homedir();
  
  switch (platform) {
    case 'win32':
      return path.join(homeDir, 'AppData', 'Roaming', 'Claude', 'claude_desktop_config.json');
    case 'darwin':
      return path.join(homeDir, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
    case 'linux':
      return path.join(homeDir, '.config', 'claude', 'claude_desktop_config.json');
    default:
      throw new Error(`Unsupported platform: ${platform}`);
  }
};

const syncMCPConfigurations = () => {
  console.log('🔗 Syncing shared MCP configurations...');
  
  const projectRoot = path.resolve(__dirname, '../..');
  const templatesDir = path.join(__dirname, '../templates');
  const overridesDir = path.join(__dirname, '../local-overrides');
  
  // Load shared MCP configuration template
  const sharedMCPTemplate = loadJSONFile(path.join(templatesDir, 'shared-mcp.template.json'));
  if (Object.keys(sharedMCPTemplate).length === 0) {
    console.log('❌ No shared MCP template found');
    return;
  }
  
  // Load local MCP overrides
  const mcpOverrides = loadJSONFile(path.join(overridesDir, 'mcp-local.json'));
  if (Object.keys(mcpOverrides).length > 0) {
    console.log(`🔧 Loaded local MCP overrides`);
  }
  
  // Merge configurations
  const mergedMCPConfig = deepMerge(sharedMCPTemplate, mcpOverrides);
  
  // 1. Update Claude Code configuration
  const claudeConfigPath = getClaudeMCPConfigPath();
  const claudeConfigDir = path.dirname(claudeConfigPath);
  
  // Ensure Claude config directory exists
  if (!fs.existsSync(claudeConfigDir)) {
    fs.mkdirSync(claudeConfigDir, { recursive: true });
    console.log(`📁 Created Claude config directory: ${claudeConfigDir}`);
  }
  
  // Read existing Claude config or create new one
  let existingClaudeConfig = {};
  if (fs.existsSync(claudeConfigPath)) {
    try {
      existingClaudeConfig = JSON.parse(fs.readFileSync(claudeConfigPath, 'utf8'));
    } catch (error) {
      console.log('⚠️  Could not parse existing Claude config, creating new one');
    }
  }
  
  // Update Claude config with shared MCP servers
  const claudeConfig = {
    ...existingClaudeConfig,
    mcpServers: {
      ...existingClaudeConfig.mcpServers,
      ...mergedMCPConfig.mcpServers
    }
  };
  
  fs.writeFileSync(claudeConfigPath, JSON.stringify(claudeConfig, null, 2));
  console.log(`✅ Updated Claude Code MCP config: ${claudeConfigPath}`);
  
  // 2. Create project-specific MCP configurations in target project
  // Note: MCP templates are now stored in settings-sync/templates/
  const projectMCPDir = path.join(projectRoot, '.mcp');
  if (!fs.existsSync(projectMCPDir)) {
    fs.mkdirSync(projectMCPDir, { recursive: true });
  }
  
  // Generate agent-specific configs
  for (const [agentName, agentConfig] of Object.entries(mergedMCPConfig.agentConfigs || {})) {
    const agentMCPConfig = {
      mcpServers: {},
      metadata: {
        agent: agentName,
        focus: agentConfig.focus,
        enabledServers: agentConfig.enabledServers
      }
    };
    
    // Add only enabled servers for this agent
    for (const serverName of agentConfig.enabledServers) {
      if (mergedMCPConfig.mcpServers[serverName]) {
        agentMCPConfig.mcpServers[serverName] = mergedMCPConfig.mcpServers[serverName];
      }
    }
    
    const agentConfigPath = path.join(projectMCPDir, `${agentName.replace('@', '')}-mcp.json`);
    fs.writeFileSync(agentConfigPath, JSON.stringify(agentMCPConfig, null, 2));
    console.log(`✅ Created ${agentName} MCP config: ${agentConfigPath}`);
  }
  
  // 3. Create shared environment file
  const envVars = {
    ...mergedMCPConfig.sharedEnv,
    MCP_CONFIG_DIR: projectMCPDir,
    SHARED_MCP_CONFIG: path.join(projectMCPDir, 'shared-mcp.json')
  };
  
  const envFile = Object.entries(envVars)
    .map(([key, value]) => `export ${key}="${value}"`)
    .join('\n') + '\n';
    
  const envFilePath = path.join(projectMCPDir, 'mcp-env.sh');
  fs.writeFileSync(envFilePath, envFile);
  fs.chmodSync(envFilePath, '755');
  console.log(`✅ Created MCP environment file: ${envFilePath}`);
  
  // 4. Create shared MCP configuration file
  const sharedMCPPath = path.join(projectMCPDir, 'shared-mcp.json');
  fs.writeFileSync(sharedMCPPath, JSON.stringify(mergedMCPConfig, null, 2));
  console.log(`✅ Created shared MCP config: ${sharedMCPPath}`);
  
  // 5. Create agent setup script
  const setupScript = `#!/bin/bash
# AI Agent MCP Setup Script
# Ensures all AI tools use shared MCP configurations

set -e

# Source MCP environment
source .mcp/mcp-env.sh

echo "🤖 Setting up AI agent MCP configurations..."

# Claude Code - Already configured via claude_desktop_config.json
echo "✅ Claude Code: Using shared MCP servers"

# Ollama agents setup
if command -v ollama > /dev/null 2>&1; then
    echo "🦙 Setting up Ollama agents..."
    
    # Pull required models if not present
    ollama list | grep -q qwen2.5:7b || ollama pull qwen2.5:7b
    
    echo "✅ Ollama: @qwen model ready"
else
    echo "⚠️  Ollama not installed - run: curl -fsSL https://ollama.ai/install.sh | sh"
fi

# Gemini CLI setup
if command -v gemini > /dev/null 2>&1; then
    echo "✅ Gemini CLI: Ready for @gemini tasks"
else
    echo "⚠️  Gemini CLI not found - install via npm: npm install -g @google-ai/generativelanguage"
fi

# Codex CLI setup  
if command -v codex > /dev/null 2>&1; then
    echo "✅ Codex CLI: Ready for @codex tasks"
else
    echo "⚠️  Codex CLI not found - install via: pip install openai-cli"
fi

# GitHub Copilot - works via VS Code extension
echo "✅ GitHub Copilot: Configure via VS Code extension"

echo ""
echo "🎯 @Symbol Coordination System Ready!"
echo ""
echo "Usage Examples:"
echo "  Claude Code:  Use subagents directly"
echo "  Ollama:       ollama run qwen2.5:7b 'optimize this code'"
echo "  Gemini:       gemini -p 'research best practices'"
echo "  Codex:        codex exec 'implement unit tests'"
echo ""
echo "Task Format:  - [ ] T001 @agent Description"
echo "Complete:     - [x] T001 @agent Description ✅"
`;

  const setupScriptPath = path.join(projectRoot, 'sync-project-template.sh');
  fs.writeFileSync(setupScriptPath, setupScript);
  fs.chmodSync(setupScriptPath, '755');
  console.log(`✅ Created agent setup script: ${setupScriptPath}`);
  
  console.log('\n🎉 Shared MCP configuration sync complete!');
  console.log('\n💡 Next steps:');
  console.log('1. Run: ./sync-project-template.sh');
  console.log('2. Restart Claude Code to pick up new MCP servers');
  console.log('3. Test @symbol coordination in tasks.md files');
  console.log('4. All agents now share the same MCP tool access!');
};

// CLI handling
if (require.main === module) {
  try {
    syncMCPConfigurations();
  } catch (error) {
    console.error('❌ Error syncing MCP configs:', error.message);
    process.exit(1);
  }
}

module.exports = { syncMCPConfigurations };