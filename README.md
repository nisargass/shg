# SHG Saathi – AI-Powered Enterprise Multi-Portal Platform

**SHG Saathi** is an integrated AI/ML operating system engineered for Women's Self-Help Groups (SHGs) under the National Rural Livelihoods Mission (NRLM). It empowers grassroots women collectives to manage corporate bulk orders, optimize fair work distribution, enforce product quality through computer vision, calculate transparent pricing, eliminate inventory bottlenecks, and conduct democratic quorum payouts.

---

## 1. System Architecture

The project is structured into three cleanly separated, communicating tiers:

```
+-------------------------------------------------------------------------------+
|                       PRESENTATION LAYER (PORT 5173)                          |
|  React 18 + Vite SPA | Tailwind CSS | Lucide Icons | Recharts                  |
|  Portals: SHG Leader (/leader), SHG Member (/member), Wholesale Buyer (/buyer)|
|           NRLM Federation (/federation), Retail Marketplace (/marketplace)    |
+-------------------------------------------------------------------------------+
                                        |  REST API (JWT Bearer Auth)
                                        v
+-------------------------------------------------------------------------------+
|                     ENTERPRISE BACKEND (PORT 8000)                            |
|  FastAPI | SQLAlchemy 2.0 | Pydantic v2 | SQLite (Dev) / PostgreSQL (Prod)    |
|  Business rules, order lifecycle, member records, human approval gating       |
+-------------------------------------------------------------------------------+
                                        |  REST API (X-SHG-Service-Key Header)
                                        v
+-------------------------------------------------------------------------------+
|                     AI/ML AUTONOMOUS MICROSERVICE (PORT 8001)                 |
|  FastAPI | Scikit-learn | SciPy LP HiGHS | LangGraph | SentenceTransformers   |
|  4 Trained ML Models | Computer Vision | OCR | Multilingual RAG (KN, HI, EN)  |
+-------------------------------------------------------------------------------+
```

---

## 2. Directory Structure

```
SHG-SAATHI-INTEGRATED/
├── ai-ml/                   # AI/ML Autonomous Microservice (FastAPI, Port 8001)
│   ├── app/                 # Routers, schemas, services, agents, RAG retriever
│   ├── saved_models/        # 4 trained scikit-learn models (.joblib)
│   ├── training/            # Synthetic data generation and training pipelines
│   └── tests/               # 50 unit and regression tests
├── backend/                 # Enterprise Core Backend (FastAPI, Port 8000)
│   ├── app/                 # Database models, schemas, auth, API endpoints
│   ├── scripts/             # Database initialization and full demo seeders
│   ├── shg_saathi.db        # Pre-seeded SQLite demonstration database
│   └── tests/               # 29 backend tests
├── frontend/                # Presentation Layer (React + Vite, Port 5173)
│   ├── src/                 # Multi-portal components, views, layouts, state
│   ├── public/              # Static assets and icons
│   └── package.json         # React dependencies and build scripts
├── integration/             # End-to-End System Integration Tests
│   └── test_e2e_integration.py # 7 tri-layer E2E integration tests
├── documentation/           # Comprehensive System Documentation
│   ├── architecture.md      # Tri-layer architecture and data flows
│   ├── feature-integration-matrix.md # 10 module matrix and model metrics
│   ├── api-integration.md   # API endpoints, auth headers, and contracts
│   ├── database.md          # Domain model ER schema and seed personas
│   └── troubleshooting.md   # Windows C-extensions, ports, and operations
├── start-all.bat            # Windows 1-click launch orchestrator (Batch)
├── start-all.ps1            # Windows 1-click launch orchestrator (PowerShell)
├── run-tests.bat            # Master automated test runner (Batch)
└── run-tests.ps1            # Master automated test runner (PowerShell)
```

---

## 3. Quickstart – 1-Click Launch

### Prerequisites
- Python 3.10+ (with FastAPI, Uvicorn, Scikit-learn, SciPy, Pydantic, SQLAlchemy)
- Node.js 18+ (with npm)

### Launch All Services
Double-click `start-all.bat` or run in PowerShell:
```powershell
.\start-all.ps1
```

This automatically launches all three services in separate, dedicated terminal windows:
- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **AI Microservice Docs**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## 4. Demo Accounts & Portals

All personas use password: **`Saathi@2026`** (or 1-click switch in the frontend header):

| Persona | Email | Portal Route | Primary Role |
|---------|-------|--------------|--------------|
| **SHG Leader** | `savitribai@pragati-shg.org` | `/leader` | Allocation approval, quality review gate, costing, payouts |
| **SHG Member** | `sunita.rathod@shg.in` | `/member` | View tasks, submit production batches, quorum voting |
| **Wholesale Buyer** | `procurement@ecofab.in` | `/buyer` | Create bulk orders, track milestones, digital certificates |
| **NRLM Officer** | `deepa.narayan@ksrlps.gov.in` | `/federation` | District & state monitoring, anomaly audit |
| **Retail Customer** | `pooja.h@gmail.com` | `/marketplace` | Browse retail catalog, shopping cart, checkout |

---

## 5. Automated Test Suite (86/86 Tests Passing)

To execute the entire automated test suite:
```powershell
.\run-tests.ps1
```

Summary of test suites:
- **AI/ML Microservice**: `50 passed` in `ai-ml/tests/` (100%)
- **Enterprise Backend**: `29 passed` in `backend/tests/` (100%)
- **End-to-End System**: `7 passed` in `integration/test_e2e_integration.py` (100%)
- **Total**: **86 automated tests passing green**.

---

## 6. Key AI Capabilities

1. **Intelligent Work Allocation**:
   - SciPy HiGHS Linear Programming solver optimizes fair workload distribution while respecting member capacity and material stock.
   - Calibrated Random Forest model predicts completion likelihood ($P \ge 70\%$).
2. **Computer Vision Quality Inspection**:
   - Analyzes stitch density, hem alignment, and dimension tolerance from member batch photos.
   - Requires physical review and digital sign-off from the SHG Leader before batch acceptance.
3. **Dynamic Pricing & Costing Engine**:
   - Computes transparent 8-part cost structure (raw materials, handles, zippers, labor, packaging, logistics, overhead, margin) with market benchmark guidance.
4. **Financial Anomaly Detection**:
   - Isolation Forest ML model flags irregular piece-rate payouts and billing anomalies prior to bank transfer.
5. **Multilingual RAG Assistant**:
   - Domain-specific retrieval over SHG bylaws, NRLM guidelines, and scheme benefits in English, Hindi, and Kannada.

---

## 7. Non-Negotiable Preservation Rule

The original archives provided (`shg-frontened (1).zip`, `backend.zip`, `aiml.zip`) remain **100% untouched and preserved** in the user's Downloads directory as reference copies. All integration work was executed within this isolated workspace.

## 8. Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production environment keys, Docker Compose startup, frontend hosting, and pre-launch security steps.
