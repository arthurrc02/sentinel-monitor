# Sentinel

Sentinel é uma plataforma de monitoramento de infraestrutura composta por um agente coletor, uma API e um dashboard web.

## Objetivo

Monitorar computadores em tempo real, coletando métricas como CPU, memória, disco e rede, exibindo essas informações em uma interface web moderna.

## Arquitetura

Monorepo com três aplicações independentes:

| Pasta | Stack | Responsabilidade |
|---|---|---|
| [`agent/`](agent/) | Python + uv | Coleta métricas da máquina monitorada e as envia ao backend. |
| [`backend/`](backend/) | FastAPI + SQLAlchemy + Alembic + uv | Recebe, persiste (PostgreSQL) e expõe métricas via API REST. |
| [`frontend/`](frontend/) | React + Vite + TypeScript | Dashboard web que consome a API e exibe as métricas. |

Fluxo de dados: **Agent → Backend (ingestão) → PostgreSQL → Backend (consulta) → Frontend**.

O PostgreSQL usado em desenvolvimento roda via [`docker-compose.yml`](docker-compose.yml) na raiz do monorepo.

Cada aplicação possui seu próprio `README.md` com instruções de instalação e execução.

## Status

Estrutura base definida: cada aplicação com seu esqueleto (`/health` no backend, placeholders no agent e frontend), conexão SQLAlchemy e Alembic configurados no backend, e PostgreSQL disponível via Docker Compose. Ainda não há nenhum model, migration, endpoint de métricas ou coleta real — isso é o escopo da Sprint 1.