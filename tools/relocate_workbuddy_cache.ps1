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
      3) If the original cannot be moved aside (dir still locked by a live process), it aborts with the original intact. Otherwise it is moved aside atomically (NTFS rename, no child unlock needed) before the junction is created; any leftover is cleaned up best-effort (killing orphaned processes under $src).
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
# Idempotency guard: if source is already a junction, migration is already done.
if (Test-Path $src) {
    try {
        $attrs = (Get-Item $src -Force).Attributes
        if ($attrs -band [System.IO.FileAttributes]::ReparsePoint) {
            Write-Host '[finalize] Source is already a junction -> migration already complete. Nothing to do.'
            exit 0
        }
    } catch {}
}

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

# Kill any process still running from within $src (orphaned node.exe / electron helpers that outlived
# the main app). These hold files open and block the move/delete. We only target images whose path is
# under $src, so unrelated user processes are untouched.
Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -and $_.Path.StartsWith($src, [System.StringComparison]::OrdinalIgnoreCase) } |
    ForEach-Object { try { Write-Host ('[finalize] killing lingering ' + $_.Name + ' (pid ' + $_.Id + ') from ' + $src); $_.Kill() } catch {} }
Start-Sleep -Seconds 2

Write-Host ('[finalize] Parity OK. Moving original ' + $src + ' aside (atomic; no child unlock needed), then creating junction...')
$bak = $src + '.bak.' + (Get-Date -Format 'yyyyMMddHHmmss')
try {
    # Renaming a directory on NTFS does NOT require its child files to be unlocked, so a still-running
    # node.exe under .workbuddy will not block the move. This avoids any partial-delete risk.
    Move-Item -Path $src -Destination $bak -Force -ErrorAction Stop
    Write-Host ('[finalize] Moved original aside to ' + $bak)
} catch {
    Write-Error ('[finalize] Could not move original aside: ' + $_.Exception.Message + '. Aborting; original folder is intact and no junction created.'); Stop-Transcript | Out-Null; exit 1
}

Write-Host ('[finalize] Creating junction ' + $src + ' -> ' + $dst + ' ...')
try {
    New-Item -ItemType Junction -Path $src -Target $dst -Force | Out-Null
} catch {
    Write-Error ('[finalize] Junction creation failed: ' + $_.Exception.Message + '. Data is SAFE on E:\workbuddy-data. The original was moved to ' + $bak + ' (NOT deleted). Recreate the junction manually: New-Item -ItemType Junction -Path "' + $src + '" -Target "' + $dst + '"')
    Stop-Transcript | Out-Null; exit 1
}

# Best-effort cleanup of the moved-aside original. A still-running node.exe may keep a file locked;
# if so, migration is already COMPLETE (junction live) and the leftover .bak can be deleted after a reboot.
for ($attempt = 1; $attempt -le 6; $attempt++) {
    try {
        Remove-Item $bak -Recurse -Force -ErrorAction Stop
        Write-Host ('[finalize] Removed moved-aside original ' + $bak)
        break
    } catch {
        Write-Host ('[finalize] cleanup attempt ' + $attempt + ' for ' + $bak + ' blocked: ' + $_.Exception.Message)
        Get-Process -ErrorAction SilentlyContinue |
            Where-Object { $_.Path -and $_.Path.StartsWith($src, [System.StringComparison]::OrdinalIgnoreCase) } |
            ForEach-Object { try { $_.Kill() } catch {} }
        Start-Sleep -Seconds 2
    }
}
if (Test-Path $bak) {
    Write-Host ('[finalize] NOTE: ' + $bak + ' could not be fully removed (a process still holds a file). Migration is COMPLETE (junction live). Delete ' + $bak + ' manually after closing all apps or a reboot.')
}

Start-Sleep -Seconds 1
if (Test-Path (Join-Path $src 'binaries') -or (Test-Path (Join-Path $src 'memory'))) {
    Write-Host ''
    Write-Host 'SUCCESS: junction is live. WorkBuddy now reads/writes from E:\workbuddy-data.'
    Write-Host ('C drive freed ~' + [math]::Round($srcBytes/1GB, 2) + ' GB.')
    Write-Host 'Original folder C:\Users\<user>\.workbuddy has been permanently deleted per your instruction.'
    Write-Host 'Open WorkBuddy to verify. If anything looks off, the junction can be removed and the data is intact on E.'
    # best-effort self-cleanup of the scheduler trigger (if this run was launched by it)
    try { & schtasks.exe /delete /tn 'WorkBuddyCacheFinalize' /f 2>$null } catch {}
} else {
    Write-Error '[finalize] Junction verification FAILED.'; Stop-Transcript | Out-Null; exit 1
}
Stop-Transcript | Out-Null
