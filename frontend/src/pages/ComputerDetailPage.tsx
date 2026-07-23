import { useParams } from "react-router-dom";

import { PollingIntervalSelect } from "../components/common/PollingIntervalSelect";
import { ComputerStatusBadge } from "../components/computers/ComputerStatusBadge";
import { EmptyState } from "../components/feedback/EmptyState";
import { ErrorState } from "../components/feedback/ErrorState";
import { Skeleton } from "../components/feedback/Skeleton";
import { AppLayout } from "../components/layout/AppLayout";
import { MetricHistoryTable } from "../components/metrics/MetricHistoryTable";
import { MetricHistoryTableSkeleton } from "../components/metrics/MetricHistoryTableSkeleton";
import { useComputers } from "../hooks/useComputers";
import { useMetricHistory } from "../hooks/useMetricHistory";
import { usePollingInterval } from "../hooks/usePollingInterval";
import { formatDateTime } from "../lib/formatDate";
import { formatRelativeTime } from "../lib/formatRelativeTime";

export function ComputerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const computerId = Number(id);

  const [pollingIntervalMs, setPollingIntervalMs] = usePollingInterval();
  const computersQuery = useComputers(pollingIntervalMs);
  const metricsQuery = useMetricHistory(computerId, pollingIntervalMs);

  const computer = computersQuery.data?.find((item) => item.id === computerId);
  const title = computer?.hostname ?? "Computador";
  const isRefreshing =
    (computersQuery.isFetching && !computersQuery.isPending) ||
    (metricsQuery.isFetching && !metricsQuery.isPending);

  return (
    <AppLayout title={title} isRefreshing={isRefreshing}>
      {computersQuery.isPending ? (
        <div className="space-y-2 rounded-lg border border-slate-200 bg-white p-4">
          <Skeleton className="h-4 w-1/3" />
          <Skeleton className="h-3 w-1/2" />
        </div>
      ) : computersQuery.isError ? (
        <ErrorState message={computersQuery.error.message} />
      ) : !computer ? (
        <ErrorState message="Computador não encontrado." />
      ) : (
        <div className="space-y-6">
          <div className="flex items-center justify-end">
            <PollingIntervalSelect value={pollingIntervalMs} onChange={setPollingIntervalMs} />
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm font-semibold text-slate-900">{computer.hostname}</div>
              <ComputerStatusBadge isOnline={computer.is_online} />
            </div>
            <div className="mt-1 text-xs text-slate-500">
              Registrado em {formatDateTime(computer.created_at)}
            </div>
            <div className="mt-1 text-xs text-slate-500">
              Última atualização: {formatRelativeTime(computer.last_seen_at)}
            </div>
          </div>

          <div>
            <h2 className="mb-2 text-sm font-medium text-slate-700">Histórico de métricas</h2>
            {metricsQuery.isPending ? (
              <MetricHistoryTableSkeleton />
            ) : metricsQuery.isError ? (
              <ErrorState message={metricsQuery.error.message} />
            ) : metricsQuery.data.length === 0 ? (
              <EmptyState message="Nenhuma métrica registrada para este computador ainda." />
            ) : (
              <MetricHistoryTable metrics={metricsQuery.data} />
            )}
          </div>
        </div>
      )}
    </AppLayout>
  );
}
