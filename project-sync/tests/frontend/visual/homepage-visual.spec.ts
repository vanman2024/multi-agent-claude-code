/**
 * Visual regression tests for homepage components.
 * 
 * These tests take screenshots and compare them against baseline images
 * to detect visual changes in the UI.
 */

import { test, expect } from '@playwright/test';

test.describe('Homepage Visual Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for any animations or async content
    await page.waitForLoadState('networkidle');
  });

  test('homepage full page screenshot', async ({ page }) => {
    await expect(page).toHaveScreenshot('homepage-full.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('homepage above fold screenshot', async ({ page }) => {
    await expect(page).toHaveScreenshot('homepage-above-fold.png', {
      animations: 'disabled'
    });
  });

  test('navigation bar visual', async ({ page }) => {
    const nav = page.locator('[data-testid="navigation"]').first();
    await expect(nav).toHaveScreenshot('navigation-bar.png');
  });

  test('hero section visual', async ({ page }) => {
    const hero = page.locator('[data-testid="hero-section"]').first();
    await expect(hero).toHaveScreenshot('hero-section.png');
  });

  test('footer visual', async ({ page }) => {
    const footer = page.locator('[data-testid="footer"]').first();
    await expect(footer).toHaveScreenshot('footer.png');
  });

  test('mobile viewport visual', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 }); // iPhone X
    await expect(page).toHaveScreenshot('homepage-mobile.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('tablet viewport visual', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await expect(page).toHaveScreenshot('homepage-tablet.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('dark mode visual', async ({ page }) => {
    // Toggle dark mode if available
    const darkModeToggle = page.locator('[data-testid="dark-mode-toggle"]');
    if (await darkModeToggle.count() > 0) {
      await darkModeToggle.click();
      await page.waitForTimeout(500); // Wait for theme transition
    }
    
    await expect(page).toHaveScreenshot('homepage-dark-mode.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('hover states visual', async ({ page }) => {
    const button = page.locator('[data-testid="primary-button"]').first();
    if (await button.count() > 0) {
      await button.hover();
      await expect(button).toHaveScreenshot('button-hover-state.png');
    }
  });

  test('form elements visual', async ({ page }) => {
    const form = page.locator('[data-testid="contact-form"]').first();
    if (await form.count() > 0) {
      await expect(form).toHaveScreenshot('contact-form.png');
    }
  });
});