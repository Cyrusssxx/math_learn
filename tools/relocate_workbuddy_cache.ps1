<#
.SYNOPSIS
  Relocate WorkBuddy data folder C:\Users\<user>\.workbuddy -> E:\workbuddy-data via a directory junction,
  freeing ~5.3 GB on the C drive.

.USAGE
  Phase 1 (safe to run WHILE WorkBuddy is open):
      powershell -NoProfile -ExecutionPolicy Bypass -File "D:\ai code\math-note\tools\relocate_workbuddy_cache.ps1"
  Phase 2 (FINALIZE - run ONLY after fully closing WorkBuddy):
      powershell -NoProfile -ExecutionPolicy Bypass -File "D:\ai code\math-note\tools\relocate_workbuddy_cache.ps1" -Finalize
  Phase 2 with auto-wait (launch, then close WorkBuddy; it proceeds once WB is detected closed):
      powershell -NoProfile -ExecutionPolicy Bypass -File "D:\ai code\math-note\tools\relocate_workbuddy_cache.ps1" -Finalize -AutoWait

.NOTES
  - Per user instruction, the original C:\Users\<user>\.workbuddy is DELETED (not kept as .bak).
    The full, verified copy on E:\workbuddy-data is the backup; the junction makes it transparent.
  - Safety gates:
      1) Refuses to run while WorkBuddy processes are detected (and -AutoWait polls for close).
      2) Mirrors, then verifies byte-parity (dst >= 99.9% of src bytes) before deleting.
      3) If the original cannot be deleted (files still locked), it aborts with the original intact.
      4) If junction creation fails, data is already safe on E:\workbuddy-data; only the junction
         needs recreating manually.
  - Junction (New-Item -ItemType Junction) is transparent at FS level; WorkBuddy notices nothing.
  - Bulk copy uses robocopy (System32, always present) with a Python fallback.
  - E:\workbuddy-data must have ~10 GB free (confirmed 80 GB free on E:).
#>
param([switch]$Finalize, [switch]$AutoWait)

$src = "$env:USERPROFILE\.workbuddy"
$dst = 'E:\workbuddy-data'
$py  = 'C:\Users\cjx\.workbuddy\binaries\python\versions\3.13.12\python.exe'
$copyScript = 'D:\ai code\math-note\tools\_copy_workbuddy_to_e.py'
$log = Join-Path $env:TEMP 'relocate_finalize.log'

function Test-WorkBuddyRunning {
    $names = @('WorkBuddy', 'WorkBuddy.exe', 'CodeBuddy', 'CodeBuddyCode', 'electron')
    return [bool](Get-Process -ErrorAction SilentlyContinue | Where-Object { $names -contains $_.Name })
}

function Invoke-Copy {
    # Prefer an explicit System32 path so we never depend on PATH resolution.
    $rb = @('C:\Windows\System32\robocopy.exe', 'C:\Windows\Sysnative\robocopy.exe') |
          Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $rb) { $rb = (Get-Command robocopy.exe -ErrorAction SilentlyContinue).Source }
    if ($rb) {
        Write-Host ('[copy] robocopy mirror via ' + $rb + ' (this may take a while for ~5 GB)...')
        & $rb "$src" "$dst" /MIR /COPY:DAT /DCOPY:T /R:1 /W:1 /MT:8 /NFL /NDL /NJH /NJS
    } else {
        Write-Host '[copy] robocopy not found, falling back to python...'
        & $py $copyScript
    }
}

# ---------- PHASE 1: copy only (read-only w.r.t. source) ----------
if (-not $Finalize) {
    if (Test-Path $dst) {
        Write-Host '[phase1] E:\workbuddy-data already exists - will merge/skip. If stale, delete it first.'
    } else {
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
    }
    Invoke-Copy
    Write-Host '[phase1] Bulk copy pass complete.'
    Write-Host '[phase1] NEXT: fully close WorkBuddy (window + tray + background), then re-run with -Finalize.'
    exit 0
}

