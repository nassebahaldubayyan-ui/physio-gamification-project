@echo off

cd "ai-module"
start cmd /k python main.py
timeout /t 2 >nul
cd ..
cd "Game/Catch_falling_objects/Bulid"
start "" "CatchingFallingObjects.exe"

pause