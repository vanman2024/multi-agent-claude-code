# Multi-Agent Claude Code

A collaborative multi-agent system for automated GitHub issue management and code development.

## 🚀 New: Real-time Notification System

A comprehensive notification system has been implemented with real-time WebSocket updates, user preferences, and complete UI.

### Features
- ✅ Real-time notifications via WebSocket
- ✅ In-app notification center with full UI  
- ✅ User preference management
- ✅ Notification history with read/unread status
- ✅ REST API for all operations
- ✅ Toast notifications for immediate alerts
- ✅ Mobile-responsive design
- ✅ Integration with existing agent workflows

### Quick Start
```bash
# Start the notification system
cd app/
npm install
npm start
# Visit http://localhost:3000

# Or run the integration demo
node notification-integration.js demo
```

## Architecture

This repository implements a multi-agent system where different AI agents collaborate to handle GitHub issues:

- **Agent Dispatcher** (`scripts/agent-dispatcher.js`) - Routes issues to appropriate agents
- **GitHub Copilot** - Handles simple tasks and documentation updates  
- **Claude Code** - Manages complex features and refactoring
- **Human Developers** - Handle architecture decisions and reviews
- **Notification System** - Real-time updates and user communication

## Components

### Scripts
- `scripts/agent-dispatcher.js` - Issue routing and agent assignment
- `scripts/utility/` - Helper scripts and utilities

### Tests  
- `tests/workflow-validation.js` - GitHub Actions workflow testing
- `app/tests/notification-tests.js` - Notification system tests

### Templates
- `templates/guides/` - Feature specification templates
- `templates/local_dev/` - Development issue templates

### Documentation
- `MCP_SERVERS_GUIDE.md` - Model Context Protocol server setup
- `CLAUDE.md` - AI assistant instructions and guidelines  
- `IDEAS.md` - Architecture decisions and improvement ideas

### Notification System (`app/`)
- `server.js` - WebSocket server with SQLite database
- `public/` - Frontend notification center
- `tests/` - Comprehensive test suite
- Complete API for notification management

## Integration

The notification system integrates seamlessly with existing workflows:

```javascript
// Agent notifications
await notifyAgentStart(issueNumber, 'Claude Code');
await notifyAgentComplete(issueNumber, 'Claude Code', success);

// GitHub webhook integration  
await notifyIssueCreated(issue);
await notifyPRMerged(pullRequest);

// System monitoring
await notifyTestResults(passed, total, context);
await notifySystemError(error, context);
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/vanman2024/multi-agent-claude-code.git
   cd multi-agent-claude-code
   ```

2. **Start the notification system**
   ```bash
   cd app/
   npm install
   npm start
   ```

3. **Run the integration demo**
   ```bash
   node notification-integration.js demo
   ```

4. **Access the notification center**
   Visit http://localhost:3000 to see real-time notifications

## Testing

```bash
# Test the notification system
cd app/
npm test

# Test workflow validation
node tests/workflow-validation.js

# Run integration demo
node notification-integration.js demo
```

## Architecture Principles

This system follows the "House Metaphor" from `CLAUDE.md`:

- **Foundation** (Database) - Solid, unchanging data structures
- **Plumbing** (GitHub Actions) - Automated workflows without intelligence  
- **Electrical** (Agent System) - Smart decision-making and task routing
- **UI** (Notification Center) - User-facing interfaces and interactions

The notification system acts as the communication layer between all components, providing real-time updates and user feedback throughout the development process.

## Contributing

See `CLAUDE.md` for development guidelines and `CONTRIBUTING.md` for contribution workflow.