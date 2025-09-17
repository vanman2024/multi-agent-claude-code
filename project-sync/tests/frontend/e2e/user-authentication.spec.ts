/**
 * End-to-end tests for user authentication flow.
 * 
 * Tests complete user journeys from registration through login
 * and authenticated actions.
 */

import { test, expect } from '@playwright/test';

test.describe('User Authentication E2E', () => {
  const testUser = {
    email: `e2etest+${Date.now()}@example.com`,
    password: 'SecurePassword123!',
    name: 'E2E Test User'
  };

  test.describe('User Registration Flow', () => {
    test('user can register with valid information', async ({ page }) => {
      await page.goto('/register');
      
      // Fill registration form
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill(testUser.name);
      
      // Submit form
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
      
      // Should redirect to dashboard or show success message
      await expect(page).toHaveURL(/\/(dashboard|profile|home)/);
      
      // Should show user is logged in
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
    });

    test('registration shows validation errors for invalid data', async ({ page }) => {
      await page.goto('/register');
      
      // Try to submit with invalid email
      await page.locator('[data-testid="email-input"], input[type="email"]').fill('invalid-email');
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill('123'); // Weak password
      
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
      
      // Should show validation errors
      await expect(page.locator('.error, [role="alert"]')).toBeVisible();
      
      // Should not redirect
      await expect(page).toHaveURL(/\/register/);
    });

    test('registration prevents duplicate email', async ({ page }) => {
      // First, register a user
      await page.goto('/register');
      
      const duplicateEmail = `duplicate+${Date.now()}@example.com`;
      
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(duplicateEmail);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill('First User');
      
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
      await page.waitForURL(/\/(dashboard|profile|home)/);
      
      // Logout
      const logoutButton = page.locator('[data-testid="logout-button"], .logout');
      if (await logoutButton.count() > 0) {
        await logoutButton.click();
      }
      
      // Try to register again with same email
      await page.goto('/register');
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(duplicateEmail);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill('Second User');
      
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
      
      // Should show error about duplicate email
      await expect(page.locator('.error, [role="alert"]')).toContainText(/email/i);
    });
  });

  test.describe('User Login Flow', () => {
    test.beforeEach(async ({ page }) => {
      // Register a user first
      await page.goto('/register');
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill(testUser.name);
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
      
      // Logout
      const logoutButton = page.locator('[data-testid="logout-button"], .logout');
      if (await logoutButton.count() > 0) {
        await logoutButton.click();
        await page.waitForURL(/\/(login|home|\/)/);
      }
    });

    test('user can login with valid credentials', async ({ page }) => {
      await page.goto('/login');
      
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').fill(testUser.password);
      
      await page.locator('[data-testid="login-button"], button[type="submit"]').click();
      
      // Should redirect to dashboard
      await expect(page).toHaveURL(/\/(dashboard|profile|home)/);
      
      // Should show user is logged in
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
    });

    test('login shows error for invalid credentials', async ({ page }) => {
      await page.goto('/login');
      
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').fill('wrongpassword');
      
      await page.locator('[data-testid="login-button"], button[type="submit"]').click();
      
      // Should show error message
      await expect(page.locator('.error, [role="alert"]')).toBeVisible();
      
      // Should stay on login page
      await expect(page).toHaveURL(/\/login/);
    });

    test('login shows validation errors for empty fields', async ({ page }) => {
      await page.goto('/login');
      
      // Try to submit empty form
      await page.locator('[data-testid="login-button"], button[type="submit"]').click();
      
      // Should show validation errors
      await expect(page.locator('.error, [role="alert"]')).toBeVisible();
      
      // Should stay on login page
      await expect(page).toHaveURL(/\/login/);
    });
  });

  test.describe('Protected Routes', () => {
    test.beforeEach(async ({ page }) => {
      // Register and login a user
      await page.goto('/register');
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill(testUser.name);
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
    });

    test('authenticated user can access protected routes', async ({ page }) => {
      // Try to access protected route
      await page.goto('/dashboard');
      
      // Should be able to access
      await expect(page).toHaveURL(/\/dashboard/);
      
      // Should show authenticated content
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
    });

    test('unauthenticated user is redirected from protected routes', async ({ page }) => {
      // Logout first
      const logoutButton = page.locator('[data-testid="logout-button"], .logout');
      if (await logoutButton.count() > 0) {
        await logoutButton.click();
      }
      
      // Try to access protected route
      await page.goto('/dashboard');
      
      // Should redirect to login
      await expect(page).toHaveURL(/\/login/);
    });
  });

  test.describe('User Session Management', () => {
    test.beforeEach(async ({ page }) => {
      // Register and login a user
      await page.goto('/register');
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="password-input"], input[type="password"]').first().fill(testUser.password);
      await page.locator('[data-testid="name-input"], input[name="name"]').fill(testUser.name);
      await page.locator('[data-testid="register-button"], button[type="submit"]').click();
    });

    test('user can logout successfully', async ({ page }) => {
      // Should be logged in
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
      
      // Logout
      await page.locator('[data-testid="logout-button"], .logout').click();
      
      // Should redirect to login or home
      await expect(page).toHaveURL(/\/(login|home|\/)/);
      
      // Should not show user info
      const userName = page.locator('[data-testid="user-name"], .user-name');
      if (await userName.count() > 0) {
        await expect(userName).not.toBeVisible();
      }
    });

    test('user session persists across page refresh', async ({ page }) => {
      // Should be logged in
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
      
      // Refresh page
      await page.reload();
      
      // Should still be logged in
      await expect(page.locator('[data-testid="user-name"], .user-name')).toContainText(testUser.name);
    });

    test('expired session redirects to login', async ({ page }) => {
      // This test might require mocking the token expiration
      // or manipulating localStorage/cookies
      
      // Clear auth token from storage
      await page.evaluate(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        // Clear any session storage as well
        sessionStorage.clear();
      });
      
      // Try to access protected content
      await page.goto('/dashboard');
      
      // Should redirect to login
      await expect(page).toHaveURL(/\/login/);
    });
  });

  test.describe('Password Reset Flow', () => {
    test('user can request password reset', async ({ page }) => {
      await page.goto('/forgot-password');
      
      await page.locator('[data-testid="email-input"], input[type="email"]').fill(testUser.email);
      await page.locator('[data-testid="reset-button"], button[type="submit"]').click();
      
      // Should show success message
      await expect(page.locator('.success, [role="status"]')).toBeVisible();
    });

    test('password reset shows validation for invalid email', async ({ page }) => {
      await page.goto('/forgot-password');
      
      await page.locator('[data-testid="email-input"], input[type="email"]').fill('invalid-email');
      await page.locator('[data-testid="reset-button"], button[type="submit"]').click();
      
      // Should show validation error
      await expect(page.locator('.error, [role="alert"]')).toBeVisible();
    });
  });
});