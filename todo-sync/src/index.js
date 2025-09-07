#!/usr/bin/env node

import dotenv from 'dotenv';
import { SyncService } from './services/SyncService.js';
import { WebhookServer } from './services/WebhookServer.js';
import { Database } from './database/Database.js';
import { logger } from './utils/logger.js';

dotenv.config();

class TodoSyncApp {
    constructor() {
        this.db = new Database(process.env.DB_PATH || './data/sync.db');
        this.syncService = new SyncService(this.db);
        this.webhookServer = new WebhookServer(this.syncService);
        this.isRunning = false;
    }

    async start() {
        try {
            logger.info('Starting Todo-GitHub Sync Service...');
            
            // Initialize database
            await this.db.initialize();
            logger.info('Database initialized');

            // Start webhook server
            await this.webhookServer.start();
            logger.info(`Webhook server started on port ${process.env.WEBHOOK_PORT || 3001}`);

            // Start sync service
            await this.syncService.start();
            logger.info('Sync service started');

            // Perform initial sync
            logger.info('Performing initial sync...');
            await this.syncService.performFullSync();
            logger.info('Initial sync completed');

            this.isRunning = true;
            this.setupGracefulShutdown();
            
            logger.info('Todo-GitHub Sync Service is running');
        } catch (error) {
            logger.error('Failed to start sync service:', error);
            process.exit(1);
        }
    }

    async stop() {
        if (!this.isRunning) return;
        
        logger.info('Shutting down Todo-GitHub Sync Service...');
        
        await this.syncService.stop();
        await this.webhookServer.stop();
        await this.db.close();
        
        this.isRunning = false;
        logger.info('Service shut down complete');
    }

    setupGracefulShutdown() {
        const shutdown = async (signal) => {
            logger.info(`Received ${signal}, shutting down gracefully...`);
            await this.stop();
            process.exit(0);
        };

        process.on('SIGTERM', () => shutdown('SIGTERM'));
        process.on('SIGINT', () => shutdown('SIGINT'));
        
        process.on('uncaughtException', (error) => {
            logger.error('Uncaught Exception:', error);
            shutdown('UNCAUGHT_EXCEPTION');
        });
        
        process.on('unhandledRejection', (reason, promise) => {
            logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
            shutdown('UNHANDLED_REJECTION');
        });
    }
}

// Start the application
const app = new TodoSyncApp();
app.start().catch(error => {
    logger.error('Failed to start application:', error);
    process.exit(1);
});