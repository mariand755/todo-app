// First E2E smoke test — verifies app and API are reachable
// This is the scaffold validation test: if this passes, the E2E framework is working
import { test } from '../../fixtures';
import { AppPage } from '../../pages/AppPage';

test.describe('Health check', () => {
  test('@E2E001 | verifies app health endpoint', async ({ todoApp }) => {
    const appPage = new AppPage(todoApp.page);

    // Verify the frontend loaded successfully
    await appPage.expectLoaded();

    // Verify the backend health endpoint responds
    await appPage.checkHealthEndpoint();
  });
});
