$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path '.\packwiz.exe')) { & powershell -ExecutionPolicy Bypass -File '.\scripts\bootstrap.ps1' }

$ServerDir = Join-Path $Root 'server\instance'
New-Item -ItemType Directory -Force -Path $ServerDir | Out-Null

Write-Host 'QuestForge server preparation'
Write-Host 'The pack metadata is ready. Use packwiz-installer on the dedicated server with side=server.'
Write-Host 'See docs\server.md for the exact command and EULA requirement.'
