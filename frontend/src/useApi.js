import { logger } from "./logger";

// API base URL — environment-aware via Vite env vars
// Browser dev/Docker: falls back to "/api" (proxied by Vite to real backend)
// Unit tests: VITE_API_URL set to absolute URL for Node.js fetch compat
const apiURL = (import.meta.env.VITE_API_URL || "/api").replace(/\/+$/, "");

// Security: path-validation URL builder
// Ensures every fetch path starts with "/" and stays under the API base.
// With relative base (/api), the browser's same-origin policy provides
// cross-origin protection naturally. With absolute base (tests), we
// validate the resolved URL stays at the configured origin.
function buildSafeApiUrl(apiPath) {
  if (typeof apiPath !== "string" || !apiPath.startsWith("/")) {
    throw new Error("API path must start with '/'.");
  }

  if (apiPath.startsWith("//")) {
    throw new Error("API path must not start with '//'.");
  }

  if (apiPath.includes("..")) {
    throw new Error("API path must not contain path traversal.");
  }

  const fullPath = apiURL + apiPath;

  // Absolute base — validate origin stays pinned
  if (apiURL.startsWith("http")) {
    const resolvedUrl = new URL(fullPath);
    const configuredOrigin = new URL(apiURL).origin;
    /* v8 ignore next 3 -- defence-in-depth guard; prior // and .. checks make this unreachable */
    if (resolvedUrl.origin !== configuredOrigin) {
      throw new Error("API path must resolve to the configured API origin.");
    }
    return resolvedUrl.toString();
  }

  // Relative base — return path directly (same-origin by definition)
  return fullPath;
}

// Central fetch wrapper — all API calls go through here.
// Returns the raw Response on success, or null if the request fails.
export async function makeAPICall(http_method, api_path, payload = null) {
  let url;
  try {
    url = buildSafeApiUrl(api_path);
  } catch (ex) {
    logger.error("Invalid API path", { api_path, error: ex });
    return null;
  }

  const method = http_method.toUpperCase();
  if (method == "GET") {
    try {
      const result = await fetch(url);
      return result;
    } catch (ex) {
      logger.error("GET request failed", { url, error: ex });
      return null;
    }
  }
  try {
    const result = await fetch(url, {
      method: method,
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    });
    return result;
  } catch (ex) {
    logger.error("Request failed", { method, url, error: ex });
    return null;
  }
}
