param(
  [switch]$WithPreview,
  [int]$Port = 30812,
  [string]$CliPath = "",
  [string]$ProjectPath = (Resolve-Path ".").Path
)

$ErrorActionPreference = "Stop"

function Get-DefaultCliPath {
  $folderName = -join @(
    [char]24494,
    [char]20449,
    "web",
    [char]24320,
    [char]21457,
    [char]32773,
    [char]24037,
    [char]20855
  )

  return Join-Path -Path "F:\" -ChildPath (Join-Path -Path $folderName -ChildPath "cli.bat")
}

if (-not $CliPath) {
  $CliPath = Get-DefaultCliPath
}

function Invoke-Check {
  param(
    [string]$Name,
    [scriptblock]$Command
  )

  Write-Host ""
  Write-Host "==> $Name" -ForegroundColor Cyan
  & $Command
}

Invoke-Check "Ops service fallback tests" {
  node scripts\test-ops-services.js
}

Invoke-Check "Settlement engine tests" {
  node scripts\test-settlement-engine.js
}

Invoke-Check "Admin config validator tests" {
  node scripts\test-admin-config-validator.js
}

Invoke-Check "Member profile tests" {
  node scripts\test-member-profile.js
}

Invoke-Check "Cloud contract tests" {
  node scripts\test-cloud-contracts.js
}

Invoke-Check "Service layer boundary check" {
  node scripts\check-service-layer-boundary.js
}

Invoke-Check "JSON check" {
  node scripts\check-json-files.js
}

Invoke-Check "Production copy check" {
  node scripts\check-production-copy.js
}

Invoke-Check "Player flow route check" {
  node scripts\check-player-flow-routes.js
}

Invoke-Check "UI asset edge check" {
  powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
}

Invoke-Check "Mini-program JS syntax check" {
  Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object {
    node --check $_.FullName
  }
}

Invoke-Check "Cloud function JS syntax check" {
  Get-ChildItem cloudfunctions -Recurse -Filter *.js | ForEach-Object {
    node --check $_.FullName
  }
}

if ($WithPreview) {
  Invoke-Check "WeChat DevTools preview" {
    & $CliPath --port $Port --lang zh preview --project $ProjectPath
  }
}

Write-Host ""
Write-Host "Launch verification OK" -ForegroundColor Green
