param(
  [string]$Project = "F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx",
  [string]$Cli = "",
  [int]$Port = 55121,
  [string]$EnvId = "",
  [switch]$Deploy
)

$ErrorActionPreference = "Stop"

if (-not $Cli) {
  $wechatDevToolsFolder = -join @(
    [char]0x5FAE,
    [char]0x4FE1,
    "web",
    [char]0x5F00,
    [char]0x53D1,
    [char]0x8005,
    [char]0x5DE5,
    [char]0x5177
  )
  $Cli = Join-Path -Path ("F:\" + $wechatDevToolsFolder) -ChildPath "cli.bat"
}

function Invoke-DevToolsCli {
  param(
    [string]$Label,
    [string[]]$Arguments,
    [switch]$AllowFail
  )

  Write-Host ""
  Write-Host "== $Label =="
  Write-Host "$Cli $($Arguments -join ' ')"

  $stdoutPath = [System.IO.Path]::GetTempFileName()
  $stderrPath = [System.IO.Path]::GetTempFileName()
  $argumentLine = ($Arguments | ForEach-Object {
    $value = "$_"
    if ($value.Contains(" ") -or $value.Contains('"')) {
      '"' + $value.Replace('"', '\"') + '"'
    } else {
      $value
    }
  }) -join " "

  try {
    $process = Start-Process `
      -FilePath $Cli `
      -ArgumentList $argumentLine `
      -NoNewWindow `
      -PassThru `
      -Wait `
      -RedirectStandardOutput $stdoutPath `
      -RedirectStandardError $stderrPath

    $exitCode = $process.ExitCode
    $stdout = Get-Content -LiteralPath $stdoutPath -Raw -Encoding UTF8
    $stderr = Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8
    $output = @($stdout, $stderr) | Where-Object { $_ }
  } finally {
    Remove-Item -LiteralPath $stdoutPath, $stderrPath -Force -ErrorAction SilentlyContinue
  }

  $text = ($output | Out-String).Trim()

  if ($text) {
    Write-Host $text
  }

  $hasCliError = $exitCode -ne 0
  $errorPatterns = @("[error]", "Missing required argument")

  foreach ($pattern in $errorPatterns) {
    if ($text.Contains($pattern)) {
      $hasCliError = $true
    }
  }

  if ($hasCliError -and -not $AllowFail) {
    throw "Step failed: $Label"
  }

  return @{
    ExitCode = $exitCode
    Text = $text
    Failed = $hasCliError
  }
}

if (-not (Test-Path -LiteralPath $Cli)) {
  throw "WeChat DevTools CLI not found: $Cli"
}

if (-not (Test-Path -LiteralPath $Project)) {
  throw "Project not found: $Project"
}

$loginCheck = Invoke-DevToolsCli `
  -Label "Check login" `
  -Arguments @("--port", "$Port", "--lang", "zh", "islogin")

if (-not $loginCheck.Text.Contains('"login":true')) {
  throw "WeChat DevTools is not logged in."
}

$envList = Invoke-DevToolsCli `
  -Label "List cloud environments" `
  -Arguments @("--port", "$Port", "--lang", "zh", "cloud", "env", "list", "--project", $Project) `
  -AllowFail

if ($envList.Failed) {
  Write-Host ""
  Write-Host "Cloud readiness blocked."
  Write-Host "The CLI returned an error while listing cloud environments."
  Write-Host "If the output says the test AppID cannot use cloud service, switch to a registered mini program AppID first."
  Write-Host "After creating a cloud environment, rerun this script with -EnvId ENV_ID."
  exit 2
}

if (-not $EnvId) {
  Write-Host ""
  Write-Host "Cloud environment list is reachable. Pass -EnvId ENV_ID to check yunhanApi."
  exit 0
}

Invoke-DevToolsCli `
  -Label "List cloud functions" `
  -Arguments @("--port", "$Port", "--lang", "zh", "cloud", "functions", "list", "--project", $Project, "--env", $EnvId) | Out-Null

if ($Deploy) {
  Invoke-DevToolsCli `
    -Label "Deploy yunhanApi with remote npm install" `
    -Arguments @("--port", "$Port", "--lang", "zh", "cloud", "functions", "deploy", "--project", $Project, "--env", $EnvId, "--names", "yunhanApi", "--remote-npm-install") | Out-Null
}

Invoke-DevToolsCli `
  -Label "Get yunhanApi info" `
  -Arguments @("--port", "$Port", "--lang", "zh", "cloud", "functions", "info", "--project", $Project, "--env", $EnvId, "--names", "yunhanApi") | Out-Null

Write-Host ""
Write-Host "WeChat cloud readiness check completed."
