param(
  [Parameter(Mandatory=$true)]
  [string]$HostKey,

  [ValidateSet("print", "connect", "preflight", "forward")]
  [string]$Action = "print",

  [int]$LocalPort = 4317,
  [int]$RemotePort = 4317,
  [string]$ResearchRoot = "/data/250010109/Research_System"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir
$hostsFile = Join-Path $skillDir "references/remote_hosts.yaml"

if (-not (Test-Path -LiteralPath $hostsFile)) {
  throw "Missing host registry: $hostsFile"
}

$hosts = @()
$current = $null
foreach ($line in Get-Content -LiteralPath $hostsFile) {
  if ($line -match '^\s*-\s+id:\s+(.+?)\s*$') {
    if ($current) { $hosts += [pscustomobject]$current }
    $current = @{}
    $current.id = $Matches[1].Trim().Trim('"')
    continue
  }
  if ($current -and $line -match '^\s+([a-zA-Z_]+):\s+(.+?)\s*$') {
    $key = $Matches[1].Trim()
    $value = $Matches[2].Trim().Trim('"')
    if ($key -in @("alias", "hostname", "port", "user", "expected_gpu", "default_duration_hours", "role")) {
      $current[$key] = $value
    }
  }
}
if ($current) { $hosts += [pscustomobject]$current }

$hostEntry = $hosts | Where-Object {
  $_.id -eq $HostKey -or $_.alias -eq $HostKey -or $_.port -eq $HostKey
} | Select-Object -First 1

if (-not $hostEntry) {
  $known = ($hosts | ForEach-Object { "$($_.id) => $($_.alias)" }) -join [Environment]::NewLine
  throw "Unknown host '$HostKey'. Known hosts:$([Environment]::NewLine)$known"
}

$alias = $hostEntry.alias
$sshTarget = if ($alias) { $alias } else { "$($hostEntry.user)@$($hostEntry.hostname) -p $($hostEntry.port)" }
$preflight = "hostname; pwd; nvidia-smi; (which sco || ls /root/.sco/bin/sco); if [ -d '$ResearchRoot' ]; then cd '$ResearchRoot' && git status --short --branch; else echo MISSING_RESEARCH_ROOT=$ResearchRoot; fi"

switch ($Action) {
  "print" {
    "host_id=$($hostEntry.id)"
    "alias=$alias"
    "expected_gpu=$($hostEntry.expected_gpu)"
    "default_duration_hours=$($hostEntry.default_duration_hours)"
    "connect: ssh `"$sshTarget`""
    "preflight: ssh `"$sshTarget`" `"$preflight`""
    "forward: ssh -N -L ${LocalPort}:127.0.0.1:${RemotePort} `"$sshTarget`""
  }
  "connect" {
    & ssh $sshTarget
  }
  "preflight" {
    & ssh $sshTarget $preflight
  }
  "forward" {
    & ssh -N -L "${LocalPort}:127.0.0.1:${RemotePort}" $sshTarget
  }
}
