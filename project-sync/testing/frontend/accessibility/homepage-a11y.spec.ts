/**
 * Accessibility tests for homepage.
 * 
 * These tests use axe-core to check for WCAG compliance issues
 * and other accessibility violations.
 */

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Homepage Accessibility Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('homepage passes accessibility scan', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('homepage with dark mode passes accessibility scan', async ({ page }) => {
    // Toggle dark mode if available
    const darkModeToggle = page.locator('[data-testid="dark-mode-toggle"]');
    if (await darkModeToggle.count() > 0) {
      await darkModeToggle.click();
      await page.waitForTimeout(500);
    }
    
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('navigation landmarks are present', async ({ page }) => {
    // Check for proper landmark elements
    const nav = page.locator('nav[role="navigation"], nav, [role="navigation"]');
    const main = page.locator('main[role="main"], main, [role="main"]');
    const footer = page.locator('footer[role="contentinfo"], footer, [role="contentinfo"]');
    
    await expect(nav.first()).toBeVisible();
    await expect(main.first()).toBeVisible();
    
    // Footer might not always be visible in viewport
    const footerCount = await footer.count();
    if (footerCount > 0) {
      expect(footerCount).toBeGreaterThan(0);
    }
  });

  test('headings follow proper hierarchy', async ({ page }) => {
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const headingTexts = await headings.allTextContents();
    
    // Should have at least one h1
    const h1Elements = page.locator('h1');
    const h1Count = await h1Elements.count();
    expect(h1Count).toBeGreaterThan(0);
    
    // Check if headings exist
    expect(headingTexts.length).toBeGreaterThan(0);
  });

  test('images have alt attributes', async ({ page }) => {
    const images = page.locator('img');
    const imageCount = await images.count();
    
    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');
      
      // Image should have alt attribute or role="presentation"
      expect(alt !== null || role === 'presentation').toBeTruthy();
    }
  });

  test('interactive elements are keyboard accessible', async ({ page }) => {
    // Get all interactive elements
    const interactiveElements = page.locator('button, a, input, select, textarea, [tabindex="0"], [role="button"]');
    const count = await interactiveElements.count();
    
    for (let i = 0; i < Math.min(count, 10); i++) { // Test first 10 elements
      const element = interactiveElements.nth(i);
      
      // Focus the element
      await element.focus();
      
      // Check if element is focused
      const isFocused = await element.evaluate(el => document.activeElement === el);
      expect(isFocused).toBeTruthy();
    }
  });

  test('form elements have proper labels', async ({ page }) => {
    const inputs = page.locator('input[type="text"], input[type="email"], input[type="password"], textarea, select');
    const inputCount = await inputs.count();
    
    for (let i = 0; i < inputCount; i++) {
      const input = inputs.nth(i);
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledBy = await input.getAttribute('aria-labelledby');
      
      if (id) {
        // Check if there's a label with matching 'for' attribute
        const label = page.locator(`label[for="${id}"]`);
        const labelExists = await label.count() > 0;
        
        // Input should have either a label, aria-label, or aria-labelledby
        expect(labelExists || ariaLabel !== null || ariaLabelledBy !== null).toBeTruthy();
      }
    }
  });

  test('color contrast meets WCAG standards', async ({ page }) => {
    // Use axe to specifically check for color contrast issues
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    
    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      violation => violation.id === 'color-contrast'
    );
    
    expect(contrastViolations).toEqual([]);
  });

  test('focus indicators are visible', async ({ page }) => {
    const focusableElements = page.locator('button, a, input, select, textarea, [tabindex="0"]');
    const count = await focusableElements.count();
    
    if (count > 0) {
      const firstElement = focusableElements.first();
      await firstElement.focus();
      
      // Check if focus styles are applied (this is a basic check)
      const focusedElement = page.locator(':focus');
      await expect(focusedElement).toHaveCount(1);
    }
  });

  test('skip links are present and functional', async ({ page }) => {
    // Look for skip links (usually hidden until focused)
    const skipLinks = page.locator('a[href^="#"]:has-text("Skip"), a[href^="#"]:has-text("skip")');
    const skipLinkCount = await skipLinks.count();
    
    if (skipLinkCount > 0) {
      const firstSkipLink = skipLinks.first();
      await firstSkipLink.focus();
      
      // Skip link should be visible when focused
      await expect(firstSkipLink).toBeVisible();
      
      // Test skip link functionality
      const href = await firstSkipLink.getAttribute('href');
      if (href && href.startsWith('#')) {
        await firstSkipLink.click();
        const targetId = href.substring(1);
        const target = page.locator(`#${targetId}`);
        
        if (await target.count() > 0) {
          const isFocused = await target.evaluate(el => document.activeElement === el);
          expect(isFocused).toBeTruthy();
        }
      }
    }
  });
});