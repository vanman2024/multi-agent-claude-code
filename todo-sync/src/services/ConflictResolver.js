import { logger } from '../utils/logger.js';

export class ConflictResolver {
    constructor() {
        this.resolutionStrategies = {
            'github_wins': this.githubWinsStrategy.bind(this),
            'local_wins': this.localWinsStrategy.bind(this),
            'merged': this.mergedStrategy.bind(this),
            'timestamp': this.timestampStrategy.bind(this),
            'status_priority': this.statusPriorityStrategy.bind(this),
            'content_length': this.contentLengthStrategy.bind(this)
        };
        
        this.conflictDetectors = [
            this.detectContentConflict.bind(this),
            this.detectStatusConflict.bind(this),
            this.detectTimestampConflict.bind(this)
        ];
    }

    async resolve(localTodo, githubData, strategy = 'auto') {
        try {
            const conflict = this.analyzeConflict(localTodo, githubData);
            
            if (!conflict.hasConflict) {
                return {
                    canResolve: true,
                    strategy: 'no_conflict',
                    resolvedData: githubData,
                    conflict: null
                };
            }

            logger.info(`Resolving conflict for todo ${localTodo.id}:`, {
                conflictType: conflict.type,
                conflictSeverity: conflict.severity,
                strategy: strategy
            });

            let resolvedData;
            let usedStrategy = strategy;

            if (strategy === 'auto') {
                // Determine best automatic resolution strategy
                usedStrategy = this.determineOptimalStrategy(conflict, localTodo, githubData);
            }

            // Apply the resolution strategy
            if (this.resolutionStrategies[usedStrategy]) {
                resolvedData = await this.resolutionStrategies[usedStrategy](localTodo, githubData, conflict);
            } else {
                logger.warn(`Unknown resolution strategy: ${usedStrategy}, falling back to timestamp`);
                resolvedData = await this.resolutionStrategies['timestamp'](localTodo, githubData, conflict);
                usedStrategy = 'timestamp';
            }

            return {
                canResolve: conflict.severity !== 'critical',
                strategy: usedStrategy,
                resolvedData: resolvedData,
                conflict: conflict
            };

        } catch (error) {
            logger.error('Error during conflict resolution:', error);
            
            return {
                canResolve: false,
                strategy: 'manual_required',
                resolvedData: null,
                conflict: { error: error.message }
            };
        }
    }

    analyzeConflict(localTodo, githubData) {
        const conflicts = [];
        let maxSeverity = 'minor';

        // Run all conflict detectors
        for (const detector of this.conflictDetectors) {
            const conflict = detector(localTodo, githubData);
            if (conflict) {
                conflicts.push(conflict);
                if (this.getSeverityLevel(conflict.severity) > this.getSeverityLevel(maxSeverity)) {
                    maxSeverity = conflict.severity;
                }
            }
        }

        return {
            hasConflict: conflicts.length > 0,
            conflicts: conflicts,
            severity: maxSeverity,
            type: this.categorizeConflict(conflicts),
            resolutionComplexity: this.calculateComplexity(conflicts)
        };
    }

    detectContentConflict(localTodo, githubData) {
        const localContent = localTodo.content?.trim() || '';
        const githubContent = githubData.content?.trim() || githubData.githubTitle?.trim() || '';
        
        if (localContent === githubContent) {
            return null; // No conflict
        }

        // Check if it's a minor difference (like case or punctuation)
        const normalizedLocal = this.normalizeContent(localContent);
        const normalizedGithub = this.normalizeContent(githubContent);
        
        if (normalizedLocal === normalizedGithub) {
            return {
                type: 'content_format',
                severity: 'minor',
                description: 'Minor formatting differences in content',
                localValue: localContent,
                githubValue: githubContent
            };
        }

        // Check content similarity to determine severity
        const similarity = this.calculateContentSimilarity(localContent, githubContent);
        
        let severity;
        if (similarity > 0.8) {
            severity = 'minor';
        } else if (similarity > 0.5) {
            severity = 'moderate';
        } else {
            severity = 'major';
        }

        return {
            type: 'content_difference',
            severity: severity,
            description: `Content differs significantly (${Math.round(similarity * 100)}% similar)`,
            localValue: localContent,
            githubValue: githubContent,
            similarity: similarity
        };
    }

