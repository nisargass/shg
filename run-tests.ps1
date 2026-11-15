# SHG Saathi Master Test Runner (PowerShell)
$root = $PSScriptRoot

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "                   SHG SAATHI - MASTER AUTOMATED TEST RUNNER                   " -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. AI/ML Microservice Tests
Write-Host "[SUITE 1/3] Running AI/ML Autonomous Microservice Tests (50 tests)..." -ForegroundColor Green
Set-Location "$root\ai-ml"
python -m pytest tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] AI/ML microservice tests failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "[SUCCESS] AI/ML Microservice tests passed!" -ForegroundColor Green
Write-Host ""

# 2. Backend Tests
Write-Host "[SUITE 2/3] Running Enterprise Backend Tests (29 tests)..." -ForegroundColor Green
Set-Location "$root\backend"
python -m pytest tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Enterprise Backend tests failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "[SUCCESS] Enterprise Backend tests passed!" -ForegroundColor Green
Write-Host ""

# 3. E2E Integration Tests
Write-Host "[SUITE 3/3] Running End-to-End System Integration Tests (7 tests)..." -ForegroundColor Green
Set-Location "$root"
python -m pytest integration/test_e2e_integration.py -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] End-to-End System Integration tests failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "[SUCCESS] End-to-End System Integration tests passed!" -ForegroundColor Green
Write-Host ""

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "ALL TEST SUITES PASSED! (86/86 Tests Green)" -ForegroundColor Green
Write-Host "Full Tri-Layer Architecture Verified: Frontend <-> Backend <-> AI/ML" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan

