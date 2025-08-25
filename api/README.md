# User Profile Management API

A RESTful API for user profile management following established patterns from the notification system (PR #42).

## Features

- ✅ **GET /api/v1/users/:id** - Get user profile
- ✅ **PUT /api/v1/users/:id** - Update user profile
- ✅ **POST /api/v1/users/:id/avatar** - Upload avatar
- ✅ **DELETE /api/v1/users/:id** - Soft delete user
- ✅ **Input validation** using Joi
- ✅ **Rate limiting** (10 requests per minute)
- ✅ **SQLite database** with proper schema
- ✅ **Unit tests** (8/8 passing)
- ✅ **File upload** for avatars (5MB limit, images only)
- ✅ **Soft delete** functionality
- ✅ **Proper HTTP status codes**

## Database Schema

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,           -- UUID
  email TEXT UNIQUE NOT NULL,    -- User email
  name TEXT NOT NULL,           -- Display name
  avatar_url TEXT,              -- Path to avatar file
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL      -- Soft delete timestamp
);
```

## Quick Start

```bash
# Install dependencies
npm install

# Start server
npm start
# Server runs on http://localhost:8891

# Run tests
npm test
```

## API Documentation

### GET /api/v1/users/:id

Get user profile by ID.

**Parameters:**
- `id` (string, required): User UUID

**Response:**
```json
{
  "id": "886b37ff-ff51-486d-a365-75eb8623a2fc",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar_url": "/uploads/avatar.jpg",
  "created_at": "2025-01-01 12:00:00",
  "updated_at": "2025-01-01 12:00:00"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid UUID format
- `404` - User not found
- `500` - Server error

### PUT /api/v1/users/:id

Update user profile.

**Parameters:**
- `id` (string, required): User UUID

**Request Body:**
```json
{
  "email": "newemail@example.com",  // Optional
  "name": "New Name"                // Optional
}
```

**Response:**
```json
{
  "message": "User profile updated successfully"
}
```

**Status Codes:**
- `200` - Success
- `400` - Validation error
- `404` - User not found  
- `409` - Email already exists
- `500` - Server error

### POST /api/v1/users/:id/avatar

Upload user avatar.

**Parameters:**
- `id` (string, required): User UUID

**Request:** 
- `Content-Type: multipart/form-data`
- Form field: `avatar` (file)

**File Requirements:**
- Format: Images only (jpg, png, gif, etc.)
- Size: Maximum 5MB
- Storage: `/uploads/` directory

**Response:**
```json
{
  "message": "Avatar uploaded successfully",
  "avatar_url": "/uploads/user_123456789.jpg"
}
```

**Status Codes:**
- `200` - Success
- `400` - No file uploaded or invalid file type
- `404` - User not found
- `413` - File too large
- `500` - Server error

### DELETE /api/v1/users/:id

Soft delete user (sets `deleted_at` timestamp).

**Parameters:**
- `id` (string, required): User UUID

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid UUID format
- `404` - User not found
- `500` - Server error

## Rate Limiting

- **Limit:** 10 requests per minute per IP address
- **Response when exceeded:**
  ```json
  {
    "error": "Too many requests, please try again later",
    "retryAfter": "1 minute"
  }
  ```

## Testing

Run the comprehensive test suite:

```bash
npm test
```

**Test Coverage:**
- ✅ Health check endpoint
- ✅ Get user profile (exists/not found)
- ✅ Update user profile
- ✅ Input validation (UUID, email format)
- ✅ Soft delete functionality
- ✅ Rate limiting
- ✅ Avatar upload validation

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message describing the issue"
}
```

## Environment Variables

- `PORT` - Server port (default: 8891)
- `NODE_ENV` - Environment mode (test/development/production)

## Integration

This API follows the same patterns as the notification system:
- Express.js server
- SQLite database
- Rate limiting middleware  
- Joi validation
- Comprehensive testing
- RESTful endpoints

## File Structure

```
api/
├── server.js              # Main server file
├── package.json           # Dependencies and scripts
├── data/                  # SQLite database
│   └── users.db
├── uploads/               # Avatar files
├── tests/                 # Test suite
│   └── user-profile-tests.js
└── README.md              # This file
```

## Production Considerations

- Consider migrating from SQLite to PostgreSQL for production
- Implement proper authentication middleware
- Add request logging
- Set up proper avatar file cleanup for deleted users
- Configure CORS for your domain
- Add API documentation with tools like Swagger
- Implement backup strategies for the database