    detectStatusConflict(localTodo, githubData) {
        const localStatus = localTodo.status;
        const githubStatus = githubData.status;
        
        if (localStatus === githubStatus) {
            return null; // No conflict
        }

        // Determine severity based on status transition
        const severity = this.getStatusConflictSeverity(localStatus, githubStatus);
        
        return {
            type: 'status_difference',
            severity: severity,
            description: `Status differs: local="${localStatus}" vs github="${githubStatus}"`,
            localValue: localStatus,
            githubValue: githubStatus
        };
    }

    detectTimestampConflict(localTodo, githubData) {
        const localTimestamp = new Date(localTodo.updatedAt || localTodo.createdAt);
        const githubTimestamp = new Date(githubData.githubLastModified || githubData.updatedAt);
        
        const timeDiff = Math.abs(localTimestamp.getTime() - githubTimestamp.getTime());
        const hoursDiff = timeDiff / (1000 * 60 * 60);
        
        // Only flag as conflict if there's a significant time difference
        if (hoursDiff < 1) {
            return null; // No conflict if within 1 hour
        }

        let severity;
        if (hoursDiff < 24) {
            severity = 'minor';
        } else if (hoursDiff < 168) { // 1 week
            severity = 'moderate';
        } else {
            severity = 'major';
        }

        return {
            type: 'timestamp_difference',
            severity: severity,
            description: `Significant time difference: ${hoursDiff.toFixed(1)} hours`,
            localValue: localTimestamp.toISOString(),
            githubValue: githubTimestamp.toISOString(),
            hoursDifference: hoursDiff
        };
    }

