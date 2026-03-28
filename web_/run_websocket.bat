@echo off
title rehabbo - Physiotherapy System (WebSocket Mode)
color 0A

echo ========================================
echo    rehabbo Physiotherapy System
echo    WebSocket Mode for Pose Detection
echo ========================================
echo.

echo Installing WebSocket requirements...
pip install channels daphne channels-redis >nul 2>&1
echo.

echo Starting server with WebSocket support...
echo.
echo ========================================
echo  Server running at: http://127.0.0.1:8000/
echo  AI Pose Detection is ACTIVE
echo  Press Ctrl+C to stop
echo ========================================
echo.

daphne -b 127.0.0.1 -p 8000 config.asgi:application

pause