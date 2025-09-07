import sqlite3 from 'sqlite3';
import { promisify } from 'util';
import { logger } from '../utils/logger.js';
import fs from 'fs/promises';
import path from 'path';

export class Database {
    constructor(dbPath) {
        this.dbPath = dbPath;
        this.db = null;
    }

    async initialize() {
        // Ensure data directory exists
        const dir = path.dirname(this.dbPath);
        await fs.mkdir(dir, { recursive: true });

        // Open database connection
        this.db = new sqlite3.Database(this.dbPath);
        
        // Promisify database methods
        this.db.run = promisify(this.db.run.bind(this.db));
        this.db.get = promisify(this.db.get.bind(this.db));
        this.db.all = promisify(this.db.all.bind(this.db));

        // Create tables
        await this.createTables();
        
        logger.info(`Database initialized at ${this.dbPath}`);
    }

    async createTables() {
        // Extended TodoWrite entries with GitHub metadata
        await this.db.run(`
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                active_form TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                project_path TEXT,
                
                -- GitHub integration fields
                github_issue_number INTEGER,
                github_issue_id INTEGER,
                github_synced_at DATETIME,
                github_last_modified DATETIME,
                github_state TEXT, -- open/closed
                github_title TEXT,
                github_body TEXT,
                github_labels TEXT, -- JSON array string
                github_assignees TEXT, -- JSON array string
                
                -- Sync metadata
                sync_version INTEGER DEFAULT 1,
                last_sync_hash TEXT,
                conflict_detected BOOLEAN DEFAULT 0,
                needs_github_sync BOOLEAN DEFAULT 0,
                needs_local_sync BOOLEAN DEFAULT 0,
                
                UNIQUE(content, session_id, project_path)
            )
        `);

        // Sync operation queue for offline support
        await this.db.run(`
            CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                todo_id INTEGER,
                operation TEXT NOT NULL, -- 'create', 'update', 'delete'
                target TEXT NOT NULL, -- 'github' or 'local'
                payload TEXT, -- JSON data
                priority INTEGER DEFAULT 1,
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                scheduled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                error_message TEXT,
                
                FOREIGN KEY(todo_id) REFERENCES todos(id) ON DELETE CASCADE
            )
        `);

        // Conflict resolution log
        await this.db.run(`
            CREATE TABLE IF NOT EXISTS conflicts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                todo_id INTEGER NOT NULL,
                local_version TEXT,
                github_version TEXT,
                resolution TEXT, -- 'local_wins', 'github_wins', 'merged', 'manual'
                resolved_at DATETIME,
                resolved_by TEXT, -- 'auto' or 'user'
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY(todo_id) REFERENCES todos(id) ON DELETE CASCADE
            )
        `);

        // Sync statistics and performance tracking
        await this.db.run(`
            CREATE TABLE IF NOT EXISTS sync_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT NOT NULL,
                duration_ms INTEGER,
                todos_processed INTEGER,
                errors_encountered INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Create indexes for performance
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_todos_github_issue ON todos(github_issue_number)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_todos_session ON todos(session_id)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_todos_project ON todos(project_path)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_todos_sync_needed ON todos(needs_github_sync, needs_local_sync)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_sync_queue_target ON sync_queue(target, scheduled_at)`);
        await this.db.run(`CREATE INDEX IF NOT EXISTS idx_sync_queue_priority ON sync_queue(priority, scheduled_at)`);
    }

