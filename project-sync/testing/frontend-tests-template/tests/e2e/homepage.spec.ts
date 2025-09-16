import { test, expect, Page } from '@play  test('has working navigation', async ({ page }: { page: Page }) => {
    await expect(homePage.getPage().locator('nav')).toBeVisible();
    await expect(homePage.getPage().locator('[data-testid="nav-home"]')).toBeVisible();
  });

  test('can perform search', async ({ page }: { page: Page }) => {
    const searchQuery = TestUtils.randomString();
    await homePage.searchFor(searchQuery);

    // Verify search results page
    await expect(homePage.getPage()).toHaveURL(/.*search.*/);
    await expect(homePage.getPage().locator('[data-testid="search-results"]')).toBeVisible();
  });
import { BasePage, TestUtils } from '../utils/test-utils';

/**
 * Example E2E Test Suite
 * Demonstrates common patterns for end-to-end testing
 */

class HomePage extends BasePage {
  async navigateToHome() {
    await this.goto('/');
    await this.waitForLoad();
  }

  async getWelcomeMessage() {
    return await this.page.textContent('[data-testid="welcome-message"]');
  }

  async clickGetStarted() {
    await this.clickSafely('[data-testid="get-started-button"]');
  }

  async searchFor(query: string) {
    await this.fillSafely('[data-testid="search-input"]', query);
    await this.clickSafely('[data-testid="search-button"]');
  }
}

test.describe('Homepage', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.navigateToHome();
  });

  test('displays welcome message', async () => {
    const message = await homePage.getWelcomeMessage();
    expect(message).toContain('Welcome');
  });

  test('has working navigation', async () => {
    await expect(homePage.page.locator('nav')).toBeVisible();
    await expect(homePage.page.locator('[data-testid="nav-home"]')).toBeVisible();
  });

  test('can perform search', async () => {
    const searchQuery = TestUtils.randomString();
    await homePage.searchFor(searchQuery);

    // Verify search results page
    await expect(homePage.page).toHaveURL(/.*search.*/);
    await expect(homePage.page.locator('[data-testid="search-results"]')).toBeVisible();
  });

  test('is accessible', async ({ page }: { page: Page }) => {
    // Basic accessibility check
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();

    // Check for alt text on images
    const images = page.locator('img');
    const imageCount = await images.count();

    for (let i = 0; i < imageCount; i++) {
      const alt = await images.nth(i).getAttribute('alt');
      expect(alt).toBeTruthy();
    }
  });
});

test.describe('User Authentication', () => {
  test('user can sign up with valid data', async ({ page }: { page: Page }) => {
    const homePage = new HomePage(page);
    await homePage.navigateToHome();

    // Navigate to signup
    await page.click('[data-testid="signup-link"]');

    // Fill signup form
    const testUser = {
      name: TestUtils.randomString(8),
      email: TestUtils.randomEmail(),
      password: 'TestPassword123!'
    };

    await page.fill('[data-testid="name-input"]', testUser.name);
    await page.fill('[data-testid="email-input"]', testUser.email);
    await page.fill('[data-testid="password-input"]', testUser.password);
    await page.fill('[data-testid="confirm-password-input"]', testUser.password);

    // Submit form
    await page.click('[data-testid="signup-button"]');

    // Verify success
    await expect(page.locator('[data-testid="welcome-user"]')).toContainText(testUser.name);
  });

  test('shows validation errors for invalid data', async ({ page }: { page: Page }) => {
    const homePage = new HomePage(page);
    await homePage.navigateToHome();

    await page.click('[data-testid="signup-link"]');

    // Try to submit empty form
    await page.click('[data-testid="signup-button"]');

    // Check for validation messages
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });
});

test.describe('Responsive Design', () => {
  test('works on mobile viewport', async ({ page }: { page: Page }) => {
    const homePage = new HomePage(page);

    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await homePage.navigateToHome();

    // Check mobile menu is visible
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();

    // Check content is readable
    const welcomeMessage = await homePage.getWelcomeMessage();
    expect(welcomeMessage).toBeTruthy();
  });

  test('works on tablet viewport', async ({ page }: { page: Page }) => {
    const homePage = new HomePage(page);

    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });

    await homePage.navigateToHome();

    // Check tablet layout
    await expect(page.locator('[data-testid="tablet-layout"]')).toBeVisible();
  });
});

// Smoke tests - run these first to catch major issues
test.describe('Smoke Tests', () => {
  test('@smoke homepage loads', async ({ page }: { page: Page }) => {
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();
  });

  test('@smoke page title is set', async ({ page }: { page: Page }) => {
    await page.goto('/');
    const title = await page.title();
    expect(title).toBeTruthy();
    expect(title.length).toBeGreaterThan(0);
  });
});

// Performance tests
test.describe('Performance', () => {
  test('page loads within 3 seconds', async ({ page }: { page: Page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;

    expect(loadTime).toBeLessThan(3000); // 3 seconds
  });
});
