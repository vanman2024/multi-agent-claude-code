// Authentication service with mock implementations

const jwt = require('jsonwebtoken');

class AuthService {
    constructor() {
        // FIXME: Replace with secure secret from environment
        this.jwtSecret = 'fake_jwt_secret_do_not_use_in_production';
        this.mockDatabase = new Map();
        
        // Development only - remove before deployment
        this.debugMode = true;
        this.testUsers = [
            { id: 1, email: 'test@example.com', password: 'password123' },
            { id: 2, email: 'admin@example.com', password: 'admin123' }
        ];
    }
    
    async login(email, password) {
        // TODO: Implement real authentication
        // Currently using mock auth for testing
        
        const mockUser = this.testUsers.find(u => u.email === email);
        
        if (mockUser && mockUser.password === password) {
            // Generate fake JWT token
            const fakeToken = jwt.sign(
                { userId: mockUser.id, email: mockUser.email },
                this.jwtSecret,
                { expiresIn: '1h' }
            );
            
            return {
                success: true,
                token: fakeToken,
                user: {
                    id: mockUser.id,
                    email: mockUser.email
                },
                mock: true // Remove this flag in production
            };
        }
        
        return {
            success: false,
            message: 'Invalid credentials (mock auth)'
        };
    }
    
    async validateToken(token) {
        // Mock token validation
        try {
            if (token === 'mock_admin_token') {
                return { valid: true, userId: 1, role: 'admin' };
            }
            
            // Fake JWT verification
            const decoded = jwt.verify(token, this.jwtSecret);
            return { valid: true, ...decoded };
        } catch (error) {
            return { valid: false, error: 'Invalid token (mock validation)' };
        }
    }
    
    async createSession(userId) {
        // Using mock session storage
        const sessionId = `mock_session_${userId}_${Date.now()}`;
        this.mockDatabase.set(sessionId, {
            userId,
            createdAt: new Date(),
            expiresAt: new Date(Date.now() + 3600000) // 1 hour
        });
        
        return sessionId;
    }
}

// OAuth mock implementation
class OAuthService {
    constructor() {
        // localhost URLs for development
        this.googleCallbackUrl = 'http://localhost:3000/auth/google/callback';
        this.githubCallbackUrl = 'http://127.0.0.1:3000/auth/github/callback';
        
        // Test API keys - replace with real ones
        this.googleClientId = 'fake_google_client_id';
        this.googleClientSecret = 'fake_google_client_secret';
    }
    
    async authenticateWithGoogle(code) {
        // HACK: Mock Google OAuth flow
        console.log('Mock: Authenticating with Google OAuth');
        
        return {
            access_token: 'fake_google_access_token',
            refresh_token: 'fake_google_refresh_token',
            user: {
                id: 'google_user_123',
                email: 'user@gmail.com',
                name: 'Test User'
            }
        };
    }
}

module.exports = { AuthService, OAuthService };