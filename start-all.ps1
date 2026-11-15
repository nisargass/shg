# SHG Saathi Master Startup Script (PowerShell)
$root = $PSScriptRoot

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                  SHG SAATHI - AI-POWERED ENTERPRISE PLATFORM                  " -ForegroundColor Yellow
Write-Host "               Women's Self-Help Group Multi-Portal Operating System           " -ForegroundColor Cyan
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. AI/ML Microservice (Port 8001)
Write-Host "[1/3] Starting AI/ML Autonomous Microservice on Port 8001..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root\ai-ml'; Write-Host '--- SHG SAATHI AI/ML SERVICE (PORT 8001) ---' -ForegroundColor Magenta; python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

# 2. Main Backend (Port 8000)
Write-Host "[2/3] Starting FastAPI Enterprise Backend on Port 8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root\backend'; Write-Host '--- SHG SAATHI BACKEND (PORT 8000) ---' -ForegroundColor Cyan; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# 3. React Frontend (Port 5173)
Write-Host "[3/3] Starting React + Vite Frontend on Port 5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root\frontend'; Write-Host '--- SHG SAATHI FRONTEND (PORT 5173) ---' -ForegroundColor Yellow; npm run dev"

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "All three microservices launched successfully in separate terminal windows:" -ForegroundColor White
Write-Host "  * AI/ML Microservice:   http://localhost:8001  (Docs: http://localhost:8001/docs)" -ForegroundColor Magenta
Write-Host "  * Main FastAPI Backend: http://localhost:8000  (Docs: http://localhost:8000/docs)" -ForegroundColor Cyan
Write-Host "  * React Vite Frontend:  http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Demo Credentials (Password: Saathi@2026 for all):" -ForegroundColor White
Write-Host "  * SHG Leader:         savitribai@pragati-shg.org" -ForegroundColor Gray
Write-Host "  * SHG Member:         sunita.rathod@shg.in" -ForegroundColor Gray
Write-Host "  * Wholesale Buyer:    procurement@ecofab.in" -ForegroundColor Gray
Write-Host "  * NRLM Federation:    deepa.narayan@ksrlps.gov.in" -ForegroundColor Gray
Write-Host "  * Retail Customer:    pooja.h@gmail.com" -ForegroundColor Gray
Write-Host "===============================================================================" -ForegroundColor Cyan

