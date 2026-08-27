$ErrorActionPreference = 'Continue'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host '=== QuestForge diagnostics ==='
Write-Host "Root: $Root"
Write-Host ''

Write-Host 'Java:'
java -version
Write-Host ''

if (Test-Path '.\packwiz.exe') {
    Write-Host 'packwiz:'
    & .\packwiz.exe --version
} else {
    Write-Warning 'packwiz.exe is missing. Run scripts\bootstrap.ps1.'
}

Write-Host ''
Write-Host 'Pack metadata:'
if (Test-Path '.\pack.toml') { Get-Content '.\pack.toml' } else { Write-Warning 'pack.toml missing' }

Write-Host ''
Write-Host 'Generated quest files:'
Get-ChildItem '.\config\ftbquests\quests' -Recurse -File -ErrorAction SilentlyContinue | Select-Object FullName,Length

Write-Host ''
Write-Host 'Known log errors:'
if (Test-Path '.\logs\latest.log') {
    Select-String -Path '.\logs\latest.log' -Pattern 'ERROR|FATAL|Caused by:' | Select-Object -Last 80
} else {
    Write-Host 'No local logs directory. Run the client first.'
}
