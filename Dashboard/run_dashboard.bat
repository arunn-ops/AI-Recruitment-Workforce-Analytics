@echo off
echo =====================================================================
echo AI Recruitment & Workforce Analytics Dashboard Launcher
echo =====================================================================
echo.
echo Starting Backend Server on http://localhost:5000...
start "" http://localhost:5000
python Dashboard/backend/app.py
pause
