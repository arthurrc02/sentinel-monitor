# Sentinel Backend

API responsável por receber métricas do Sentinel Agent, persisti-las (PostgreSQL) e disponibilizá-las para o frontend.

> Status: scaffolding inicial. A conexão com o banco e o Alembic estão configurados, mas ainda não há nenhum model ou migration — isso será implementado na Sprint 1. Endpoints de métricas também ainda não existem.

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

Aplique as migrations (nenhuma existe ainda até a Sprint 1):

```bash
uv run alembic upgrade head
```

## Execução

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

## Lint

```bash
uv run ruff check .
uv run ruff format .
```
