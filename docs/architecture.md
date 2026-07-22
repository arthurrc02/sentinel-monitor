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

## Frontend

```
Route (React Router) → Page → Hook (React Query) → api/ (fetch) → Backend
                          ↓
                    Componentes (layout / domínio / feedback)
```

- `src/api/`: única camada que conhece o formato HTTP da API.
- `src/hooks/`: hooks de React Query que encapsulam as chamadas de `api/`.
- `src/components/`: `layout/` (AppLayout, Sidebar, Header), `computers/`, `metrics/`, `feedback/` (estados de loading/erro/vazio).
- `src/pages/`: páginas roteadas (`DashboardPage`, `ComputerDetailPage`).
- Estilização com Tailwind CSS v4 (via `@tailwindcss/vite`), sem sistema de design customizado.

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
- `collectors/`: uma função por métrica (`collect_cpu_percent`, `collect_memory_percent`, `collect_disk_percent`), sem abstração de plugin — não há registro dinâmico de coletores.
- `client/sentinel_client.py`: único ponto que fala HTTP com o backend; cada requisição é retentada com backoff exponencial (erro de rede ou `5xx`; `4xx` não é retentado).
- `services/registration_service.py`: registra o computador ou, se já existir (`409`), localiza seu `id` via `GET /computers`.
- `services/collection_service.py`: agrega os três coletores em uma `MetricSample`.

Falha ao registrar no startup: o agent bloqueia e tenta de novo indefinidamente. Falha ao enviar uma métrica já registrada: loga o erro e segue para o próximo ciclo, sem derrubar o processo.

## Qualidade e infraestrutura

- Lint: ruff (Python), ESLint (TypeScript).
- Tipagem estática: mypy em modo strict (agent e backend), `tsc` (frontend).
- Testes: pytest (agent e backend).
- CI: GitHub Actions roda lint, typecheck e testes das três aplicações a cada push/PR.
- Gerenciador de dependências Python: uv.