    // Resolution strategies
    async githubWinsStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying github_wins strategy for todo ${localTodo.id}`);
        
        return {
            content: githubData.githubTitle || githubData.content,
            status: githubData.status,
            githubState: githubData.githubState,
            githubTitle: githubData.githubTitle,
            githubBody: githubData.githubBody,
            githubLastModified: githubData.githubLastModified,
            needsLocalSync: false,
            needsGithubSync: false
        };
    }

    async localWinsStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying local_wins strategy for todo ${localTodo.id}`);
        
        return {
            ...localTodo,
            needsLocalSync: false,
            needsGithubSync: true // Will sync local data back to GitHub
        };
    }

    async mergedStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying merged strategy for todo ${localTodo.id}`);
        
        const merged = { ...localTodo };
        
        // Merge based on conflict analysis
        for (const conf of conflict.conflicts) {
            switch (conf.type) {
                case 'content_difference':
                    // Use the longer content (likely more detailed)
                    if (githubData.githubTitle && githubData.githubTitle.length > localTodo.content.length) {
                        merged.content = githubData.githubTitle;
                    }
                    break;
                    
                case 'status_difference':
                    // Use the more "advanced" status
                    merged.status = this.selectAdvancedStatus(localTodo.status, githubData.status);
                    break;
                    
                case 'timestamp_difference':
                    // Keep the more recent update
                    const localTime = new Date(localTodo.updatedAt || localTodo.createdAt);
                    const githubTime = new Date(githubData.githubLastModified || githubData.updatedAt);
                    
                    if (githubTime > localTime) {
                        merged.updatedAt = githubData.githubLastModified || githubData.updatedAt;
                    }
                    break;
            }
        }
        
        // Always update GitHub sync data
        merged.githubState = githubData.githubState;
        merged.githubTitle = githubData.githubTitle;
        merged.githubBody = githubData.githubBody;
        merged.githubLastModified = githubData.githubLastModified;
        merged.needsLocalSync = false;
        merged.needsGithubSync = false;
        
        return merged;
    }

    async timestampStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying timestamp strategy for todo ${localTodo.id}`);
        
        const localTime = new Date(localTodo.updatedAt || localTodo.createdAt);
        const githubTime = new Date(githubData.githubLastModified || githubData.updatedAt);
        
        // Use the more recently updated data
        if (githubTime > localTime) {
            return this.githubWinsStrategy(localTodo, githubData, conflict);
        } else {
            return this.localWinsStrategy(localTodo, githubData, conflict);
        }
    }

    async statusPriorityStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying status_priority strategy for todo ${localTodo.id}`);
        
        const statusPriority = {
            'completed': 3,
            'in_progress': 2,
            'pending': 1
        };
        
        const localPriority = statusPriority[localTodo.status] || 0;
        const githubPriority = statusPriority[githubData.status] || 0;
        
        // Use the status with higher priority, or fall back to timestamp
        if (localPriority > githubPriority) {
            return this.localWinsStrategy(localTodo, githubData, conflict);
        } else if (githubPriority > localPriority) {
            return this.githubWinsStrategy(localTodo, githubData, conflict);
        } else {
            return this.timestampStrategy(localTodo, githubData, conflict);
        }
    }

    async contentLengthStrategy(localTodo, githubData, conflict) {
        logger.debug(`Applying content_length strategy for todo ${localTodo.id}`);
        
        const localLength = localTodo.content?.length || 0;
        const githubLength = githubData.githubTitle?.length || githubData.content?.length || 0;
        
        // Use the longer content (assuming it's more detailed)
        if (localLength > githubLength) {
            return this.localWinsStrategy(localTodo, githubData, conflict);
        } else {
            return this.githubWinsStrategy(localTodo, githubData, conflict);
        }
    }

    // Helper methods
    determineOptimalStrategy(conflict, localTodo, githubData) {
        // Smart strategy selection based on conflict analysis
        
        if (conflict.severity === 'minor') {
            return 'merged'; // Minor conflicts can usually be merged safely
        }
        
        if (conflict.conflicts.some(c => c.type === 'status_difference')) {
            return 'status_priority'; // Use status-based resolution for status conflicts
        }
        
        if (conflict.conflicts.some(c => c.type === 'content_difference' && c.similarity < 0.3)) {
            return 'timestamp'; // Major content differences - use most recent
        }
        
        if (conflict.conflicts.length === 1 && conflict.conflicts[0].type === 'timestamp_difference') {
            return 'timestamp'; // Pure timestamp conflicts
        }
        
        // Default to merge strategy for moderate conflicts
        return 'merged';
    }

    categorizeConflict(conflicts) {
        const types = conflicts.map(c => c.type);
        
        if (types.includes('content_difference') && types.includes('status_difference')) {
            return 'complex';
        } else if (types.includes('content_difference')) {
            return 'content';
        } else if (types.includes('status_difference')) {
            return 'status';
        } else if (types.includes('timestamp_difference')) {
            return 'temporal';
        } else {
            return 'simple';
        }
    }

    calculateComplexity(conflicts) {
        let complexity = 0;
        
        for (const conflict of conflicts) {
            switch (conflict.severity) {
                case 'minor': complexity += 1; break;
                case 'moderate': complexity += 3; break;
                case 'major': complexity += 5; break;
                case 'critical': complexity += 10; break;
            }
        }
        
        return complexity;
    }

    getSeverityLevel(severity) {
        const levels = {
            'minor': 1,
            'moderate': 2,
            'major': 3,
            'critical': 4
        };
        return levels[severity] || 0;
    }

    normalizeContent(content) {
        return content.toLowerCase()
            .replace(/[^\w\s]/g, '') // Remove punctuation
            .replace(/\s+/g, ' ') // Normalize whitespace
            .trim();
    }

    calculateContentSimilarity(str1, str2) {
        // Simple similarity calculation using Levenshtein distance
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) {
            return 1.0;
        }
        
        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }

    levenshteinDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1, // substitution
                        matrix[i][j - 1] + 1,     // insertion
                        matrix[i - 1][j] + 1      // deletion
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }

    getStatusConflictSeverity(localStatus, githubStatus) {
        // Define status transition severity
        const statusOrder = ['pending', 'in_progress', 'completed'];
        const localIndex = statusOrder.indexOf(localStatus);
        const githubIndex = statusOrder.indexOf(githubStatus);
        
        if (localIndex === -1 || githubIndex === -1) {
            return 'moderate'; // Unknown statuses
        }
        
        const difference = Math.abs(localIndex - githubIndex);
        
        if (difference === 0) return 'none';
        if (difference === 1) return 'minor';
        if (difference === 2) return 'major';
        
        return 'moderate';
    }

    selectAdvancedStatus(localStatus, githubStatus) {
        const statusPriority = {
            'completed': 3,
            'in_progress': 2,
            'pending': 1
        };
        
        const localPriority = statusPriority[localStatus] || 0;
        const githubPriority = statusPriority[githubStatus] || 0;
        
        return localPriority >= githubPriority ? localStatus : githubStatus;
    }

    // Monitoring and reporting
    getResolutionStats() {
        return {
            availableStrategies: Object.keys(this.resolutionStrategies),
            conflictDetectors: this.conflictDetectors.length
        };
    }
}