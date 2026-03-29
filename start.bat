@echo off
echo ==========================================
echo   Polymarket Paper Trader - Starting...
echo ==========================================
echo.

cd /d "C:\Users\ian_l\OneDrive\Desktop\polymarket-bot"

:: Kill any existing instances
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

:: Start dashboard server
echo Starting dashboard on http://localhost:5555 ...
start /B "Dashboard" python server.py

:: Wait for server to be ready
timeout /t 3 >nul

:: Start auto trader bot
echo Starting auto trader bot...
start /B "AutoTrader" python auto_trader.py

echo.
echo ==========================================
echo   Dashboard: http://localhost:5555
echo   Bot: Running every 5 minutes
echo   Press Ctrl+C to stop everything
echo ==========================================
echo.

:: Keep window open
pause
