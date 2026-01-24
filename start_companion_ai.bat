@echo off
echo Starting CompanionAI - React UI Version
echo.

echo [1/4] Installing Python dependencies...
python -m pip install -q fastapi uvicorn faiss-cpu sentence-transformers python-dotenv requests

echo [2/4] Installing Node.js dependencies...
call npm install --legacy-peer-deps

echo [3/4] Starting backend API server...
start "CompanionAI Backend" cmd /k "uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo [4/4] Waiting 3 seconds, then starting React frontend...
timeout /t 3 /nobreak > nul

start "CompanionAI Frontend" cmd /k "npm run dev"

echo.
echo ✅ CompanionAI is starting up!
echo.
echo 📡 Backend API: http://127.0.0.1:8000
echo 🌐 React Frontend: http://localhost:5173
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo.
echo Press any key to close this window...
pause > nul