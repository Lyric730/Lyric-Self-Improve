param(
  [string]$Source = "docs/design/imagegen-references/08-rank-leaderboard-assets-board.png",
  [string]$OutputDir = "miniprogram/assets/ui-kit",
  [string]$DarkPreview = "docs/design/extracted-ui-assets-preview.png",
  [string]$CheckerPreview = "docs/design/extracted-ui-assets-checker-preview.png",
  [int]$SafePadding = 18,
  [int]$AlphaThreshold = 16
)

$ErrorActionPreference = "Stop"

function Get-ProjectRoot {
  return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

function Resolve-ProjectPath {
  param([string]$Path)

  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }

  return Join-Path (Get-ProjectRoot) $Path
}

function Convert-MattePixel {
  param([System.Drawing.Color]$Color)

  $max = [Math]::Max($Color.R, [Math]::Max($Color.G, $Color.B))
  $min = [Math]::Min($Color.R, [Math]::Min($Color.G, $Color.B))
  $spread = $max - $min

  if ($max -le 12) {
    return [System.Drawing.Color]::FromArgb(0, $Color.R, $Color.G, $Color.B)
  }

  if ($max -le 30 -and $spread -le 18) {
    return [System.Drawing.Color]::FromArgb(0, $Color.R, $Color.G, $Color.B)
  }

  if ($max -le 46 -and $spread -le 12) {
    $alpha = [Math]::Min(200, [Math]::Max(48, [int](($max - 30) / 16 * 200)))
    return [System.Drawing.Color]::FromArgb($alpha, $Color.R, $Color.G, $Color.B)
  }

  return [System.Drawing.Color]::FromArgb(255, $Color.R, $Color.G, $Color.B)
}

function Find-AlphaBounds {
  param(
    [System.Drawing.Bitmap]$Bitmap,
    [int]$Threshold
  )

  $minX = $Bitmap.Width
  $minY = $Bitmap.Height
  $maxX = -1
  $maxY = -1

  for ($y = 0; $y -lt $Bitmap.Height; $y++) {
    for ($x = 0; $x -lt $Bitmap.Width; $x++) {
      if ($Bitmap.GetPixel($x, $y).A -gt $Threshold) {
        if ($x -lt $minX) { $minX = $x }
        if ($y -lt $minY) { $minY = $y }
        if ($x -gt $maxX) { $maxX = $x }
        if ($y -gt $maxY) { $maxY = $y }
      }
    }
  }

  if ($maxX -lt 0 -or $maxY -lt 0) {
    return [PSCustomObject]@{
      X = 0
      Y = 0
      Width = $Bitmap.Width
      Height = $Bitmap.Height
    }
  }

  return [PSCustomObject]@{
    X = $minX
    Y = $minY
    Width = $maxX - $minX + 1
    Height = $maxY - $minY + 1
  }
}

function Export-Asset {
  param(
    [System.Drawing.Bitmap]$SourceBitmap,
    [hashtable]$Asset,
    [string]$AssetOutputDir,
    [int]$Padding,
    [int]$Threshold
  )

  $crop = New-Object System.Drawing.Bitmap $Asset.W, $Asset.H, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)

  try {
    for ($y = 0; $y -lt $Asset.H; $y++) {
      for ($x = 0; $x -lt $Asset.W; $x++) {
        $sourceX = $Asset.X + $x
        $sourceY = $Asset.Y + $y

        if ($sourceX -lt 0 -or $sourceY -lt 0 -or $sourceX -ge $SourceBitmap.Width -or $sourceY -ge $SourceBitmap.Height) {
          $crop.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
          continue
        }

        $pixel = $SourceBitmap.GetPixel($sourceX, $sourceY)
        $crop.SetPixel($x, $y, (Convert-MattePixel $pixel))
      }
    }

    $bounds = Find-AlphaBounds -Bitmap $crop -Threshold $Threshold
    $finalWidth = $bounds.Width + ($Padding * 2)
    $finalHeight = $bounds.Height + ($Padding * 2)
    $final = New-Object System.Drawing.Bitmap $finalWidth, $finalHeight, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)

    try {
      $graphics = [System.Drawing.Graphics]::FromImage($final)
      try {
        $graphics.Clear([System.Drawing.Color]::Transparent)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $dest = New-Object System.Drawing.Rectangle $Padding, $Padding, $bounds.Width, $bounds.Height
        $src = New-Object System.Drawing.Rectangle $bounds.X, $bounds.Y, $bounds.Width, $bounds.Height
        $graphics.DrawImage($crop, $dest, $src, [System.Drawing.GraphicsUnit]::Pixel)
      }
      finally {
        $graphics.Dispose()
      }

      $outputPath = Join-Path $AssetOutputDir "$($Asset.Name).png"
      $final.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
      return $outputPath
    }
    finally {
      if ($null -ne $final) {
        $final.Dispose()
      }
    }
  }
  finally {
    $crop.Dispose()
  }
}

