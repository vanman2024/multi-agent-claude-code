import { Page, expect } from '@playwright/test';

/**
 * Universal Page Object Base Class
 * Provides common functionality for all page objects
 */
export class BasePage {
  protected page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * Get the page instance (for advanced usage)
   */
  getPage(): Page {
    return this.page;
  }

  /**
   * Navigate to a URL
   */
  async goto(url: string) {
    await this.page.goto(url);
  }

  /**
   * Wait for page to load completely
   */
  async waitForLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Take a screenshot
   */
  async screenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  /**
   * Get page title
   */
  async getTitle() {
    return await this.page.title();
  }

  /**
   * Check if element is visible
   */
  async isVisible(selector: string) {
    return await this.page.isVisible(selector);
  }

  /**
   * Wait for element to be visible
   */
  async waitForVisible(selector: string, timeout = 5000) {
    await this.page.waitForSelector(selector, { state: 'visible', timeout });
  }

  /**
   * Click element safely
   */
  async clickSafely(selector: string) {
    await this.waitForVisible(selector);
    await this.page.click(selector);
  }

  /**
   * Fill input field safely
   */
  async fillSafely(selector: string, value: string) {
    await this.waitForVisible(selector);
    await this.page.fill(selector, value);
  }
}

/**
 * Common test utilities
 */
export class TestUtils {
  /**
   * Generate random test data
   */
  static randomString(length = 8) {
    return Math.random().toString(36).substring(2, length + 2);
  }

  static randomEmail() {
    return `test.${this.randomString()}@example.com`;
  }

  static randomNumber(min = 1, max = 100) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  /**
   * Wait for a specific amount of time
   */
  static async wait(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Retry a function until it succeeds or max attempts reached
   */
  static async retry<T>(
    fn: () => Promise<T>,
    maxAttempts = 3,
    delay = 1000
  ): Promise<T> {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        return await fn();
      } catch (error) {
        if (i === maxAttempts - 1) throw error;
        await this.wait(delay);
      }
    }
    throw new Error('Retry failed');
  }
}

/**
 * API Testing Utilities
 */
export class ApiUtils {
  static async makeRequest(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    url: string,
    options: RequestInit = {}
  ) {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    return {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
      json: () => response.json(),
      text: () => response.text(),
    };
  }

  static async get(url: string, options?: RequestInit) {
    return this.makeRequest('GET', url, options);
  }

  static async post(url: string, data?: any, options?: RequestInit) {
    return this.makeRequest('POST', url, {
      body: JSON.stringify(data),
      ...options,
    });
  }
}
