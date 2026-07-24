# Sentinel Agent

Agente que roda na máquina monitorada: se registra no backend do Sentinel e envia periodicamente métricas de CPU, memória e disco.

> Status: Fase 5 concluída (Release Candidate 1.0). Coleta e envio funcionais, com retry e backoff exponencial (logado a cada nova tentativa) em falhas de rede/API.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Backend do Sentinel acessível (veja [`backend/README.md`](../backend/README.md))

## Instalação

```bash
uv sync
```

Copie o arquivo de variáveis de ambiente de exemplo:

```bash
cp .env.example .env
```

Principais variáveis (todas opcionais, com valores padrão):

| Variável | Padrão | Descrição |
|---|---|---|
| `SENTINEL_API_BASE_URL` | `http://localhost:8000` | URL base da API do backend. |
| `SENTINEL_HOSTNAME` | hostname do sistema | Identificador do computador. Só defina para sobrescrever o hostname real. |
| `SENTINEL_COLLECTION_INTERVAL_SECONDS` | `60` | Intervalo entre coletas/envios. |
| `SENTINEL_REQUEST_TIMEOUT_SECONDS` | `10` | Timeout de cada requisição HTTP. |
| `SENTINEL_MAX_RETRY_ATTEMPTS` | `5` | Tentativas por requisição antes de desistir do ciclo atual. |
| `SENTINEL_RETRY_BASE_DELAY_SECONDS` | `1` | Base do backoff exponencial entre tentativas. |
| `SENTINEL_LOG_LEVEL` | `INFO` | Nível de log. |
| `SENTINEL_DISK_PATH` | `/` | Caminho cujo uso de disco é monitorado. |

## Execução

```bash
uv run sentinel-agent
```

O agent se registra no backend (ou localiza seu registro existente), depois entra em loop: coleta CPU/memória/disco, envia ao backend e aguarda o intervalo configurado. `Ctrl+C` encerra de forma limpa. Se o backend estiver fora do ar, o agent loga o erro e continua tentando — não derruba o processo.

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
