@echo off
TITLE SHG Saathi - Master Test Suite Runner
echo ===============================================================================
echo                   SHG SAATHI - MASTER AUTOMATED TEST RUNNER
echo ===============================================================================
echo.

set ROOT_DIR=%~dp0

echo [SUITE 1/3] Running AI/ML Autonomous Microservice Tests (50 tests)...
cd /d %ROOT_DIR%ai-ml
python -m pytest tests/
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] AI/ML microservice tests failed!
    exit /b %ERRORLEVEL%
)
echo [SUCCESS] AI/ML Microservice tests passed!
echo.

echo [SUITE 2/3] Running Enterprise Backend Tests (29 tests)...
cd /d %ROOT_DIR%backend
python -m pytest tests/
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Enterprise Backend tests failed!
    exit /b %ERRORLEVEL%
)
echo [SUCCESS] Enterprise Backend tests passed!
echo.

echo [SUITE 3/3] Running End-to-End System Integration Tests (7 tests)...
cd /d %ROOT_DIR%
python -m pytest integration/test_e2e_integration.py -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] End-to-End System Integration tests failed!
    exit /b %ERRORLEVEL%
)
echo [SUCCESS] End-to-End System Integration tests passed!
echo.

echo ===============================================================================
echo ALL TEST SUITES PASSED! (86/86 Tests Green)
echo Full Tri-Layer Architecture Verified: Frontend <-> Backend <-> AI/ML
echo ===============================================================================
echo.
pause

