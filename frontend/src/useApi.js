import { logger } from "./logger";

const apiURL = "http://localhost:8000";
const apiOrigin = new URL(apiURL).origin;

function buildSafeApiUrl(apiPath) {
  if (typeof apiPath !== "string" || !apiPath.startsWith("/")) {
    throw new Error("API path must start with '/'.");
  }

  const resolvedUrl = new URL(apiPath, apiURL);
  if (resolvedUrl.origin !== apiOrigin) {
    throw new Error("API path must resolve to the configured API origin.");
  }

  return resolvedUrl.toString();
}

export async function makeAPICall(http_method, api_path, payload = null) {
  let url = "";
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
