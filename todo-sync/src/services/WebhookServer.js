import express from 'express';
import crypto from 'crypto';
import { WebSocketServer } from 'ws';
import { logger } from '../utils/logger.js';
import { EventEmitter } from 'events';

export class WebhookServer extends EventEmitter {
    constructor(syncService) {
        super();
        this.syncService = syncService;
        this.app = express();
        this.server = null;
        this.wss = null;
        this.port = parseInt(process.env.WEBHOOK_PORT) || 3001;
        this.webhookSecret = process.env.WEBHOOK_SECRET;
        this.connections = new Set();
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupWebSocket();
        this.setupEventHandlers();
    }

    setupMiddleware() {
        // Parse JSON bodies
        this.app.use('/webhook', express.raw({ type: 'application/json' }));
        this.app.use(express.json());
        
        // CORS for development
        this.app.use((req, res, next) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
            res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
            if (req.method === 'OPTIONS') {
                res.sendStatus(200);
            } else {
                next();
            }
        });

        // Health check middleware
        this.app.use((req, res, next) => {
            req.startTime = Date.now();
            next();
        });

        // Request logging
        this.app.use((req, res, next) => {
            logger.debug(`${req.method} ${req.path}`, {
                headers: req.headers,
                query: req.query,
                ip: req.ip
            });
            next();
        });
    }

    setupRoutes() {
        // GitHub webhook endpoint
        this.app.post('/webhook/github', this.handleGitHubWebhook.bind(this));
        
        // Health check
        this.app.get('/health', this.handleHealthCheck.bind(this));
        
        // Sync status endpoint
        this.app.get('/status', this.handleStatusCheck.bind(this));
        
        // Manual sync triggers
        this.app.post('/sync/full', this.handleFullSync.bind(this));
        this.app.post('/sync/incremental', this.handleIncrementalSync.bind(this));
        
        // Conflict management
        this.app.get('/conflicts', this.handleGetConflicts.bind(this));
        this.app.post('/conflicts/:id/resolve', this.handleResolveConflict.bind(this));
        
        // Statistics and monitoring
        this.app.get('/stats', this.handleGetStats.bind(this));
        
        // Todo management endpoints
        this.app.get('/todos', this.handleGetTodos.bind(this));
        this.app.get('/todos/:id', this.handleGetTodo.bind(this));
        this.app.put('/todos/:id', this.handleUpdateTodo.bind(this));
        this.app.delete('/todos/:id', this.handleDeleteTodo.bind(this));
        
        // Error handler
        this.app.use(this.errorHandler.bind(this));
    }

    setupWebSocket() {
        // WebSocket server will be attached when HTTP server starts
        this.wsHandlers = {
            'subscribe': this.handleWebSocketSubscribe.bind(this),
            'unsubscribe': this.handleWebSocketUnsubscribe.bind(this),
            'ping': this.handleWebSocketPing.bind(this),
            'manualSync': this.handleWebSocketManualSync.bind(this)
        };
    }

    setupEventHandlers() {
        // Listen to sync service events
        this.syncService.on('syncComplete', (data) => {
            this.broadcastToClients('syncComplete', data);
            logger.info('Broadcasted sync completion to WebSocket clients');
        });

        this.syncService.on('syncError', (data) => {
            this.broadcastToClients('syncError', data);
            logger.warn('Broadcasted sync error to WebSocket clients');
        });

        this.syncService.on('conflictDetected', (data) => {
            this.broadcastToClients('conflictDetected', data);
            logger.info('Broadcasted conflict detection to WebSocket clients');
        });
    }

    async start() {
        return new Promise((resolve, reject) => {
            try {
                this.server = this.app.listen(this.port, () => {
                    // Setup WebSocket server
                    this.wss = new WebSocketServer({ 
                        server: this.server,
                        path: '/ws'
                    });
                    
                    this.wss.on('connection', this.handleWebSocketConnection.bind(this));
                    
                    logger.info(`Webhook server started on port ${this.port}`);
                    resolve();
                });

                this.server.on('error', (error) => {
                    logger.error('Server error:', error);
                    reject(error);
                });

            } catch (error) {
                logger.error('Failed to start webhook server:', error);
                reject(error);
            }
        });
    }

    async stop() {
        return new Promise((resolve) => {
            // Close all WebSocket connections
            this.connections.forEach(ws => {
                if (ws.readyState === ws.OPEN) {
                    ws.close(1000, 'Server shutting down');
                }
            });
            this.connections.clear();

            // Close WebSocket server
            if (this.wss) {
                this.wss.close(() => {
                    logger.info('WebSocket server closed');
                });
            }

            // Close HTTP server
            if (this.server) {
                this.server.close(() => {
                    logger.info('HTTP server closed');
                    resolve();
                });
            } else {
                resolve();
            }
        });
    }

    // GitHub Webhook Handler
    async handleGitHubWebhook(req, res) {
        try {
            const signature = req.headers['x-hub-signature-256'];
            const event = req.headers['x-github-event'];
            const delivery = req.headers['x-github-delivery'];
            
            // Verify webhook signature
            if (this.webhookSecret && !this.verifyGitHubSignature(req.body, signature)) {
                logger.warn('Invalid GitHub webhook signature');
                return res.status(401).json({ error: 'Invalid signature' });
            }

            logger.info(`Received GitHub webhook: ${event}`, { delivery });

            const payload = JSON.parse(req.body.toString());
            
            // Handle different GitHub events
            switch (event) {
                case 'issues':
                    await this.handleIssuesEvent(payload);
                    break;
                    
                case 'issue_comment':
                    await this.handleIssueCommentEvent(payload);
                    break;
                    
                case 'ping':
                    logger.info('GitHub webhook ping received');
                    break;
                    
                default:
                    logger.debug(`Unhandled GitHub event: ${event}`);
            }

            res.status(200).json({ 
                status: 'success', 
                event: event,
                processed: true 
            });

        } catch (error) {
            logger.error('Error handling GitHub webhook:', error);
            res.status(500).json({ 
                error: 'Internal server error',
                message: error.message 
            });
        }
    }

    async handleIssuesEvent(payload) {
        const { action, issue } = payload;
        
        // Only process issues with 'todo-sync' label
        if (!issue.labels.some(label => label.name === 'todo-sync')) {
            return;
        }

        logger.info(`Processing GitHub issue event: ${action} for #${issue.number}`);

        switch (action) {
            case 'opened':
            case 'edited':
            case 'closed':
            case 'reopened':
                // Trigger sync for this specific issue
                await this.syncService.syncGitHubIssueToLocal(issue.number, issue);
                
                // Broadcast update to connected clients
                this.broadcastToClients('issueUpdated', {
                    action: action,
                    issueNumber: issue.number,
                    timestamp: new Date().toISOString()
                });
                break;
                
            case 'deleted':
                // Handle issue deletion
                const todo = await this.syncService.db.getTodoByGithubIssue(issue.number);
                if (todo) {
                    await this.syncService.db.updateTodo(todo.id, {
                        githubIssueNumber: null,
                        githubIssueId: null,
                        githubState: null,
                        needsGithubSync: false
                    });
                }
                break;
        }
    }

    async handleIssueCommentEvent(payload) {
        const { action, issue, comment } = payload;
        
        if (!issue.labels.some(label => label.name === 'todo-sync')) {
            return;
        }

        logger.info(`Processing GitHub issue comment event: ${action} for #${issue.number}`);
        
        // For now, just log comment events - could be extended to sync comments
        this.broadcastToClients('issueCommented', {
            action: action,
            issueNumber: issue.number,
            commentId: comment.id,
            timestamp: new Date().toISOString()
        });
    }

    verifyGitHubSignature(payload, signature) {
        if (!signature) return false;
        
        const expectedSignature = 'sha256=' + crypto
            .createHmac('sha256', this.webhookSecret)
            .update(payload)
            .digest('hex');
            
        return crypto.timingSafeEqual(
            Buffer.from(signature),
            Buffer.from(expectedSignature)
        );
    }

    // REST API Handlers
    async handleHealthCheck(req, res) {
        const health = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
            memory: process.memoryUsage(),
            sync: {
                isRunning: this.syncService.isRunning,
                isSyncing: this.syncService.isSyncing,
                lastSyncTime: this.syncService.syncStats.lastSyncTime
            },
            connections: this.connections.size
        };
        
        res.json(health);
    }

    async handleStatusCheck(req, res) {
        try {
            const stats = this.syncService.getStats();
            const dbStats = await this.syncService.getDetailedStats(24);
            
            res.json({
                sync: stats,
                database: dbStats,
                server: {
                    port: this.port,
                    connections: this.connections.size,
                    uptime: process.uptime()
                }
            });
        } catch (error) {
            logger.error('Error getting status:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleFullSync(req, res) {
        try {
            logger.info('Manual full sync triggered via API');
            
            // Run sync in background
            this.syncService.performFullSync()
                .then(() => {
                    this.broadcastToClients('manualSyncComplete', { type: 'full' });
                })
                .catch(error => {
                    logger.error('Manual full sync failed:', error);
                    this.broadcastToClients('manualSyncError', { 
                        type: 'full', 
                        error: error.message 
                    });
                });
            
            res.json({ 
                status: 'started',
                type: 'full',
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            logger.error('Error starting full sync:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleIncrementalSync(req, res) {
        try {
            logger.info('Manual incremental sync triggered via API');
            
            // Run sync in background
            this.syncService.performIncrementalSync()
                .then(() => {
                    this.broadcastToClients('manualSyncComplete', { type: 'incremental' });
                })
                .catch(error => {
                    logger.error('Manual incremental sync failed:', error);
                    this.broadcastToClients('manualSyncError', { 
                        type: 'incremental', 
                        error: error.message 
                    });
                });
            
            res.json({ 
                status: 'started',
                type: 'incremental',
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            logger.error('Error starting incremental sync:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetConflicts(req, res) {
        try {
            // Get todos with conflicts
            const conflictedTodos = await this.syncService.db.getAllTodos({ 
                conflictDetected: true 
            });
            
            res.json({
                conflicts: conflictedTodos,
                count: conflictedTodos.length
            });
        } catch (error) {
            logger.error('Error getting conflicts:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleResolveConflict(req, res) {
        try {
            const { id } = req.params;
            const { strategy = 'auto' } = req.body;
            
            const todo = await this.syncService.db.getTodo(parseInt(id));
            if (!todo) {
                return res.status(404).json({ error: 'Todo not found' });
            }
            
            if (!todo.conflictDetected) {
                return res.status(400).json({ error: 'No conflict detected for this todo' });
            }
            
            // Resolve conflict (implementation would need GitHub data)
            logger.info(`Manual conflict resolution requested for todo ${id} using ${strategy}`);
            
            res.json({ 
                status: 'resolved',
                todoId: id,
                strategy: strategy,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            logger.error('Error resolving conflict:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetStats(req, res) {
        try {
            const { hours = 24 } = req.query;
            const stats = await this.syncService.getDetailedStats(parseInt(hours));
            
            res.json({
                ...stats,
                server: {
                    uptime: process.uptime(),
                    connections: this.connections.size,
                    memory: process.memoryUsage()
                }
            });
        } catch (error) {
            logger.error('Error getting stats:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetTodos(req, res) {
        try {
            const { status, project, limit = 100, offset = 0 } = req.query;
            
            const filters = {};
            if (status) filters.status = status;
            if (project) filters.projectPath = project;
            
            const todos = await this.syncService.db.getAllTodos(filters);
            const paginatedTodos = todos.slice(offset, offset + limit);
            
            res.json({
                todos: paginatedTodos,
                total: todos.length,
                offset: parseInt(offset),
                limit: parseInt(limit)
            });
        } catch (error) {
            logger.error('Error getting todos:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetTodo(req, res) {
        try {
            const { id } = req.params;
            const todo = await this.syncService.db.getTodo(parseInt(id));
            
            if (!todo) {
                return res.status(404).json({ error: 'Todo not found' });
            }
            
            res.json(todo);
        } catch (error) {
            logger.error('Error getting todo:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleUpdateTodo(req, res) {
        try {
            const { id } = req.params;
            const updates = req.body;
            
            await this.syncService.db.updateTodo(parseInt(id), updates);
            const updatedTodo = await this.syncService.db.getTodo(parseInt(id));
            
            this.broadcastToClients('todoUpdated', updatedTodo);
            
            res.json(updatedTodo);
        } catch (error) {
            logger.error('Error updating todo:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleDeleteTodo(req, res) {
        try {
            const { id } = req.params;
            
            await this.syncService.db.deleteTodo(parseInt(id));
            
            this.broadcastToClients('todoDeleted', { id: parseInt(id) });
            
            res.json({ status: 'deleted', id: parseInt(id) });
        } catch (error) {
            logger.error('Error deleting todo:', error);
            res.status(500).json({ error: error.message });
        }
    }

    // WebSocket Handlers
    handleWebSocketConnection(ws, req) {
        logger.info('New WebSocket connection established');
        
        this.connections.add(ws);
        
        ws.on('message', (message) => {
            try {
                const data = JSON.parse(message.toString());
                this.handleWebSocketMessage(ws, data);
            } catch (error) {
                logger.error('Invalid WebSocket message:', error);
                ws.send(JSON.stringify({ 
                    error: 'Invalid message format',
                    type: 'error'
                }));
            }
        });
        
        ws.on('close', () => {
            logger.info('WebSocket connection closed');
            this.connections.delete(ws);
        });
        
        ws.on('error', (error) => {
            logger.error('WebSocket error:', error);
            this.connections.delete(ws);
        });
        
        // Send initial connection confirmation
        ws.send(JSON.stringify({
            type: 'connected',
            timestamp: new Date().toISOString(),
            stats: this.syncService.getStats()
        }));
    }

    handleWebSocketMessage(ws, data) {
        const { type, payload } = data;
        
        if (this.wsHandlers[type]) {
            this.wsHandlers[type](ws, payload);
        } else {
            logger.warn(`Unknown WebSocket message type: ${type}`);
            ws.send(JSON.stringify({
                error: `Unknown message type: ${type}`,
                type: 'error'
            }));
        }
    }

    handleWebSocketSubscribe(ws, payload) {
        // Client subscribes to specific events
        ws.subscriptions = ws.subscriptions || new Set();
        
        if (payload.events && Array.isArray(payload.events)) {
            payload.events.forEach(event => ws.subscriptions.add(event));
        }
        
        ws.send(JSON.stringify({
            type: 'subscribed',
            events: Array.from(ws.subscriptions)
        }));
    }

    handleWebSocketUnsubscribe(ws, payload) {
        ws.subscriptions = ws.subscriptions || new Set();
        
        if (payload.events && Array.isArray(payload.events)) {
            payload.events.forEach(event => ws.subscriptions.delete(event));
        }
        
        ws.send(JSON.stringify({
            type: 'unsubscribed',
            events: Array.from(ws.subscriptions)
        }));
    }

    handleWebSocketPing(ws, payload) {
        ws.send(JSON.stringify({
            type: 'pong',
            timestamp: new Date().toISOString()
        }));
    }

    handleWebSocketManualSync(ws, payload) {
        const { syncType = 'incremental' } = payload;
        
        if (syncType === 'full') {
            this.handleFullSync({ body: {} }, { json: () => {} });
        } else {
            this.handleIncrementalSync({ body: {} }, { json: () => {} });
        }
        
        ws.send(JSON.stringify({
            type: 'syncStarted',
            syncType: syncType,
            timestamp: new Date().toISOString()
        }));
    }

    broadcastToClients(type, data) {
        const message = JSON.stringify({
            type: type,
            data: data,
            timestamp: new Date().toISOString()
        });
        
        let sent = 0;
        this.connections.forEach(ws => {
            if (ws.readyState === ws.OPEN) {
                // Check if client is subscribed to this event type
                if (!ws.subscriptions || ws.subscriptions.has(type) || ws.subscriptions.has('*')) {
                    ws.send(message);
                    sent++;
                }
            }
        });
        
        logger.debug(`Broadcasted ${type} to ${sent} clients`);
    }

    errorHandler(err, req, res, next) {
        logger.error('Express error:', err);
        
        res.status(err.status || 500).json({
            error: 'Internal server error',
            message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong',
            timestamp: new Date().toISOString(),
            path: req.path,
            method: req.method
        });
    }
}