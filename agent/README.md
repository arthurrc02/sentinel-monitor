# Sentinel Agent

Agente responsável por coletar métricas de infraestrutura (CPU, memória, disco, rede) e enviá-las ao backend do Sentinel.

> Status: scaffolding inicial. A lógica de coleta e envio de métricas ainda será implementada em sprints futuras.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Instalação

```bash
uv sync
```

## Execução

```bash
uv run sentinel-agent
```

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
