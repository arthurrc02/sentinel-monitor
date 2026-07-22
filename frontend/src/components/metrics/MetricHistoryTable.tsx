import type { Metric } from "../../api/types";
import { formatDateTime } from "../../lib/formatDate";

interface MetricHistoryTableProps {
  metrics: Metric[];
}

export function MetricHistoryTable({ metrics }: MetricHistoryTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs font-medium uppercase text-slate-500">
          <tr>
            <th className="px-4 py-2">Coletado em</th>
            <th className="px-4 py-2">CPU</th>
            <th className="px-4 py-2">Memória</th>
            <th className="px-4 py-2">Disco</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {metrics.map((metric) => (
            <tr key={metric.id}>
              <td className="px-4 py-2 text-slate-600">{formatDateTime(metric.collected_at)}</td>
              <td className="px-4 py-2 text-slate-900">{metric.cpu_percent.toFixed(1)}%</td>
              <td className="px-4 py-2 text-slate-900">{metric.memory_percent.toFixed(1)}%</td>
              <td className="px-4 py-2 text-slate-900">{metric.disk_percent.toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
