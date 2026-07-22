import { AppLayout } from "../components/layout/AppLayout";
import { ComputerList } from "../components/computers/ComputerList";
import { EmptyState } from "../components/feedback/EmptyState";
import { ErrorState } from "../components/feedback/ErrorState";
import { LoadingState } from "../components/feedback/LoadingState";
import { useComputers } from "../hooks/useComputers";

export function DashboardPage() {
  const query = useComputers();

  return (
    <AppLayout title="Computadores">
      {query.isPending ? (
        <LoadingState message="Carregando computadores..." />
      ) : query.isError ? (
        <ErrorState message={query.error.message} />
      ) : query.data.length === 0 ? (
        <EmptyState message="Nenhum computador registrado ainda." />
      ) : (
        <ComputerList computers={query.data} />
      )}
    </AppLayout>
  );
}
