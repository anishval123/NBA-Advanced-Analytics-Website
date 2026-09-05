@echo off
echo ========================================
echo Restart Backend + Test Basketball Reference
echo ========================================

echo.
echo Step 1: Stopping old backend...
taskkill /F /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Deleting old cache...
cd backend
python -c "from pathlib import Path; cache = Path('data/live_players_cache.json'); cache.unlink() if cache.exists() else None; print('Cache deleted')"
cd ..

echo.
echo Step 3: Starting backend...
cd backend
start "NBA Backend" /B python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
cd ..

echo.
echo Step 4: Waiting for backend to start (Basketball Reference fetch takes ~10s)...
timeout /t 15 /nobreak >nul

echo.
echo Step 5: Testing all players have stats...
python test_all_players.py

echo.
echo ========================================
echo Done!
echo ========================================
pause