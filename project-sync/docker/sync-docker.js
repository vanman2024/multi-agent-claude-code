#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { deepMerge, loadJSONFile } = require('../setup/sync-settings');

/**
 * Docker Settings Sync Script
 * Merges Docker template configurations with project-specific overrides
 */

// Load YAML content (simple approach for template merging)
const loadYAMLTemplate = (filePath) => {
  if (!fs.existsSync(filePath)) {
    console.log(`Template not found: ${filePath}`);
    return '';
  }
  return fs.readFileSync(filePath, 'utf8');
};

// Simple environment variable substitution
const substituteEnvVars = (content, vars) => {
  let result = content;
  for (const [key, value] of Object.entries(vars)) {
    const regex = new RegExp(`\\$\\{${key}[^}]*\\}`, 'g');
    result = result.replace(regex, value);
  }
  return result;
};

const syncDockerConfigs = () => {
  console.log('🐳 Syncing Docker configurations...');
  
  const projectRoot = path.resolve(__dirname, '../..');
  const templatesDir = path.join(__dirname, '.');
  const overridesDir = path.join(__dirname, '../local-overrides');
  
  // Load Docker overrides
  const dockerOverrides = loadJSONFile(path.join(overridesDir, 'docker-local.json'));
  console.log('📝 Loaded Docker overrides');
  
  // Default environment variables
  const defaultEnvVars = {
    PROJECT_NAME: path.basename(projectRoot),
    PYTHON_VERSION: '3.12',
    NODE_VERSION: '18',
    ...dockerOverrides.environment
  };
  
  // 1. Sync docker-compose.dev.yml
  const dockerComposeTemplate = loadYAMLTemplate(path.join(templatesDir, 'docker-dev.template.yml'));
  if (dockerComposeTemplate) {
    const dockerCompose = substituteEnvVars(dockerComposeTemplate, defaultEnvVars);
    const dockerComposePath = path.join(projectRoot, 'docker-compose.dev.yml');
    fs.writeFileSync(dockerComposePath, dockerCompose);
    console.log(`✅ Updated: ${dockerComposePath}`);
  }
  
  // 2. Sync Dockerfile.dev
  const dockerfileTemplate = path.join(templatesDir, 'Dockerfile.dev.template');
  if (fs.existsSync(dockerfileTemplate)) {
    const dockerfilePath = path.join(projectRoot, 'Dockerfile.dev');
    fs.copyFileSync(dockerfileTemplate, dockerfilePath);
    console.log(`✅ Updated: ${dockerfilePath}`);
  }
  
  // 3. Sync .devcontainer/devcontainer.json
  const devcontainerDir = path.join(projectRoot, '.devcontainer');
  if (!fs.existsSync(devcontainerDir)) {
    fs.mkdirSync(devcontainerDir, { recursive: true });
  }
  
  const devcontainerTemplate = loadJSONFile(path.join(templatesDir, 'devcontainer.json.template'));
  if (Object.keys(devcontainerTemplate).length > 0) {
    const devcontainerPath = path.join(devcontainerDir, 'devcontainer.json');
    fs.writeFileSync(devcontainerPath, JSON.stringify(devcontainerTemplate, null, 2));
    console.log(`✅ Updated: ${devcontainerPath}`);
  }
  
  // 4. Sync docker-scripts.sh
  const scriptsTemplate = path.join(templatesDir, 'docker-scripts.template.sh');
  if (fs.existsSync(scriptsTemplate)) {
    const scriptsPath = path.join(projectRoot, 'docker-scripts.sh');
    fs.copyFileSync(scriptsTemplate, scriptsPath);
    // Make executable
    fs.chmodSync(scriptsPath, '755');
    console.log(`✅ Updated: ${scriptsPath}`);
  }
  
  // 5. Create/update .env.docker.example
  const envDockerExample = `# Docker Development Environment Variables
# Copy this to .env.docker for local development

# Project Configuration
PROJECT_NAME=${defaultEnvVars.PROJECT_NAME}
PYTHON_VERSION=${defaultEnvVars.PYTHON_VERSION}
NODE_VERSION=${defaultEnvVars.NODE_VERSION}

# Development Ports
PYTHON_DEV_PORT=${dockerOverrides.services?.python_dev_port || 8000}
FRONTEND_DEV_PORT=${dockerOverrides.services?.frontend_dev_port || 3000}
POSTGRES_PORT=${dockerOverrides.services?.postgres_port || 5432}
REDIS_PORT=${dockerOverrides.services?.redis_port || 6379}

# Database Configuration (Development)
DB_NAME=devdb
DB_USER=devuser
DB_PASSWORD=devpass

# Python Configuration
PYTHONPATH=/workspace
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1
DEVELOPMENT=true

# Add your project-specific environment variables below:
# API_KEY=your-api-key
# DEBUG=true
`;
  
  const envDockerPath = path.join(projectRoot, '.env.docker.example');
  fs.writeFileSync(envDockerPath, envDockerExample);
  console.log(`✅ Updated: ${envDockerPath}`);
  
  // 6. Create .dockerignore if it doesn't exist
  const dockerignorePath = path.join(projectRoot, '.dockerignore');
  if (!fs.existsSync(dockerignorePath)) {
    const dockerignoreContent = `# Git
.git
.gitignore

# Development
.vscode
.idea
*.swp
*.swo

# Dependencies
node_modules
__pycache__
*.pyc
.pytest_cache
.mypy_cache

# Environment
.env
.env.local
.env.*.local
.env.docker

# Build outputs
dist
build
.next
out

# Logs
*.log
logs

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml
.dockerignore

# Settings sync local overrides
settings-sync/local-overrides
settings-sync/backups

# Temporary files
tmp
temp
*.tmp
*.temp
`;
    fs.writeFileSync(dockerignorePath, dockerignoreContent);
    console.log(`✅ Created: ${dockerignorePath}`);
  }
  
  console.log('\n🎉 Docker configuration sync complete!');
  console.log('\n💡 Next steps:');
  console.log('1. Copy .env.docker.example to .env.docker and customize');
  console.log('2. Run: ./docker-scripts.sh dev-up');
  console.log('3. Open in VS Code Dev Container for full IDE integration');
  console.log('4. Use ./docker-scripts.sh help for all available commands');
};

// CLI handling
if (require.main === module) {
  try {
    syncDockerConfigs();
  } catch (error) {
    console.error('❌ Error syncing Docker configs:', error.message);
    process.exit(1);
  }
}

module.exports = { syncDockerConfigs };