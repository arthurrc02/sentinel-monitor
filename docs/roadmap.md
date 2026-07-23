# Roadmap

Status das fases de desenvolvimento do Sentinel. Uma fase só é marcada como concluída depois de implementada e revisada.

| Fase | Descrição | Status |
|---|---|---|
| Fase 0 | Fundação do projeto: estrutura dos três apps, uv, Docker Compose, lint/typecheck/testes, CI | Concluída |
| Fase 1 | Backend funcional: SQLAlchemy, Alembic, models `Computer`/`Metric`, endpoints de cadastro e métricas | Concluída |
| Fase 2 | Dashboard inicial: React + TypeScript + Tailwind consumindo a API, listagem e detalhe de computadores | Concluída |
| Fase 3 | Sentinel Agent: coleta de CPU/memória/disco, registro automático, envio periódico com retry e backoff exponencial | Concluída |
| Fase 4 | Integração e experiência de uso: status online/offline, atualização automática (polling), busca/ordenação, skeletons e tratamento de erros mais amigável | Concluída |

Próximas fases: Em desenvolvimento.
