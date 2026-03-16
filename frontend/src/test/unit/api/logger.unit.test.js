import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { logger } from "@/logger";

describe("logger", () => {
  let debugSpy;
  let infoSpy;
  let warnSpy;
  let errorSpy;

  beforeEach(() => {
    debugSpy = vi
      .spyOn(globalThis.console, "debug")
      .mockImplementation(() => {});
    infoSpy = vi.spyOn(globalThis.console, "info").mockImplementation(() => {});
    warnSpy = vi.spyOn(globalThis.console, "warn").mockImplementation(() => {});
    errorSpy = vi
      .spyOn(globalThis.console, "error")
      .mockImplementation(() => {});
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("@FUT45 | logger.debug calls console.debug in dev mode", () => {
    logger.debug("test debug");
    expect(debugSpy).toHaveBeenCalledWith("test debug");
  });

  it("@FUT46 | logger.info calls console.info in dev mode", () => {
    logger.info("test info");
    expect(infoSpy).toHaveBeenCalledWith("test info");
  });

  it("@FUT47 | logger.warn always calls console.warn", () => {
    logger.warn("test warning");
    expect(warnSpy).toHaveBeenCalledWith("test warning");
  });

  it("@FUT48 | logger.error always calls console.error", () => {
    logger.error("something broke");
    expect(errorSpy).toHaveBeenCalledWith("something broke");
  });
});