function Draw-CheckerBackground {
  param(
    [System.Drawing.Graphics]$Graphics,
    [int]$Width,
    [int]$Height,
    [int]$Size = 18
  )

  $light = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 44, 44, 44))
  $dark = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 26, 26, 26))

  try {
    for ($y = 0; $y -lt $Height; $y += $Size) {
      for ($x = 0; $x -lt $Width; $x += $Size) {
        $brush = if ((($x / $Size) + ($y / $Size)) % 2 -eq 0) { $light } else { $dark }
        $Graphics.FillRectangle($brush, $x, $y, $Size, $Size)
      }
    }
  }
  finally {
    $light.Dispose()
    $dark.Dispose()
  }
}

function Draw-Preview {
  param(
    [string[]]$AssetPaths,
    [string]$PreviewPath,
    [switch]$Checker
  )

  $columns = 5
  $cellWidth = 250
  $cellHeight = 210
  $margin = 28
  $titleHeight = 56
  $rows = [Math]::Ceiling($AssetPaths.Count / $columns)
  $width = ($columns * $cellWidth) + ($margin * 2)
  $height = $titleHeight + ($rows * $cellHeight) + ($margin * 2)

  $canvas = New-Object System.Drawing.Bitmap $width, $height, ([System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $graphics = [System.Drawing.Graphics]::FromImage($canvas)

  try {
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

    if ($Checker) {
      Draw-CheckerBackground -Graphics $graphics -Width $width -Height $height
    }
    else {
      $graphics.Clear([System.Drawing.Color]::FromArgb(255, 8, 7, 5))
    }

    $titleBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 255, 211, 107))
    $textBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 220, 200, 170))
    $linePen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(120, 255, 118, 0), 1)
    $titleFont = New-Object System.Drawing.Font "Arial", 16, ([System.Drawing.FontStyle]::Bold)
    $textFont = New-Object System.Drawing.Font "Arial", 8, ([System.Drawing.FontStyle]::Regular)

    try {
      $label = if ($Checker) { "UI Kit Extracted Assets - Checker Preview" } else { "UI Kit Extracted Assets - Dark Preview" }
      $graphics.DrawString($label, $titleFont, $titleBrush, $margin, 18)

      for ($i = 0; $i -lt $AssetPaths.Count; $i++) {
        $assetPath = $AssetPaths[$i]
        $row = [Math]::Floor($i / $columns)
        $col = $i % $columns
        $cellX = $margin + ($col * $cellWidth)
        $cellY = $titleHeight + $margin + ($row * $cellHeight)
        $graphics.DrawRectangle($linePen, $cellX, $cellY, $cellWidth - 12, $cellHeight - 14)

        $image = [System.Drawing.Image]::FromFile($assetPath)
        try {
          $maxW = $cellWidth - 48
          $maxH = $cellHeight - 58
          $scale = [Math]::Min($maxW / $image.Width, $maxH / $image.Height)
          $drawW = [int]($image.Width * $scale)
          $drawH = [int]($image.Height * $scale)
          $drawX = $cellX + [int](($cellWidth - $drawW - 12) / 2)
          $drawY = $cellY + 16 + [int](($maxH - $drawH) / 2)
          $graphics.DrawImage($image, $drawX, $drawY, $drawW, $drawH)
        }
        finally {
          $image.Dispose()
        }

        $name = [System.IO.Path]::GetFileNameWithoutExtension($assetPath)
        $graphics.DrawString($name, $textFont, $textBrush, $cellX + 12, $cellY + $cellHeight - 34)
      }
    }
    finally {
      $titleBrush.Dispose()
      $textBrush.Dispose()
      $linePen.Dispose()
      $titleFont.Dispose()
      $textFont.Dispose()
    }

    $previewDir = Split-Path -Parent $PreviewPath
    New-Item -ItemType Directory -Path $previewDir -Force | Out-Null
    $canvas.Save($PreviewPath, [System.Drawing.Imaging.ImageFormat]::Png)
  }
  finally {
    $graphics.Dispose()
    $canvas.Dispose()
  }
}

