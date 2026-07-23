interface ComputerStatusBadgeProps {
  isOnline: boolean;
}

export function ComputerStatusBadge({ isOnline }: ComputerStatusBadgeProps) {
  const label = isOnline ? "Online" : "Offline";

  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-medium ${
        isOnline ? "text-emerald-700" : "text-slate-500"
      }`}
    >
      <span
        className={`h-2 w-2 rounded-full ${isOnline ? "bg-emerald-500" : "bg-slate-400"}`}
        aria-hidden="true"
      />
      {label}
    </span>
  );
}
