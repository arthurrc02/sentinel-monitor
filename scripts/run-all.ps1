#Requires -Version 5.1
<#
.SYNOPSIS
    Sobe o PostgreSQL, aplica as migrations e inicia backend + frontend do Sentinel.
    Cada serviço abre em uma janela própria — feche a janela para parar o serviço.
#>

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Write-Host "== Sentinel run-all ==" -ForegroundColor Cyan

Push-Location $root
docker compose up -d postgres
Pop-Location

Write-Host "Aguardando o PostgreSQL ficar saudavel..."
$attempts = 0
$status = ""
do {
    Start-Sleep -Seconds 2
    $status = docker inspect --format "{{.State.Health.Status}}" sentinel-postgres 2>$null
    $attempts++
} while ($status -ne "healthy" -and $attempts -lt 30)

if ($status -ne "healthy") {
    Write-Warning "PostgreSQL nao ficou saudavel a tempo - continuando mesmo assim."
}

Write-Host "-- aplicando migrations --" -ForegroundColor Cyan
Push-Location (Join-Path $root "backend")
uv run alembic upgrade head
Pop-Location

Write-Host "-- iniciando backend (nova janela) --" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; uv run uvicorn app.main:app --reload"

Write-Host "-- iniciando frontend (nova janela) --" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Write-Host ""
Write-Host "Backend:  http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "O Agent representa uma maquina monitorada e nao sobe por padrao. Para rodar:" -ForegroundColor Yellow
Write-Host "  cd agent; uv run sentinel-agent"
