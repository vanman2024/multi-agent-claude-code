/**
 * Visual regression tests for individual components.
 * 
 * Tests specific UI components in isolation to catch visual regressions
 * at the component level.
 */

import { test, expect } from '@playwright/test';

test.describe('Component Visual Tests', () => {
  
  test.describe('Button Components', () => {
    test.beforeEach(async ({ page }) => {
      // Navigate to a page with buttons or component showcase
      await page.goto('/components'); // Adjust path as needed
      await page.waitForLoadState('networkidle');
    });

    test('primary button states', async ({ page }) => {
      const button = page.locator('[data-testid="button-primary"]').first();
      
      if (await button.count() > 0) {
        // Default state
        await expect(button).toHaveScreenshot('button-primary-default.png');
        
        // Hover state
        await button.hover();
        await expect(button).toHaveScreenshot('button-primary-hover.png');
        
        // Focus state
        await button.focus();
        await expect(button).toHaveScreenshot('button-primary-focus.png');
        
        // Disabled state (if available)
        const disabledButton = page.locator('[data-testid="button-primary"][disabled]');
        if (await disabledButton.count() > 0) {
          await expect(disabledButton).toHaveScreenshot('button-primary-disabled.png');
        }
      }
    });

    test('secondary button states', async ({ page }) => {
      const button = page.locator('[data-testid="button-secondary"]').first();
      
      if (await button.count() > 0) {
        await expect(button).toHaveScreenshot('button-secondary-default.png');
        
        await button.hover();
        await expect(button).toHaveScreenshot('button-secondary-hover.png');
      }
    });
  });

  test.describe('Form Components', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/forms'); // Adjust path as needed
      await page.waitForLoadState('networkidle');
    });

    test('input field states', async ({ page }) => {
      const input = page.locator('[data-testid="input-text"]').first();
      
      if (await input.count() > 0) {
        // Empty state
        await expect(input).toHaveScreenshot('input-empty.png');
        
        // Focused state
        await input.focus();
        await expect(input).toHaveScreenshot('input-focused.png');
        
        // Filled state
        await input.fill('Sample text');
        await expect(input).toHaveScreenshot('input-filled.png');
        
        // Error state (if available)
        const errorInput = page.locator('[data-testid="input-error"]');
        if (await errorInput.count() > 0) {
          await expect(errorInput).toHaveScreenshot('input-error.png');
        }
      }
    });

    test('dropdown component', async ({ page }) => {
      const dropdown = page.locator('[data-testid="dropdown"]').first();
      
      if (await dropdown.count() > 0) {
        // Closed state
        await expect(dropdown).toHaveScreenshot('dropdown-closed.png');
        
        // Opened state
        await dropdown.click();
        await page.waitForTimeout(300); // Wait for animation
        await expect(dropdown).toHaveScreenshot('dropdown-opened.png');
      }
    });
  });

  test.describe('Card Components', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/'); // Cards might be on homepage
      await page.waitForLoadState('networkidle');
    });

    test('product card visual', async ({ page }) => {
      const card = page.locator('[data-testid="product-card"]').first();
      
      if (await card.count() > 0) {
        await expect(card).toHaveScreenshot('product-card.png');
        
        // Hover state
        await card.hover();
        await expect(card).toHaveScreenshot('product-card-hover.png');
      }
    });

    test('info card visual', async ({ page }) => {
      const card = page.locator('[data-testid="info-card"]').first();
      
      if (await card.count() > 0) {
        await expect(card).toHaveScreenshot('info-card.png');
      }
    });
  });

  test.describe('Modal Components', () => {
    test('modal dialog visual', async ({ page }) => {
      await page.goto('/');
      
      const modalTrigger = page.locator('[data-testid="modal-trigger"]').first();
      
      if (await modalTrigger.count() > 0) {
        await modalTrigger.click();
        await page.waitForTimeout(500); // Wait for modal animation
        
        const modal = page.locator('[data-testid="modal"]');
        await expect(modal).toHaveScreenshot('modal-dialog.png');
        
        // Test modal backdrop
        await expect(page).toHaveScreenshot('modal-with-backdrop.png', {
          fullPage: true,
          animations: 'disabled'
        });
      }
    });
  });

  test.describe('Loading States', () => {
    test('loading spinner visual', async ({ page }) => {
      await page.goto('/');
      
      const loadingSpinner = page.locator('[data-testid="loading-spinner"]').first();
      
      if (await loadingSpinner.count() > 0) {
        await expect(loadingSpinner).toHaveScreenshot('loading-spinner.png');
      }
    });

    test('skeleton loading visual', async ({ page }) => {
      await page.goto('/');
      
      const skeleton = page.locator('[data-testid="skeleton-loader"]').first();
      
      if (await skeleton.count() > 0) {
        await expect(skeleton).toHaveScreenshot('skeleton-loader.png');
      }
    });
  });
});