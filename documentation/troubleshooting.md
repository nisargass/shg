# SHG Saathi – Troubleshooting & Operations Guide

## 1. Windows Application Control (AppLocker) C-Extension Handling

On certain managed Windows systems or enterprise environments, C-extension binaries (`.pyd` files) residing in user AppData folders can be blocked by Windows Defender Application Control.

### A. xxhash pure-Python fallback
If `import xxhash` raises:
`ImportError: DLL load failed while importing _xxhash: This program is blocked by group policy`
- **Resolution**: A pure-Python fallback is installed in `ai-ml/app/core/pure_xxhash.py` (and aliased in the python environment). It maps `xxhash.xxh64()` to Python's built-in `hashlib.blake2b(digest_size=8)`, maintaining 100% API compatibility with zero binary DLL dependencies.

### B. SQLAlchemy Cython C-Extension fallback
If SQLAlchemy raises:
`ImportError: DLL load failed while importing _cache_key_cy: This program is blocked by group policy`
- **Resolution**: Rename the compiled Cython files in your python environment:
  - `_cache_key_cy.pyd` -> `_cache_key_cy.pyd.blocked`
  - `_processors_cy.pyd` -> `_processors_cy.pyd.blocked`
  SQLAlchemy detects the missing C extensions and automatically falls back to its robust pure-Python implementation.

---

## 2. Port Conflicts & Lingering Processes

SHG Saathi requires three ports:
- **Port 5173**: React + Vite Dev Server
- **Port 8000**: FastAPI Enterprise Backend
- **Port 8001**: AI/ML Autonomous Microservice

If a server fails to bind with `error: [Errno 10048] Only one usage of each socket address is normally permitted`, run these PowerShell commands to clear existing listeners:

```powershell
# Identify process using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess

# Kill process by PID (e.g. PID 1234)
Stop-Process -Id 1234 -Force

# One-liner to clear all 3 ports:
@(5173, 8000, 8001) | ForEach-Object {
    $proc = (Get-NetTCPConnection -LocalPort $_ -ErrorAction SilentlyContinue).OwningProcess
    if ($proc) { Stop-Process -Id $proc -Force; Write-Host "Cleared port $_ (PID: $proc)" }
}
```

---

## 3. Database Path Resolution & Reseeding

The backend uses a canonical SQLite path resolution defined in `backend/app/core/config.py`.
Whether invoked from `backend/`, `frontend/`, `integration/`, or the repository root, `DATABASE_URL` resolves to `backend/shg_saathi.db`.

To completely wipe and reseed the demonstration database:
```powershell
cd backend
python -c "from app.database.session import Base, engine; Base.metadata.drop_all(bind=engine)"
python scripts/seed_full_demo.py
```

---

## 4. AI Microservice Fallback Mode

If running the backend in isolation without the AI microservice active:
In `backend/.env`:
```ini
AI_SERVICE_BASE_URL=mock
AI_SERVICE_USE_MOCK_FALLBACK=true
```
When `AI_SERVICE_USE_MOCK_FALLBACK=true`, the backend client automatically produces deterministic heuristic predictions whenever the AI service on port 8001 is unreachable, preventing any disruption to client UI workflows.

---

## 5. Automated Health Verification

Before running production builds or demonstrations, run the unified test runner:
```powershell
.\run-tests.ps1
```
All 86 automated unit, regression, and integration tests should pass green.

