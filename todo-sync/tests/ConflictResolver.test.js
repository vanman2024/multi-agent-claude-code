import { ConflictResolver } from '../src/services/ConflictResolver.js';
import { jest } from '@jest/globals';

describe('ConflictResolver', () => {
    let resolver;

    beforeEach(() => {
        resolver = new ConflictResolver();
    });

    describe('Conflict detection', () => {
        test('should detect no conflict when data is identical', async () => {
            const localTodo = {
                content: 'Same content',
                status: 'pending',
                updatedAt: '2023-01-01T12:00:00Z'
            };

            const githubData = {
                githubTitle: 'Same content',
                status: 'pending',
                githubLastModified: '2023-01-01T12:00:00Z'
            };

            const result = await resolver.resolve(localTodo, githubData);

            expect(result.canResolve).toBe(true);
            expect(result.strategy).toBe('no_conflict');
        });

        test('should detect content conflict', () => {
            const localTodo = {
                content: 'Local content',
                status: 'pending'
            };

            const githubData = {
                githubTitle: 'GitHub content',
                status: 'pending'
            };

            const conflict = resolver.detectContentConflict(localTodo, githubData);

            expect(conflict).toBeDefined();
            expect(conflict.type).toBe('content_difference');
            expect(conflict.severity).toBeDefined();
        });

        test('should detect minor content formatting differences', () => {
            const localTodo = {
                content: 'Test Todo!'
            };

            const githubData = {
                githubTitle: 'test todo'
            };

            const conflict = resolver.detectContentConflict(localTodo, githubData);

            expect(conflict.type).toBe('content_format');
            expect(conflict.severity).toBe('minor');
        });

        test('should detect status conflict', () => {
            const localTodo = {
                status: 'pending'
            };

            const githubData = {
                status: 'completed'
            };

            const conflict = resolver.detectStatusConflict(localTodo, githubData);

            expect(conflict).toBeDefined();
            expect(conflict.type).toBe('status_difference');
            expect(conflict.localValue).toBe('pending');
            expect(conflict.githubValue).toBe('completed');
        });

        test('should detect timestamp conflict', () => {
            const localTodo = {
                updatedAt: '2023-01-01T12:00:00Z'
            };

            const githubData = {
                githubLastModified: '2023-01-02T12:00:00Z' // 24 hours later
            };

            const conflict = resolver.detectTimestampConflict(localTodo, githubData);

            expect(conflict).toBeDefined();
            expect(conflict.type).toBe('timestamp_difference');
            expect(conflict.hoursDifference).toBeGreaterThan(20);
        });
    });

    describe('Content similarity calculation', () => {
        test('should calculate high similarity for nearly identical strings', () => {
            const str1 = 'Fix authentication bug';
            const str2 = 'Fix authentication bug in login';

            const similarity = resolver.calculateContentSimilarity(str1, str2);

            expect(similarity).toBeGreaterThan(0.8);
        });

        test('should calculate low similarity for very different strings', () => {
            const str1 = 'Fix authentication bug';
            const str2 = 'Create user dashboard';

            const similarity = resolver.calculateContentSimilarity(str1, str2);

            expect(similarity).toBeLessThan(0.3);
        });

        test('should return 1.0 for identical strings', () => {
            const str1 = 'Identical string';
            const str2 = 'Identical string';

            const similarity = resolver.calculateContentSimilarity(str1, str2);

            expect(similarity).toBe(1.0);
        });
    });

    describe('Resolution strategies', () => {
        test('should apply github_wins strategy', async () => {
            const localTodo = {
                id: 1,
                content: 'Local content',
                status: 'pending'
            };

            const githubData = {
                githubTitle: 'GitHub content',
                status: 'completed',
                githubState: 'closed'
            };

            const resolved = await resolver.githubWinsStrategy(localTodo, githubData, {});

            expect(resolved.content).toBe('GitHub content');
            expect(resolved.status).toBe('completed');
            expect(resolved.githubState).toBe('closed');
            expect(resolved.needsGithubSync).toBe(false);
        });

        test('should apply local_wins strategy', async () => {
            const localTodo = {
                id: 1,
                content: 'Local content',
                status: 'in_progress'
            };

            const githubData = {
                githubTitle: 'GitHub content',
                status: 'pending'
            };

            const resolved = await resolver.localWinsStrategy(localTodo, githubData, {});

            expect(resolved.content).toBe('Local content');
            expect(resolved.status).toBe('in_progress');
            expect(resolved.needsGithubSync).toBe(true);
        });

        test('should apply timestamp strategy with newer GitHub data', async () => {
            const localTodo = {
                id: 1,
                content: 'Local content',
                updatedAt: '2023-01-01T12:00:00Z'
            };

            const githubData = {
                githubTitle: 'GitHub content',
                githubLastModified: '2023-01-01T13:00:00Z' // 1 hour later
            };

            const resolved = await resolver.timestampStrategy(localTodo, githubData, {});

            // Should resolve to GitHub version since it's newer
            expect(resolved.content).toBe('GitHub content');
            expect(resolved.needsGithubSync).toBe(false);
        });

        test('should apply timestamp strategy with newer local data', async () => {
            const localTodo = {
                id: 1,
                content: 'Local content',
                updatedAt: '2023-01-01T14:00:00Z'
            };

            const githubData = {
                githubTitle: 'GitHub content',
                githubLastModified: '2023-01-01T13:00:00Z' // 1 hour earlier
            };

            const resolved = await resolver.timestampStrategy(localTodo, githubData, {});

            // Should resolve to local version since it's newer
            expect(resolved.content).toBe('Local content');
            expect(resolved.needsGithubSync).toBe(true);
        });

        test('should apply status_priority strategy', async () => {
            const localTodo = {
                id: 1,
                status: 'completed'
            };

            const githubData = {
                status: 'pending'
            };

            const resolved = await resolver.statusPriorityStrategy(localTodo, githubData, {});

            // Completed has higher priority than pending
            expect(resolved.status).toBe('completed');
            expect(resolved.needsGithubSync).toBe(true);
        });

        test('should apply content_length strategy', async () => {
            const localTodo = {
                id: 1,
                content: 'Short'
            };

            const githubData = {
                githubTitle: 'Much longer and more detailed description'
            };

            const resolved = await resolver.contentLengthStrategy(localTodo, githubData, {});

            // GitHub content is longer, so it should win
            expect(resolved.content).toBe('Much longer and more detailed description');
            expect(resolved.needsGithubSync).toBe(false);
        });

        test('should apply merged strategy for complex conflicts', async () => {
            const localTodo = {
                id: 1,
                content: 'Short local content',
                status: 'completed',
                updatedAt: '2023-01-01T14:00:00Z'
            };

            const githubData = {
                githubTitle: 'Much longer GitHub content with more details',
                status: 'pending',
                githubState: 'open',
                githubLastModified: '2023-01-01T13:00:00Z'
            };

            const conflict = {
                conflicts: [
                    { type: 'content_difference' },
                    { type: 'status_difference' }
                ]
            };

            const resolved = await resolver.mergedStrategy(localTodo, githubData, conflict);

            // Should use longer content and advanced status
            expect(resolved.content).toBe('Much longer GitHub content with more details');
            expect(resolved.status).toBe('completed'); // More advanced status
            expect(resolved.githubState).toBe('open'); // Always update GitHub metadata
        });
    });

    describe('Automatic strategy selection', () => {
        test('should select merged strategy for minor conflicts', async () => {
            const localTodo = {
                content: 'Test content',
                status: 'pending'
            };

            const githubData = {
                githubTitle: 'test content', // Minor case difference
                status: 'pending'
            };

            const result = await resolver.resolve(localTodo, githubData, 'auto');

            expect(result.strategy).toBe('merged');
        });

        test('should select status_priority for status conflicts', async () => {
            const localTodo = {
                content: 'Same content',
                status: 'completed'
            };

            const githubData = {
                githubTitle: 'Same content',
                status: 'pending'
            };

            const result = await resolver.resolve(localTodo, githubData, 'auto');

            expect(result.strategy).toBe('status_priority');
        });

        test('should select timestamp for major content differences', async () => {
            const localTodo = {
                content: 'Completely different local content',
                status: 'pending',
                updatedAt: '2023-01-01T14:00:00Z'
            };

            const githubData = {
                githubTitle: 'Totally unrelated GitHub content',
                status: 'pending',
                githubLastModified: '2023-01-01T13:00:00Z'
            };

            const result = await resolver.resolve(localTodo, githubData, 'auto');

            expect(result.strategy).toBe('timestamp');
        });
    });

    describe('Utility functions', () => {
        test('should normalize content correctly', () => {
            const content = 'Test Content! With... Punctuation?';
            const normalized = resolver.normalizeContent(content);

            expect(normalized).toBe('test content with punctuation');
        });

        test('should calculate Levenshtein distance correctly', () => {
            expect(resolver.levenshteinDistance('kitten', 'sitting')).toBe(3);
            expect(resolver.levenshteinDistance('hello', 'hello')).toBe(0);
            expect(resolver.levenshteinDistance('', 'test')).toBe(4);
        });

        test('should get severity level correctly', () => {
            expect(resolver.getSeverityLevel('minor')).toBe(1);
            expect(resolver.getSeverityLevel('moderate')).toBe(2);
            expect(resolver.getSeverityLevel('major')).toBe(3);
            expect(resolver.getSeverityLevel('critical')).toBe(4);
        });

        test('should categorize conflicts correctly', () => {
            const contentConflicts = [{ type: 'content_difference' }];
            const statusConflicts = [{ type: 'status_difference' }];
            const complexConflicts = [
                { type: 'content_difference' },
                { type: 'status_difference' }
            ];

            expect(resolver.categorizeConflict(contentConflicts)).toBe('content');
            expect(resolver.categorizeConflict(statusConflicts)).toBe('status');
            expect(resolver.categorizeConflict(complexConflicts)).toBe('complex');
        });

        test('should calculate complexity correctly', () => {
            const conflicts = [
                { severity: 'minor' },
                { severity: 'major' },
                { severity: 'moderate' }
            ];

            const complexity = resolver.calculateComplexity(conflicts);

            expect(complexity).toBe(1 + 5 + 3); // 9
        });

        test('should select advanced status correctly', () => {
            expect(resolver.selectAdvancedStatus('pending', 'completed')).toBe('completed');
            expect(resolver.selectAdvancedStatus('completed', 'pending')).toBe('completed');
            expect(resolver.selectAdvancedStatus('in_progress', 'pending')).toBe('in_progress');
            expect(resolver.selectAdvancedStatus('pending', 'in_progress')).toBe('in_progress');
        });
    });

    describe('Error handling', () => {
        test('should handle resolution errors gracefully', async () => {
            // Mock an error in strategy execution
            resolver.resolutionStrategies.timestamp = jest.fn().mockRejectedValue(new Error('Strategy error'));

            const localTodo = { content: 'test' };
            const githubData = { githubTitle: 'different' };

            const result = await resolver.resolve(localTodo, githubData, 'timestamp');

            expect(result.canResolve).toBe(false);
            expect(result.strategy).toBe('manual_required');
            expect(result.conflict.error).toBeDefined();
        });
    });

    describe('Statistics and monitoring', () => {
        test('should return resolution stats', () => {
            const stats = resolver.getResolutionStats();

            expect(stats).toMatchObject({
                availableStrategies: expect.any(Array),
                conflictDetectors: expect.any(Number)
            });

            expect(stats.availableStrategies).toContain('github_wins');
            expect(stats.availableStrategies).toContain('local_wins');
            expect(stats.availableStrategies).toContain('merged');
            expect(stats.conflictDetectors).toBeGreaterThan(0);
        });
    });
});