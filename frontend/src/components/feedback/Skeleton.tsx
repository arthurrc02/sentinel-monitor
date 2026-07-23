interface SkeletonProps {
  className?: string;
}

/** Primitivo de carregamento (pulsing block). Composto pelos skeletons de cada tela. */
export function Skeleton({ className = "" }: SkeletonProps) {
  return <div className={`animate-pulse rounded bg-slate-200 ${className}`} aria-hidden="true" />;
}