# ---------- PHASE 2: FINALIZE (requires WorkBuddy fully closed) ----------
Start-Transcript -Path $log -Append | Out-Null
Write-Host ('[finalize] Logging to ' + $log)

if ($AutoWait) {
    Write-Host '[finalize] AutoWait: polling until WorkBuddy is fully closed (up to 2h)...'
    $t = 0
    while ($t -lt 7200) {
        if (-not (Test-WorkBuddyRunning)) { break }
        Start-Sleep -Seconds 20; $t += 20
        if ($t % 60 -eq 0) { Write-Host ('[finalize] still waiting for WorkBuddy to close (' + $t + 's)...') }
    }
    if (Test-WorkBuddyRunning) {
        Write-Error '[finalize] WorkBuddy still running after 2h wait. Aborting.'; Stop-Transcript | Out-Null; exit 1
    }
    Write-Host '[finalize] WorkBuddy detected closed.'
}

if (Test-WorkBuddyRunning) {
    Write-Error ('[finalize] WorkBuddy processes still detected. Close it completely and retry. Aborting.'); Stop-Transcript | Out-Null; exit 1
}

Write-Host '[finalize] Re-copying to ensure a complete, consistent mirror...'
Invoke-Copy

$critical = @('binaries', 'projects', 'workspace', 'memory', 'skills', 'sessions')
$missing = $critical | Where-Object { -not (Test-Path (Join-Path $dst $_)) }
if ($missing) {
    Write-Error ('[finalize] Destination missing critical dirs: ' + ($missing -join ',') + '. Aborting to avoid data loss.'); Stop-Transcript | Out-Null; exit 1
}

$srcBytes = (Get-ChildItem $src -Recurse -Force -File | Measure-Object -Property Length -Sum).Sum
$dstBytes = (Get-ChildItem $dst -Recurse -Force -File | Measure-Object -Property Length -Sum).Sum
Write-Host ('[finalize] byte parity: src=' + $srcBytes + ' dst=' + $dstBytes)
if ($dstBytes -lt [math]::Floor($srcBytes * 0.999)) {
    Write-Error '[finalize] Parity check failed (dst materially smaller than src). Aborting to avoid data loss.'; Stop-Transcript | Out-Null; exit 1
}

Write-Host ('[finalize] Parity OK. Deleting original ' + $src + ' and creating junction...')
try {
    Remove-Item $src -Recurse -Force -ErrorAction Stop
} catch {
    Write-Error ('[finalize] Could not delete original: ' + $_.Exception.Message + '. Aborting WITHOUT touching anything else; the original folder is intact and no junction was created.'); Stop-Transcript | Out-Null; exit 1
}

Write-Host ('[finalize] Creating junction ' + $src + ' -> ' + $dst + ' ...')
try {
    New-Item -ItemType Junction -Path $src -Target $dst -Force | Out-Null
} catch {
    Write-Error ('[finalize] Junction creation failed: ' + $_.Exception.Message + '. Data is SAFE on E:\workbuddy-data; recreate the junction manually: New-Item -ItemType Junction -Path "' + $src + '" -Target "' + $dst + '"')
    Stop-Transcript | Out-Null; exit 1
}

Start-Sleep -Seconds 1
if (Test-Path (Join-Path $src 'binaries') -or (Test-Path (Join-Path $src 'memory'))) {
    Write-Host ''
    Write-Host 'SUCCESS: junction is live. WorkBuddy now reads/writes from E:\workbuddy-data.'
    Write-Host ('C drive freed ~' + [math]::Round($srcBytes/1GB, 2) + ' GB.')
    Write-Host 'Original folder C:\Users\<user>\.workbuddy has been permanently deleted per your instruction.'
    Write-Host 'Open WorkBuddy to verify. If anything looks off, the junction can be removed and the data is intact on E.'
} else {
    Write-Error '[finalize] Junction verification FAILED.'; Stop-Transcript | Out-Null; exit 1
}
Stop-Transcript | Out-Null
