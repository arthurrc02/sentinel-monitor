# Arquitetura

## Visão geral

O Sentinel é um monorepo com três aplicações independentes:

| Pasta | Stack | Responsabilidade |
|---|---|---|
| `agent/` | Python + uv | Coleta métricas da máquina monitorada e as envia ao backend. |
| `backend/` | FastAPI + SQLAlchemy + Alembic + PostgreSQL + uv | Recebe, persiste e expõe métricas via API REST. |
| `frontend/` | React + Vite + TypeScript + Tailwind CSS | Dashboard web que consome a API e exibe as métricas. |

Fluxo de dados: **Agent → Backend (ingestão) → PostgreSQL → Backend (consulta) → Frontend**.

O PostgreSQL de desenvolvimento roda via `docker-compose.yml` na raiz do monorepo.

## Backend

Arquitetura em camadas:

```
Router (HTTP) → Service (regra de negócio) → Repository (SQLAlchemy) → Model → PostgreSQL
                                     ↑
                          Schema (Pydantic, validação)
```

- `app/routers/`: endpoints HTTP, sem lógica de negócio.
- `app/services/`: regras de negócio; lança exceções de domínio e não conhece FastAPI.
- `app/repositories/`: única camada que fala SQLAlchemy/Session.
- `app/models/`: entidades ORM (`Computer`, `Metric`).
- `app/schemas/`: DTOs Pydantic de entrada/saída.
- `app/core/`: configuração (`config.py`), exceções de domínio, exception handlers (traduzem exceções de domínio em respostas HTTP) e providers de injeção de dependência.
- `app/db/`: base declarativa e sessão do SQLAlchemy.
- `alembic/`: migrations do banco.

CORS liberado para a origem do frontend em desenvolvimento (`http://localhost:5173`), configurável via `SENTINEL_CORS_ORIGINS`.

### Status online/offline

`GET /computers` calcula, a cada chamada, `last_seen_at` (timestamp da métrica mais recente do computador, via `JOIN` com `MAX(collected_at)` em `app/repositories/computer_repository.py`) e `is_online` (`last_seen_at` dentro de `SENTINEL_OFFLINE_THRESHOLD_SECONDS`, calculado em `app/services/computer_service.py`). Nenhum dado é armazenado a mais — é sempre recalculado na leitura, então nunca fica desatualizado. `metrics` tem um índice composto `(computer_id, collected_at)` para essa consulta e para o histórico não ficarem lentos com o crescimento da tabela.

### Logs e tratamento de erro

`app/core/logging_config.py` (mesmo formatador JSON do Agent) registra eventos de negócio nos `services` — computador registrado, tentativa de hostname duplicado, referência a computador inexistente. `POST /computers` também trata a corrida entre duas requisições simultâneas com o mesmo hostname (`IntegrityError` do banco é traduzido para `409`, não vaza como erro 500) e normaliza espaços nas pontas do hostname antes de validar.

## Frontend

```
Route (React Router) → Page → Hook (React Query, com polling) → api/ (fetch) → Backend
                          ↓
                    Componentes (layout / domínio / feedback)
```

- `src/api/`: única camada que conhece o formato HTTP da API.
- `src/hooks/`: `useComputers`/`useMetricHistory` (React Query com `refetchInterval`) e `usePollingInterval` (preferência do usuário, persistida em `localStorage`, compartilhada entre páginas).
- `src/components/`: `layout/` (AppLayout, Sidebar, Header), `computers/` (lista, card, badge de status, skeleton), `metrics/` (tabela de histórico e seu skeleton), `feedback/` (`Skeleton`, `ErrorState`, `EmptyState`), `common/` (`PollingIntervalSelect`, reusado entre páginas).
- `src/pages/`: páginas roteadas (`DashboardPage` — busca e ordenação client-side sobre a lista já carregada; `ComputerDetailPage`).
- `src/lib/`: utilitários compartilhados (`formatDate`, `formatRelativeTime`, `pollingIntervals`).
- Estilização com Tailwind CSS v4 (via `@tailwindcss/vite`), sem sistema de design customizado.
- Atualização automática via polling (não WebSocket/SSE): cada página busca dados novos no intervalo escolhido pelo usuário; o carregamento inicial mostra skeletons, atualizações em segundo plano mostram só um indicador sutil no cabeçalho, sem substituir o conteúdo já exibido.
- Testes: Vitest + Testing Library (`*.test.ts(x)` ao lado do arquivo testado), cobrindo utilitários puros e componentes/hooks pequenos. ESLint inclui `eslint-plugin-jsx-a11y` para pegar problemas de acessibilidade automaticamente.

## Agent

Processo que roda na máquina monitorada: se registra no backend e envia métricas de CPU, memória e disco a cada `SENTINEL_COLLECTION_INTERVAL_SECONDS`. Execução síncrona (loop + `time.sleep`), sem `asyncio`. Ver diagrama de fluxo em [`docs/diagrams/system-flow.md`](diagrams/system-flow.md).

```
main.py (orquestração)
  → services/registration_service.py  → client/sentinel_client.py (POST/GET /computers)
  → services/collection_service.py    → collectors/{cpu,memory,disk}.py (psutil)
                                       → client/sentinel_client.py (POST /computers/{id}/metrics)
```

- `config.py`: `Settings` (pydantic-settings), mesmo padrão do backend.
- `exceptions.py`: `SentinelApiError` — erro de API com `status_code`.
- `logging_config.py`: logs estruturados em JSON no stdout.
- `models/`: `Computer` e `MetricSample`, espelhando os schemas do backend.
- `collectors/`: uma função por métrica (`collect_cpu_percent`, `collect_memory_percent`, `collect_disk_percent`, esse último sobre `SENTINEL_DISK_PATH`), sem abstração de plugin — não há registro dinâmico de coletores.
- `client/sentinel_client.py`: único ponto que fala HTTP com o backend; cada requisição é retentada com backoff exponencial (erro de rede ou `5xx`; `4xx` não é retentado), e cada nova tentativa é logada (nível WARNING) antes de esperar.
- `services/registration_service.py`: registra o computador ou, se já existir (`409`), localiza seu `id` via `GET /computers`.
- `services/collection_service.py`: agrega os três coletores em uma `MetricSample`.

Falha ao registrar no startup: o agent bloqueia e tenta de novo indefinidamente. Falha ao enviar uma métrica já registrada: loga o erro e segue para o próximo ciclo, sem derrubar o processo.

## Qualidade e infraestrutura

- Lint: ruff (Python, com `E`/`F`/`I`/`UP`/`B`/`SIM`), ESLint (TypeScript, com `jsx-a11y`).
- Tipagem estática: mypy em modo strict (agent e backend), `tsc` (frontend).
- Testes: pytest (agent e backend), Vitest + Testing Library (frontend).
- CI: GitHub Actions roda lint, typecheck e testes das três aplicações a cada push/PR.
- Gerenciador de dependências Python: uv.
