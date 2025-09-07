import { logger } from '../utils/logger.js';
import { EventEmitter } from 'events';

export class PerformanceOptimizer extends EventEmitter {
    constructor(syncService, database) {
        super();
        this.syncService = syncService;
        this.db = database;
        
        // Performance settings
        this.batchSize = parseInt(process.env.BATCH_SIZE) || 50;
        this.concurrentLimit = parseInt(process.env.CONCURRENT_OPERATIONS) || 10;
        this.cacheTimeout = 300000; // 5 minutes
        
        // Caching
        this.cache = new Map();
        this.cacheStats = {
            hits: 0,
            misses: 0,
            evictions: 0
        };
        
        // Performance tracking
        this.performanceMetrics = {
            syncDurations: [],
            throughput: [],
            errorRates: [],
            cacheHitRates: []
        };
        
        // Batch processing queue
        this.batchQueue = [];
        this.processing = false;
        
        this.startPerformanceMonitoring();
    }

    startPerformanceMonitoring() {
        // Clear old metrics every hour
        setInterval(() => {
            this.performanceMetrics.syncDurations = this.performanceMetrics.syncDurations.slice(-100);
            this.performanceMetrics.throughput = this.performanceMetrics.throughput.slice(-100);
            this.performanceMetrics.errorRates = this.performanceMetrics.errorRates.slice(-100);
            this.performanceMetrics.cacheHitRates = this.performanceMetrics.cacheHitRates.slice(-100);
        }, 3600000); // 1 hour

        // Cache cleanup every 5 minutes
        setInterval(() => {
            this.cleanupCache();
        }, 300000); // 5 minutes
    }

    // Optimized batch sync for large datasets
    async performOptimizedSync(todos, direction = 'bidirectional') {
        const startTime = Date.now();
        let processed = 0;
        let errors = 0;

        try {
            logger.info(`Starting optimized sync for ${todos.length} todos (${direction})`);

            if (todos.length <= this.batchSize) {
                // Small dataset - process normally
                return await this.processStandardSync(todos, direction);
            }

            // Large dataset - use optimized batch processing
            const batches = this.createBatches(todos, this.batchSize);
            const results = await this.processBatchesConcurrently(batches, direction);

            // Aggregate results
            for (const result of results) {
                processed += result.processed;
                errors += result.errors;
            }

            const duration = Date.now() - startTime;
            
            // Record performance metrics
            this.recordPerformanceMetrics(duration, processed, errors);

            logger.info(`Optimized sync completed: ${processed} processed, ${errors} errors in ${duration}ms`);
            
            return { processed, errors, duration };

        } catch (error) {
            logger.error('Optimized sync failed:', error);
            throw error;
        }
    }

    async processStandardSync(todos, direction) {
        let processed = 0;
        let errors = 0;

        for (const todo of todos) {
            try {
                if (direction === 'to_github' || direction === 'bidirectional') {
                    if (todo.needsGithubSync) {
                        await this.syncService.syncTodoToGitHub(todo);
                        processed++;
                    }
                }

                if (direction === 'from_github' || direction === 'bidirectional') {
                    if (todo.githubIssueNumber && todo.needsLocalSync) {
                        await this.syncService.syncGitHubIssueToLocal(todo.githubIssueNumber);
                        processed++;
                    }
                }
            } catch (error) {
                errors++;
                logger.error(`Error syncing todo ${todo.id}:`, error);
            }
        }

        return { processed, errors };
    }

    createBatches(items, batchSize) {
        const batches = [];
        for (let i = 0; i < items.length; i += batchSize) {
            batches.push(items.slice(i, i + batchSize));
        }
        return batches;
    }

    async processBatchesConcurrently(batches, direction) {
        const results = [];
        const activePromises = [];

        for (const batch of batches) {
            // Limit concurrent operations
            if (activePromises.length >= this.concurrentLimit) {
                const result = await Promise.race(activePromises);
                results.push(result.value);
                activePromises.splice(activePromises.indexOf(result.promise), 1);
            }

            const promise = this.processBatch(batch, direction);
            activePromises.push({
                promise: promise,
                value: promise
            });
        }

        // Wait for remaining promises
        const remainingResults = await Promise.all(activePromises.map(p => p.value));
        results.push(...remainingResults);

        return results;
    }

