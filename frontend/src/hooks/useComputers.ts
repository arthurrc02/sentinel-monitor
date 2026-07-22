import { useQuery } from "@tanstack/react-query";

import { fetchComputers } from "../api/computers";

export function useComputers() {
  return useQuery({
    queryKey: ["computers"],
    queryFn: fetchComputers,
  });
}