$assets = @(
  @{ Name = "rank-bronze"; X = 34; Y = 132; W = 100; H = 126 },
  @{ Name = "rank-silver"; X = 143; Y = 130; W = 104; H = 130 },
  @{ Name = "rank-gold"; X = 255; Y = 126; W = 110; H = 134 },
  @{ Name = "rank-gold-iii-featured"; X = 374; Y = 96; W = 156; H = 174 },
  @{ Name = "rank-platinum"; X = 548; Y = 132; W = 94; H = 128 },
  @{ Name = "rank-diamond"; X = 664; Y = 130; W = 92; H = 110 },
  @{ Name = "rank-star-glory"; X = 785; Y = 119; W = 86; H = 142 },
  @{ Name = "rank-king"; X = 900; Y = 118; W = 88; H = 116 },

  @{ Name = "star-empty"; X = 1018; Y = 148; W = 98; H = 96 },
  @{ Name = "star-earned"; X = 1134; Y = 148; W = 68; H = 98 },
  @{ Name = "star-new"; X = 1224; Y = 130; W = 86; H = 112 },
  @{ Name = "star-protected"; X = 1326; Y = 136; W = 96; H = 114 },
  @{ Name = "star-lost"; X = 1432; Y = 138; W = 70; H = 108 },

  @{ Name = "settlement-rank-up-card"; X = 602; Y = 404; W = 136; H = 196 },
  @{ Name = "settlement-points-plus"; X = 744; Y = 406; W = 132; H = 194 },
  @{ Name = "settlement-points-minus"; X = 890; Y = 406; W = 132; H = 194 },
  @{ Name = "settlement-reward-card"; X = 1030; Y = 404; W = 158; H = 198 },
  @{ Name = "settlement-victory-banner"; X = 1198; Y = 420; W = 148; H = 144 },
  @{ Name = "settlement-accept-stamp"; X = 1378; Y = 440; W = 112; H = 124 },

  @{ Name = "reward-crate-normal"; X = 580; Y = 690; W = 108; H = 94 },
  @{ Name = "reward-crate-sprint"; X = 696; Y = 688; W = 106; H = 96 },
  @{ Name = "points-coin"; X = 806; Y = 690; W = 80; H = 92 },
  @{ Name = "rank-medal-gold"; X = 902; Y = 688; W = 78; H = 96 },
  @{ Name = "season-badge-s1"; X = 998; Y = 690; W = 76; H = 92 },

  @{ Name = "tv-ranking-title"; X = 1106; Y = 684; W = 302; H = 92 },
  @{ Name = "tv-sponsor-slot"; X = 1106; Y = 784; W = 292; H = 70 },
  @{ Name = "tv-refresh-badge"; X = 1408; Y = 742; W = 96; H = 122 },

  @{ Name = "deco-progress-stripe"; X = 822; Y = 904; W = 62; H = 44 },
  @{ Name = "deco-nameplate"; X = 910; Y = 904; W = 84; H = 46 },
  @{ Name = "deco-corner-star"; X = 1000; Y = 898; W = 88; H = 66 },
  @{ Name = "deco-target"; X = 1014; Y = 902; W = 76; H = 78 },
  @{ Name = "deco-crown"; X = 1148; Y = 896; W = 52; H = 86 }
)

$sourcePath = Resolve-ProjectPath $Source
$outputPath = Resolve-ProjectPath $OutputDir
$darkPreviewPath = Resolve-ProjectPath $DarkPreview
$checkerPreviewPath = Resolve-ProjectPath $CheckerPreview

New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
Get-ChildItem -LiteralPath $outputPath -Filter "*.png" -File | Remove-Item -Force

Add-Type -AssemblyName System.Drawing

$sourceBitmap = [System.Drawing.Bitmap]::FromFile($sourcePath)
$assetPaths = New-Object System.Collections.Generic.List[string]

try {
  foreach ($asset in $assets) {
    $assetPaths.Add((Export-Asset -SourceBitmap $sourceBitmap -Asset $asset -AssetOutputDir $outputPath -Padding $SafePadding -Threshold $AlphaThreshold))
  }
}
finally {
  $sourceBitmap.Dispose()
}

Draw-Preview -AssetPaths $assetPaths.ToArray() -PreviewPath $darkPreviewPath
Draw-Preview -AssetPaths $assetPaths.ToArray() -PreviewPath $checkerPreviewPath -Checker

Write-Output "Extracted $($assetPaths.Count) UI assets"
Write-Output "Output: $outputPath"
Write-Output "Dark preview: $darkPreviewPath"
Write-Output "Checker preview: $checkerPreviewPath"
