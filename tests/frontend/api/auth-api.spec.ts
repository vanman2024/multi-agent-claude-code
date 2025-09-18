/**
 * API tests for authentication endpoints.
 * 
 * Tests API functionality without requiring the UI layer.
 * Useful for backend API validation and contract testing.
 */

import { test, expect } from '@playwright/test';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3001/api';

test.describe('Authentication API Tests', () => {
  
  test.describe('User Registration', () => {
    test('POST /auth/register - successful registration', async ({ request }) => {
      const newUser = {
        email: `test+${Date.now()}@example.com`,
        password: 'SecurePassword123!',
        name: 'Test User'
      };

      const response = await request.post(`${API_BASE_URL}/auth/register`, {
        data: newUser
      });

      expect(response.status()).toBe(201);
      
      const data = await response.json();
      expect(data).toHaveProperty('token');
      expect(data).toHaveProperty('user');
      expect(data.user.email).toBe(newUser.email);
      expect(data.user).not.toHaveProperty('password'); // Password should not be returned
    });

    test('POST /auth/register - validation errors', async ({ request }) => {
      const invalidUser = {
        email: 'invalid-email',
        password: '123', // Too weak
        name: ''
      };

      const response = await request.post(`${API_BASE_URL}/auth/register`, {
        data: invalidUser
      });

      expect(response.status()).toBe(400);
      
      const data = await response.json();
      expect(data).toHaveProperty('errors');
      expect(Array.isArray(data.errors)).toBeTruthy();
    });

    test('POST /auth/register - duplicate email', async ({ request }) => {
      const duplicateUser = {
        email: 'existing@example.com',
        password: 'SecurePassword123!',
        name: 'Duplicate User'
      };

      // First registration should succeed
      await request.post(`${API_BASE_URL}/auth/register`, {
        data: duplicateUser
      });

      // Second registration with same email should fail
      const response = await request.post(`${API_BASE_URL}/auth/register`, {
        data: duplicateUser
      });

      expect(response.status()).toBe(409);
      
      const data = await response.json();
      expect(data).toHaveProperty('error');
      expect(data.error).toContain('email');
    });
  });

  test.describe('User Login', () => {
    test('POST /auth/login - successful login', async ({ request }) => {
      // First register a user
      const testUser = {
        email: `logintest+${Date.now()}@example.com`,
        password: 'SecurePassword123!',
        name: 'Login Test User'
      };

      await request.post(`${API_BASE_URL}/auth/register`, {
        data: testUser
      });

      // Now login
      const loginResponse = await request.post(`${API_BASE_URL}/auth/login`, {
        data: {
          email: testUser.email,
          password: testUser.password
        }
      });

      expect(loginResponse.status()).toBe(200);
      
      const loginData = await loginResponse.json();
      expect(loginData).toHaveProperty('token');
      expect(loginData).toHaveProperty('user');
      expect(loginData.user.email).toBe(testUser.email);
    });

    test('POST /auth/login - invalid credentials', async ({ request }) => {
      const response = await request.post(`${API_BASE_URL}/auth/login`, {
        data: {
          email: 'nonexistent@example.com',
          password: 'wrongpassword'
        }
      });

      expect(response.status()).toBe(401);
      
      const data = await response.json();
      expect(data).toHaveProperty('error');
    });

    test('POST /auth/login - missing fields', async ({ request }) => {
      const response = await request.post(`${API_BASE_URL}/auth/login`, {
        data: {
          email: 'test@example.com'
          // Missing password
        }
      });

      expect(response.status()).toBe(400);
      
      const data = await response.json();
      expect(data).toHaveProperty('errors');
    });
  });

  test.describe('Token Validation', () => {
    let authToken: string;
    let userId: string;

    test.beforeAll(async ({ request }) => {
      // Create a user and get auth token for protected route tests
      const testUser = {
        email: `tokentest+${Date.now()}@example.com`,
        password: 'SecurePassword123!',
        name: 'Token Test User'
      };

      const registerResponse = await request.post(`${API_BASE_URL}/auth/register`, {
        data: testUser
      });
      
      const registerData = await registerResponse.json();
      authToken = registerData.token;
      userId = registerData.user.id;
    });

    test('GET /auth/me - valid token', async ({ request }) => {
      const response = await request.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data).toHaveProperty('user');
      expect(data.user.id).toBe(userId);
    });

    test('GET /auth/me - missing token', async ({ request }) => {
      const response = await request.get(`${API_BASE_URL}/auth/me`);

      expect(response.status()).toBe(401);
      
      const data = await response.json();
      expect(data).toHaveProperty('error');
    });

    test('GET /auth/me - invalid token', async ({ request }) => {
      const response = await request.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': 'Bearer invalid-token-here'
        }
      });

      expect(response.status()).toBe(401);
      
      const data = await response.json();
      expect(data).toHaveProperty('error');
    });
  });

  test.describe('Password Reset', () => {
    test('POST /auth/forgot-password - valid email', async ({ request }) => {
      const response = await request.post(`${API_BASE_URL}/auth/forgot-password`, {
        data: {
          email: 'user@example.com'
        }
      });

      // Should return success even for non-existent emails (security)
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data).toHaveProperty('message');
    });

    test('POST /auth/forgot-password - invalid email format', async ({ request }) => {
      const response = await request.post(`${API_BASE_URL}/auth/forgot-password`, {
        data: {
          email: 'invalid-email'
        }
      });

      expect(response.status()).toBe(400);
      
      const data = await response.json();
      expect(data).toHaveProperty('errors');
    });

    test('POST /auth/reset-password - valid reset token', async ({ request }) => {
      // This would typically require a valid reset token from email
      // In a real test, you might need to mock the email service
      const response = await request.post(`${API_BASE_URL}/auth/reset-password`, {
        data: {
          token: 'mock-reset-token',
          password: 'NewSecurePassword123!'
        }
      });

      // Expecting 400 since mock token is invalid
      expect([400, 401]).toContain(response.status());
    });
  });

  test.describe('Logout', () => {
    test('POST /auth/logout - valid token', async ({ request }) => {
      // First login to get a token
      const testUser = {
        email: `logouttest+${Date.now()}@example.com`,
        password: 'SecurePassword123!',
        name: 'Logout Test User'
      };

      await request.post(`${API_BASE_URL}/auth/register`, {
        data: testUser
      });

      const loginResponse = await request.post(`${API_BASE_URL}/auth/login`, {
        data: {
          email: testUser.email,
          password: testUser.password
        }
      });

      const { token } = await loginResponse.json();

      // Now logout
      const logoutResponse = await request.post(`${API_BASE_URL}/auth/logout`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      expect(logoutResponse.status()).toBe(200);
      
      const data = await logoutResponse.json();
      expect(data).toHaveProperty('message');
    });
  });
});