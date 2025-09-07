import fs from 'fs/promises';
import path from 'path';

class Logger {
    constructor() {
        this.logLevels = {
            error: 0,
            warn: 1,
            info: 2,
            debug: 3
        };
        
        this.currentLevel = this.logLevels[process.env.LOG_LEVEL] || this.logLevels.info;
        this.logDir = process.env.LOG_DIR || './logs';
        this.logToFile = process.env.LOG_TO_FILE === 'true';
        this.maxLogFiles = parseInt(process.env.MAX_LOG_FILES) || 7;
        this.maxLogSize = parseInt(process.env.MAX_LOG_SIZE) || 10 * 1024 * 1024; // 10MB
        
        if (this.logToFile) {
            this.initializeLogDirectory();
        }
    }

    async initializeLogDirectory() {
        try {
            await fs.mkdir(this.logDir, { recursive: true });
        } catch (error) {
            console.error('Failed to create log directory:', error);
            this.logToFile = false;
        }
    }

    formatMessage(level, message, meta = null) {
        const timestamp = new Date().toISOString();
        const levelStr = level.toUpperCase().padEnd(5);
        
        let formatted = `[${timestamp}] ${levelStr} ${message}`;
        
        if (meta) {
            if (typeof meta === 'object') {
                formatted += '\n' + JSON.stringify(meta, null, 2);
            } else {
                formatted += ` ${meta}`;
            }
        }
        
        return formatted;
    }

    async writeToFile(level, message, meta) {
        if (!this.logToFile) return;
        
        try {
            const logFile = path.join(this.logDir, `sync-service.log`);
            const formatted = this.formatMessage(level, message, meta) + '\n';
            
            await fs.appendFile(logFile, formatted);
            
            // Check if log rotation is needed
            await this.rotateLogsIfNeeded();
        } catch (error) {
            console.error('Failed to write to log file:', error);
        }
    }

    async rotateLogsIfNeeded() {
        try {
            const logFile = path.join(this.logDir, 'sync-service.log');
            const stats = await fs.stat(logFile);
            
            if (stats.size > this.maxLogSize) {
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                const rotatedFile = path.join(this.logDir, `sync-service-${timestamp}.log`);
                
                await fs.rename(logFile, rotatedFile);
                
                // Clean up old log files
                await this.cleanupOldLogs();
            }
        } catch (error) {
            // Log file might not exist yet, which is okay
            if (error.code !== 'ENOENT') {
                console.error('Failed to rotate logs:', error);
            }
        }
    }

    async cleanupOldLogs() {
        try {
            const files = await fs.readdir(this.logDir);
            const logFiles = files
                .filter(file => file.startsWith('sync-service-') && file.endsWith('.log'))
                .map(file => ({
                    name: file,
                    path: path.join(this.logDir, file)
                }))
                .sort((a, b) => b.name.localeCompare(a.name)); // Sort by name (timestamp) descending
            
            // Remove old files beyond the limit
            if (logFiles.length > this.maxLogFiles) {
                const filesToDelete = logFiles.slice(this.maxLogFiles);
                
                for (const file of filesToDelete) {
                    await fs.unlink(file.path);
                }
            }
        } catch (error) {
            console.error('Failed to cleanup old logs:', error);
        }
    }

    shouldLog(level) {
        return this.logLevels[level] <= this.currentLevel;
    }

    log(level, message, meta = null) {
        if (!this.shouldLog(level)) return;
        
        const formatted = this.formatMessage(level, message, meta);
        
        // Always log to console
        if (level === 'error') {
            console.error(formatted);
        } else if (level === 'warn') {
            console.warn(formatted);
        } else {
            console.log(formatted);
        }
        
        // Also log to file if enabled
        this.writeToFile(level, message, meta);
    }

    error(message, meta = null) {
        this.log('error', message, meta);
    }

    warn(message, meta = null) {
        this.log('warn', message, meta);
    }

    info(message, meta = null) {
        this.log('info', message, meta);
    }

    debug(message, meta = null) {
        this.log('debug', message, meta);
    }

    // Convenience methods for structured logging
    logSync(operation, status, stats = {}) {
        this.info(`Sync ${operation} ${status}`, {
            operation,
            status,
            ...stats,
            timestamp: new Date().toISOString()
        });
    }

    logConflict(todoId, conflictType, resolution = null) {
        this.warn(`Conflict detected for todo ${todoId}`, {
            todoId,
            conflictType,
            resolution,
            timestamp: new Date().toISOString()
        });
    }

    logPerformance(operation, durationMs, details = {}) {
        this.info(`Performance: ${operation} completed in ${durationMs}ms`, {
            operation,
            duration: durationMs,
            ...details,
            timestamp: new Date().toISOString()
        });
    }

    logRateLimit(service, remaining, resetTime) {
        this.warn(`Rate limit warning for ${service}`, {
            service,
            remaining,
            resetTime,
            timestamp: new Date().toISOString()
        });
    }

    // Log aggregation for debugging
    async getRecentLogs(lines = 100) {
        if (!this.logToFile) {
            return 'File logging is disabled';
        }

        try {
            const logFile = path.join(this.logDir, 'sync-service.log');
            const content = await fs.readFile(logFile, 'utf8');
            const logLines = content.split('\n').filter(line => line.trim());
            
            return logLines.slice(-lines).join('\n');
        } catch (error) {
            return `Failed to read logs: ${error.message}`;
        }
    }

    async getLogStats() {
        if (!this.logToFile) {
            return { fileLogging: false };
        }

        try {
            const files = await fs.readdir(this.logDir);
            const logFiles = files.filter(file => 
                file.startsWith('sync-service') && file.endsWith('.log')
            );

            let totalSize = 0;
            for (const file of logFiles) {
                const stats = await fs.stat(path.join(this.logDir, file));
                totalSize += stats.size;
            }

            return {
                fileLogging: true,
                logDirectory: this.logDir,
                logFiles: logFiles.length,
                totalSize: totalSize,
                currentLevel: Object.keys(this.logLevels)[this.currentLevel]
            };
        } catch (error) {
            return {
                fileLogging: true,
                error: error.message
            };
        }
    }
}

// Export a singleton instance
export const logger = new Logger();