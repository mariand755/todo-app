// Playwright configuration — applies all Q5.1 architecture decisions
// Q5.1-04 (browser matrix), Q5.1-05 (trigger policy), Q5.1-06 (artifacts),
// Q5.1-09 (reporters), Q5.1-17 (timeouts), Q5.1-18 (retry), Q5.1-22 (logging)
import { defineConfig, devices } from '@playwright/test';
import * as path from 'path';

export default defineConfig({
  // Test directory — all specs live under tests/
  testDir: path.join(__dirname, 'tests'),

  // Global setup/teardown — app readiness check and safety-net cleanup
  globalSetup: path.join(__dirname, 'global.setup.ts'),
  globalTeardown: path.join(__dirname, 'global.teardown.ts'),

  // Timeouts per Q5.1-17
  timeout: 30_000,
  expect: { timeout: 5_000 },

  // Retry policy per Q5.1-18: CI gets retries, local gets zero
  retries: process.env.CI ? 1 : 0,

  // Parallel execution — Playwright default (workers auto-detected)
  fullyParallel: true,

  // Fail the build on test.only left in source
  forbidOnly: !!process.env.CI,

  // Reporter config per Q5.1-09: html + junit + json (+ github in CI)
  reporter: process.env.CI
    ? [
        ['html', { open: 'never', outputFolder: 'playwright-report' }],
        ['junit', { outputFile: 'test-results/results.xml' }],
        ['json', { outputFile: 'test-results/results.json' }],
        ['github'],
      ]
    : [
        ['html', { open: 'on-failure', outputFolder: 'playwright-report' }],
        ['list'],
      ],

  // Shared settings for all projects
  use: {
    // Base URL from environment — Docker Compose and CI set this directly
    // Fallback default matches .env.example for safe local runs
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',

    // Artifact config per Q5.1-06 / Q5.1-22
    trace: 'on-first-retry',
    video: 'on-first-retry',
    screenshot: 'only-on-failure',

    // Viewport defaults
    viewport: { width: 1280, height: 720 },
  },

  // Browser projects per Q5.1-04
  projects: [
    // PR smoke — Chromium only (required gate)
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // Nightly — Firefox
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    // Nightly — WebKit
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  // Output directory for test artifacts
  outputDir: 'test-results',
});
