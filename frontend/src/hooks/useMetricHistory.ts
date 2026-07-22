import { useQuery } from "@tanstack/react-query";

import { fetchMetricHistory } from "../api/metrics";

export function useMetricHistory(computerId: number) {
  return useQuery({
    queryKey: ["computers", computerId, "metrics"],
    queryFn: () => fetchMetricHistory(computerId),
  });
}
