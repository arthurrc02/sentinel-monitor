import { describe, expect, it } from "vitest";

import { formatDateTime } from "./formatDate";

describe("formatDateTime", () => {
  it("formata data e hora no padrão pt-BR", () => {
    expect(formatDateTime("2026-07-23T09:05:00.000Z")).toBe("23/07/2026, 09:05");
  });
});
