#!/usr/bin/env bash
# Sobe o PostgreSQL, aplica as migrations e inicia backend + frontend do Sentinel.
# Ctrl+C encerra backend e frontend.
#
# `set -m` (job control) coloca cada processo em segundo plano no seu próprio grupo de
# processos — sem isso, matar só o PID do `uv run`/`npm run dev` não derruba os processos
# filhos reais (o worker do uvicorn --reload, o vite), e eles ficam presos nas portas.
#
# No Git Bash para Windows especificamente, os processos são processos Win32 nativos sem
# grupo de processos POSIX de verdade — a limpeza automática pode não derrubar tudo. Em
# Windows, prefira `scripts/run-all.ps1` (testado e confiável nesse ambiente).
set -euo pipefail
set -m

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Sentinel run-all =="

(cd "$root" && docker compose up -d postgres)

echo "Aguardando o PostgreSQL ficar saudável..."
attempts=0
until [ "$(docker inspect --format '{{.State.Health.Status}}' sentinel-postgres 2>/dev/null)" = "healthy" ] || [ "$attempts" -ge 30 ]; do
    sleep 2
    attempts=$((attempts + 1))
done

echo "-- aplicando migrations --"
(cd "$root/backend" && uv run alembic upgrade head)

pids=()
cleanup() {
    echo ""
    echo "Encerrando..."
    for pid in "${pids[@]}"; do
        # PID negativo = sinaliza o grupo de processos inteiro, não só o processo raiz.
        kill -- "-$pid" 2>/dev/null || kill "$pid" 2>/dev/null || true
    done
}
trap cleanup EXIT INT TERM

echo "-- iniciando backend --"
(cd "$root/backend" && uv run uvicorn app.main:app --reload) &
pids+=("$!")

echo "-- iniciando frontend --"
(cd "$root/frontend" && npm run dev) &
pids+=("$!")

echo ""
echo "Backend:  http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"
echo ""
echo "O Agent representa uma máquina monitorada e não sobe por padrão. Para rodar:"
echo "  cd agent && uv run sentinel-agent"
echo ""
echo "Ctrl+C encerra backend e frontend."

wait
