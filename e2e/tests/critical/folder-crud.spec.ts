// Folder CRUD E2E tests — create, rename, delete, pin/unpin, ordering
// Tests the full folder lifecycle through the UI
import { test } from '../../fixtures/index.js';
import { FolderPage } from '../../pages/FolderPage.js';
import { folderData } from '../../data/folder.js';

test.describe('Folder CRUD operations', () => {
  let folderPage: FolderPage;

  test.beforeEach(async ({ todoApp }) => {
    folderPage = new FolderPage(todoApp.page);
  });

  test('creates a new folder', { tag: '@E2E002' }, async () => {
    const newFolderName = folderData.single().name;
    await folderPage.createFolder(newFolderName);
    await folderPage.expectFolderVisible(newFolderName);
  });

  test('renames a folder via edit dialog', { tag: '@E2E003' }, async () => {
    const { originalFolderName, renamedFolderName } = folderData.forRename();
    await folderPage.createFolder(originalFolderName);
    await folderPage.selectFolder(originalFolderName);
    await folderPage.renameFolder(renamedFolderName);
    await folderPage.expectFolderVisible(renamedFolderName);
    await folderPage.expectFolderNotVisible(originalFolderName);
  });

  test('deletes a folder', { tag: '@E2E004' }, async () => {
    const newFolderName = folderData.single().name;
    await folderPage.createFolder(newFolderName);
    await folderPage.selectFolder(newFolderName);
    await folderPage.deleteFolder(newFolderName);
    await folderPage.expectFolderNotVisible(newFolderName);
  });

  test('pins a folder', { tag: '@E2E005' }, async () => {
    const newFolderName = folderData.single().name;
    await folderPage.createFolder(newFolderName);
    await folderPage.toggleFolderPin(newFolderName);
    await folderPage.expectFolderPinned(newFolderName, true);
  });

  test('unpins a folder', { tag: '@E2E006' }, async () => {
    const newFolderName = folderData.single().name;
    await folderPage.createFolder(newFolderName);
    await folderPage.toggleFolderPin(newFolderName);
    await folderPage.expectFolderPinned(newFolderName, true);
    await folderPage.toggleFolderPin(newFolderName);
    await folderPage.expectFolderPinned(newFolderName, false);
  });

  test('pinned folders appear first in sidebar', { tag: '@E2E007' }, async () => {
    const { firstFolderName, secondFolderName } = folderData.pair();
    await folderPage.createFolder(firstFolderName);
    await folderPage.createFolder(secondFolderName);
    await folderPage.toggleFolderPin(secondFolderName);
    await folderPage.expectFolderOrder([secondFolderName, firstFolderName]);
  });
});
