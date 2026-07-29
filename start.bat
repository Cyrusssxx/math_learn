@echo off
rem 数学记忆卡片 - 一键启动本地服务器
rem 必须经 http:// 访问（Service Worker 与 fetch 在 file:// 下不可用）
cd /d "%~dp0pwa"
start "" http://localhost:8409/index.html
python -m http.server 8409
