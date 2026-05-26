param(
  [string]$Source = "docs/design/imagegen-references/08-rank-leaderboard-assets-board.png",
  [string]$OutputDir = "miniprogram/assets/ui-kit",
  [string]$Preview = "docs/design/extracted-ui-assets-preview.png"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

function Resolve-RepoPath {
  param([string]$Path)
  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }
  return (Join-Path (Get-Location) $Path)
}

function Save-Crop {
  param(
    [System.Drawing.Bitmap]$SourceImage,
    [string]$Name,
    [int]$X,
    [int]$Y,
    [int]$W,
    [int]$H,
    [bool]$TransparentDark = $true
  )

  $rect = New-Object System.Drawing.Rectangle($X, $Y, $W, $H)
  $bmp = $SourceImage.Clone($rect, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)

  if ($TransparentDark) {
    for ($py = 0; $py -lt $bmp.Height; $py++) {
      for ($px = 0; $px -lt $bmp.Width; $px++) {
        $c = $bmp.GetPixel($px, $py)
        $max = [Math]::Max($c.R, [Math]::Max($c.G, $c.B))
        $min = [Math]::Min($c.R, [Math]::Min($c.G, $c.B))
        $spread = $max - $min
        $lum = [int](0.2126 * $c.R + 0.7152 * $c.G + 0.0722 * $c.B)

        if ($lum -lt 28 -and $spread -lt 26) {
          $bmp.SetPixel($px, $py, [System.Drawing.Color]::FromArgb(0, $c.R, $c.G, $c.B))
        } elseif ($lum -lt 48 -and $spread -lt 34) {
          $alpha = [Math]::Min(170, [Math]::Max(0, ($lum - 28) * 8))
          $bmp.SetPixel($px, $py, [System.Drawing.Color]::FromArgb($alpha, $c.R, $c.G, $c.B))
        }
      }
    }
  }

  $outPath = Join-Path $script:ResolvedOutputDir "$Name.png"
  $bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  return $outPath
}

function Draw-Preview {
  param(
    [string[]]$Paths,
    [string]$PreviewPath
  )

  $thumbW = 150
  $thumbH = 132
  $cols = 5
  $rows = [Math]::Ceiling($Paths.Count / $cols)
  $canvas = New-Object System.Drawing.Bitmap($($cols * $thumbW), $($rows * $thumbH), [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($canvas)
  $g.Clear([System.Drawing.Color]::FromArgb(255, 12, 10, 8))
  $font = New-Object System.Drawing.Font("Arial", 8)
  $brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 230, 210, 170))

  for ($i = 0; $i -lt $Paths.Count; $i++) {
    $img = [System.Drawing.Image]::FromFile($Paths[$i])
    $col = $i % $cols
    $row = [Math]::Floor($i / $cols)
    $slotX = $col * $thumbW
    $slotY = $row * $thumbH

    $scale = [Math]::Min(112 / $img.Width, 92 / $img.Height)
    $drawW = [int]($img.Width * $scale)
    $drawH = [int]($img.Height * $scale)
    $drawX = $slotX + [int](($thumbW - $drawW) / 2)
    $drawY = $slotY + 10
    $g.DrawImage($img, $drawX, $drawY, $drawW, $drawH)
    $label = [System.IO.Path]::GetFileNameWithoutExtension($Paths[$i])
    $g.DrawString($label, $font, $brush, $slotX + 8, $slotY + 108)
    $img.Dispose()
  }

  $canvas.Save($PreviewPath, [System.Drawing.Imaging.ImageFormat]::Png)
  $brush.Dispose()
  $font.Dispose()
  $g.Dispose()
  $canvas.Dispose()
}

$sourcePath = Resolve-RepoPath $Source
$script:ResolvedOutputDir = Resolve-RepoPath $OutputDir
$previewPath = Resolve-RepoPath $Preview

New-Item -ItemType Directory -Force -Path $script:ResolvedOutputDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $previewPath -Parent) | Out-Null
Get-ChildItem -Path $script:ResolvedOutputDir -Filter *.png -File | Remove-Item -Force

$sourceImage = [System.Drawing.Bitmap]::FromFile($sourcePath)

$assets = @(
  @{ name = "rank-bronze"; x = 34; y = 140; w = 100; h = 110 },
  @{ name = "rank-silver"; x = 144; y = 138; w = 100; h = 112 },
  @{ name = "rank-gold"; x = 254; y = 126; w = 112; h = 122 },
  @{ name = "rank-gold-iii-featured"; x = 382; y = 96; w = 142; h = 222 },
  @{ name = "rank-platinum"; x = 552; y = 140; w = 98; h = 112 },
  @{ name = "rank-diamond"; x = 660; y = 136; w = 100; h = 116 },
  @{ name = "rank-star"; x = 770; y = 122; w = 108; h = 132 },
  @{ name = "rank-king"; x = 882; y = 118; w = 104; h = 134 },
  @{ name = "reward-crate-normal"; x = 586; y = 694; w = 102; h = 94 },
  @{ name = "reward-crate-sprint"; x = 708; y = 692; w = 96; h = 98 },
  @{ name = "reward-coin"; x = 812; y = 706; w = 80; h = 96 },
  @{ name = "settlement-reward-crate"; x = 1072; y = 452; w = 108; h = 124 },
  @{ name = "settlement-rank-up"; x = 604; y = 442; w = 116; h = 142 },
  @{ name = "settlement-victory"; x = 1218; y = 446; w = 150; h = 140 },
  @{ name = "settlement-confirmed"; x = 1404; y = 446; w = 104; h = 140 }
)

$paths = New-Object System.Collections.Generic.List[string]
foreach ($asset in $assets) {
  $paths.Add((Save-Crop -SourceImage $sourceImage -Name $asset.name -X $asset.x -Y $asset.y -W $asset.w -H $asset.h))
}

$sourceImage.Dispose()
Draw-Preview -Paths $paths.ToArray() -PreviewPath $previewPath

"Extracted $($paths.Count) assets to $script:ResolvedOutputDir"
"Preview: $previewPath"
