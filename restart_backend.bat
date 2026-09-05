@echo off
echo Stopping backend server...
taskkill /F /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting backend server...
cd backend
start "NBA Backend" /B python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
timeout /t 3 /nobreak >nul
echo.
echo Backend restarted. Testing...
python -c "import requests; r = requests.get('http://127.0.0.1:8000/players/all?page=1&page_size=1', timeout=5); data = r.json(); p = data.get('items', [{}])[0]; print('Player:', p.get('player')); print('Points:', p.get('points')); print('Rebounds:', p.get('rebounds'))"
pause