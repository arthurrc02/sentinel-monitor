import { apiGet } from "./client";
import type { Computer } from "./types";

export function fetchComputers(): Promise<Computer[]> {
  return apiGet<Computer[]>("/computers");
}
