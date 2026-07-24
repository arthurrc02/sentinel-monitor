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

## Status online/offline calculado na leitura, não armazenado

`GET /computers` computa `last_seen_at`/`is_online` a cada chamada (`JOIN` com `MAX(collected_at)` por computador) em vez de gravar isso como coluna. Evita escrita extra a cada métrica recebida e evita o dado "envelhecer" (ficar online indefinidamente por engano caso algo falhe em atualizar uma coluna). Sem migration nova.

## Regra de offline parametrizável (`SENTINEL_OFFLINE_THRESHOLD_SECONDS`)

Um computador é considerado offline se não há métrica dentro dessa janela (padrão 120s = 2× o intervalo padrão do Agent). É uma configuração do backend, não do Agent — o backend não sabe o intervalo de coleta configurado em cada Agent, então usa sua própria tolerância independente.

## Busca e ordenação de computadores são client-side

A lista de computadores já vem inteira para o frontend a cada poll; filtrar/ordenar em memória no `DashboardPage` evita crescer a API (novos query params) para uma necessidade que a escala atual não justifica.

## Intervalo de polling é preferência do usuário, persistida em `localStorage`

Hook `usePollingInterval` (frontend), compartilhado entre `DashboardPage` e `ComputerDetailPage` — escolher "10s" em uma tela mantém a escolha ao navegar para a outra. Sem WebSocket/SSE: o requisito desta fase é polling.

## Erros de rede do frontend viram `ApiError` amigável

`api/client.ts` captura falha do `fetch` (backend inacessível) e lança uma `ApiError` com mensagem em português, em vez de propagar a mensagem crua do navegador (ex.: "Failed to fetch").

## Colunas de data do backend viraram `DateTime(timezone=True)` explícito

Durante a Fase 5, gerar uma migration nova revelou que o Postgres já guardava `computers.created_at`/`metrics.collected_at`/`metrics.created_at` como `TIMESTAMP WITH TIME ZONE` (a primeira migration, escrita à mão na Fase 1, já usava isso), mas os models SQLAlchemy nunca declararam `timezone=True` — o autogenerate ia "corrigir" isso silenciosamente removendo a informação de fuso do banco. Em vez de deixar isso acontecer, os models passaram a declarar `DateTime(timezone=True)` explicitamente, alinhados ao que já existia de fato.

## Índice composto `(computer_id, collected_at)` em `metrics`

Substitui o índice simples em `computer_id`. Cobre tanto consultas por computador (prefixo esquerdo) quanto o `MAX(collected_at) GROUP BY computer_id` do cálculo de status e o `ORDER BY collected_at DESC` do histórico — sem manter dois índices redundantes.

## Corrida no registro de computador tratada como `IntegrityError` → `409`

`POST /computers` fazia só um check-then-insert (`get_by_hostname` seguido de `create`), sem proteção contra duas requisições simultâneas com o mesmo hostname. O repositório agora captura `IntegrityError` do `commit()` (com rollback) e o service traduz para `ComputerAlreadyExistsError`, mantendo a resposta um `409` limpo em vez de um `500` cru.

## Logging estruturado também no backend (paridade com o Agent)

O Agent tinha logs JSON desde a Fase 3; o backend não tinha nenhum log de aplicação (só o access log do uvicorn). Reaproveitado o mesmo `JsonFormatter` do Agent (`app/core/logging_config.py`) para registrar eventos de negócio nos `services`.

## `ruff` com `B` (bugbear) e `SIM` (simplify) em `backend/` e `agent/`

Rede de segurança automática adicional além de `E`/`F`/`I`/`UP`. Nenhuma violação nova apareceu — confirma que o código já seguia essas práticas, mas fica garantido daqui para frente.

## Vitest + Testing Library no frontend

Até a Fase 4, o frontend era a única das três aplicações sem nenhum teste automatizado. Vitest foi escolhido por já compartilhar a configuração do Vite (`vite.config.ts`) sem infraestrutura nova; os testes cobrem lógica pura e componentes/hooks pequenos, não é tentativa de cobertura exaustiva. Vitest foi fixado na major 3 (não a 4) porque a 4 exige Vite 6+, e o projeto está em Vite 5 — misturar as duas trouxe uma versão de Vite duplicada na árvore de dependências que quebrava simulação de eventos em testes de componente.

## `eslint-plugin-jsx-a11y` no frontend

Acessibilidade vinha sendo revisada manualmente a cada fase; o plugin adiciona verificação automática nas revisões seguintes.

## Diagramas Mermaid em arquivos `.mmd` separados, com PNG versionado

Cada aplicação ganhou seu próprio diagrama (`architecture.mmd`, `backend-flow.mmd`, `agent-flow.mmd`, `frontend-flow.mmd`) em vez de um único bloco Mermaid solto em `system-flow.md`. Os `.mmd` são renderizados nativamente pelo GitHub; o PNG de cada um também foi gerado (via `npx @mermaid-js/mermaid-cli`) e versionado, para funcionar em qualquer lugar que não renderize Mermaid (ex.: o README).

## Scripts `setup`/`run-all` em vez de Makefile

`make` não é nativo no Windows — exigiria mais uma instalação para quem for rodar o projeto. Os scripts `.ps1`/`.sh` cobrem a mesma necessidade (onboarding com um comando) sem essa dependência extra.

## `run-all.sh` usa `set -m` + kill de grupo de processos

Descoberto testando o script de verdade: matar só o PID do `uv run uvicorn --reload`/`npm run dev` não derruba os processos filhos reais (o worker do reload, o vite) — eles ficam presos na porta. `set -m` (job control) coloca cada serviço em background no seu próprio grupo de processos, e o cleanup manda o sinal pro grupo inteiro (`kill -- -$pid`), não só pro processo raiz. No Git Bash para Windows especificamente essa limpeza pode não pegar tudo, porque lá os processos são processos Win32 nativos sem grupo POSIX de verdade — por isso o script recomenda `run-all.ps1` no Windows (testado e confiável nesse ambiente).

## `CONTRIBUTING.md` curto, sem processo burocrático

Cobre só o que importa para abrir um PR sem fricção: como rodar, checklist de qualidade por aplicação, padrão de commits (Conventional Commits, já usado no histórico do projeto). Nada de template de issue elaborado ou processo de governança — desproporcional para o tamanho do projeto.
