import { apiGet } from "./client";
import type { Metric } from "./types";

export function fetchMetricHistory(computerId: number, limit = 100): Promise<Metric[]> {
  return apiGet<Metric[]>(`/computers/${computerId}/metrics?limit=${limit}`);
}
