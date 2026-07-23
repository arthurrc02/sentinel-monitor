export interface PollingIntervalOption {
  label: string;
  value: number;
}

export const POLLING_INTERVAL_OPTIONS: PollingIntervalOption[] = [
  { label: "5s", value: 5_000 },
  { label: "10s", value: 10_000 },
  { label: "30s", value: 30_000 },
  { label: "60s", value: 60_000 },
];

export const DEFAULT_POLLING_INTERVAL_MS = 10_000;
