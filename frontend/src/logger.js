// Using this thin wrapper around console instead of raw console calls, so debug/info logs can easily be disabled in production builds.
// Debug/Info only log in dev mode,
// Warn/Error always in log (e.g. for reporting a problem feature,
// or unexpected edge cases that don't warrant a user-facing error but should be visible in prod logs).
const isDev = import.meta.env?.DEV ?? false;

export const logger = {
  debug: (...args) => {
    if (isDev) {
      console.debug(...args);
    }
  },
  info: (...args) => {
    if (isDev) {
      console.info(...args);
    }
  },
  warn: (...args) => {
    console.warn(...args);
  },
  error: (...args) => {
    console.error(...args);
  },
};