    // Todo CRUD operations
    async createTodo(todo) {
        const query = `
            INSERT INTO todos (
                content, status, active_form, session_id, project_path,
                github_issue_number, github_issue_id, github_state,
                github_title, github_body, github_labels, github_assignees,
                needs_github_sync, last_sync_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;
        
        const result = await this.db.run(query, [
            todo.content,
            todo.status || 'pending',
            todo.activeForm,
            todo.sessionId,
            todo.projectPath,
            todo.githubIssueNumber || null,
            todo.githubIssueId || null,
            todo.githubState || null,
            todo.githubTitle || null,
            todo.githubBody || null,
            todo.githubLabels ? JSON.stringify(todo.githubLabels) : null,
            todo.githubAssignees ? JSON.stringify(todo.githubAssignees) : null,
            todo.githubIssueNumber ? 0 : 1, // needs_github_sync
            this.generateSyncHash(todo)
        ]);
        
        return result.lastID;
    }

    async updateTodo(id, updates) {
        const fields = [];
        const values = [];
        
        // Build dynamic update query
        const allowedFields = [
            'content', 'status', 'active_form', 'github_issue_number', 
            'github_issue_id', 'github_state', 'github_title', 'github_body',
            'github_labels', 'github_assignees', 'github_synced_at',
            'github_last_modified', 'needs_github_sync', 'needs_local_sync',
            'sync_version', 'conflict_detected'
        ];
        
        Object.keys(updates).forEach(key => {
            const dbKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
            if (allowedFields.includes(dbKey)) {
                fields.push(`${dbKey} = ?`);
                values.push(typeof updates[key] === 'object' && updates[key] !== null 
                    ? JSON.stringify(updates[key]) 
                    : updates[key]
                );
            }
        });
        
        if (fields.length === 0) return;
        
        // Always update the updated_at and sync_version
        fields.push('updated_at = CURRENT_TIMESTAMP');
        fields.push('sync_version = sync_version + 1');
        fields.push('last_sync_hash = ?');
        
        values.push(this.generateSyncHash({ id, ...updates }));
        values.push(id);
        
        const query = `UPDATE todos SET ${fields.join(', ')} WHERE id = ?`;
        await this.db.run(query, values);
    }

    async getTodo(id) {
        const todo = await this.db.get('SELECT * FROM todos WHERE id = ?', [id]);
        return this.parseTodo(todo);
    }

    async getTodoByGithubIssue(issueNumber) {
        const todo = await this.db.get(
            'SELECT * FROM todos WHERE github_issue_number = ?', 
            [issueNumber]
        );
        return this.parseTodo(todo);
    }

    async getTodoByContent(content, sessionId) {
        const todo = await this.db.get(
            'SELECT * FROM todos WHERE content = ? AND session_id = ?', 
            [content, sessionId]
        );
        return this.parseTodo(todo);
    }

    async getAllTodos(filters = {}) {
        let query = 'SELECT * FROM todos';
        const conditions = [];
        const values = [];
        
        if (filters.status) {
            conditions.push('status = ?');
            values.push(filters.status);
        }
        
        if (filters.projectPath) {
            conditions.push('project_path = ?');
            values.push(filters.projectPath);
        }
        
        if (filters.needsSync) {
            conditions.push('(needs_github_sync = 1 OR needs_local_sync = 1)');
        }
        
        if (conditions.length > 0) {
            query += ` WHERE ${conditions.join(' AND ')}`;
        }
        
        query += ' ORDER BY updated_at DESC';
        
        const todos = await this.db.all(query, values);
        return todos.map(todo => this.parseTodo(todo));
    }

    async deleteTodo(id) {
        await this.db.run('DELETE FROM todos WHERE id = ?', [id]);
    }

    // Sync queue operations
    async addToSyncQueue(operation) {
        const query = `
            INSERT INTO sync_queue (
                todo_id, operation, target, payload, priority, max_retries
            ) VALUES (?, ?, ?, ?, ?, ?)
        `;
        
        await this.db.run(query, [
            operation.todoId,
            operation.operation,
            operation.target,
            JSON.stringify(operation.payload || {}),
            operation.priority || 1,
            operation.maxRetries || 3
        ]);
    }

    async getNextSyncOperations(target, limit = 10) {
        const query = `
            SELECT * FROM sync_queue 
            WHERE target = ? AND completed_at IS NULL 
                AND retry_count < max_retries
                AND scheduled_at <= CURRENT_TIMESTAMP
            ORDER BY priority DESC, scheduled_at ASC
            LIMIT ?
        `;
        
        return await this.db.all(query, [target, limit]);
    }

    async markSyncOperationComplete(queueId, success = true, errorMessage = null) {
        if (success) {
            await this.db.run(
                'UPDATE sync_queue SET completed_at = CURRENT_TIMESTAMP WHERE id = ?',
                [queueId]
            );
        } else {
            // Increment retry count and reschedule
            const retryDelay = Math.min(300000, Math.pow(2, await this.getRetryCount(queueId)) * 1000); // Exponential backoff, max 5 min
            const scheduledAt = new Date(Date.now() + retryDelay).toISOString();
            
            await this.db.run(`
                UPDATE sync_queue 
                SET retry_count = retry_count + 1, 
                    scheduled_at = ?, 
                    error_message = ?
                WHERE id = ?
            `, [scheduledAt, errorMessage, queueId]);
        }
    }

    async getRetryCount(queueId) {
        const result = await this.db.get('SELECT retry_count FROM sync_queue WHERE id = ?', [queueId]);
        return result ? result.retry_count : 0;
    }

    // Conflict management
    async logConflict(todoId, localVersion, githubVersion) {
        const query = `
            INSERT INTO conflicts (todo_id, local_version, github_version)
            VALUES (?, ?, ?)
        `;
        
        await this.db.run(query, [
            todoId,
            JSON.stringify(localVersion),
            JSON.stringify(githubVersion)
        ]);
    }

    async resolveConflict(conflictId, resolution, resolvedBy = 'auto') {
        await this.db.run(`
            UPDATE conflicts 
            SET resolution = ?, resolved_at = CURRENT_TIMESTAMP, resolved_by = ?
            WHERE id = ?
        `, [resolution, resolvedBy, conflictId]);
    }

    // Performance tracking
    async recordSyncStats(operationType, durationMs, todosProcessed, errorsEncountered) {
        await this.db.run(`
            INSERT INTO sync_stats (operation_type, duration_ms, todos_processed, errors_encountered)
            VALUES (?, ?, ?, ?)
        `, [operationType, durationMs, todosProcessed, errorsEncountered]);
    }

    async getSyncStats(hoursBack = 24) {
        const since = new Date(Date.now() - hoursBack * 60 * 60 * 1000).toISOString();
        
        return await this.db.all(`
            SELECT operation_type, 
                   COUNT(*) as operation_count,
                   AVG(duration_ms) as avg_duration,
                   SUM(todos_processed) as total_todos_processed,
                   SUM(errors_encountered) as total_errors
            FROM sync_stats 
            WHERE timestamp >= ?
            GROUP BY operation_type
            ORDER BY timestamp DESC
        `, [since]);
    }

    // Utility methods
    parseTodo(todo) {
        if (!todo) return null;
        
        return {
            id: todo.id,
            content: todo.content,
            status: todo.status,
            activeForm: todo.active_form,
            createdAt: todo.created_at,
            updatedAt: todo.updated_at,
            sessionId: todo.session_id,
            projectPath: todo.project_path,
            githubIssueNumber: todo.github_issue_number,
            githubIssueId: todo.github_issue_id,
            githubSyncedAt: todo.github_synced_at,
            githubLastModified: todo.github_last_modified,
            githubState: todo.github_state,
            githubTitle: todo.github_title,
            githubBody: todo.github_body,
            githubLabels: todo.github_labels ? JSON.parse(todo.github_labels) : [],
            githubAssignees: todo.github_assignees ? JSON.parse(todo.github_assignees) : [],
            syncVersion: todo.sync_version,
            lastSyncHash: todo.last_sync_hash,
            conflictDetected: Boolean(todo.conflict_detected),
            needsGithubSync: Boolean(todo.needs_github_sync),
            needsLocalSync: Boolean(todo.needs_local_sync)
        };
    }

    generateSyncHash(data) {
        const crypto = require('crypto');
        const hashContent = JSON.stringify({
            content: data.content,
            status: data.status,
            activeForm: data.activeForm,
            githubState: data.githubState,
            githubTitle: data.githubTitle,
            githubBody: data.githubBody
        });
        return crypto.createHash('sha256').update(hashContent).digest('hex');
    }

    async close() {
        if (this.db) {
            await new Promise((resolve, reject) => {
                this.db.close((err) => {
                    if (err) reject(err);
                    else resolve();
                });
            });
        }
    }
}