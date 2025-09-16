import { test, expect, Page } from '@playwright/test';
import { BasePage, TestUtils } from '../utils/test-utils';

/**
 * Critical User Journey Tests
 * Focus on high-value user workflows rather than every page
 */

class LoginPage extends BasePage {
  async login(email: string, password: string) {
    await this.fillSafely('[data-testid="email"]', email);
    await this.fillSafely('[data-testid="password"]', password);
    await this.clickSafely('[data-testid="login-button"]');
  }
}

class DashboardPage extends BasePage {
  async getWelcomeMessage() {
    return await this.page.textContent('[data-testid="dashboard-welcome"]');
  }

  async navigateToFeature(feature: string) {
    await this.clickSafely(`[data-testid="nav-${feature}"]`);
  }
}

// 🔴 HIGH PRIORITY: Core User Journeys
test.describe('Critical User Journeys', () => {
  test('complete user registration and first login @critical', async ({ page }) => {
    // Tests: Registration form, email verification, login, welcome flow
    const loginPage = new LoginPage(page);

    // This single test covers: signup page, verification, login page, dashboard
    await page.goto('/signup');
    // ... complete registration flow
    await loginPage.login('newuser@example.com', 'password123');
    // ... verify dashboard loads correctly
  });

  test('authenticated user completes primary workflow @critical', async ({ page }) => {
    // Tests: Login, main dashboard, primary feature, completion
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    await loginPage.login('test@example.com', 'password');
    await dashboardPage.navigateToFeature('main-workflow');
    // ... complete primary user journey
  });
});

// 🟡 MEDIUM PRIORITY: Key Interactions
test.describe('Key Feature Interactions', () => {
  test('settings page saves user preferences', async ({ page }) => {
    // Tests: Navigation to settings, form interaction, save, persistence
  });

  test('search functionality works across app', async ({ page }) => {
    // Tests: Search from multiple pages, results display, navigation
  });
});

// 🟢 LOW PRIORITY: Edge Cases & Error States
test.describe('Error States & Edge Cases', () => {
  test('handles network errors gracefully', async ({ page }) => {
    // Tests: Error pages, offline states, retry mechanisms
  });

  test('validates form inputs correctly', async ({ page }) => {
    // Tests: Validation messages, error states, recovery flows
  });
});

// 🔵 UTILITY: Helper Functions (not full E2E tests)
test.describe('Page Component Tests', () => {
  // These are more like integration tests than full E2E
  test('header navigation works', async ({ page }) => {
    // Quick smoke test of navigation component
  });
});
