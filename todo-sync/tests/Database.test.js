import { Database } from '../src/database/Database.js';
import { jest } from '@jest/globals';
import fs from 'fs/promises';
import path from 'path';

describe('Database', () => {
    let db;
    const testDbPath = './test-data/test.db';

    beforeEach(async () => {
        // Clean up any existing test database
        try {
            await fs.unlink(testDbPath);
        } catch (error) {
            // File doesn't exist, which is fine
        }

        db = new Database(testDbPath);
        await db.initialize();
    });

    afterEach(async () => {
        if (db) {
            await db.close();
        }
        
        // Clean up test database
        try {
            await fs.unlink(testDbPath);
            await fs.rmdir('./test-data');
        } catch (error) {
            // Cleanup error is not critical
        }
    });

    describe('Todo CRUD operations', () => {
        test('should create and retrieve a todo', async () => {
            const todoData = {
                content: 'Test todo',
                status: 'pending',
                activeForm: 'Testing todo functionality',
                sessionId: 'test-session-123',
                projectPath: '/test/project'
            };

            const todoId = await db.createTodo(todoData);
            expect(todoId).toBeGreaterThan(0);

            const retrieved = await db.getTodo(todoId);
            expect(retrieved).toMatchObject({
                id: todoId,
                content: todoData.content,
                status: todoData.status,
                activeForm: todoData.activeForm,
                sessionId: todoData.sessionId,
                projectPath: todoData.projectPath
            });
        });

        test('should update todo fields', async () => {
            const todoId = await db.createTodo({
                content: 'Original content',
                status: 'pending'
            });

            await db.updateTodo(todoId, {
                content: 'Updated content',
                status: 'in_progress',
                githubIssueNumber: 123
            });

            const updated = await db.getTodo(todoId);
            expect(updated.content).toBe('Updated content');
            expect(updated.status).toBe('in_progress');
            expect(updated.githubIssueNumber).toBe(123);
            expect(updated.syncVersion).toBe(2); // Should increment
        });

        test('should find todo by GitHub issue number', async () => {
            const todoId = await db.createTodo({
                content: 'GitHub linked todo',
                githubIssueNumber: 456
            });

            const found = await db.getTodoByGithubIssue(456);
            expect(found.id).toBe(todoId);
            expect(found.githubIssueNumber).toBe(456);
        });

        test('should find todo by content and session', async () => {
            const todoData = {
                content: 'Unique todo content',
                sessionId: 'unique-session'
            };

            const todoId = await db.createTodo(todoData);

            const found = await db.getTodoByContent(
                todoData.content, 
                todoData.sessionId
            );
            
            expect(found.id).toBe(todoId);
            expect(found.content).toBe(todoData.content);
        });

        test('should filter todos by status', async () => {
            await db.createTodo({ content: 'Pending todo', status: 'pending' });
            await db.createTodo({ content: 'In progress todo', status: 'in_progress' });
            await db.createTodo({ content: 'Completed todo', status: 'completed' });

            const pendingTodos = await db.getAllTodos({ status: 'pending' });
            const inProgressTodos = await db.getAllTodos({ status: 'in_progress' });

            expect(pendingTodos).toHaveLength(1);
            expect(inProgressTodos).toHaveLength(1);
            expect(pendingTodos[0].status).toBe('pending');
            expect(inProgressTodos[0].status).toBe('in_progress');
        });

        test('should delete todo', async () => {
            const todoId = await db.createTodo({
                content: 'Todo to delete'
            });

            await db.deleteTodo(todoId);

            const retrieved = await db.getTodo(todoId);
            expect(retrieved).toBeNull();
        });
    });

    describe('Sync queue operations', () => {
        test('should add and retrieve sync operations', async () => {
            const todoId = await db.createTodo({ content: 'Test todo' });

            await db.addToSyncQueue({
                todoId: todoId,
                operation: 'create',
                target: 'github',
                payload: { test: 'data' },
                priority: 2
            });

            const operations = await db.getNextSyncOperations('github', 5);
            expect(operations).toHaveLength(1);
            expect(operations[0].todo_id).toBe(todoId);
            expect(operations[0].operation).toBe('create');
            expect(operations[0].target).toBe('github');
        });

        test('should mark sync operation as complete', async () => {
            const todoId = await db.createTodo({ content: 'Test todo' });

            await db.addToSyncQueue({
                todoId: todoId,
                operation: 'update',
                target: 'github'
            });

            const operations = await db.getNextSyncOperations('github', 1);
            const operationId = operations[0].id;

            await db.markSyncOperationComplete(operationId, true);

            const remainingOps = await db.getNextSyncOperations('github', 10);
            expect(remainingOps).toHaveLength(0);
        });

        test('should retry failed sync operations', async () => {
            const todoId = await db.createTodo({ content: 'Test todo' });

            await db.addToSyncQueue({
                todoId: todoId,
                operation: 'create',
                target: 'github',
                maxRetries: 3
            });

            const operations = await db.getNextSyncOperations('github', 1);
            const operationId = operations[0].id;

            // Mark as failed
            await db.markSyncOperationComplete(operationId, false, 'Test error');

            const retryCount = await db.getRetryCount(operationId);
            expect(retryCount).toBe(1);

            // Should still be available for retry (but scheduled later)
            // We won't test the scheduling delay in this unit test
        });
    });

    describe('Conflict management', () => {
        test('should log and resolve conflicts', async () => {
            const todoId = await db.createTodo({ content: 'Conflicted todo' });

            const localVersion = { content: 'Local version', status: 'pending' };
            const githubVersion = { content: 'GitHub version', status: 'in_progress' };

            await db.logConflict(todoId, localVersion, githubVersion);

            await db.resolveConflict(1, 'merged', 'auto'); // Assuming first conflict has ID 1

            // Verify conflict was logged (we'd need to add a getConflicts method to test this properly)
        });
    });

    describe('Performance tracking', () => {
        test('should record and retrieve sync stats', async () => {
            await db.recordSyncStats('test_operation', 1500, 10, 2);
            await db.recordSyncStats('test_operation', 2000, 15, 1);

            const stats = await db.getSyncStats(24);
            
            expect(stats).toHaveLength(1);
            expect(stats[0].operation_type).toBe('test_operation');
            expect(stats[0].operation_count).toBe('2'); // SQLite returns strings for aggregates
            expect(stats[0].total_todos_processed).toBe('25');
            expect(stats[0].total_errors).toBe('3');
        });
    });

    describe('Utility methods', () => {
        test('should generate consistent sync hash', async () => {
            const todo1 = {
                content: 'Test content',
                status: 'pending',
                activeForm: 'Testing'
            };

            const todo2 = { ...todo1 };

            const hash1 = db.generateSyncHash(todo1);
            const hash2 = db.generateSyncHash(todo2);

            expect(hash1).toBe(hash2);
            expect(hash1).toHaveLength(64); // SHA256 hex string
        });

        test('should parse todo with all fields correctly', () => {
            const dbTodo = {
                id: 1,
                content: 'Test todo',
                status: 'pending',
                active_form: 'Testing todo',
                created_at: '2023-01-01T00:00:00Z',
                updated_at: '2023-01-01T01:00:00Z',
                session_id: 'session-123',
                project_path: '/test/project',
                github_issue_number: 456,
                github_labels: '["bug", "enhancement"]',
                github_assignees: '["user1", "user2"]',
                sync_version: 2,
                conflict_detected: 1,
                needs_github_sync: 0
            };

            const parsed = db.parseTodo(dbTodo);

            expect(parsed).toMatchObject({
                id: 1,
                content: 'Test todo',
                status: 'pending',
                activeForm: 'Testing todo',
                sessionId: 'session-123',
                projectPath: '/test/project',
                githubIssueNumber: 456,
                githubLabels: ['bug', 'enhancement'],
                githubAssignees: ['user1', 'user2'],
                syncVersion: 2,
                conflictDetected: true,
                needsGithubSync: false
            });
        });
    });
});