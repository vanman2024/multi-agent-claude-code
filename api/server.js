#!/usr/bin/env node

/**
 * User Profile Management API Server
 * Provides RESTful endpoints for user profile management
 * Following patterns from notification system (PR #42)
 */

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const multer = require('multer');
const rateLimit = require('express-rate-limit');
const { v4: uuidv4 } = require('uuid');
const Joi = require('joi');
const fs = require('fs');

class UserProfileServer {
  constructor(port = 8891) {
    this.port = port;
    this.app = express();
    
    this.setupDatabase();
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupDatabase() {
    // Create database directory if it doesn't exist
    const dbPath = path.join(__dirname, 'data', 'users.db');
    const dbDir = path.dirname(dbPath);
    
    if (!fs.existsSync(dbDir)) {
      fs.mkdirSync(dbDir, { recursive: true });
    }

    this.db = new sqlite3.Database(dbPath);
    
    // Create users table with required schema
    this.db.serialize(() => {
      this.db.run(`
        CREATE TABLE IF NOT EXISTS users (
          id TEXT PRIMARY KEY,
          email TEXT UNIQUE NOT NULL,
          name TEXT NOT NULL,
          avatar_url TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          deleted_at DATETIME NULL
        )
      `);
      
      // Create index for better performance
      this.db.run('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)');
      this.db.run('CREATE INDEX IF NOT EXISTS idx_users_deleted ON users(deleted_at)');
    });
  }

  setupMiddleware() {
    // Basic middleware
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true }));
    
    // Rate limiting - 10 requests per minute per IP (more lenient for testing)
    const limiter = rateLimit({
      windowMs: 60 * 1000, // 1 minute
      max: process.env.NODE_ENV === 'test' ? 100 : 10, // Higher limit for testing
      message: {
        error: 'Too many requests, please try again later',
        retryAfter: '1 minute'
      },
      standardHeaders: true,
      legacyHeaders: false,
    });
    this.app.use('/api/', limiter);
    
    // CORS middleware
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
      res.header('Access-Control-Allow-Headers', 'Content-Type');
      next();
    });

    // Avatar upload configuration
    const storage = multer.diskStorage({
      destination: (req, file, cb) => {
        const uploadDir = path.join(__dirname, 'uploads');
        if (!fs.existsSync(uploadDir)) {
          fs.mkdirSync(uploadDir, { recursive: true });
        }
        cb(null, uploadDir);
      },
      filename: (req, file, cb) => {
        const ext = path.extname(file.originalname);
        const filename = `${req.params.id}_${Date.now()}${ext}`;
        cb(null, filename);
      }
    });

    this.upload = multer({
      storage,
      limits: {
        fileSize: 5 * 1024 * 1024, // 5MB limit
      },
      fileFilter: (req, file, cb) => {
        // Only allow image files
        if (file.mimetype.startsWith('image/')) {
          cb(null, true);
        } else {
          cb(new Error('Only image files are allowed'), false);
        }
      }
    });
  }

  setupRoutes() {
    // API Routes
    this.app.get('/api/v1/users/:id', this.getUserProfile.bind(this));
    this.app.put('/api/v1/users/:id', this.updateUserProfile.bind(this));
    this.app.post('/api/v1/users/:id/avatar', this.upload.single('avatar'), this.uploadAvatar.bind(this));
    this.app.delete('/api/v1/users/:id', this.softDeleteUser.bind(this));
    
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: new Date().toISOString() });
    });

    // Serve uploaded avatars
    this.app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
    
    // Error handling middleware
    this.app.use(this.errorHandler.bind(this));
  }

  // Validation schemas
  getUserSchema() {
    return Joi.object({
      id: Joi.string().uuid().required()
    });
  }

  updateUserSchema() {
    return Joi.object({
      id: Joi.string().uuid().required(),
      email: Joi.string().email().optional(),
      name: Joi.string().min(1).max(255).optional()
    });
  }

  // API Handlers
  getUserProfile(req, res) {
    const { error } = this.getUserSchema().validate({ id: req.params.id });
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    const { id } = req.params;
    
    this.db.get(
      'SELECT id, email, name, avatar_url, created_at, updated_at FROM users WHERE id = ? AND deleted_at IS NULL',
      [id],
      (err, row) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Internal server error' });
        }
        
        if (!row) {
          return res.status(404).json({ error: 'User not found' });
        }
        
        res.json(row);
      }
    );
  }

  updateUserProfile(req, res) {
    const validation = this.updateUserSchema().validate({ 
      id: req.params.id,
      ...req.body 
    });
    
    if (validation.error) {
      return res.status(400).json({ error: validation.error.details[0].message });
    }

    const { id } = req.params;
    const { email, name } = req.body;
    
    // Check if user exists and is not deleted
    this.db.get(
      'SELECT id FROM users WHERE id = ? AND deleted_at IS NULL',
      [id],
      (err, row) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Internal server error' });
        }
        
        if (!row) {
          return res.status(404).json({ error: 'User not found' });
        }
        
        // Build dynamic update query
        const updates = [];
        const values = [];
        
        if (email !== undefined) {
          updates.push('email = ?');
          values.push(email);
        }
        
        if (name !== undefined) {
          updates.push('name = ?');
          values.push(name);
        }
        
        if (updates.length === 0) {
          return res.status(400).json({ error: 'No fields to update' });
        }
        
        updates.push('updated_at = CURRENT_TIMESTAMP');
        values.push(id);
        
        const query = `UPDATE users SET ${updates.join(', ')} WHERE id = ?`;
        
        this.db.run(query, values, function(err) {
          if (err) {
            console.error('Database error:', err);
            if (err.code === 'SQLITE_CONSTRAINT_UNIQUE') {
              return res.status(409).json({ error: 'Email already exists' });
            }
            return res.status(500).json({ error: 'Internal server error' });
          }
          
          res.json({ message: 'User profile updated successfully' });
        });
      }
    );
  }

  uploadAvatar(req, res) {
    const { error } = this.getUserSchema().validate({ id: req.params.id });
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { id } = req.params;
    const avatarUrl = `/uploads/${req.file.filename}`;
    
    // Check if user exists
    this.db.get(
      'SELECT id, avatar_url FROM users WHERE id = ? AND deleted_at IS NULL',
      [id],
      (err, row) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Internal server error' });
        }
        
        if (!row) {
          // Clean up uploaded file if user not found
          fs.unlink(req.file.path, () => {});
          return res.status(404).json({ error: 'User not found' });
        }
        
        // Delete old avatar if exists
        if (row.avatar_url) {
          const oldAvatarPath = path.join(__dirname, row.avatar_url);
          fs.unlink(oldAvatarPath, () => {}); // Ignore errors
        }
        
        // Update user with new avatar URL
        this.db.run(
          'UPDATE users SET avatar_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
          [avatarUrl, id],
          function(err) {
            if (err) {
              console.error('Database error:', err);
              return res.status(500).json({ error: 'Internal server error' });
            }
            
            res.json({ 
              message: 'Avatar uploaded successfully',
              avatar_url: avatarUrl
            });
          }
        );
      }
    );
  }

  softDeleteUser(req, res) {
    const { error } = this.getUserSchema().validate({ id: req.params.id });
    if (error) {
      return res.status(400).json({ error: error.details[0].message });
    }

    const { id } = req.params;
    
    this.db.run(
      'UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = ? AND deleted_at IS NULL',
      [id],
      function(err) {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Internal server error' });
        }
        
        if (this.changes === 0) {
          return res.status(404).json({ error: 'User not found' });
        }
        
        res.json({ message: 'User deleted successfully' });
      }
    );
  }

  // Error handling middleware
  errorHandler(err, req, res, next) {
    console.error('Unhandled error:', err);
    
    if (err instanceof multer.MulterError) {
      if (err.code === 'LIMIT_FILE_SIZE') {
        return res.status(413).json({ error: 'File too large. Maximum size is 5MB' });
      }
      return res.status(400).json({ error: err.message });
    }
    
    if (err.message === 'Only image files are allowed') {
      return res.status(400).json({ error: 'Only image files are allowed' });
    }
    
    res.status(500).json({ error: 'Internal server error' });
  }

  start() {
    this.app.listen(this.port, () => {
      console.log(`🚀 User Profile API server running on port ${this.port}`);
      console.log(`🌐 Health check: http://localhost:${this.port}/health`);
      console.log('📋 API Endpoints:');
      console.log('  GET    /api/v1/users/:id      - Get user profile');
      console.log('  PUT    /api/v1/users/:id      - Update user profile');
      console.log('  POST   /api/v1/users/:id/avatar - Upload avatar');
      console.log('  DELETE /api/v1/users/:id      - Soft delete user');
    });
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new UserProfileServer(process.env.PORT || 8891);
  server.start();
}

module.exports = UserProfileServer;