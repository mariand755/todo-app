// Factory for folder test data — deterministic names with unique suffixes
// Prevents collisions in parallel runs per Q5.1-21
// Format: "Label Counter-HH:MM:SS AM/PM" e.g. "Folder 1-02:30:25 PM"
let counter = 0;

function uniqueId(): string {
  counter += 1;
  const time = new Date().toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
  });
  return `${counter}-${time}`;
}

export const folderData = {
  single: () => ({ name: `Folder ${uniqueId()}` }),
  pair: () => ({
    firstFolderName: `Alpha ${uniqueId()}`,
    secondFolderName: `Beta ${uniqueId()}`,
  }),
  forRename: () => ({
    originalFolderName: `Original ${uniqueId()}`,
    renamedFolderName: `Renamed ${uniqueId()}`,
  }),
};
