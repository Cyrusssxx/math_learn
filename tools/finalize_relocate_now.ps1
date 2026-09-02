# finalize_relocate_now.ps1
# 一步到位：彻底关闭 WorkBuddy -> 等其完全退出 -> 执行迁移（删 C 盘目录 + 建 E 盘 junction）
# 用法：在【独立的】PowerShell（Win+R 输入 powershell）里运行：
#   & "D:\ai code\math-note\tools\finalize_relocate_now.ps1"
# 注意：运行后 WorkBuddy 会被强制关闭，当前对话会断开，这是正常的。
$ErrorActionPreference = 'Stop'

$relocate = 'D:\ai code\math-note\tools\relocate_workbuddy_cache.ps1'
$psExe = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
if (-not (Test-Path $relocate)) { Write-Error ("迁移脚本不存在: " + $relocate); exit 1 }

Write-Host '[step1] 强制结束所有 WorkBuddy 进程...'
Get-Process -Name 'WorkBuddy*' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
# 清理仍残留、路径在 .workbuddy 下的孤儿 node/electron
Get-Process -ErrorAction SilentlyContinue |
  Where-Object { $_.Path -like '*\.workbuddy\*' -and ($_.ProcessName -match 'node|electron') } |
  Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host '[step2] 等待 WorkBuddy 完全退出（最多 60 秒）...'
$waited = 0
while ($waited -lt 60) {
    $still = Get-Process -Name 'WorkBuddy*' -ErrorAction SilentlyContinue
    if ($still.Count -eq 0) { break }
    Start-Sleep -Seconds 2
    $waited += 2
}
$remain = Get-Process -Name 'WorkBuddy*' -ErrorAction SilentlyContinue
if ($remain.Count -gt 0) {
    Write-Error ("[step2] 60 秒后 WorkBuddy 仍有 " + $remain.Count + " 个进程在运行，中止。请手动结束它们后再试。")
    exit 1
}
Write-Host '[step2] WorkBuddy 已完全关闭。开始执行迁移...'

& $psExe -NoProfile -ExecutionPolicy Bypass -File $relocate -Finalize
$rc = $LASTEXITCODE
Write-Host ("[done] finalize 退出码=" + $rc)
if ($rc -eq 0) {
    Write-Host 'SUCCESS: 迁移完成。C:\Users\cjx\.workbuddy 已变为指向 E:\workbuddy-data 的 junction。'
} else {
    Write-Host ('WARNING: finalize 退出码非 0（=' + $rc + '）。请查看 %TEMP%\relocate_finalize.log。')
}
