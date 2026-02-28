import { describe, it, expect, vi, beforeEach } from "vitest";
import { makeAPICall } from "@/useApi";

describe("makeAPICall", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("calls fetch for GET requests without JSON body/options", async () => {
    const response = { ok: true };
    fetch.mockResolvedValue(response);

    const result = await makeAPICall("GET", "/folders");

    expect(fetch).toHaveBeenCalledWith("http://localhost:8000/folders");
    expect(result).toBe(response);
  });

  it("uppercases http method before request", async () => {
    const response = { ok: true };
    fetch.mockResolvedValue(response);

    await makeAPICall("post", "/folders", { title: "Work" });

    expect(fetch).toHaveBeenCalledWith("http://localhost:8000/folders", {
      method: "POST",
      body: JSON.stringify({ title: "Work" }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  it("returns null when GET fetch throws", async () => {
    vi.spyOn(console, "log").mockImplementation(() => {});
    fetch.mockRejectedValue(new Error("network error"));

    const result = await makeAPICall("GET", "/folders");

    expect(result).toBeNull();
  });

  it("returns null when non-GET fetch throws", async () => {
    vi.spyOn(console, "log").mockImplementation(() => {});
    fetch.mockRejectedValue(new Error("network error"));

    const result = await makeAPICall("PUT", "/folders/1", { title: "x" });

    expect(result).toBeNull();
  });
});
