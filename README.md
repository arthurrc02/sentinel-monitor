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
| [`frontend/`](frontend/) | React + Vite + TypeScript + Tailwind CSS | Dashboard web que consome a API e exibe as métricas. |

Fluxo de dados: **Agent → Backend (ingestão) → PostgreSQL → Backend (consulta) → Frontend**.

O PostgreSQL usado em desenvolvimento roda via [`docker-compose.yml`](docker-compose.yml) na raiz do monorepo.

Cada aplicação possui seu próprio `README.md` com instruções de instalação e execução.

## Documentação

- [Arquitetura](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [API](docs/api.md)
- [Decisões técnicas](docs/decisions.md)
- [Setup](docs/setup.md)
- [Diagrama de fluxo](docs/diagrams/system-flow.md)

## Qualidade

- **Lint**: [ruff](https://docs.astral.sh/ruff/) (Python) e [ESLint](https://eslint.org/) (TypeScript).
- **Tipagem estática**: [mypy](https://mypy-lang.org/) em modo strict (agent e backend) e `tsc` (frontend).
- **Testes**: [pytest](https://docs.pytest.org/) (agent e backend).
- **CI**: [GitHub Actions](.github/workflows/ci.yml) roda lint, typecheck e testes das três aplicações a cada push/PR.

## Licença

Distribuído sob a licença [MIT](LICENSE).

## Status

**Fase 3 concluída**: as três aplicações já funcionam de ponta a ponta — o Agent coleta CPU/memória/disco e envia periodicamente para o backend (com retry e backoff exponencial), o backend persiste em PostgreSQL e expõe a API, e o dashboard React exibe os dados. Ver [roadmap](docs/roadmap.md).