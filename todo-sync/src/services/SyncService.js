import { Octokit } from '@octokit/rest';
import { TodoWriteReader } from './TodoWriteReader.js';
import { ConflictResolver } from './ConflictResolver.js';
import { PerformanceOptimizer } from './PerformanceOptimizer.js';
import { logger } from '../utils/logger.js';
import { EventEmitter } from 'events';

export class SyncService extends EventEmitter {
    constructor(database) {
        super();
        this.db = database;
        this.github = new Octokit({
            auth: process.env.GITHUB_TOKEN,
        });
        
        this.owner = process.env.GITHUB_OWNER || 'vanman2024';
        this.repo = process.env.GITHUB_REPO || 'multi-agent-claude-code';
        
        this.todoReader = new TodoWriteReader();
        this.conflictResolver = new ConflictResolver();
        this.performanceOptimizer = new PerformanceOptimizer(this, database);
        
        this.syncInterval = null;
        this.isRunning = false;
        this.isSyncing = false;
        
        // Performance tracking
        this.syncStats = {
            totalSyncs: 0,
            successfulSyncs: 0,
            failedSyncs: 0,
            lastSyncDuration: 0,
            lastSyncTime: null,
            todosProcessed: 0,
            conflictsResolved: 0
        };
        
        // Rate limiting
        this.rateLimiter = {
            requestsThisHour: 0,
            hourlyLimit: parseInt(process.env.RATE_LIMIT_PER_HOUR) || 5000,
            resetTime: Date.now() + 3600000 // 1 hour from now
        };
    }

    async start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        const intervalMs = parseInt(process.env.SYNC_INTERVAL_MS) || 30000; // 30 seconds default
        
        // Start periodic sync
        this.syncInterval = setInterval(async () => {
            if (!this.isSyncing) {
                await this.performIncrementalSync();
            }
        }, intervalMs);
        
