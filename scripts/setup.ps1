#Requires -Version 5.1
<#
.SYNOPSIS
    Instala as dependências das três aplicações do Sentinel e prepara os arquivos .env.
#>

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

function Test-CommandExists($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

function Copy-EnvExample($dir) {
    $example = Join-Path $dir ".env.example"
    $target = Join-Path $dir ".env"
    if ((Test-Path $example) -and -not (Test-Path $target)) {
        Copy-Item $example $target
        Write-Host "  criado $target"
    }
}

Write-Host "== Sentinel setup ==" -ForegroundColor Cyan

foreach ($tool in @("uv", "npm", "docker")) {
    if (-not (Test-CommandExists $tool)) {
        Write-Warning "'$tool' nao encontrado no PATH. Instale antes de continuar."
    }
}

Write-Host "-- backend --" -ForegroundColor Cyan
Push-Location (Join-Path $root "backend")
uv sync
Pop-Location
Copy-EnvExample (Join-Path $root "backend")

Write-Host "-- agent --" -ForegroundColor Cyan
Push-Location (Join-Path $root "agent")
uv sync
Pop-Location
Copy-EnvExample (Join-Path $root "agent")

Write-Host "-- frontend --" -ForegroundColor Cyan
Push-Location (Join-Path $root "frontend")
npm install
Pop-Location
Copy-EnvExample (Join-Path $root "frontend")

Write-Host ""
Write-Host "Setup concluido. Rode scripts/run-all.ps1 para subir o projeto." -ForegroundColor Green
