@echo off
title rehabbo - Physiotherapy System
color 0A

echo ========================================
echo    rehabbo Physiotherapy System
echo ========================================
echo.

echo [1/3] Installing requirements...
pip install django django-cors-headers pillow >nul 2>&1
echo Done.

echo.
echo [2/3] Running migrations...
python manage.py migrate >nul 2>&1
echo Done.

echo.
echo [3/3] Starting server...
echo.
echo ========================================
echo  Server running at: http://127.0.0.1:8000/
echo  Press Ctrl+C to stop
echo ========================================
echo.

python manage.py runserver

pause