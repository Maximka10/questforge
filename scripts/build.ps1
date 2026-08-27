$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path '.\packwiz.exe')) { & powershell -ExecutionPolicy Bypass -File '.\scripts\bootstrap.ps1' }

& .\packwiz.exe refresh
if ($LASTEXITCODE -ne 0) { throw 'packwiz refresh failed.' }

New-Item -ItemType Directory -Force -Path '.\builds' | Out-Null
& .\packwiz.exe modrinth export -o '.\builds\QuestForge-0.1.0.mrpack'
if ($LASTEXITCODE -ne 0) { throw 'Modrinth export failed.' }
& .\packwiz.exe curseforge export -o '.\builds\QuestForge-0.1.0-curseforge.zip'
if ($LASTEXITCODE -ne 0) { throw 'CurseForge export failed.' }

Write-Host 'QuestForge build completed.'
Write-Host 'Artifacts are in .\builds'
