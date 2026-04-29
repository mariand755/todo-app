// Centralized selectors for folder-related UI elements
// Update here when the frontend changes — page objects and tests stay untouched
// Selector priority per Q5.1-16: data-testid > getByRole > getByText > CSS
export const FolderSelectors = {
  // Sidebar — folder list
  folderList: '#folder-list',
  folderItem: '#folder-list li.folder-item',
  folderName: '.folder-name',
  folderPinBtn: '.folder-pin-btn',
  addFolderRow: '.add-folder',

  // Sidebar — new folder form
  newFolderInput: '#new-folder-input',
  addFolderBtn: '#add-folder-btn',

  // Main content — folder header
  currentFolderTitle: '#current-folder-title',
  folderMenuBtn: '.folder-menu-button',

  // Main content — folder menu items
  menuItemRole: 'menuitem' as const,
  editMenuItem: 'Edit',
  deleteMenuItem: 'Delete',

  // Main content — edit folder dialog
  editDialog: 'sl-dialog[label="Edit Folder Name"]',
  editFolderInput: '#edit-folder-input',

  // Main content — delete folder dialog
  // deleteDialog is a bare tag selector — page objects use filter({ hasText })
  // to match the dynamic label because the title contains quotes that break CSS
  deleteDialog: 'sl-dialog',
  deleteDialogLabel: (title: string) => `Delete "${title}"?`,

  // Shadow DOM — native input inside Shoelace web components
  nativeInput: 'input',
} as const;
