export interface Computer {
  id: number;
  hostname: string;
  created_at: string;
  last_seen_at: string | null;
  is_online: boolean;
}

export interface Metric {
  id: number;
  computer_id: number;
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  collected_at: string;
  created_at: string;
}
