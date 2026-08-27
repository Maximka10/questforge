$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Packwiz = Join-Path $Root 'packwiz.exe'
$PackwizZip = Join-Path $Root '.tools\packwiz.zip'
$PackwizDir = Join-Path $Root '.tools'

function Get-Packwiz {
    if (Test-Path $Packwiz) { return }
    New-Item -ItemType Directory -Force -Path $PackwizDir | Out-Null
    Write-Host 'Downloading packwiz...'
    $url = 'https://nightly.link/packwiz/packwiz/workflows/go/main/Windows%2064-bit.zip'
    Invoke-WebRequest -Uri $url -OutFile $PackwizZip
    Expand-Archive -Path $PackwizZip -DestinationPath $PackwizDir -Force
    $candidate = Get-ChildItem $PackwizDir -Recurse -Filter 'packwiz.exe' | Select-Object -First 1
    if (-not $candidate) { throw 'packwiz.exe was not found after download.' }
    Copy-Item $candidate.FullName $Packwiz -Force
}

function Invoke-Packwiz([string[]]$Args) {
    & $Packwiz @Args
    if ($LASTEXITCODE -ne 0) { throw "packwiz failed with exit code $LASTEXITCODE: $($Args -join ' ')" }
}

Get-Packwiz

# Recreate the metadata deterministically. This also repairs the bootstrap placeholder hash.
Invoke-Packwiz @('init','--reinit','-y','--name','QuestForge','--author','Maximka10','--version','0.1.0','--mc-version','1.20.1','--modloader','forge','--forge-version','47.4.23')

$mods = Get-Content (Join-Path $Root 'scripts\mods.txt') | Where-Object {
    $_ -and -not $_.Trim().StartsWith('#')
}

foreach ($line in $mods) {
    $parts = $line.Split('|',2)
    if ($parts.Count -ne 2) { throw "Invalid mod manifest line: $line" }
    $source = $parts[0].Trim()
    $slug = $parts[1].Trim()
    switch ($source) {
        'cf' { Invoke-Packwiz @('cf','install',$slug,'-y') }
        'mr' { Invoke-Packwiz @('mr','install',$slug,'-y') }
        default { throw "Unsupported source '$source' in $line" }
    }
}

# Generate the quest book and apply repository configs.
$questGenerator = Join-Path $Root 'scripts\generate_quests.py'
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $questGenerator
    if ($LASTEXITCODE -ne 0) { throw 'Quest generation failed.' }
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py $questGenerator
    if ($LASTEXITCODE -ne 0) { throw 'Quest generation failed.' }
} else {
    throw 'Python 3 is required to generate the Quest Book.'
}

Invoke-Packwiz @('refresh')
Write-Host ''
Write-Host 'QuestForge bootstrap completed.'
Write-Host 'Next: run scripts\build.ps1 to validate and export the pack.'
