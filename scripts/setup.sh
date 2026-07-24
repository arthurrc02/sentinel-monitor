#!/usr/bin/env bash
# Instala as dependências das três aplicações do Sentinel e prepara os arquivos .env.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Sentinel setup =="

for tool in uv npm docker; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "aviso: '$tool' não encontrado no PATH. Instale antes de continuar." >&2
    fi
done

copy_env_example() {
    local dir="$1"
    if [ -f "$dir/.env.example" ] && [ ! -f "$dir/.env" ]; then
        cp "$dir/.env.example" "$dir/.env"
        echo "  criado $dir/.env"
    fi
}

echo "-- backend --"
(cd "$root/backend" && uv sync)
copy_env_example "$root/backend"

echo "-- agent --"
(cd "$root/agent" && uv sync)
copy_env_example "$root/agent"

echo "-- frontend --"
(cd "$root/frontend" && npm install)
copy_env_example "$root/frontend"

echo
echo "Setup concluído. Rode scripts/run-all.sh para subir o projeto."
