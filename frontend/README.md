# Sentinel Frontend

Dashboard web para visualização das métricas coletadas pelo Sentinel: lista de computadores registrados e histórico de métricas de cada um.

> Status: Fase 5 concluída (Release Candidate 1.0). Dashboard consumindo a API real (React Query) com atualização automática por polling, status online/offline, busca/ordenação e estados de carregamento/erro tratados. Testes automatizados com Vitest + Testing Library.

## Requisitos

- Node.js 20+
- Backend do Sentinel rodando (veja [`backend/README.md`](../backend/README.md))

## Instalação

```bash
npm install
```

Copie o arquivo de variáveis de ambiente de exemplo:

```bash
cp .env.example .env
```

`VITE_API_URL` aponta para a API do backend (padrão `http://localhost:8000`).

## Execução

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`.

## Estrutura

```
src/
  api/          cliente HTTP e funções de acesso à API (única camada que conhece o formato HTTP)
  hooks/        useComputers/useMetricHistory (React Query + polling), usePollingInterval
  components/
    layout/     AppLayout, Sidebar, Header
    computers/  ComputerCard, ComputerList (+ skeleton), ComputerStatusBadge
    metrics/    MetricHistoryTable (+ skeleton)
    feedback/   Skeleton, ErrorState, EmptyState
    common/     PollingIntervalSelect (reusado entre páginas)
  pages/        DashboardPage (/, com busca e ordenação), ComputerDetailPage (/computers/:id)
  lib/          utilitários compartilhados (formatação de data/hora relativa, opções de polling)
  router.tsx        definição das rotas
  queryClient.ts    instância do QueryClient
```

O dashboard atualiza sozinho por polling — o intervalo é escolhido pelo usuário (seletor no topo de cada página) e persiste entre navegações via `localStorage`.

## Lint, testes e build

```bash
npm run lint
npm run test
npm run build
```
