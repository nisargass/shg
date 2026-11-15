@echo off
TITLE SHG Saathi - Master Launch Orchestrator
echo ===============================================================================
echo                   SHG SAATHI - AI-POWERED ENTERPRISE PLATFORM
echo                Women's Self-Help Group Multi-Portal Operating System
echo ===============================================================================
echo.
echo [1/3] Starting AI/ML Autonomous Microservice on Port 8001...
start "SHG Saathi - AI/ML Microservice (Port 8001)" cmd /k "cd /d %~dp0ai-ml && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

echo [2/3] Starting FastAPI Enterprise Backend on Port 8000...
start "SHG Saathi - Main Backend (Port 8000)" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [3/3] Starting React + Vite Frontend on Port 5173...
start "SHG Saathi - Frontend (Port 5173)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ===============================================================================
echo All three microservices have been launched in separate dedicated terminals:
echo   - AI/ML Microservice:   http://localhost:8001  (OpenAPI Docs: http://localhost:8001/docs)
echo   - Main FastAPI Backend: http://localhost:8000  (OpenAPI Docs: http://localhost:8000/docs)
echo   - React Vite Frontend:  http://localhost:5173
echo.
echo Demo Accounts Available:
echo   - SHG Leader:         savitribai@pragati-shg.org      Password: Saathi@2026
echo   - SHG Member:         sunita.rathod@shg.in           Password: Saathi@2026
echo   - Wholesale Buyer:    procurement@ecofab.in          Password: Saathi@2026
echo   - NRLM Federation:    deepa.narayan@ksrlps.gov.in    Password: Saathi@2026
echo   - Retail Customer:    pooja.h@gmail.com              Password: Saathi@2026
echo ===============================================================================
echo.
pause