        logger.info(`Sync service started with ${intervalMs}ms interval`);
        this.emit('started');
    }

    async stop() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
        
        // Wait for any ongoing sync to complete
        while (this.isSyncing) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        logger.info('Sync service stopped');
        this.emit('stopped');
    }

    async performFullSync() {
        if (this.isSyncing) {
            logger.warn('Sync already in progress, skipping full sync');
            return;
        }
        
        const startTime = Date.now();
        this.isSyncing = true;
        this.syncStats.totalSyncs++;
        
        try {
            logger.info('Starting full bidirectional sync...');
            
            // Step 1: Sync GitHub Issues to local database
            const githubStats = await this.syncGitHubToLocal();
            
            // Step 2: Sync local TodoWrite data to GitHub
            const localStats = await this.syncLocalToGitHub();
            
            // Step 3: Process any pending queue operations
            await this.processOfflineQueue();
            
            const duration = Date.now() - startTime;
            this.syncStats.lastSyncDuration = duration;
            this.syncStats.lastSyncTime = new Date();
            this.syncStats.successfulSyncs++;
            this.syncStats.todosProcessed += githubStats.processed + localStats.processed;
            
            // Record performance metrics
            await this.db.recordSyncStats(
                'full_sync', 
                duration, 
                githubStats.processed + localStats.processed,
                githubStats.errors + localStats.errors
            );
            
            logger.info(`Full sync completed in ${duration}ms`, {
                githubProcessed: githubStats.processed,
                localProcessed: localStats.processed,
                totalErrors: githubStats.errors + localStats.errors
            });
            
            this.emit('syncComplete', {
                type: 'full',
                duration,
                githubStats,
                localStats
            });
            
        } catch (error) {
            this.syncStats.failedSyncs++;
            logger.error('Full sync failed:', error);
            this.emit('syncError', { type: 'full', error });
            throw error;
        } finally {
            this.isSyncing = false;
        }
    }

    async performIncrementalSync() {
        if (this.isSyncing) return;
        
        const startTime = Date.now();
        this.isSyncing = true;
        
        try {
            // Only sync items that need syncing
            const pendingTodos = await this.db.getAllTodos({ needsSync: true });
            
            if (pendingTodos.length === 0) {
                // Still process offline queue
                await this.processOfflineQueue();
                return;
            }
            
            logger.info(`Starting incremental sync for ${pendingTodos.length} todos...`);
            
            let processed = 0;
            let errors = 0;
            
            // Process each todo that needs syncing
            for (const todo of pendingTodos) {
                try {
                    if (todo.needsGithubSync) {
                        await this.syncTodoToGitHub(todo);
                    }
                    if (todo.needsLocalSync) {
                        await this.syncGitHubIssueToLocal(todo.githubIssueNumber);
                    }
                    processed++;
                } catch (error) {
                    errors++;
                    logger.error(`Failed to sync todo ${todo.id}:`, error);
                }
            }
            
            // Process offline queue
            await this.processOfflineQueue();
            
            const duration = Date.now() - startTime;
            
            if (processed > 0) {
                logger.info(`Incremental sync completed: ${processed} processed, ${errors} errors in ${duration}ms`);
                this.emit('syncComplete', {
                    type: 'incremental',
                    duration,
                    processed,
                    errors
                });
            }
            
        } catch (error) {
            logger.error('Incremental sync failed:', error);
            this.emit('syncError', { type: 'incremental', error });
        } finally {
            this.isSyncing = false;
        }
    }

    async syncGitHubToLocal() {
        let processed = 0;
        let errors = 0;
        
        try {
            // Get all issues from GitHub (paginated)
            const issues = await this.getAllGitHubIssues();
            
            for (const issue of issues) {
                try {
                    await this.syncGitHubIssueToLocal(issue.number, issue);
                    processed++;
                } catch (error) {
                    errors++;
                    logger.error(`Failed to sync GitHub issue #${issue.number}:`, error);
                }
            }
            
            logger.info(`GitHub to local sync: ${processed} issues processed, ${errors} errors`);
            
        } catch (error) {
            logger.error('Failed to fetch GitHub issues:', error);
            errors++;
        }
        
        return { processed, errors };
    }

    async syncLocalToGitHub() {
        let processed = 0;
        let errors = 0;
        
        try {
            // Get local todos from TodoWrite files
            const localTodos = await this.todoReader.getAllTodos();
            
            for (const todo of localTodos) {
                try {
                    // Check if this todo already exists in database
                    let dbTodo = await this.db.getTodoByContent(todo.content, todo.sessionId);
                    
                    if (!dbTodo) {
                        // New todo, create in database and sync to GitHub
                        const todoId = await this.db.createTodo({
                            ...todo,
                            needsGithubSync: true
                        });
                        dbTodo = await this.db.getTodo(todoId);
                    }
                    
                    // Sync to GitHub if needed
                    if (dbTodo.needsGithubSync) {
                        await this.syncTodoToGitHub(dbTodo);
                    }
                    
                    processed++;
                } catch (error) {
                    errors++;
                    logger.error(`Failed to sync local todo "${todo.content}":`, error);
                }
            }
            
            logger.info(`Local to GitHub sync: ${processed} todos processed, ${errors} errors`);
            
        } catch (error) {
            logger.error('Failed to read local todos:', error);
            errors++;
        }
        
        return { processed, errors };
    }

    async syncTodoToGitHub(todo) {
        if (!this.canMakeRequest()) {
            logger.warn('Rate limit reached, queuing GitHub operation');
            await this.db.addToSyncQueue({
                todoId: todo.id,
                operation: todo.githubIssueNumber ? 'update' : 'create',
                target: 'github',
                payload: todo
            });
            return;
        }
        
        try {
            let issue;
            
            if (todo.githubIssueNumber) {
                // Update existing issue
                issue = await this.github.rest.issues.update({
                    owner: this.owner,
                    repo: this.repo,
                    issue_number: todo.githubIssueNumber,
                    title: todo.content.substring(0, 100), // GitHub title limit
                    body: this.generateIssueBody(todo),
                    state: this.mapStatusToGitHubState(todo.status)
                });
                
                logger.debug(`Updated GitHub issue #${todo.githubIssueNumber}`);
            } else {
                // Create new issue
                issue = await this.github.rest.issues.create({
                    owner: this.owner,
                    repo: this.repo,
                    title: todo.content.substring(0, 100),
                    body: this.generateIssueBody(todo),
                    labels: ['todo-sync', `status:${todo.status}`]
                });
                
                logger.debug(`Created GitHub issue #${issue.data.number}`);
            }
            
            // Update local database with GitHub data
            await this.db.updateTodo(todo.id, {
                githubIssueNumber: issue.data.number,
                githubIssueId: issue.data.id,
                githubState: issue.data.state,
                githubTitle: issue.data.title,
                githubBody: issue.data.body,
                githubSyncedAt: new Date().toISOString(),
                githubLastModified: issue.data.updated_at,
                needsGithubSync: false
            });
            
            this.incrementRateLimit();
            
        } catch (error) {
            logger.error(`Failed to sync todo ${todo.id} to GitHub:`, error);
            
            // Queue for retry if it's a temporary error
            if (this.isTemporaryError(error)) {
                await this.db.addToSyncQueue({
                    todoId: todo.id,
                    operation: todo.githubIssueNumber ? 'update' : 'create',
                    target: 'github',
                    payload: todo,
                    priority: 2 // Higher priority for retries
                });
            }
            
            throw error;
        }
    }

    async syncGitHubIssueToLocal(issueNumber, issueData = null) {
        try {
            // Fetch issue data if not provided
            if (!issueData) {
                const response = await this.github.rest.issues.get({
                    owner: this.owner,
                    repo: this.repo,
                    issue_number: issueNumber
                });
                issueData = response.data;
            }
            
            // Skip if not a todo-sync issue
            if (!issueData.labels.some(label => 
                typeof label === 'string' ? label === 'todo-sync' : label.name === 'todo-sync'
            )) {
                return;
            }
            
            let dbTodo = await this.db.getTodoByGithubIssue(issueNumber);
            
            if (!dbTodo) {
                // Create new todo from GitHub issue
                const todoId = await this.db.createTodo({
                    content: issueData.title,
                    status: this.mapGitHubStateToStatus(issueData.state),
                    githubIssueNumber: issueData.number,
                    githubIssueId: issueData.id,
                    githubState: issueData.state,
                    githubTitle: issueData.title,
                    githubBody: issueData.body,
                    githubSyncedAt: new Date().toISOString(),
                    githubLastModified: issueData.updated_at,
                    needsLocalSync: false,
                    needsGithubSync: false
                });
                
                logger.debug(`Created local todo from GitHub issue #${issueNumber}`);
                return;
            }
            
            // Check for conflicts
            const localHash = this.db.generateSyncHash(dbTodo);
            const githubHash = this.db.generateSyncHash({
                content: issueData.title,
                status: this.mapGitHubStateToStatus(issueData.state),
                githubState: issueData.state,
                githubTitle: issueData.title,
                githubBody: issueData.body
            });
            
            if (localHash !== githubHash && dbTodo.lastSyncHash !== githubHash) {
                // Conflict detected
                await this.handleConflict(dbTodo, {
                    content: issueData.title,
                    status: this.mapGitHubStateToStatus(issueData.state),
                    githubState: issueData.state,
                    githubTitle: issueData.title,
                    githubBody: issueData.body,
                    githubLastModified: issueData.updated_at
                });
                return;
            }
            
            // Update local todo with GitHub data
            await this.db.updateTodo(dbTodo.id, {
                content: issueData.title,
                status: this.mapGitHubStateToStatus(issueData.state),
                githubState: issueData.state,
                githubTitle: issueData.title,
                githubBody: issueData.body,
                githubSyncedAt: new Date().toISOString(),
                githubLastModified: issueData.updated_at,
                needsLocalSync: false
            });
            
            this.incrementRateLimit();
            
        } catch (error) {
            logger.error(`Failed to sync GitHub issue #${issueNumber} to local:`, error);
            throw error;
        }
    }

    async handleConflict(localTodo, githubData) {
        logger.warn(`Conflict detected for todo ${localTodo.id}`);
        
        // Log the conflict
        await this.db.logConflict(localTodo.id, localTodo, githubData);
        
        // Attempt automatic resolution
        const resolution = await this.conflictResolver.resolve(localTodo, githubData);
        
        if (resolution.canResolve) {
            await this.db.updateTodo(localTodo.id, {
                ...resolution.resolvedData,
                conflictDetected: false
            });
            
            await this.db.resolveConflict(resolution.conflictId, resolution.strategy, 'auto');
            
            this.syncStats.conflictsResolved++;
            logger.info(`Auto-resolved conflict for todo ${localTodo.id} using ${resolution.strategy}`);
        } else {
            // Mark as requiring manual resolution
            await this.db.updateTodo(localTodo.id, {
                conflictDetected: true
            });
            
            logger.warn(`Manual resolution required for todo ${localTodo.id}`);
            this.emit('conflictDetected', { todoId: localTodo.id, localTodo, githubData });
        }
    }

    async processOfflineQueue() {
        const githubOperations = await this.db.getNextSyncOperations('github', 10);
        const localOperations = await this.db.getNextSyncOperations('local', 10);
        
        // Process GitHub operations
        for (const operation of githubOperations) {
            try {
                const payload = JSON.parse(operation.payload);
                
                switch (operation.operation) {
                    case 'create':
                    case 'update':
                        const todo = await this.db.getTodo(operation.todo_id);
                        if (todo) {
                            await this.syncTodoToGitHub(todo);
                        }
                        break;
                        
                    case 'delete':
                        if (payload.githubIssueNumber && this.canMakeRequest()) {
                            await this.github.rest.issues.update({
                                owner: this.owner,
                                repo: this.repo,
                                issue_number: payload.githubIssueNumber,
                                state: 'closed'
                            });
                        }
                        break;
                }
                
                await this.db.markSyncOperationComplete(operation.id, true);
                
            } catch (error) {
                logger.error(`Failed to process queue operation ${operation.id}:`, error);
                await this.db.markSyncOperationComplete(operation.id, false, error.message);
            }
        }
        
        // Process local operations (TodoWrite updates)
        for (const operation of localOperations) {
            try {
                // Local operations are handled by TodoWrite reader
                await this.db.markSyncOperationComplete(operation.id, true);
            } catch (error) {
                logger.error(`Failed to process local operation ${operation.id}:`, error);
                await this.db.markSyncOperationComplete(operation.id, false, error.message);
            }
        }
    }

    async getAllGitHubIssues() {
        const issues = [];
        let page = 1;
        const perPage = 100;
        
        while (true) {
            if (!this.canMakeRequest()) {
                logger.warn('Rate limit reached while fetching GitHub issues');
                break;
            }
            
            const response = await this.github.rest.issues.listForRepo({
                owner: this.owner,
                repo: this.repo,
                state: 'all',
                labels: 'todo-sync',
                per_page: perPage,
                page: page
            });
            
            issues.push(...response.data);
            this.incrementRateLimit();
            
            if (response.data.length < perPage) {
                break; // Last page
            }
            
            page++;
        }
        
        return issues;
    }

    // Utility methods
    generateIssueBody(todo) {
        return `**Todo:** ${todo.content}

**Status:** ${todo.status}
**Active Form:** ${todo.activeForm || 'N/A'}
**Session:** ${todo.sessionId || 'N/A'}
**Project:** ${todo.projectPath || 'N/A'}

---
*This issue is automatically synchronized with Claude Code TodoWrite. Do not edit manually.*
*Last sync: ${new Date().toISOString()}*`;
    }

    mapStatusToGitHubState(status) {
        return status === 'completed' ? 'closed' : 'open';
    }

    mapGitHubStateToStatus(state) {
        return state === 'closed' ? 'completed' : 'pending';
    }

    canMakeRequest() {
        const now = Date.now();
        if (now > this.rateLimiter.resetTime) {
            this.rateLimiter.requestsThisHour = 0;
            this.rateLimiter.resetTime = now + 3600000;
        }
        return this.rateLimiter.requestsThisHour < this.rateLimiter.hourlyLimit;
    }

    incrementRateLimit() {
        this.rateLimiter.requestsThisHour++;
    }

    isTemporaryError(error) {
        // GitHub API temporary errors
        const temporaryErrorCodes = [403, 429, 500, 502, 503, 504];
        return temporaryErrorCodes.includes(error.status);
    }

    // Stats and monitoring
    getStats() {
        return {
            ...this.syncStats,
            rateLimiter: {
                requestsThisHour: this.rateLimiter.requestsThisHour,
                hourlyLimit: this.rateLimiter.hourlyLimit,
                remainingRequests: this.rateLimiter.hourlyLimit - this.rateLimiter.requestsThisHour
            },
            isRunning: this.isRunning,
            isSyncing: this.isSyncing
        };
    }

    async getDetailedStats(hoursBack = 24) {
        const dbStats = await this.db.getSyncStats(hoursBack);
        return {
            runtime: this.getStats(),
            database: dbStats
        };
    }
}