#!/usr/bin/env node

/**
 * Notification System Server
 * Provides real-time notifications with WebSocket support
 */

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const { v4: uuidv4 } = require('uuid');

class NotificationServer {
  constructor(port = 3000) {
    this.port = port;
    this.app = express();
    this.server = http.createServer(this.app);
    this.io = new Server(this.server, {
      cors: {
        origin: "*",
        methods: ["GET", "POST", "PUT", "DELETE"]
      }
    });
    
    this.setupDatabase();
    this.setupMiddleware();
    this.setupRoutes();
    this.setupWebSocket();
  }

  setupDatabase() {
    // Create database directory if it doesn't exist
    const dbPath = path.join(__dirname, 'data', 'notifications.db');
    const dbDir = path.dirname(dbPath);
    
    const fs = require('fs');
    if (!fs.existsSync(dbDir)) {
      fs.mkdirSync(dbDir, { recursive: true });
    }

    this.db = new sqlite3.Database(dbPath);
    
    // Create tables
    this.db.serialize(() => {
      this.db.run(`
        CREATE TABLE IF NOT EXISTS notifications (
          id TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          title TEXT NOT NULL,
          message TEXT NOT NULL,
          type TEXT DEFAULT 'info',
          priority TEXT DEFAULT 'normal',
          read INTEGER DEFAULT 0,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);
      
      this.db.run(`
        CREATE TABLE IF NOT EXISTS user_preferences (
          user_id TEXT PRIMARY KEY,
          email_notifications INTEGER DEFAULT 1,
          push_notifications INTEGER DEFAULT 1,
          in_app_notifications INTEGER DEFAULT 1,
          notification_frequency TEXT DEFAULT 'immediate',
          email TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);
    });
  }

  setupMiddleware() {
    this.app.use(express.json());
    this.app.use(express.static(path.join(__dirname, 'public')));
    
    // CORS middleware
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
      res.header('Access-Control-Allow-Headers', 'Content-Type');
      next();
    });
  }

  setupRoutes() {
    // API Routes
    this.app.get('/api/v1/notifications', this.getNotifications.bind(this));
    this.app.post('/api/v1/notifications', this.createNotification.bind(this));
    this.app.put('/api/v1/notifications/:id/read', this.markAsRead.bind(this));
    this.app.delete('/api/v1/notifications/:id', this.deleteNotification.bind(this));
    
    // User preferences
    this.app.get('/api/v1/preferences/:userId', this.getPreferences.bind(this));
    this.app.put('/api/v1/preferences/:userId', this.updatePreferences.bind(this));
    
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: new Date().toISOString() });
    });

    // Serve main app
    this.app.get('/', (req, res) => {
      res.sendFile(path.join(__dirname, 'public', 'index.html'));
    });
  }

  setupWebSocket() {
    this.io.on('connection', (socket) => {
      console.log('Client connected:', socket.id);
      
      socket.on('join_user', (userId) => {
        socket.join(`user_${userId}`);
        console.log(`User ${userId} joined notifications`);
      });

      socket.on('disconnect', () => {
        console.log('Client disconnected:', socket.id);
      });
    });
  }

  // API Handlers
  getNotifications(req, res) {
    const { userId, page = 1, limit = 50, unread_only = false } = req.query;
    
    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }

    const offset = (page - 1) * limit;
    const whereClause = unread_only === 'true' ? 'user_id = ? AND read = 0' : 'user_id = ?';
    
    this.db.all(
      `SELECT * FROM notifications WHERE ${whereClause} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
      [userId, limit, offset],
      (err, rows) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        res.json({ notifications: rows, page: parseInt(page), limit: parseInt(limit) });
      }
    );
  }

  createNotification(req, res) {
    const { userId, title, message, type = 'info', priority = 'normal' } = req.body;
    
    if (!userId || !title || !message) {
      return res.status(400).json({ error: 'userId, title, and message are required' });
    }

    const id = uuidv4();
    const notification = {
      id,
      user_id: userId,
      title,
      message,
      type,
      priority
    };

    this.db.run(
      'INSERT INTO notifications (id, user_id, title, message, type, priority) VALUES (?, ?, ?, ?, ?, ?)',
      [id, userId, title, message, type, priority],
      (err) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }

        // Send real-time notification
        this.io.to(`user_${userId}`).emit('new_notification', notification);
        
        // Send email if enabled (to be implemented)
        this.sendEmailNotification(userId, notification);
        
        res.status(201).json(notification);
      }
    );
  }

  markAsRead(req, res) {
    const { id } = req.params;
    
    this.db.run(
      'UPDATE notifications SET read = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [id],
      function(err) {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        
        if (this.changes === 0) {
          return res.status(404).json({ error: 'Notification not found' });
        }
        
        res.json({ message: 'Notification marked as read' });
      }
    );
  }

  deleteNotification(req, res) {
    const { id } = req.params;
    
    this.db.run('DELETE FROM notifications WHERE id = ?', [id], function(err) {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }
      
      if (this.changes === 0) {
        return res.status(404).json({ error: 'Notification not found' });
      }
      
      res.json({ message: 'Notification deleted' });
    });
  }

  getPreferences(req, res) {
    const { userId } = req.params;
    
    this.db.get(
      'SELECT * FROM user_preferences WHERE user_id = ?',
      [userId],
      (err, row) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        
        if (!row) {
          // Return default preferences
          const defaults = {
            user_id: userId,
            email_notifications: 1,
            push_notifications: 1,
            in_app_notifications: 1,
            notification_frequency: 'immediate',
            email: null
          };
          return res.json(defaults);
        }
        
        res.json(row);
      }
    );
  }

  updatePreferences(req, res) {
    const { userId } = req.params;
    const { email_notifications, push_notifications, in_app_notifications, notification_frequency, email } = req.body;
    
    this.db.run(
      `INSERT OR REPLACE INTO user_preferences 
       (user_id, email_notifications, push_notifications, in_app_notifications, notification_frequency, email, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`,
      [userId, email_notifications, push_notifications, in_app_notifications, notification_frequency, email],
      (err) => {
        if (err) {
          console.error('Database error:', err);
          return res.status(500).json({ error: 'Database error' });
        }
        
        res.json({ message: 'Preferences updated successfully' });
      }
    );
  }

  // Email notification handler (placeholder)
  async sendEmailNotification(userId, notification) {
    // Get user preferences
    this.db.get(
      'SELECT email, email_notifications FROM user_preferences WHERE user_id = ? AND email_notifications = 1',
      [userId],
      (err, row) => {
        if (err || !row || !row.email) return;
        
        console.log(`📧 Would send email to ${row.email}: ${notification.title}`);
        // Email implementation would go here using nodemailer
      }
    );
  }

  start() {
    this.server.listen(this.port, () => {
      console.log(`🚀 Notification server running on port ${this.port}`);
      console.log(`📱 WebSocket endpoint: ws://localhost:${this.port}`);
      console.log(`🌐 Web interface: http://localhost:${this.port}`);
    });
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new NotificationServer(process.env.PORT || 3000);
  server.start();
}

module.exports = NotificationServer;