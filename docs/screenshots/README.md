# Screenshots

Esta pasta ainda não tem screenshots — foram preparadas as instruções para capturá-las, mas gerá-las exige um navegador rodando a aplicação, que não está disponível no ambiente onde este projeto foi desenvolvido até agora.

## Como capturar

Com o projeto rodando localmente ([`docs/setup.md`](../setup.md) ou `scripts/run-all`), capture as telas abaixo e salve nesta pasta com o nome indicado. Resolução recomendada: janela do navegador em ~1440×900, sem DevTools aberto.

| Arquivo | Tela | O que mostrar |
|---|---|---|
| `dashboard-empty.png` | `/` | Dashboard sem nenhum computador registrado (estado vazio). |
| `dashboard.png` | `/` | Dashboard com pelo menos 2 computadores — um online e um offline, para a badge de status aparecer nos dois estados. |
| `computer-detail.png` | `/computers/:id` | Página de detalhe de um computador, com histórico de métricas populado. |

## Depois de adicionar os arquivos

Atualize a seção "Screenshots" do [`README.md`](../../README.md) na raiz, trocando o link para estas instruções pelas imagens:

```markdown
![Dashboard](docs/screenshots/dashboard.png)
![Detalhe do computador](docs/screenshots/computer-detail.png)
```
