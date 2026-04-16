// Base test fixture — extends Playwright with app-specific setup
// Provides todoApp fixture: navigates to baseURL, exposes page + baseURL
// All E2E tests import { test, expect } from this file instead of @playwright/test
import { test as base, expect, Page } from '@playwright/test';

// App fixture type — shared across all tests
type TodoAppFixtures = {
  todoApp: { page: Page; baseURL: string };
};

// Extended test with todoApp fixture per Q5.1-20
export const test = base.extend<TodoAppFixtures>({
  todoApp: async ({ page, baseURL }, use) => {
    // Navigate to the app and wait for initial load
    await page.goto(baseURL ?? 'http://localhost:3000');
    await page.waitForLoadState('domcontentloaded');
    await use({ page, baseURL: baseURL ?? 'http://localhost:3000' });
  },
});

// Re-export expect so tests import everything from fixtures
export { expect };
