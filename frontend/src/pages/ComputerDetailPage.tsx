import { useParams } from "react-router-dom";

import { AppLayout } from "../components/layout/AppLayout";
import { EmptyState } from "../components/feedback/EmptyState";
import { ErrorState } from "../components/feedback/ErrorState";
import { LoadingState } from "../components/feedback/LoadingState";
import { MetricHistoryTable } from "../components/metrics/MetricHistoryTable";
import { useComputers } from "../hooks/useComputers";
import { useMetricHistory } from "../hooks/useMetricHistory";
import { formatDateTime } from "../lib/formatDate";

export function ComputerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const computerId = Number(id);

  const computersQuery = useComputers();
  const metricsQuery = useMetricHistory(computerId);

  const computer = computersQuery.data?.find((item) => item.id === computerId);
  const title = computer?.hostname ?? "Computador";

  return (
    <AppLayout title={title}>
      {computersQuery.isPending ? (
        <LoadingState message="Carregando computador..." />
      ) : computersQuery.isError ? (
        <ErrorState message={computersQuery.error.message} />
      ) : !computer ? (
        <ErrorState message="Computador não encontrado." />
      ) : (
        <div className="space-y-6">
          <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="text-sm font-semibold text-slate-900">{computer.hostname}</div>
            <div className="mt-1 text-xs text-slate-500">
              Registrado em {formatDateTime(computer.created_at)}
            </div>
          </div>

          <div>
            <h2 className="mb-2 text-sm font-medium text-slate-700">Histórico de métricas</h2>
            {metricsQuery.isPending ? (
              <LoadingState message="Carregando métricas..." />
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
