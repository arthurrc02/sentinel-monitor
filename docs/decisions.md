# Decisões técnicas

Registro das decisões técnicas relevantes já tomadas no projeto, na ordem em que foram feitas. Cada entrada documenta uma decisão já implementada — não intenções futuras.

## uv como gerenciador de dependências Python

Substituiu Poetry em `agent/` e `backend/`. `pyproject.toml` no formato PEP 621, com `[dependency-groups]` para dependências de desenvolvimento.

## SQLAlchemy + Alembic + PostgreSQL

Persistência do backend. Conexão configurada via `SENTINEL_DATABASE_URL`. PostgreSQL de desenvolvimento disponibilizado via Docker Compose.

## Arquitetura em camadas no backend

Routers → Services → Repositories → Models, com schemas Pydantic para validação de entrada/saída e exceções de domínio traduzidas para HTTP por exception handlers centralizados (`app/core/exception_handlers.py`). Objetivo: manter services e repositories livres de FastAPI.

## Sem endpoint `GET /computers/{id}`

O frontend deriva os dados de um computador a partir da lista já cacheada (`GET /computers`) via React Query, em vez de criar um endpoint dedicado só para a página de detalhe.

## CORS liberado para o frontend em desenvolvimento

`CORSMiddleware` no backend libera `http://localhost:5173` (configurável via `SENTINEL_CORS_ORIGINS`), necessário para o dashboard consumir a API a partir do navegador.

## React Query para consumo de dados no frontend

Todo acesso a dados remotos passa por hooks de React Query (`src/hooks/`), que encapsulam a camada `api/`. Sem Redux ou outro gerenciador de estado global.

## Tailwind CSS v4 via `@tailwindcss/vite`

Estilização do frontend com utilitários Tailwind, sem `tailwind.config.js`/`postcss.config.js` — configuração mínima via plugin oficial do Vite.

## Testes com SQLite em memória no backend

Os testes do backend (`pytest`) sobrescrevem a dependência do banco por um SQLite em memória, para não depender do PostgreSQL estar rodando em CI.

## pydantic-settings também no Agent

Mesmo padrão já usado no backend (`BaseSettings`/`SettingsConfigDict`) para carregar `.env` de forma tipada, em vez de reinventar um parser.

## Resolução do `computer_id` no Agent via `GET /computers`

O Agent não tem como saber seu próprio `id` depois do primeiro registro (`POST /computers` responde `409` sem `id` no corpo em execuções seguintes). Em vez de criar um endpoint dedicado, reaproveita o mesmo padrão já adotado pelo frontend: busca a lista completa (`GET /computers`) e localiza a si mesmo pelo `hostname`.

## Retry com backoff exponencial centralizado no `SentinelApiClient`

Cada chamada HTTP do Agent (registro, listagem, envio de métrica) passa por um único ponto (`SentinelApiClient._request`) que retenta em erro de rede ou `5xx`, com backoff exponencial. Erros `4xx` (ex.: `404`, `409`) não são retentados — são tratados como regra de negócio pela camada de serviço, não como falha transitória.

## Agent síncrono, sem `asyncio`

O Agent faz uma coisa por vez (coleta → envia → aguarda), sem concorrência real a explorar. Um loop síncrono com `time.sleep` é mais simples de ler e depurar do que introduzir `asyncio` sem necessidade.

## Logs estruturados em JSON via `logging.Formatter` customizado

Sem adicionar `structlog` ou similar — um `Formatter` que serializa cada registro como uma linha JSON (com `ensure_ascii=True`, para não depender da codificação do terminal/redirecionamento) já atende à necessidade do Agent.
