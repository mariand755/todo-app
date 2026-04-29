import {
  describe,
  it,
  expect,
  vi,
  beforeAll,
  afterAll,
  afterEach,
} from "vitest";
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { makeAPICall } from "@/useApi";
import { logger } from "@/logger";

const server = setupServer(
  http.get("http://localhost:8000/folders", () => {
    return HttpResponse.json([{ id: 1, title: "Test Folder" }]);
  }),
  http.post("http://localhost:8000/folders", async ({ request }) => {
    const payload = await request.json();
    return HttpResponse.json(payload, { status: 201 });
  }),
  http.put("http://localhost:8000/folders/1", async ({ request }) => {
    const payload = await request.json();
    return HttpResponse.json(payload, { status: 200 });
  }),
);

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  server.resetHandlers();
  vi.restoreAllMocks();
});

afterAll(() => {
  server.close();
});

describe("makeAPICall", () => {
  it("@FUT01 | calls fetch for GET requests without JSON body/options", async () => {
    const result = await makeAPICall("GET", "/folders");
    const body = await result.json();

    expect(result.ok).toBe(true);
    expect(body).toEqual([{ id: 1, title: "Test Folder" }]);
  });

  it("@FUT02 | uppercases http method before request", async () => {
    let methodSeenByHandler = "";
    server.use(
      http.post("http://localhost:8000/folders", async ({ request }) => {
        methodSeenByHandler = request.method;
        return HttpResponse.json(await request.json(), { status: 201 });
      }),
    );

    const result = await makeAPICall("post", "/folders", { title: "Work" });
    const body = await result.json();

    expect(result.status).toBe(201);
    expect(methodSeenByHandler).toBe("POST");
    expect(body).toEqual({ title: "Work" });
  });

  it("@FUT03 | returns null when GET fetch throws", async () => {
    server.use(
      http.get("http://localhost:8000/folders", () => {
        return HttpResponse.error();
      }),
    );
    const errorSpy = vi.spyOn(logger, "error").mockImplementation(() => {});

    const result = await makeAPICall("GET", "/folders");

    expect(result).toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      "GET request failed",
      expect.objectContaining({ url: "http://localhost:8000/folders" }),
    );
  });

  it("@FUT04 | returns null when non-GET fetch throws", async () => {
    server.use(
      http.put("http://localhost:8000/folders/1", () => {
        return HttpResponse.error();
      }),
    );
    const errorSpy = vi.spyOn(logger, "error").mockImplementation(() => {});

    const result = await makeAPICall("PUT", "/folders/1", { title: "x" });

    expect(result).toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      "Request failed",
      expect.objectContaining({
        method: "PUT",
        url: "http://localhost:8000/folders/1",
      }),
    );
  });

  it("@FUT50 | rejects API paths that resolve outside configured origin", async () => {
    const errorSpy = vi.spyOn(logger, "error").mockImplementation(() => {});

    const result = await makeAPICall("GET", "//evil.example/steal");

    expect(result).toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      "Invalid API path",
      expect.objectContaining({ api_path: "//evil.example/steal" }),
    );
  });

  it("@FUT51 | rejects non-leading-slash relative paths", async () => {
    const errorSpy = vi.spyOn(logger, "error").mockImplementation(() => {});

    const result = await makeAPICall("GET", "folders");

    expect(result).toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      "Invalid API path",
      expect.objectContaining({ api_path: "folders" }),
    );
  });

  it("@FUT52 | allows valid relative API paths through to fetch", async () => {
    const result = await makeAPICall("GET", "/folders");

    expect(result).not.toBeNull();
    expect(result.ok).toBe(true);
    const body = await result.json();
    expect(body).toEqual([{ id: 1, title: "Test Folder" }]);
  });

  it("@FUT53 | rejects API paths containing path traversal sequences", async () => {
    const errorSpy = vi.spyOn(logger, "error").mockImplementation(() => {});
    const result = await makeAPICall("GET", "/folders/../etc/passwd");
    expect(result).toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      "Invalid API path",
      expect.objectContaining({ api_path: "/folders/../etc/passwd" }),
    );
  });
});

// FUT54 must remain last: afterAll resets the module registry via vi.resetModules()
describe("makeAPICall — relative base (VITE_API_URL unset)", () => {
  let makeAPICallFresh;
  beforeAll(async () => {
    vi.stubEnv("VITE_API_URL", ""); // MUST come before resetModules
    vi.resetModules();
    const mod = await import("@/useApi");
    makeAPICallFresh = mod.makeAPICall;
  });
  afterAll(() => {
    vi.unstubAllEnvs();
    vi.resetModules();
  });
  it("@FUT54 | uses relative /api base when VITE_API_URL is unset", async () => {
    const { logger: freshLogger } = await import("@/logger");
    const errorSpy = vi
      .spyOn(freshLogger, "error")
      .mockImplementation(() => {});
    // result is null because Node fetch rejects relative URLs with a TypeError — not a test misconfiguration
    const result = await makeAPICallFresh("GET", "/folders");
    expect(result).toBeNull();
    // url: "/api/folders" confirms line 39 (relative return) executed
    expect(errorSpy).toHaveBeenCalledWith(
      "GET request failed",
      expect.objectContaining({ url: "/api/folders" }),
    );
  });
});
