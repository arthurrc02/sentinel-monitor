# API

Base URL em desenvolvimento: `http://localhost:8000`. Documentação interativa automática (Swagger) em `/docs`.

## Health

### `GET /health`

Verifica se a API está no ar.

**Resposta `200`**

```json
{ "status": "ok" }
```

## Computadores

### `POST /computers`

Registra um computador.

**Request**

```json
{ "hostname": "pc-01" }
```

**Resposta `201`**

```json
{
  "id": 1,
  "hostname": "pc-01",
  "created_at": "2026-07-22T10:00:00Z",
  "last_seen_at": null,
  "is_online": false
}
```

**Erros**: `409` se o `hostname` já estiver registrado.

### `GET /computers`

Lista os computadores registrados, com status calculado no momento da consulta.

`last_seen_at` é o `collected_at` da métrica mais recente do computador (`null` se nunca reportou). `is_online` é `true` se `last_seen_at` está dentro de `SENTINEL_OFFLINE_THRESHOLD_SECONDS` (padrão 120s) a contar de agora.

**Resposta `200`**

```json
[
  {
    "id": 1,
    "hostname": "pc-01",
    "created_at": "2026-07-22T10:00:00Z",
    "last_seen_at": "2026-07-22T10:04:30Z",
    "is_online": true
  }
]
```

## Métricas

### `POST /computers/{id}/metrics`

Registra uma amostra de métricas para um computador.

**Request**

```json
{
  "cpu_percent": 42.5,
  "memory_percent": 60.0,
  "disk_percent": 75.3,
  "collected_at": "2026-07-22T10:00:00Z"
}
```

`cpu_percent`, `memory_percent` e `disk_percent` são percentuais entre 0 e 100.

**Resposta `201`**

```json
{
  "id": 1,
  "computer_id": 1,
  "cpu_percent": 42.5,
  "memory_percent": 60.0,
  "disk_percent": 75.3,
  "collected_at": "2026-07-22T10:00:00Z",
  "created_at": "2026-07-22T10:05:00Z"
}
```

**Erros**: `404` se o computador não existir.

### `GET /computers/{id}/metrics`

Consulta o histórico de métricas de um computador, mais recente primeiro (por `collected_at`).

**Query params**: `limit` (padrão 100, máximo 1000).

**Resposta `200`**: lista de objetos no mesmo formato do `POST`.

**Erros**: `404` se o computador não existir.
