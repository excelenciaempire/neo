# Re-clona los repos de terceros en resources/ (no versionados).
# Uso:  pwsh resources/setup.ps1
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$repos = @(
  'https://github.com/afsh4ck/WSTG-Scan.git',
  'https://github.com/jakejarvis/awesome-shodan-queries.git',
  'https://github.com/pabpereza/kali-mcp.git',
  'https://github.com/0x4m4/hexstrike-ai.git'
)

foreach ($r in $repos) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($r)
  if (Test-Path $name) {
    Write-Host "[=] $name ya existe, omitido" -ForegroundColor Yellow
  } else {
    Write-Host "[*] Clonando $name ..." -ForegroundColor Cyan
    git clone --depth 1 $r
  }
}
Write-Host "[+] Listo. Para ejecucion real de herramientas ver ../execution/SETUP.md" -ForegroundColor Green
