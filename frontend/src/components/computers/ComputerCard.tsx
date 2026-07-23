import { Link } from "react-router-dom";

import type { Computer } from "../../api/types";
import { formatRelativeTime } from "../../lib/formatRelativeTime";
import { ComputerStatusBadge } from "./ComputerStatusBadge";

interface ComputerCardProps {
  computer: Computer;
}

export function ComputerCard({ computer }: ComputerCardProps) {
  return (
    <Link
      to={`/computers/${computer.id}`}
      className="block rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:border-slate-300 hover:shadow-md"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="text-sm font-semibold text-slate-900">{computer.hostname}</div>
        <ComputerStatusBadge isOnline={computer.is_online} />
      </div>
      <div className="mt-1 text-xs text-slate-500">
        Última atualização: {formatRelativeTime(computer.last_seen_at)}
      </div>
    </Link>
  );
}
