# Notification System

A comprehensive real-time notification system with WebSocket support, user preferences, and notification history.

## Features

### ✅ Core Features (Implemented)
- **Real-time notifications** via WebSocket connections
- **In-app notification center** with full UI
- **User preference management** (email, push, in-app settings)
- **Notification history** with read/unread status
- **REST API** for all notification operations
- **SQLite database** for persistent storage
- **Toast notifications** for immediate alerts
- **Mark as read/unread** functionality
- **Notification filtering** (unread only)
- **Priority levels** (low, normal, high, urgent)
- **Notification types** (info, success, warning, error)

### 🚀 Additional Features
- **Test interface** for sending test notifications
- **Responsive design** for mobile and desktop
- **Auto-cleanup** of toast notifications
- **Connection status indicators**
- **Error handling** and validation

## Quick Start

```bash
cd app/
npm install
npm start
```

Visit http://localhost:3000 to access the notification center.

## API Endpoints

### Notifications
- `GET /api/v1/notifications?userId=<id>&unread_only=<bool>` - List notifications
- `POST /api/v1/notifications` - Create notification
- `PUT /api/v1/notifications/:id/read` - Mark as read
- `DELETE /api/v1/notifications/:id` - Delete notification

### User Preferences  
- `GET /api/v1/preferences/:userId` - Get preferences
- `PUT /api/v1/preferences/:userId` - Update preferences

### WebSocket Events
- `join_user` - Join user's notification room
- `new_notification` - Receive real-time notifications

## Architecture

```
app/
├── server.js              # Main server with WebSocket support
├── package.json           # Dependencies and scripts
├── data/                  # SQLite database storage
│   └── notifications.db
├── public/                # Frontend files
│   ├── index.html        # Main UI
│   ├── app.js            # Frontend JavaScript
│   └── styles.css        # Responsive CSS
└── tests/                 # Test suite
    └── notification-tests.js
```

## Database Schema

### notifications
- `id` (TEXT PRIMARY KEY) - UUID
- `user_id` (TEXT) - User identifier
- `title` (TEXT) - Notification title
- `message` (TEXT) - Notification content
- `type` (TEXT) - info, success, warning, error
- `priority` (TEXT) - low, normal, high, urgent
- `read` (INTEGER) - 0 = unread, 1 = read
- `created_at` (DATETIME) - Creation timestamp
- `updated_at` (DATETIME) - Last update timestamp

### user_preferences
- `user_id` (TEXT PRIMARY KEY) - User identifier
- `email_notifications` (INTEGER) - Enable/disable email
- `push_notifications` (INTEGER) - Enable/disable push
- `in_app_notifications` (INTEGER) - Enable/disable in-app
- `notification_frequency` (TEXT) - immediate, hourly, daily
- `email` (TEXT) - User email address
- `created_at` (DATETIME) - Creation timestamp
- `updated_at` (DATETIME) - Last update timestamp

## Usage Examples

### Creating a Notification
```javascript
const response = await fetch('/api/v1/notifications', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 'user123',
    title: 'System Alert',
    message: 'Your account needs attention',
    type: 'warning',
    priority: 'high'
  })
});
```

### WebSocket Integration
```javascript
const socket = io();
socket.emit('join_user', 'user123');
socket.on('new_notification', (notification) => {
  console.log('New notification:', notification);
});
```

## Testing

Run the comprehensive test suite:

```bash
npm test
```

The tests cover:
- API endpoints functionality
- Database operations
- WebSocket connections
- User preferences
- Filtering and pagination

## Integration with Multi-Agent System

The notification system integrates seamlessly with the existing multi-agent architecture:

1. **Agent Dispatcher Integration**: Agents can send notifications about task status
2. **Workflow Notifications**: GitHub actions can trigger notifications
3. **Real-time Updates**: Users get immediate feedback on system activities

### Example Integration
```javascript
// From agent-dispatcher.js
const NotificationServer = require('./app/server');

// Send notification when agent completes task
await fetch('http://localhost:3000/api/v1/notifications', {
  method: 'POST',
  body: JSON.stringify({
    userId: 'developer',
    title: 'Task Completed',
    message: `Issue #${issueNumber} has been resolved by Claude agent`,
    type: 'success',
    priority: 'normal'
  })
});
```

## Configuration

### Environment Variables
- `PORT` - Server port (default: 3000)
- `NODE_ENV` - Environment mode

### Email Configuration (Future Enhancement)
```javascript
// In server.js - extend sendEmailNotification method
const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransporter({
  // Your email configuration
});
```

## Mobile Push Notifications (Future Enhancement)

For push notifications, integrate with services like:
- Firebase Cloud Messaging (FCM)
- Apple Push Notification Service (APNs)
- Web Push API for browsers

## Performance Considerations

- SQLite is suitable for development and small deployments
- For production, consider PostgreSQL or MySQL
- WebSocket connections are lightweight and scalable
- Notifications are paginated to handle large volumes
- Database indexes on `user_id` and `created_at` for performance

## Security

- Input validation on all endpoints
- XSS protection via HTML escaping
- CORS configuration for cross-origin requests
- No sensitive data logging
- Parameterized SQL queries prevent injection

## Monitoring

The system provides:
- Health check endpoint: `/health`
- Connection status in UI
- Console logging for debugging
- Error handling with user feedback