# Contribuindo com o Sentinel

Obrigado pelo interesse em contribuir. Este guia é curto de propósito — o objetivo é você conseguir rodar o projeto e abrir um PR sem fricção.

## Rodando localmente

Veja [`docs/setup.md`](docs/setup.md) para o passo a passo completo, ou use os scripts prontos:

```bash
./scripts/setup.sh    # instala dependências das três aplicações
./scripts/run-all.sh  # sobe Postgres, backend e frontend
```

No Windows, use os equivalentes `scripts/setup.ps1` e `scripts/run-all.ps1` no PowerShell.

## Antes de abrir um PR

Cada aplicação tem seus próprios comandos de qualidade — rode os da aplicação que você alterou:

| Aplicação | Comando |
|---|---|
| `agent/` | `uv run ruff check . && uv run mypy . && uv run pytest` |
| `backend/` | `uv run ruff check . && uv run mypy . && uv run pytest` |
| `frontend/` | `npm run lint && npm run test && npm run build` |

O CI ([`​.github/workflows/ci.yml`](.github/workflows/ci.yml)) roda os três conjuntos a cada push/PR — um PR só é aceito com tudo verde.

## Padrão de commits

O histórico segue [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`. Mensagens curtas, no imperativo, focadas no "porquê" quando não for óbvio.

## Escopo do projeto

O Sentinel está em fase de portfólio, não de expansão ativa de funcionalidades. Antes de propor uma feature grande, abra uma issue descrevendo o problema que ela resolve — evita trabalho descartado. Bugs, melhorias de documentação, testes e refino de UX existente são sempre bem-vindos diretamente via PR.

## Reportando bugs

Abra uma issue com: o que você esperava, o que aconteceu, passos para reproduzir, e (se relevante) logs — o backend e o Agent emitem logs estruturados em JSON, que ajudam bastante no diagnóstico.

## Licença

Ao contribuir, você concorda que sua contribuição será distribuída sob a mesma licença [MIT](LICENSE) do projeto.
