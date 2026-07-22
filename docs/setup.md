# Setup

Guia rápido para rodar o Sentinel localmente. Cada aplicação também tem instruções detalhadas no seu próprio `README.md`.

## Requisitos

- Python 3.11+ e [uv](https://docs.astral.sh/uv/)
- Node.js 20+
- [Docker](https://www.docker.com/)

## 1. Banco de dados

```bash
docker compose up -d postgres
```

## 2. Backend

```bash
cd backend
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

API em `http://localhost:8000` (documentação interativa em `/docs`).

## 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Dashboard em `http://localhost:5173`.

## 4. Agent

Com o backend rodando:

```bash
cd agent
uv sync
cp .env.example .env
uv run sentinel-agent
```

O agent se registra automaticamente e passa a enviar CPU/memória/disco a cada `SENTINEL_COLLECTION_INTERVAL_SECONDS` (padrão 60s). `Ctrl+C` encerra. Ver `agent/README.md` para as variáveis de ambiente disponíveis.

## Qualidade

Cada aplicação tem seus próprios comandos de lint/typecheck/teste — ver os `README.md` de `agent/`, `backend/` e `frontend/`. O CI (`.github/workflows/ci.yml`) roda todos eles a cada push/PR.
