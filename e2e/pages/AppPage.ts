// AppPage — top-level page object for app-wide state and health checks
// Selector hierarchy per Q5.1-16: data-testid > getByRole > getByText > CSS
import { Page, expect } from '@playwright/test';

export class AppPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Check that the app has loaded and is displaying content
  async expectLoaded() {
    // Use role-based selector (Q5.1-16 tier 2) — heading is semantic and stable
    await expect(this.page.getByRole('heading').first()).toBeVisible();
  }

  // Verify the backend health endpoint is reachable
  async checkHealthEndpoint(apiURL?: string) {
    const url = apiURL ?? process.env.API_URL ?? 'http://localhost:8000';
    const response = await this.page.request.get(`${url}/health`);
    expect(response.ok()).toBeTruthy();
  }
}
