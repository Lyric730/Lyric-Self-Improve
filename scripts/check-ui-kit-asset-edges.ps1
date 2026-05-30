param(
  [string]$AssetDir = "miniprogram/assets/ui-kit",
  [int]$AlphaThreshold = 16,
  [switch]$RequireAssets
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectPath {
  param([string]$Path)

  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }

  return Join-Path (Get-Location) $Path
}

$resolvedAssetDir = Resolve-ProjectPath $AssetDir

if (-not (Test-Path -LiteralPath $resolvedAssetDir)) {
  if ($RequireAssets) {
    Write-Error "Asset directory not found: $resolvedAssetDir"
    exit 1
  }

  Write-Output "No asset directory found; edge check skipped: $resolvedAssetDir"
  exit 0
}

$pngFiles = Get-ChildItem -LiteralPath $resolvedAssetDir -Filter "*.png" -File

if ($pngFiles.Count -eq 0) {
  if ($RequireAssets) {
    Write-Error "No PNG assets found in: $resolvedAssetDir"
    exit 1
  }

  Write-Output "No PNG assets found; edge check skipped: $resolvedAssetDir"
  exit 0
}

Add-Type -AssemblyName System.Drawing

$violations = New-Object System.Collections.Generic.List[string]

foreach ($file in $pngFiles) {
  $bitmap = [System.Drawing.Bitmap]::FromFile($file.FullName)

  try {
    $width = $bitmap.Width
    $height = $bitmap.Height

    if ($width -lt 2 -or $height -lt 2) {
      $violations.Add("$($file.Name): image is too small to validate ($width x $height)")
      continue
    }

    $top = 0
    $bottom = 0
    $left = 0
    $right = 0

    for ($x = 0; $x -lt $width; $x++) {
      if ($bitmap.GetPixel($x, 0).A -gt $AlphaThreshold) {
        $top++
      }

      if ($bitmap.GetPixel($x, $height - 1).A -gt $AlphaThreshold) {
        $bottom++
      }
    }

    for ($y = 0; $y -lt $height; $y++) {
      if ($bitmap.GetPixel(0, $y).A -gt $AlphaThreshold) {
        $left++
      }

      if ($bitmap.GetPixel($width - 1, $y).A -gt $AlphaThreshold) {
        $right++
      }
    }

    $touchingEdges = @()

    if ($top -gt 0) {
      $touchingEdges += "top=$top"
    }

    if ($right -gt 0) {
      $touchingEdges += "right=$right"
    }

    if ($bottom -gt 0) {
      $touchingEdges += "bottom=$bottom"
    }

    if ($left -gt 0) {
      $touchingEdges += "left=$left"
    }

    if ($touchingEdges.Count -gt 0) {
      $violations.Add("$($file.Name): non-transparent pixels touching edge(s): $($touchingEdges -join ', ')")
    }
  }
  finally {
    $bitmap.Dispose()
  }
}

if ($violations.Count -gt 0) {
  Write-Output "Edge check failed:"
  foreach ($violation in $violations) {
    Write-Output " - $violation"
  }
  exit 1
}

Write-Output "Edge check OK ($($pngFiles.Count) PNG assets checked)"
