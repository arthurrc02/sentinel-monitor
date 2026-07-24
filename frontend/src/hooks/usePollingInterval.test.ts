import { act, renderHook } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";

import { DEFAULT_POLLING_INTERVAL_MS } from "../lib/pollingIntervals";
import { usePollingInterval } from "./usePollingInterval";

const STORAGE_KEY = "sentinel:polling-interval-ms";

describe("usePollingInterval", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("usa o valor padrão quando nada foi salvo", () => {
    const { result } = renderHook(() => usePollingInterval());

    expect(result.current[0]).toBe(DEFAULT_POLLING_INTERVAL_MS);
  });

  it("lê um valor previamente salvo no localStorage", () => {
    localStorage.setItem(STORAGE_KEY, "30000");

    const { result } = renderHook(() => usePollingInterval());

    expect(result.current[0]).toBe(30_000);
  });

  it("ignora valor inválido salvo e usa o padrão", () => {
    localStorage.setItem(STORAGE_KEY, "não-é-um-número");

    const { result } = renderHook(() => usePollingInterval());

    expect(result.current[0]).toBe(DEFAULT_POLLING_INTERVAL_MS);
  });

  it("atualiza o estado e persiste no localStorage ao chamar o setter", () => {
    const { result } = renderHook(() => usePollingInterval());

    act(() => {
      result.current[1](5_000);
    });

    expect(result.current[0]).toBe(5_000);
    expect(localStorage.getItem(STORAGE_KEY)).toBe("5000");
  });
});
