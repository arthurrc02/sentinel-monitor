import { POLLING_INTERVAL_OPTIONS } from "../../lib/pollingIntervals";

interface PollingIntervalSelectProps {
  value: number;
  onChange: (value: number) => void;
}

export function PollingIntervalSelect({ value, onChange }: PollingIntervalSelectProps) {
  return (
    <div className="flex items-center gap-2">
      <label htmlFor="polling-interval" className="text-sm text-slate-600">
        Atualizar a cada
      </label>
      <select
        id="polling-interval"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="rounded-md border border-slate-300 bg-white px-2 py-1 text-sm text-slate-700"
      >
        {POLLING_INTERVAL_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
