@echo off
echo Starting CompanionAI - Competition Compliant Version
echo.

echo [1/3] Installing dependencies...
python -m pip install -q fastapi uvicorn streamlit faiss-cpu sentence-transformers python-dotenv requests

echo [2/3] Starting backend API server...
start "CompanionAI Backend" cmd /k "uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --reload"

echo [3/3] Waiting 3 seconds, then starting frontend...
timeout /t 3 /nobreak > nul

start "CompanionAI Frontend" cmd /k "streamlit run src/frontend/app.py --server.port 8502"

echo.
echo ✅ CompanionAI is starting up!
echo.
echo 📡 Backend API: http://127.0.0.1:8000
echo 🌐 Frontend App: http://localhost:8502
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo.
echo Press any key to close this window...
pause > nul