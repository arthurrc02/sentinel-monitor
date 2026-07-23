import { useMemo, useState } from "react";

import type { Computer } from "../api/types";
import { PollingIntervalSelect } from "../components/common/PollingIntervalSelect";
import { ComputerList } from "../components/computers/ComputerList";
import { ComputerListSkeleton } from "../components/computers/ComputerListSkeleton";
import { EmptyState } from "../components/feedback/EmptyState";
import { ErrorState } from "../components/feedback/ErrorState";
import { AppLayout } from "../components/layout/AppLayout";
import { useComputers } from "../hooks/useComputers";
import { usePollingInterval } from "../hooks/usePollingInterval";

type SortBy = "hostname" | "lastSeen";

function sortComputers(computers: Computer[], sortBy: SortBy): Computer[] {
  const sorted = [...computers];
  if (sortBy === "hostname") {
    sorted.sort((a, b) => a.hostname.localeCompare(b.hostname));
    return sorted;
  }
  sorted.sort((a, b) => {
    if (!a.last_seen_at && !b.last_seen_at) return 0;
    if (!a.last_seen_at) return 1;
    if (!b.last_seen_at) return -1;
    return new Date(b.last_seen_at).getTime() - new Date(a.last_seen_at).getTime();
  });
  return sorted;
}

export function DashboardPage() {
  const [pollingIntervalMs, setPollingIntervalMs] = usePollingInterval();
  const query = useComputers(pollingIntervalMs);
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState<SortBy>("hostname");

  const visibleComputers = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    const filtered = (query.data ?? []).filter((computer) =>
      computer.hostname.toLowerCase().includes(term),
    );
    return sortComputers(filtered, sortBy);
  }, [query.data, searchTerm, sortBy]);

  return (
    <AppLayout title="Computadores" isRefreshing={query.isFetching && !query.isPending}>
      <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div className="flex flex-col gap-1">
          <label htmlFor="computer-search" className="text-sm text-slate-600">
            Buscar por hostname
          </label>
          <input
            id="computer-search"
            type="search"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="ex.: pc-01"
            className="rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-700"
          />
        </div>
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <label htmlFor="computer-sort" className="text-sm text-slate-600">
              Ordenar por
            </label>
            <select
              id="computer-sort"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value as SortBy)}
              className="rounded-md border border-slate-300 bg-white px-2 py-1 text-sm text-slate-700"
            >
              <option value="hostname">Hostname</option>
              <option value="lastSeen">Última atualização</option>
            </select>
          </div>
          <PollingIntervalSelect value={pollingIntervalMs} onChange={setPollingIntervalMs} />
        </div>
      </div>

      {query.isPending ? (
        <ComputerListSkeleton />
      ) : query.isError ? (
        <ErrorState message={query.error.message} />
      ) : visibleComputers.length === 0 ? (
        <EmptyState
          message={
            searchTerm
              ? "Nenhum computador encontrado para essa busca."
              : "Nenhum computador registrado ainda."
          }
        />
      ) : (
        <ComputerList computers={visibleComputers} />
      )}
    </AppLayout>
  );
}
