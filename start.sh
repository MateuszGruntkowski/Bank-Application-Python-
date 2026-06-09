#!/bin/bash
echo "=========================================="
echo "   Bank - Starting Application"
echo "=========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed. Install it from: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    exit 1
fi

# Verify virtual environment exists
if [ ! -d "backend/.venv" ]; then
    echo "[ERROR] Virtual environment not found in backend/.venv"
    echo "Please run: python3 -m venv backend/.venv"
    echo "Then: source backend/.venv/bin/activate"
    echo "And: pip install -r backend/requirements.txt"
    exit 1
fi

# Verify node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "[ERROR] Frontend dependencies not found in frontend/node_modules"
    echo "Please run: cd frontend && npm install"
    exit 1
fi

# Start backend
echo "[1/2] Starting backend server..."
source backend/.venv/bin/activate
PYTHONPATH=$(pwd) python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
deactivate

# Wait for backend
sleep 4

# Start frontend
echo "[2/2] Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3

echo ""
echo "=========================================="
echo "   Application is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""

# Open browser
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

echo "Press Ctrl+C to stop the application..."
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
