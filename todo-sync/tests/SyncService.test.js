import { SyncService } from '../src/services/SyncService.js';
import { Database } from '../src/database/Database.js';
import { TodoWriteReader } from '../src/services/TodoWriteReader.js';
import { ConflictResolver } from '../src/services/ConflictResolver.js';
import { jest } from '@jest/globals';

// Mock dependencies
jest.mock('../src/services/TodoWriteReader.js');
jest.mock('../src/services/ConflictResolver.js');

describe('SyncService', () => {
    let syncService;
    let mockDb;
    let mockGithub;
    let mockTodoReader;
    let mockConflictResolver;

    beforeEach(() => {
        // Mock database
        mockDb = {
            getAllTodos: jest.fn(),
            getTodo: jest.fn(),
            getTodoByGithubIssue: jest.fn(),
            getTodoByContent: jest.fn(),
            createTodo: jest.fn(),
            updateTodo: jest.fn(),
            deleteTodo: jest.fn(),
            addToSyncQueue: jest.fn(),
            getNextSyncOperations: jest.fn(),
            markSyncOperationComplete: jest.fn(),
            logConflict: jest.fn(),
            recordSyncStats: jest.fn(),
            generateSyncHash: jest.fn().mockReturnValue('mock-hash')
        };

        // Mock GitHub API
        mockGithub = {
            rest: {
                issues: {
                    listForRepo: jest.fn(),
                    get: jest.fn(),
                    create: jest.fn(),
                    update: jest.fn()
                }
            }
        };

        // Create sync service with mocked dependencies
        syncService = new SyncService(mockDb);
        syncService.github = mockGithub;

        // Mock TodoWrite reader
        mockTodoReader = {
            getAllTodos: jest.fn()
        };
        syncService.todoReader = mockTodoReader;

        // Mock conflict resolver
        mockConflictResolver = {
            resolve: jest.fn()
        };
        syncService.conflictResolver = mockConflictResolver;
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    describe('Service lifecycle', () => {
        test('should start and stop sync service', async () => {
            expect(syncService.isRunning).toBe(false);

            await syncService.start();
            expect(syncService.isRunning).toBe(true);
            expect(syncService.syncInterval).toBeDefined();

            await syncService.stop();
            expect(syncService.isRunning).toBe(false);
            expect(syncService.syncInterval).toBeNull();
        });
    });

    describe('GitHub to Local sync', () => {
        test('should sync GitHub issues to local database', async () => {
            const mockIssues = [
                {
                    number: 123,
                    id: 456,
                    title: 'Test issue',
                    state: 'open',
                    body: 'Test description',
                    labels: [{ name: 'todo-sync' }],
                    updated_at: '2023-01-01T12:00:00Z'
                }
            ];

            mockGithub.rest.issues.listForRepo.mockResolvedValue({
                data: mockIssues
            });

            mockDb.getTodoByGithubIssue.mockResolvedValue(null); // New issue
            mockDb.createTodo.mockResolvedValue(1);
            
            const stats = await syncService.syncGitHubToLocal();

            expect(mockGithub.rest.issues.listForRepo).toHaveBeenCalledWith(
                expect.objectContaining({
                    labels: 'todo-sync',
                    state: 'all'
                })
            );

            expect(mockDb.createTodo).toHaveBeenCalledWith(
                expect.objectContaining({
                    content: 'Test issue',
                    githubIssueNumber: 123,
                    githubIssueId: 456,
                    githubState: 'open'
                })
            );

            expect(stats.processed).toBe(1);
            expect(stats.errors).toBe(0);
        });

        test('should update existing todo when GitHub issue changes', async () => {
            const mockIssue = {
                number: 123,
                title: 'Updated issue title',
                state: 'closed',
                body: 'Updated description',
                labels: [{ name: 'todo-sync' }],
                updated_at: '2023-01-01T13:00:00Z'
            };

            const existingTodo = {
                id: 1,
                content: 'Original title',
                githubIssueNumber: 123,
                lastSyncHash: 'old-hash'
            };

            mockDb.getTodoByGithubIssue.mockResolvedValue(existingTodo);
            mockDb.generateSyncHash.mockReturnValueOnce('old-hash').mockReturnValueOnce('new-hash');

            await syncService.syncGitHubIssueToLocal(123, mockIssue);

            expect(mockDb.updateTodo).toHaveBeenCalledWith(
                1,
                expect.objectContaining({
                    content: 'Updated issue title',
                    status: 'completed', // closed -> completed
                    githubState: 'closed'
                })
            );
        });

        test('should detect and handle conflicts', async () => {
            const mockIssue = {
                number: 123,
                title: 'Conflicting title',
                state: 'open',
                updated_at: '2023-01-01T14:00:00Z'
            };

            const existingTodo = {
                id: 1,
                content: 'Different local title',
                githubIssueNumber: 123,
                lastSyncHash: 'old-hash'
            };

            mockDb.getTodoByGithubIssue.mockResolvedValue(existingTodo);
            mockDb.generateSyncHash
                .mockReturnValueOnce('old-hash') // local hash
                .mockReturnValueOnce('new-hash'); // github hash

            mockConflictResolver.resolve.mockResolvedValue({
                canResolve: true,
                strategy: 'merged',
                resolvedData: { content: 'Merged title' }
            });

            await syncService.syncGitHubIssueToLocal(123, mockIssue);

            expect(mockDb.logConflict).toHaveBeenCalledWith(1, existingTodo, expect.any(Object));
            expect(mockConflictResolver.resolve).toHaveBeenCalled();
        });
    });

    describe('Local to GitHub sync', () => {
        test('should sync local todos to GitHub', async () => {
            const mockTodos = [
                {
                    content: 'New todo',
                    status: 'pending',
                    sessionId: 'session-123',
                    projectPath: '/test/project'
                }
            ];

            mockTodoReader.getAllTodos.mockResolvedValue(mockTodos);
            mockDb.getTodoByContent.mockResolvedValue(null); // New todo
            mockDb.createTodo.mockResolvedValue(1);
            mockDb.getTodo.mockResolvedValue({
                id: 1,
                ...mockTodos[0],
                needsGithubSync: true
            });

            mockGithub.rest.issues.create.mockResolvedValue({
                data: {
                    number: 456,
                    id: 789,
                    title: 'New todo',
                    state: 'open',
                    updated_at: '2023-01-01T15:00:00Z'
                }
            });

            const stats = await syncService.syncLocalToGitHub();

            expect(mockGithub.rest.issues.create).toHaveBeenCalledWith(
                expect.objectContaining({
                    title: 'New todo',
                    labels: ['todo-sync', 'status:pending']
                })
            );

            expect(mockDb.updateTodo).toHaveBeenCalledWith(
                1,
                expect.objectContaining({
                    githubIssueNumber: 456,
                    githubIssueId: 789,
                    needsGithubSync: false
                })
            );

            expect(stats.processed).toBe(1);
        });

        test('should update existing GitHub issue', async () => {
            const existingTodo = {
                id: 1,
                content: 'Updated todo content',
                status: 'completed',
                githubIssueNumber: 456,
                needsGithubSync: true
            };

            mockDb.getTodo.mockResolvedValue(existingTodo);

            mockGithub.rest.issues.update.mockResolvedValue({
                data: {
                    number: 456,
                    id: 789,
                    title: 'Updated todo content',
                    state: 'closed',
                    updated_at: '2023-01-01T16:00:00Z'
                }
            });

            await syncService.syncTodoToGitHub(existingTodo);

            expect(mockGithub.rest.issues.update).toHaveBeenCalledWith(
                expect.objectContaining({
                    issue_number: 456,
                    title: 'Updated todo content',
                    state: 'closed' // completed -> closed
                })
            );
        });

        test('should handle rate limiting by queuing operations', async () => {
            const todo = {
                id: 1,
                content: 'Rate limited todo',
                needsGithubSync: true
            };

            // Mock rate limit exceeded
            syncService.rateLimiter.requestsThisHour = syncService.rateLimiter.hourlyLimit;

            await syncService.syncTodoToGitHub(todo);

            expect(mockDb.addToSyncQueue).toHaveBeenCalledWith(
                expect.objectContaining({
                    todoId: 1,
                    operation: 'create',
                    target: 'github'
                })
            );

            expect(mockGithub.rest.issues.create).not.toHaveBeenCalled();
        });
    });

    describe('Offline queue processing', () => {
        test('should process queued GitHub operations', async () => {
            const queuedOperations = [
                {
                    id: 1,
                    todo_id: 1,
                    operation: 'create',
                    target: 'github',
                    payload: '{"content": "Queued todo"}'
                }
            ];

            mockDb.getNextSyncOperations.mockResolvedValue(queuedOperations);
            mockDb.getTodo.mockResolvedValue({
                id: 1,
                content: 'Queued todo',
                status: 'pending'
            });

            mockGithub.rest.issues.create.mockResolvedValue({
                data: { number: 789, id: 123 }
            });

            await syncService.processOfflineQueue();

            expect(mockDb.getNextSyncOperations).toHaveBeenCalledWith('github', 10);
            expect(mockDb.markSyncOperationComplete).toHaveBeenCalledWith(1, true);
        });

        test('should handle failed queue operations', async () => {
            const queuedOperations = [
                {
                    id: 1,
                    todo_id: 1,
                    operation: 'create',
                    target: 'github',
                    payload: '{}'
                }
            ];

            mockDb.getNextSyncOperations.mockResolvedValue(queuedOperations);
            mockDb.getTodo.mockResolvedValue(null); // Todo not found

            await syncService.processOfflineQueue();

            expect(mockDb.markSyncOperationComplete).toHaveBeenCalledWith(
                1, 
                false, 
                expect.any(String)
            );
        });
    });

    describe('Full sync', () => {
        test('should perform complete bidirectional sync', async () => {
            // Mock successful GitHub to local sync
            mockGithub.rest.issues.listForRepo.mockResolvedValue({ data: [] });
            
            // Mock successful local to GitHub sync
            mockTodoReader.getAllTodos.mockResolvedValue([]);
            
            // Mock empty queue
            mockDb.getNextSyncOperations.mockResolvedValue([]);

            const startTime = Date.now();
            await syncService.performFullSync();
            const endTime = Date.now();

            expect(syncService.syncStats.totalSyncs).toBe(1);
            expect(syncService.syncStats.successfulSyncs).toBe(1);
            expect(syncService.syncStats.lastSyncTime).toBeInstanceOf(Date);
            expect(syncService.syncStats.lastSyncDuration).toBeGreaterThan(0);
            expect(syncService.syncStats.lastSyncDuration).toBeLessThan(endTime - startTime + 100);

            expect(mockDb.recordSyncStats).toHaveBeenCalledWith(
                'full_sync',
                expect.any(Number),
                expect.any(Number),
                expect.any(Number)
            );
        });

        test('should handle sync errors', async () => {
            mockGithub.rest.issues.listForRepo.mockRejectedValue(new Error('GitHub API error'));

            await expect(syncService.performFullSync()).rejects.toThrow('GitHub API error');

            expect(syncService.syncStats.failedSyncs).toBe(1);
        });
    });

    describe('Utility methods', () => {
        test('should generate correct issue body', () => {
            const todo = {
                content: 'Test todo',
                status: 'in_progress',
                activeForm: 'Testing functionality',
                sessionId: 'session-123',
                projectPath: '/test/project'
            };

            const body = syncService.generateIssueBody(todo);

            expect(body).toContain('**Todo:** Test todo');
            expect(body).toContain('**Status:** in_progress');
            expect(body).toContain('**Active Form:** Testing functionality');
            expect(body).toContain('**Session:** session-123');
            expect(body).toContain('**Project:** /test/project');
        });

        test('should map status to GitHub state correctly', () => {
            expect(syncService.mapStatusToGitHubState('completed')).toBe('closed');
            expect(syncService.mapStatusToGitHubState('pending')).toBe('open');
            expect(syncService.mapStatusToGitHubState('in_progress')).toBe('open');
        });

        test('should map GitHub state to status correctly', () => {
            expect(syncService.mapGitHubStateToStatus('closed')).toBe('completed');
            expect(syncService.mapGitHubStateToStatus('open')).toBe('pending');
        });

        test('should track rate limits correctly', () => {
            const initialRequests = syncService.rateLimiter.requestsThisHour;
            
            syncService.incrementRateLimit();
            
            expect(syncService.rateLimiter.requestsThisHour).toBe(initialRequests + 1);
            
            const canMakeRequest = syncService.canMakeRequest();
            expect(typeof canMakeRequest).toBe('boolean');
        });

        test('should identify temporary errors correctly', () => {
            expect(syncService.isTemporaryError({ status: 429 })).toBe(true); // Rate limit
            expect(syncService.isTemporaryError({ status: 503 })).toBe(true); // Service unavailable
            expect(syncService.isTemporaryError({ status: 404 })).toBe(false); // Not found
            expect(syncService.isTemporaryError({ status: 400 })).toBe(false); // Bad request
        });
    });

    describe('Statistics and monitoring', () => {
        test('should return current stats', () => {
            const stats = syncService.getStats();

            expect(stats).toMatchObject({
                totalSyncs: expect.any(Number),
                successfulSyncs: expect.any(Number),
                failedSyncs: expect.any(Number),
                rateLimiter: expect.objectContaining({
                    requestsThisHour: expect.any(Number),
                    hourlyLimit: expect.any(Number),
                    remainingRequests: expect.any(Number)
                }),
                isRunning: expect.any(Boolean),
                isSyncing: expect.any(Boolean)
            });
        });

        test('should get detailed stats from database', async () => {
            const mockDbStats = [
                {
                    operation_type: 'full_sync',
                    operation_count: '5',
                    avg_duration: '2500.0',
                    total_todos_processed: '50',
                    total_errors: '2'
                }
            ];

            mockDb.getSyncStats.mockResolvedValue(mockDbStats);

            const stats = await syncService.getDetailedStats(24);

            expect(stats).toMatchObject({
                runtime: expect.any(Object),
                database: mockDbStats
            });

            expect(mockDb.getSyncStats).toHaveBeenCalledWith(24);
        });
    });
});