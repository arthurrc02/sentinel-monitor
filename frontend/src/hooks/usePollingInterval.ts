import { useState } from "react";

import { DEFAULT_POLLING_INTERVAL_MS } from "../lib/pollingIntervals";

const STORAGE_KEY = "sentinel:polling-interval-ms";

function readStoredInterval(): number {
  const stored = localStorage.getItem(STORAGE_KEY);
  const parsed = stored ? Number(stored) : NaN;
  return Number.isFinite(parsed) && parsed > 0 ? parsed : DEFAULT_POLLING_INTERVAL_MS;
}

/** Intervalo de polling escolhido pelo usuário, persistido e compartilhado entre páginas. */
export function usePollingInterval(): [number, (value: number) => void] {
  const [intervalMs, setIntervalMsState] = useState<number>(readStoredInterval);

  const setIntervalMs = (value: number): void => {
    setIntervalMsState(value);
    localStorage.setItem(STORAGE_KEY, String(value));
  };

  return [intervalMs, setIntervalMs];
}
