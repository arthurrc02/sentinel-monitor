import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { formatRelativeTime } from "./formatRelativeTime";

describe("formatRelativeTime", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-07-23T12:00:00Z"));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("retorna 'Nunca' quando não há data", () => {
    expect(formatRelativeTime(null)).toBe("Nunca");
  });

  it("formata minutos no passado", () => {
    const fiveMinutesAgo = new Date("2026-07-23T11:55:00Z").toISOString();
    expect(formatRelativeTime(fiveMinutesAgo)).toBe("há 5 minutos");
  });

  it("formata horas no passado", () => {
    const twoHoursAgo = new Date("2026-07-23T10:00:00Z").toISOString();
    expect(formatRelativeTime(twoHoursAgo)).toBe("há 2 horas");
  });

  it("formata um instante muito recente como 'agora'", () => {
    const justNow = new Date("2026-07-23T12:00:00Z").toISOString();
    expect(formatRelativeTime(justNow)).toBe("agora");
  });
});
