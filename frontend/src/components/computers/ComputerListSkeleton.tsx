import { Skeleton } from "../feedback/Skeleton";

function ComputerCardSkeleton() {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <Skeleton className="h-4 w-2/3" />
      <Skeleton className="mt-2 h-3 w-1/3" />
      <Skeleton className="mt-3 h-3 w-1/2" />
    </div>
  );
}

export function ComputerListSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }, (_, index) => (
        <ComputerCardSkeleton key={index} />
      ))}
    </div>
  );
}
