# Sentinel Frontend

Dashboard web para visualização das métricas coletadas pelo Sentinel: lista de computadores registrados e histórico de métricas de cada um.

> Status: Fase 2 concluída. Dashboard consumindo a API real (React Query), com listagem de computadores e página de detalhe/histórico de métricas.

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
  hooks/        hooks de React Query que encapsulam as chamadas de api/
  components/
    layout/     AppLayout, Sidebar, Header
    computers/  ComputerCard, ComputerList
    metrics/    MetricHistoryTable
    feedback/   LoadingState, ErrorState, EmptyState
  pages/        DashboardPage (/), ComputerDetailPage (/computers/:id)
  lib/          utilitários compartilhados (ex.: formatação de data)
  router.tsx        definição das rotas
  queryClient.ts    instância do QueryClient
```

## Lint e build

```bash
npm run lint
npm run build
```
