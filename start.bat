@echo off
title AzrielGPT Loader

echo.
echo   ╔══════════════════════════════╗
echo   ║     AzrielGPT Bootloader     ║
echo   ╚══════════════════════════════╝
echo.
echo Installing any missing python dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo [1/3] Purging Zombie Processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/3] Spinning up Grok Backend...
start /B python api_server.py >nul 2>&1

echo [3/3] Launching Frontend Interface...
node server.js

echo.
echo Done! AzrielGPT is booting up.
echo All processes are running in the background.
echo.
timeout /t 2 /nobreak >nul
exit