    async processBatch(batch, direction) {
        const startTime = Date.now();
        let processed = 0;
        let errors = 0;

        try {
            // Process batch items with optimizations
            const promises = batch.map(async (todo) => {
                try {
                    // Use cached data where possible
                    const cachedResult = this.getCachedResult(todo);
                    if (cachedResult) {
                        this.cacheStats.hits++;
                        return cachedResult;
                    }

                    this.cacheStats.misses++;

                    let result = null;

                    if (direction === 'to_github' || direction === 'bidirectional') {
                        if (todo.needsGithubSync) {
                            result = await this.syncService.syncTodoToGitHub(todo);
                        }
                    }

                    if (direction === 'from_github' || direction === 'bidirectional') {
                        if (todo.githubIssueNumber && todo.needsLocalSync) {
                            result = await this.syncService.syncGitHubIssueToLocal(todo.githubIssueNumber);
                        }
                    }

                    // Cache successful results
                    if (result) {
                        this.setCachedResult(todo, result);
                    }

                    return { success: true, result };
                } catch (error) {
                    logger.debug(`Batch item error for todo ${todo.id}:`, error.message);
                    return { success: false, error };
                }
            });

            const results = await Promise.all(promises);

            // Count successes and errors
            results.forEach(result => {
                if (result.success) {
                    processed++;
                } else {
                    errors++;
                }
            });

            const duration = Date.now() - startTime;
            
            logger.debug(`Batch processed: ${processed}/${batch.length} successful in ${duration}ms`);

            return { processed, errors, duration };

        } catch (error) {
            logger.error('Batch processing error:', error);
            return { processed: 0, errors: batch.length, duration: Date.now() - startTime };
        }
    }

    // Smart caching system
    getCachedResult(todo) {
        const cacheKey = this.generateCacheKey(todo);
        const cached = this.cache.get(cacheKey);

        if (!cached) return null;

        // Check if cache is expired
        if (Date.now() - cached.timestamp > this.cacheTimeout) {
            this.cache.delete(cacheKey);
            this.cacheStats.evictions++;
            return null;
        }

        // Check if todo has been modified since cache
        if (todo.updatedAt && cached.todoUpdated && 
            new Date(todo.updatedAt) > new Date(cached.todoUpdated)) {
            this.cache.delete(cacheKey);
            this.cacheStats.evictions++;
            return null;
        }

        return cached.result;
    }

    setCachedResult(todo, result) {
        const cacheKey = this.generateCacheKey(todo);
        
        this.cache.set(cacheKey, {
            result: result,
            timestamp: Date.now(),
            todoUpdated: todo.updatedAt
        });

        // Prevent cache from growing too large
        if (this.cache.size > 1000) {
            const oldestKey = this.cache.keys().next().value;
            this.cache.delete(oldestKey);
            this.cacheStats.evictions++;
        }
    }

    generateCacheKey(todo) {
        return `${todo.id}-${todo.lastSyncHash || todo.content}-${todo.githubIssueNumber || 'new'}`;
    }

