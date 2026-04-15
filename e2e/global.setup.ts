// Global setup — runs once before all test suites
// Verify the application is reachable before running tests
import { FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const baseURL = config.projects[0]?.use?.baseURL ?? 'http://localhost:3000';

  // Wait for the app to be ready
  const maxRetries = 10;
  const retryDelay = 2000;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(baseURL);
      if (response.ok) {
        console.log(`Global setup: app reachable at ${baseURL}`);
        return;
      }
    } catch {
      // App not ready yet
    }
    console.log(`Global setup: waiting for app... (attempt ${i + 1}/${maxRetries})`);
    await new Promise((resolve) => setTimeout(resolve, retryDelay));
  }

  throw new Error(`Global setup: app not reachable at ${baseURL} after ${maxRetries} attempts`);
}

export default globalSetup;
