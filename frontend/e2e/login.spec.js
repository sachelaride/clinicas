import { test, expect } from '@playwright/test';

test('should navigate to the login page', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await expect(page.locator('h1')).toContainText('Login');
});

test('should display error on invalid login', async ({ page }) => {
  await page.goto('http://localhost:3000/login');
  await page.locator('#username').fill('invaliduser');
  await page.locator('#password').fill('invalidpassword');
  await page.locator('button[type="submit"]').click();
  await expect(page.locator('.alert-danger')).toContainText('Ocorreu um erro ao tentar fazer login.');
});

test('should login successfully and redirect to dashboard', async ({ page }) => {
  // Assuming a default admin user exists for testing
  await page.goto('http://localhost:3000/login');
  await page.locator('#username').fill('admin'); // Replace with actual admin username
  await page.locator('#password').fill('admin'); // Replace with actual admin password
  await page.locator('button[type="submit"]').click();
  await expect(page).toHaveURL('http://localhost:3000/'); // Assuming dashboard is at root
  await expect(page.locator('h5')).toContainText('Calendário de Agendamentos'); // Assuming dashboard has a title
});