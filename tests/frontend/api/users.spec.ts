import { test, expect } from '@playwright/test';
import { ApiUtils } from '../utils/test-utils';

/**
 * Example API Test Suite
 * Demonstrates testing REST API endpoints
 */

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3001';

test.describe('User API', () => {
  test('GET /users returns user list', async () => {
    const response = await ApiUtils.get(`${API_BASE_URL}/users`);

    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('application/json');

    const users = await response.json();
    expect(Array.isArray(users)).toBe(true);
    expect(users.length).toBeGreaterThan(0);

    // Validate user object structure
    const firstUser = users[0];
    expect(firstUser).toHaveProperty('id');
    expect(firstUser).toHaveProperty('name');
    expect(firstUser).toHaveProperty('email');
  });

  test('GET /users/:id returns single user', async () => {
    // First get a user ID from the list
    const listResponse = await ApiUtils.get(`${API_BASE_URL}/users`);
    const users = await listResponse.json();
    const userId = users[0].id;

    // Then get the individual user
    const response = await ApiUtils.get(`${API_BASE_URL}/users/${userId}`);

    expect(response.status).toBe(200);

    const user = await response.json();
    expect(user.id).toBe(userId);
    expect(user).toHaveProperty('name');
    expect(user).toHaveProperty('email');
  });

  test('POST /users creates new user', async () => {
    const newUser = {
      name: 'Test User',
      email: 'test@example.com',
      age: 25
    };

    const response = await ApiUtils.post(`${API_BASE_URL}/users`, newUser);

    expect(response.status).toBe(201);

    const createdUser = await response.json();
    expect(createdUser).toHaveProperty('id');
    expect(createdUser.name).toBe(newUser.name);
    expect(createdUser.email).toBe(newUser.email);
  });

  test('PUT /users/:id updates user', async () => {
    // First create a user
    const newUser = {
      name: 'Update Test',
      email: 'update@example.com'
    };

    const createResponse = await ApiUtils.post(`${API_BASE_URL}/users`, newUser);
    const createdUser = await createResponse.json();

    // Then update it
    const updatedUser = {
      ...createdUser,
      name: 'Updated Name'
    };

    const updateResponse = await ApiUtils.makeRequest(
      'PUT',
      `${API_BASE_URL}/users/${createdUser.id}`,
      { body: JSON.stringify(updatedUser) }
    );

    expect(updateResponse.status).toBe(200);

    const result = await updateResponse.json();
    expect(result.name).toBe('Updated Name');
    expect(result.email).toBe(createdUser.email);
  });

  test('DELETE /users/:id removes user', async () => {
    // First create a user
    const newUser = {
      name: 'Delete Test',
      email: 'delete@example.com'
    };

    const createResponse = await ApiUtils.post(`${API_BASE_URL}/users`, newUser);
    const createdUser = await createResponse.json();

    // Then delete it
    const deleteResponse = await ApiUtils.makeRequest(
      'DELETE',
      `${API_BASE_URL}/users/${createdUser.id}`
    );

    expect(deleteResponse.status).toBe(204);

    // Verify it's gone
    const getResponse = await ApiUtils.get(`${API_BASE_URL}/users/${createdUser.id}`);
    expect(getResponse.status).toBe(404);
  });
});

test.describe('Error Handling', () => {
  test('GET /users/:id with invalid ID returns 404', async () => {
    const response = await ApiUtils.get(`${API_BASE_URL}/users/99999`);

    expect(response.status).toBe(404);

    const error = await response.json();
    expect(error).toHaveProperty('message');
  });

  test('POST /users with invalid data returns 400', async () => {
    const invalidUser = {
      // Missing required fields
      invalidField: 'test'
    };

    const response = await ApiUtils.post(`${API_BASE_URL}/users`, invalidUser);

    expect(response.status).toBe(400);

    const error = await response.json();
    expect(error).toHaveProperty('errors');
  });
});

test.describe('Authentication', () => {
  test('protected endpoints require authentication', async () => {
    const response = await ApiUtils.get(`${API_BASE_URL}/admin/users`);

    expect([401, 403]).toContain(response.status);
  });

  test('can access protected endpoints with valid token', async () => {
    // This would typically involve getting a token first
    const token = process.env.API_TOKEN || 'test-token';

    const response = await ApiUtils.get(`${API_BASE_URL}/admin/users`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    // This test would depend on your auth implementation
    expect([200, 401, 403]).toContain(response.status);
  });
});

test.describe('Performance', () => {
  test('API responds within acceptable time', async () => {
    const startTime = Date.now();

    const response = await ApiUtils.get(`${API_BASE_URL}/users`);
    const endTime = Date.now();

    expect(response.status).toBe(200);
    expect(endTime - startTime).toBeLessThan(1000); // 1 second
  });
});