    cleanupCache() {
        const now = Date.now();
        let cleaned = 0;

        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp > this.cacheTimeout) {
                this.cache.delete(key);
                cleaned++;
            }
        }

        if (cleaned > 0) {
            logger.debug(`Cleaned up ${cleaned} expired cache entries`);
            this.cacheStats.evictions += cleaned;
        }
    }

    // Intelligent sync prioritization
    prioritizeTodos(todos) {
        return todos.sort((a, b) => {
            // Priority factors (higher score = higher priority)
            let scoreA = 0;
            let scoreB = 0;

            // Status priority (completed todos are less urgent)
            const statusPriority = {
                'in_progress': 10,
                'pending': 5,
                'completed': 1
            };
            scoreA += statusPriority[a.status] || 0;
            scoreB += statusPriority[b.status] || 0;

            // Conflict detection priority (conflicts need immediate attention)
            if (a.conflictDetected) scoreA += 20;
            if (b.conflictDetected) scoreB += 20;

            // Sync necessity (items that need syncing are more urgent)
            if (a.needsGithubSync || a.needsLocalSync) scoreA += 15;
            if (b.needsGithubSync || b.needsLocalSync) scoreB += 15;

            // Recency (more recently updated items have higher priority)
            const aTime = new Date(a.updatedAt || a.createdAt).getTime();
            const bTime = new Date(b.updatedAt || b.createdAt).getTime();
            if (aTime > bTime) scoreA += 3;
            else if (bTime > aTime) scoreB += 3;

            return scoreB - scoreA; // Higher score first
        });
    }

    // Adaptive sync intervals based on activity
    calculateOptimalSyncInterval(recentActivity) {
        const baseInterval = 30000; // 30 seconds
        const maxInterval = 300000; // 5 minutes
        const minInterval = 10000; // 10 seconds

        if (!recentActivity || recentActivity.length === 0) {
            return maxInterval; // Low activity, sync less frequently
        }

        // Calculate activity score
        const now = Date.now();
        const recentChanges = recentActivity.filter(
            activity => now - new Date(activity.timestamp).getTime() < 3600000 // Last hour
        );

        const activityScore = recentChanges.length;
        
        if (activityScore > 10) {
            return minInterval; // High activity, sync more frequently
        } else if (activityScore > 5) {
            return baseInterval; // Normal activity
        } else {
            return Math.min(maxInterval, baseInterval * 2); // Low activity
        }
    }

    // Performance metrics recording
    recordPerformanceMetrics(duration, processed, errors) {
        this.performanceMetrics.syncDurations.push({
            timestamp: Date.now(),
            duration: duration
        });

        this.performanceMetrics.throughput.push({
            timestamp: Date.now(),
            itemsPerSecond: processed / (duration / 1000)
        });

        this.performanceMetrics.errorRates.push({
            timestamp: Date.now(),
            errorRate: errors / (processed + errors) || 0
        });

        const cacheHitRate = this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses) || 0;
        this.performanceMetrics.cacheHitRates.push({
            timestamp: Date.now(),
            hitRate: cacheHitRate
        });
    }

    // Database query optimizations
    async optimizeQueries() {
        try {
            // Add database indexes if they don't exist
            await this.db.db.run('CREATE INDEX IF NOT EXISTS idx_todos_updated_at ON todos(updated_at DESC)');
            await this.db.db.run('CREATE INDEX IF NOT EXISTS idx_todos_needs_sync ON todos(needs_github_sync, needs_local_sync) WHERE needs_github_sync = 1 OR needs_local_sync = 1');
            await this.db.db.run('CREATE INDEX IF NOT EXISTS idx_todos_conflict ON todos(conflict_detected) WHERE conflict_detected = 1');
            
            // Analyze tables for better query planning
            await this.db.db.run('ANALYZE todos');
            await this.db.db.run('ANALYZE sync_queue');
            
            logger.info('Database query optimization completed');
        } catch (error) {
            logger.error('Database optimization failed:', error);
        }
    }

    // Memory usage optimization
    optimizeMemoryUsage() {
        // Clear performance metrics if they get too large
        const maxMetrics = 1000;
        
        Object.keys(this.performanceMetrics).forEach(key => {
            if (this.performanceMetrics[key].length > maxMetrics) {
                this.performanceMetrics[key] = this.performanceMetrics[key].slice(-maxMetrics);
            }
        });

        // Force garbage collection if available
        if (global.gc) {
            global.gc();
            logger.debug('Forced garbage collection');
        }
    }

    // Performance reporting
    getPerformanceReport() {
        const recent = Date.now() - 3600000; // Last hour
        
        const recentDurations = this.performanceMetrics.syncDurations
            .filter(m => m.timestamp > recent);
        
        const recentThroughput = this.performanceMetrics.throughput
            .filter(m => m.timestamp > recent);
            
        const recentErrors = this.performanceMetrics.errorRates
            .filter(m => m.timestamp > recent);

        const avgDuration = recentDurations.length > 0 
            ? recentDurations.reduce((sum, m) => sum + m.duration, 0) / recentDurations.length
            : 0;

        const avgThroughput = recentThroughput.length > 0
            ? recentThroughput.reduce((sum, m) => sum + m.itemsPerSecond, 0) / recentThroughput.length
            : 0;

        const avgErrorRate = recentErrors.length > 0
            ? recentErrors.reduce((sum, m) => sum + m.errorRate, 0) / recentErrors.length
            : 0;

        const cacheHitRate = this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses) || 0;

        return {
            performance: {
                averageSyncDuration: Math.round(avgDuration),
                averageThroughput: Math.round(avgThroughput * 100) / 100,
                averageErrorRate: Math.round(avgErrorRate * 10000) / 100, // Percentage
                cacheHitRate: Math.round(cacheHitRate * 10000) / 100 // Percentage
            },
            cache: {
                size: this.cache.size,
                hits: this.cacheStats.hits,
                misses: this.cacheStats.misses,
                evictions: this.cacheStats.evictions,
                hitRate: Math.round(cacheHitRate * 10000) / 100
            },
            configuration: {
                batchSize: this.batchSize,
                concurrentLimit: this.concurrentLimit,
                cacheTimeout: this.cacheTimeout
            },
            memory: {
                heapUsed: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
                heapTotal: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
                external: Math.round(process.memoryUsage().external / 1024 / 1024)
            }
        };
    }

    // Cleanup and shutdown
    cleanup() {
        this.cache.clear();
        this.batchQueue = [];
        this.performanceMetrics = {
            syncDurations: [],
            throughput: [],
            errorRates: [],
            cacheHitRates: []
        };
        
        logger.info('Performance optimizer cleanup completed');
    }
}