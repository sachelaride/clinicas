/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  testDir: './e2e',
  timeout: 60000, // Increase test timeout to 60 seconds
  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000',
    timeout: 120 * 1000,
    reuseExistingServer: false,
  },
  use: {
    baseURL: 'http://localhost:3000',
    headless: false,
  },
};

module.exports = config;