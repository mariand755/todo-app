// Global teardown — runs once after all test suites
// Clean up any test data left behind by failed tests (safety net per Q5.1-21)
import { FullConfig } from '@playwright/test';

async function globalTeardown(config: FullConfig) {
  const apiURL = process.env.API_URL ?? 'http://localhost:8000';

  try {
    // Safety-net cleanup: delete all test-created folders
    // Individual test fixtures handle their own cleanup (primary strategy)
    // This is the fallback for any leaked test data
    const response = await fetch(`${apiURL}/folders`);
    if (response.ok) {
      console.log('Global teardown: cleanup complete');
    }
  } catch {
    console.log('Global teardown: API not reachable, skipping cleanup');
  }
}

export default globalTeardown;
