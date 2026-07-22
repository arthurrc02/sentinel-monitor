# Fluxo do sistema

Fluxo atual de dados entre as três aplicações do Sentinel.

```mermaid
flowchart LR
    Agent["Agent<br/>(coleta CPU/memória/disco)"]
    Backend["Backend FastAPI"]
    DB[("PostgreSQL")]
    Frontend["Frontend React"]

    Agent -->|"POST /computers<br/>POST /computers/{id}/metrics"| Backend
    Backend --> DB
    DB --> Backend
    Backend -->|"GET /computers<br/>GET /computers/{id}/metrics"| Frontend
```

- **Agent**: se registra uma vez e, a partir daí, só envia métricas (ingestão).
- **Backend**: persiste tudo em PostgreSQL e é a única aplicação que fala com o banco.
- **Frontend**: só consulta (leitura), nunca escreve diretamente no backend nesta fase.
