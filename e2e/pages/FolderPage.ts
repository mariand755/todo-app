// FolderPage — all folder interactions: sidebar navigation, CRUD, pin, assertions
// Combines sidebar and main-content folder actions into one page object
// Split into separate page objects later if this file grows too large
import { Page, expect, Locator } from '@playwright/test';
import { test } from '@playwright/test';
import { FolderSelectors as sel } from '../selectors/folder.js';

export class FolderPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // --- Sidebar navigation ---

  // Locate a folder row in the sidebar by its visible title text
  getFolderByName(name: string): Locator {
    return this.page.locator(sel.folderItem).filter({ hasText: name });
  }

  // Click the folder name text specifically — clicking the full <li> can land on
  // the pin button which has stopPropagation and would prevent folder selection
  async selectFolder(name: string) {
    await test.step(`Select folder "${name}"`, async () => {
      await this.getFolderByName(name).locator(sel.folderName).click();
      await expect(this.page.locator(sel.currentFolderTitle)).toHaveText(name);
    });
  }

  // --- CRUD actions ---

  // Create a new folder via the sidebar input form
  // Uses pressSequentially to fire real key events through Shoelace shadow DOM
  async createFolder(name: string) {
    await test.step(`Create folder "${name}"`, async () => {
      const input = this.page.locator(sel.newFolderInput).locator(sel.nativeInput);
      await input.pressSequentially(name);
      await this.page.locator(sel.addFolderBtn).click();
      await expect(this.getFolderByName(name)).toBeVisible();
    });
  }

  // Rename the currently-selected folder using the edit dialog
  // Sets value directly on Shoelace host + fires sl-input so React state syncs.
  // pressSequentially on the native shadow DOM input doesn't reliably trigger
  // Shoelace's sl-input custom events, causing stale React state on submit.
  async renameFolder(newName: string) {
    await test.step(`Rename folder to "${newName}"`, async () => {
      await this.page.locator(sel.folderMenuBtn).click();
      await this.page.locator('sl-menu').waitFor({ state: 'visible' });
      await this.page.getByRole(sel.menuItemRole, { name: sel.editMenuItem }).click();
      await this.page.locator(sel.editDialog).waitFor({ state: 'visible' });

      const slInput = this.page.locator(sel.editFolderInput);
      await slInput.waitFor({ state: 'visible' });

      await slInput.evaluate((el: any, name: string) => {
        el.value = name;
        el.dispatchEvent(new CustomEvent('sl-input', { bubbles: true }));
      }, newName);

      await this.page.locator(`${sel.editDialog} sl-button[variant="primary"]`).click();
      await this.page.locator(sel.editDialog).waitFor({ state: 'hidden' });
      await expect(this.page.locator(sel.currentFolderTitle)).toHaveText(newName);
    });
  }

  // Delete the currently-selected folder using the delete confirmation dialog
  // Uses filter({ hasText }) instead of CSS attribute selector because the dialog
  // label contains quotes that break CSS selectors: Delete "Folder Name"?
  // Waits for menu visibility to avoid Shoelace dropdown rendering race
  async deleteFolder(expectedTitle: string) {
    await test.step(`Delete folder "${expectedTitle}"`, async () => {
      await this.page.locator(sel.folderMenuBtn).click();
      await this.page.locator('sl-menu').waitFor({ state: 'visible' });
      await this.page.getByRole(sel.menuItemRole, { name: sel.deleteMenuItem }).click();
      const dialogLabel = sel.deleteDialogLabel(expectedTitle);
      const dialog = this.page.locator(sel.deleteDialog).filter({ hasText: dialogLabel });
      await dialog.locator('sl-button[variant="primary"]').click();
    });
  }

  // --- Pin actions ---

  // Toggle the pin state of a folder by clicking its pin button
  // Waits for the PUT pin response so DOM state is settled before next action
  async toggleFolderPin(name: string) {
    await test.step(`Toggle pin on folder "${name}"`, async () => {
      const responsePromise = this.page.waitForResponse(resp =>
        resp.url().match(/\/folders\/\d+\/pin$/) !== null && resp.request().method() === 'PUT'
      );
      await this.getFolderByName(name).locator(sel.folderPinBtn).click();
      await responsePromise;
    });
  }

  // --- Assertions ---

  // Assert a folder is visible in the sidebar
  async expectFolderVisible(name: string) {
    await expect(this.getFolderByName(name)).toBeVisible();
  }

  // Assert a folder is NOT visible in the sidebar
  async expectFolderNotVisible(name: string) {
    await expect(this.getFolderByName(name)).not.toBeVisible();
  }

  // Assert the pin button on a folder has the pinned state
  async expectFolderPinned(name: string, pinned: boolean) {
    const pinBtn = this.getFolderByName(name).locator(sel.folderPinBtn);
    if (pinned) {
      await expect(pinBtn).toHaveClass(/is-pinned/);
    } else {
      await expect(pinBtn).not.toHaveClass(/is-pinned/);
    }
  }

  // Assert folder order in the sidebar — filters to only the target names
  // so stale folders from previous runs don't break the assertion
  async expectFolderOrder(names: string[]) {
    const allNames = await this.page
      .locator(`${sel.folderItem}:not(${sel.addFolderRow}) ${sel.folderName}`)
      .allTextContents();
    const relevant = allNames.filter(n => names.includes(n));
    expect(relevant).toEqual(names);
  }
}
