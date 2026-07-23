import { useQuery } from "@tanstack/react-query";

import { fetchComputers } from "../api/computers";

export function useComputers(refetchIntervalMs: number) {
  return useQuery({
    queryKey: ["computers"],
    queryFn: fetchComputers,
    refetchInterval: refetchIntervalMs,
  });
}
