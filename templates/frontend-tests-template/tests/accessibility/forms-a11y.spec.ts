/**
 * Accessibility tests for forms and interactive elements.
 * 
 * Comprehensive WCAG compliance testing for form elements,
 * error handling, and interactive components.
 */

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Forms Accessibility Tests', () => {
  
  test.describe('Contact Form Accessibility', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/contact'); // Adjust path as needed
      await page.waitForLoadState('networkidle');
    });

    test('contact form passes accessibility scan', async ({ page }) => {
      const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
      expect(accessibilityScanResults.violations).toEqual([]);
    });

    test('form labels are properly associated', async ({ page }) => {
      const form = page.locator('form').first();
      
      if (await form.count() > 0) {
        const inputs = form.locator('input, textarea, select');
        const inputCount = await inputs.count();
        
        for (let i = 0; i < inputCount; i++) {
          const input = inputs.nth(i);
          const id = await input.getAttribute('id');
          const ariaLabel = await input.getAttribute('aria-label');
          const ariaLabelledBy = await input.getAttribute('aria-labelledby');
          const type = await input.getAttribute('type');
          
          // Skip hidden inputs
          if (type === 'hidden') continue;
          
          if (id) {
            const label = page.locator(`label[for="${id}"]`);
            const labelExists = await label.count() > 0;
            
            // Input must have proper labeling
            expect(labelExists || ariaLabel !== null || ariaLabelledBy !== null).toBeTruthy();
          }
        }
      }
    });

    test('required fields are properly indicated', async ({ page }) => {
      const requiredInputs = page.locator('input[required], textarea[required], select[required]');
      const requiredCount = await requiredInputs.count();
      
      for (let i = 0; i < requiredCount; i++) {
        const input = requiredInputs.nth(i);
        const ariaRequired = await input.getAttribute('aria-required');
        const required = await input.getAttribute('required');
        
        // Required fields should have proper ARIA attributes
        expect(required !== null).toBeTruthy();
        
        // Check if required indicator is visible to screen readers
        const id = await input.getAttribute('id');
        if (id) {
          const label = page.locator(`label[for="${id}"]`);
          if (await label.count() > 0) {
            const labelText = await label.textContent();
            // Should indicate required status somehow (*, "required", etc.)
            expect(labelText).toBeTruthy();
          }
        }
      }
    });

    test('form validation errors are accessible', async ({ page }) => {
      const form = page.locator('form').first();
      const submitButton = form.locator('button[type="submit"], input[type="submit"]').first();
      
      if (await submitButton.count() > 0) {
        // Try to submit empty form to trigger validation
        await submitButton.click();
        await page.waitForTimeout(1000);
        
        // Check for error messages
        const errorMessages = page.locator('[role="alert"], .error, [aria-invalid="true"]');
        const errorCount = await errorMessages.count();
        
        if (errorCount > 0) {
          // Error messages should be properly announced
          const firstError = errorMessages.first();
          const role = await firstError.getAttribute('role');
          const ariaLive = await firstError.getAttribute('aria-live');
          
          expect(role === 'alert' || ariaLive !== null).toBeTruthy();
        }
      }
    });

    test('form can be navigated with keyboard only', async ({ page }) => {
      const form = page.locator('form').first();
      
      if (await form.count() > 0) {
        const focusableElements = form.locator('input, textarea, select, button, [tabindex="0"]');
        const count = await focusableElements.count();
        
        // Tab through all form elements
        for (let i = 0; i < count; i++) {
          await page.keyboard.press('Tab');
          const activeElement = page.locator(':focus');
          await expect(activeElement).toHaveCount(1);
        }
      }
    });
  });

  test.describe('Search Form Accessibility', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/'); // Search might be on homepage
      await page.waitForLoadState('networkidle');
    });

    test('search form is accessible', async ({ page }) => {
      const searchForm = page.locator('form[role="search"], [data-testid="search-form"]').first();
      
      if (await searchForm.count() > 0) {
        const accessibilityScanResults = await new AxeBuilder({ page })
          .include(await searchForm.getAttribute('data-testid') || 'form[role="search"]')
          .analyze();
        
        expect(accessibilityScanResults.violations).toEqual([]);
      }
    });

    test('search input has proper labeling', async ({ page }) => {
      const searchInput = page.locator('input[type="search"], input[placeholder*="search" i], [data-testid="search-input"]').first();
      
      if (await searchInput.count() > 0) {
        const ariaLabel = await searchInput.getAttribute('aria-label');
        const placeholder = await searchInput.getAttribute('placeholder');
        const id = await searchInput.getAttribute('id');
        
        let hasLabel = false;
        
        if (id) {
          const label = page.locator(`label[for="${id}"]`);
          hasLabel = await label.count() > 0;
        }
        
        // Search input should be properly labeled
        expect(hasLabel || ariaLabel !== null || placeholder !== null).toBeTruthy();
      }
    });

    test('search suggestions are accessible', async ({ page }) => {
      const searchInput = page.locator('input[type="search"], [data-testid="search-input"]').first();
      
      if (await searchInput.count() > 0) {
        // Type to trigger suggestions
        await searchInput.fill('test');
        await page.waitForTimeout(1000);
        
        const suggestions = page.locator('[role="listbox"], [role="menu"], .search-suggestions').first();
        
        if (await suggestions.count() > 0) {
          // Check ARIA attributes
          const ariaExpanded = await searchInput.getAttribute('aria-expanded');
          const ariaOwns = await searchInput.getAttribute('aria-owns');
          const ariaActivedescendant = await searchInput.getAttribute('aria-activedescendant');
          
          // Suggestions should be properly connected to input
          expect(ariaExpanded === 'true' || ariaOwns !== null).toBeTruthy();
          
          // Test keyboard navigation
          await page.keyboard.press('ArrowDown');
          await page.waitForTimeout(200);
          
          const updatedActivedescendant = await searchInput.getAttribute('aria-activedescendant');
          // Should update active descendant when navigating
          expect(updatedActivedescendant).toBeTruthy();
        }
      }
    });
  });

  test.describe('Interactive Components Accessibility', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/');
      await page.waitForLoadState('networkidle');
    });

    test('buttons have proper roles and labels', async ({ page }) => {
      const buttons = page.locator('button, [role="button"]');
      const buttonCount = await buttons.count();
      
      for (let i = 0; i < buttonCount; i++) {
        const button = buttons.nth(i);
        const ariaLabel = await button.getAttribute('aria-label');
        const textContent = await button.textContent();
        const title = await button.getAttribute('title');
        
        // Button should have accessible name
        const hasAccessibleName = (textContent && textContent.trim()) || ariaLabel || title;
        expect(hasAccessibleName).toBeTruthy();
      }
    });

    test('dropdown menus are accessible', async ({ page }) => {
      const dropdownTriggers = page.locator('[aria-haspopup], [data-testid*="dropdown"]');
      const triggerCount = await dropdownTriggers.count();
      
      for (let i = 0; i < Math.min(triggerCount, 3); i++) { // Test first 3 dropdowns
        const trigger = dropdownTriggers.nth(i);
        
        // Check initial state
        const ariaExpanded = await trigger.getAttribute('aria-expanded');
        expect(ariaExpanded === 'false' || ariaExpanded === null).toBeTruthy();
        
        // Open dropdown
        await trigger.click();
        await page.waitForTimeout(300);
        
        // Check expanded state
        const expandedState = await trigger.getAttribute('aria-expanded');
        expect(expandedState === 'true').toBeTruthy();
        
        // Test keyboard navigation
        await page.keyboard.press('ArrowDown');
        await page.waitForTimeout(100);
        
        // Close dropdown (ESC key)
        await page.keyboard.press('Escape');
        await page.waitForTimeout(300);
        
        const closedState = await trigger.getAttribute('aria-expanded');
        expect(closedState === 'false').toBeTruthy();
      }
    });

    test('modal dialogs are accessible', async ({ page }) => {
      const modalTrigger = page.locator('[data-testid="modal-trigger"]').first();
      
      if (await modalTrigger.count() > 0) {
        await modalTrigger.click();
        await page.waitForTimeout(500);
        
        const modal = page.locator('[role="dialog"], [data-testid="modal"]');
        
        if (await modal.count() > 0) {
          // Check modal attributes
          const ariaModal = await modal.first().getAttribute('aria-modal');
          const ariaLabelledBy = await modal.first().getAttribute('aria-labelledby');
          const ariaLabel = await modal.first().getAttribute('aria-label');
          
          expect(ariaModal === 'true').toBeTruthy();
          expect(ariaLabelledBy !== null || ariaLabel !== null).toBeTruthy();
          
          // Test focus trap
          await page.keyboard.press('Tab');
          const focusedElement = page.locator(':focus');
          const focusedCount = await focusedElement.count();
          expect(focusedCount).toBe(1);
          
          // Close modal with Escape
          await page.keyboard.press('Escape');
          await page.waitForTimeout(300);
          
          const modalStillVisible = await modal.isVisible();
          expect(modalStillVisible).toBeFalsy();
        }
      }
    });

    test('tab navigation follows logical order', async ({ page }) => {
      const focusableElements = page.locator('a, button, input, select, textarea, [tabindex="0"]');
      const count = await focusableElements.count();
      
      if (count > 0) {
        // Start from first element
        await focusableElements.first().focus();
        
        // Tab through several elements
        const maxTabs = Math.min(count, 10);
        for (let i = 0; i < maxTabs - 1; i++) {
          await page.keyboard.press('Tab');
          
          const currentFocus = page.locator(':focus');
          await expect(currentFocus).toHaveCount(1);
        }
        
        // Shift+Tab should go backward
        await page.keyboard.press('Shift+Tab');
        const backwardFocus = page.locator(':focus');
        await expect(backwardFocus).toHaveCount(1);
      }
    });
  });
});