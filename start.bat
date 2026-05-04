@echo off
echo ==========================================
echo    Bank - Starting Application
echo ==========================================
echo.

:: Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Install it from: https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Install it from: https://www.python.org/
    pause
    exit /b 1
)

:: Verify virtual environment exists
if not exist backend\.venv (
    echo [ERROR] Virtual environment not found in backend\.venv
    echo Please follow the installation instructions in README.md first.
    echo.
    echo Quick fix:
    echo cd backend
    echo python -m venv .venv
    echo .venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

:: Verify node_modules exists
if not exist frontend\node_modules (
    echo [ERROR] Frontend dependencies not found in frontend\node_modules
    echo Please run "npm install" in the frontend directory first.
    pause
    exit /b 1
)

:: Start backend
echo [1/2] Starting backend server...
start "IO Bank Backend" cmd /c "call backend\.venv\Scripts\activate.bat && set PYTHONPATH=%cd% && cd backend && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

:: Wait for backend to start
echo Waiting for backend to start...
timeout /t 4 /nobreak >nul

:: Start frontend
echo [2/2] Starting frontend...
cd frontend
start "IO Bank Frontend" cmd /c "npm run dev"
cd ..

:: Wait and open browser
timeout /t 3 /nobreak >nul
echo.
echo ==========================================
echo    Application is running!
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo ==========================================
echo.
start http://localhost:5173
echo Press any key to stop the application...
pause >nul
