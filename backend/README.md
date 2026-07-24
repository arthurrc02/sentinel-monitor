# Sentinel Backend

API responsável por receber métricas do Sentinel Agent, persisti-las (PostgreSQL) e disponibilizá-las para o frontend.

> Status: Fase 5 concluída (Release Candidate 1.0). Cadastro de computadores, ingestão/consulta de métricas e cálculo de status online/offline, com persistência em PostgreSQL via SQLAlchemy + Alembic, logging estruturado e tratamento de corrida no registro.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (para rodar o PostgreSQL local)

## Instalação

```bash
uv sync
```

Copie o arquivo de variáveis de ambiente de exemplo:

```bash
cp .env.example .env
```

## Banco de dados

Suba o PostgreSQL local via Docker Compose (arquivo na raiz do monorepo):

```bash
docker compose up -d postgres
```

Aplique as migrations:

```bash
uv run alembic upgrade head
```

## Execução

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está no ar |
| POST | `/computers` | Registra um computador |
| GET | `/computers` | Lista os computadores registrados, com `last_seen_at`/`is_online` calculados na hora |
| POST | `/computers/{id}/metrics` | Registra uma amostra de métricas para um computador |
| GET | `/computers/{id}/metrics` | Consulta o histórico de métricas de um computador (aceita `?limit=`, padrão 100, máx. 1000) |

Exemplos com `curl`:

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/computers \
  -H "Content-Type: application/json" \
  -d '{"hostname": "pc-01"}'

curl http://localhost:8000/computers

curl -X POST http://localhost:8000/computers/1/metrics \
  -H "Content-Type: application/json" \
  -d '{"cpu_percent": 42.5, "memory_percent": 60.0, "disk_percent": 75.3, "collected_at": "2026-07-22T10:00:00Z"}'

curl http://localhost:8000/computers/1/metrics
```

`hostname` é normalizado (sem espaços nas pontas) antes de salvar. Registrar um `hostname` já existente retorna `409` (inclusive em corrida entre requisições simultâneas); referenciar um computador inexistente em qualquer rota de métricas retorna `404`.

## Lint e tipagem

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
```

## Testes

```bash
uv run pytest
```
