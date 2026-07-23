import { useQuery } from "@tanstack/react-query";

import { fetchMetricHistory } from "../api/metrics";

export function useMetricHistory(computerId: number, refetchIntervalMs: number) {
  return useQuery({
    queryKey: ["computers", computerId, "metrics"],
    queryFn: () => fetchMetricHistory(computerId),
    refetchInterval: refetchIntervalMs,
  });
}
