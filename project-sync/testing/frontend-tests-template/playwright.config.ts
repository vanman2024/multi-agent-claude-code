import { defineConfig, devices } from '@playwright/test';

/**
 * @see https://playwright.dev/docs/test-configuration
 */
const noSandbox = !!process.env.PW_NO_SANDBOX || !!process.env.CI || !!process.env.WSL;
const allBrowsers = !!process.env.ALL_BROWSERS;

export default defineConfig({
  testDir: './frontend-tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Keep some parallelism on CI for speed */
  workers: process.env.CI ? 2 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'test-results.xml' }],
    process.env.CI ? ['github'] : ['list']
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Take screenshot on failure */
    screenshot: 'only-on-failure',

    /* Record video on failure */
    video: 'retain-on-failure',

    /* Timeout settings */
    actionTimeout: 10000,
    navigationTimeout: 30000,
    expect: {
      timeout: 5000
    }
  },

  /* Configure projects (Chromium by default; others opt-in via ALL_BROWSERS=1) */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        launchOptions: noSandbox ? { args: ['--no-sandbox', '--disable-setuid-sandbox'] } : {},
      },
    },
    ...(allBrowsers
      ? [
          { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
          { name: 'webkit', use: { ...devices['Desktop Safari'] } },
          { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
          { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
          { name: 'Microsoft Edge', use: { ...devices['Desktop Edge'], channel: 'msedge' } },
          { name: 'Google Chrome', use: { ...devices['Desktop Chrome'], channel: 'chrome' } },
        ]
      : []),
  ],

  /* Run your local dev server before starting the tests */
  webServer: process.env.SKIP_WEBSERVER ? undefined : {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },

  /* Global setup and teardown */
  globalSetup: require.resolve('./frontend-tests/global-setup'),
  globalTeardown: require.resolve('./frontend-tests/global-teardown'),
});
