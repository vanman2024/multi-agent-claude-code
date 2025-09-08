#!/usr/bin/env node

/**
 * Basic Usage Example for TodoWrite-GitHub Sync Service
 * 
 * This example demonstrates how to use the sync service programmatically
 */

import dotenv from 'dotenv';
import { Database } from '../src/database/Database.js';
import { SyncService } from '../src/services/SyncService.js';
import { logger } from '../src/utils/logger.js';

dotenv.config();

async function basicExample() {
    logger.info('Starting TodoWrite-GitHub Sync Service example...');
    
    // Initialize components
    const db = new Database('./data/example.db');
    await db.initialize();
    
    const syncService = new SyncService(db);
    
    // Example: Create a local todo
    const todoId = await db.createTodo({
        content: 'Example todo from API usage',
        status: 'pending',
        activeForm: 'Creating example todo',
        sessionId: 'example-session-' + Date.now(),
        projectPath: '/example/project',
        needsGithubSync: true
    });
    
    logger.info(`Created todo with ID: ${todoId}`);
    
    // Example: Sync to GitHub (requires valid GitHub token)
    if (process.env.GITHUB_TOKEN) {
        try {
            const todo = await db.getTodo(todoId);
            await syncService.syncTodoToGitHub(todo);
            logger.info('Successfully synced todo to GitHub');
            
            // Get updated todo with GitHub data
            const updatedTodo = await db.getTodo(todoId);
            logger.info(`Todo now linked to GitHub issue #${updatedTodo.githubIssueNumber}`);
            
        } catch (error) {
            logger.error('Failed to sync to GitHub:', error.message);
        }
    } else {
        logger.warn('No GitHub token provided, skipping GitHub sync');
    }
    
    // Example: Perform a full sync
    try {
        logger.info('Performing full sync...');
        await syncService.performFullSync();
        logger.info('Full sync completed');
    } catch (error) {
        logger.error('Full sync failed:', error.message);
    }
    
    // Example: Get sync statistics
    const stats = syncService.getStats();
    logger.info('Sync statistics:', {
        totalSyncs: stats.totalSyncs,
        successfulSyncs: stats.successfulSyncs,
        failedSyncs: stats.failedSyncs,
        lastSyncTime: stats.lastSyncTime
    });
    
    // Cleanup
    await db.close();
    logger.info('Example completed');
}

async function conflictExample() {
    logger.info('Starting conflict resolution example...');
    
    const db = new Database('./data/conflict-example.db');
    await db.initialize();
    
    // Create a todo with potential for conflict
    const todoId = await db.createTodo({
        content: 'Todo that might conflict',
        status: 'pending',
        updatedAt: '2023-01-01T10:00:00Z'
    });
    
    // Simulate a conflict by updating the todo locally
    await db.updateTodo(todoId, {
        content: 'Locally updated todo',
        status: 'in_progress'
    });
    
    // Simulate GitHub data that conflicts
    const githubData = {
        githubTitle: 'GitHub updated todo',
        status: 'completed',
        githubLastModified: '2023-01-01T11:00:00Z'
    };
    
    const syncService = new SyncService(db);
    const localTodo = await db.getTodo(todoId);
    
    // Handle the conflict
    const resolution = await syncService.conflictResolver.resolve(localTodo, githubData);
    
    logger.info('Conflict resolution result:', {
        canResolve: resolution.canResolve,
        strategy: resolution.strategy,
        resolvedContent: resolution.resolvedData?.content
    });
    
    await db.close();
    logger.info('Conflict example completed');
}

async function performanceExample() {
    logger.info('Starting performance optimization example...');
    
    const db = new Database('./data/performance-example.db');
    await db.initialize();
    
    // Create many todos to test performance
    const todos = [];
    for (let i = 0; i < 100; i++) {
        const todoId = await db.createTodo({
            content: `Performance test todo ${i + 1}`,
            status: i % 3 === 0 ? 'completed' : 'pending',
            sessionId: `perf-session-${Math.floor(i / 10)}`,
            projectPath: `/test/project-${Math.floor(i / 20)}`
        });
        todos.push(await db.getTodo(todoId));
    }
    
    logger.info(`Created ${todos.length} test todos`);
    
    const syncService = new SyncService(db);
    
    // Test performance optimization
    const startTime = Date.now();
    const result = await syncService.performanceOptimizer.performOptimizedSync(
        todos, 
        'bidirectional'
    );
    const duration = Date.now() - startTime;
    
    logger.info('Performance test results:', {
        todosProcessed: result.processed,
        errors: result.errors,
        totalDuration: duration,
        throughput: Math.round((result.processed / duration) * 1000 * 100) / 100 + ' todos/sec'
    });
    
    // Get performance report
    const report = syncService.performanceOptimizer.getPerformanceReport();
    logger.info('Performance report:', report);
    
    await db.close();
    logger.info('Performance example completed');
}

// Run examples based on command line argument
const example = process.argv[2] || 'basic';

switch (example) {
    case 'basic':
        basicExample().catch(error => {
            logger.error('Basic example failed:', error);
            process.exit(1);
        });
        break;
        
    case 'conflict':
        conflictExample().catch(error => {
            logger.error('Conflict example failed:', error);
            process.exit(1);
        });
        break;
        
    case 'performance':
        performanceExample().catch(error => {
            logger.error('Performance example failed:', error);
            process.exit(1);
        });
        break;
        
    default:
        console.log('Usage: node examples/basic-usage.js [basic|conflict|performance]');
        process.exit(1);
}