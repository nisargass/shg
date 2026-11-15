# SHG Saathi – System Architecture Specification

## 1. Executive Summary

**SHG Saathi** is an enterprise multi-portal operating system tailored for Women's Self-Help Groups (SHGs) under the National Rural Livelihoods Mission (NRLM). It digitises bulk order lifecycle management, work allocation optimization, quality inspection, dynamic costing, and financial transparency.

The platform is designed around a strict **Tri-Layer Architecture**:
1. **Presentation Layer (React + Vite SPA)**: Multi-portal interface for Leaders, Members, Buyers, Federation Officers, and Retail Customers.
2. **Business & Transactional Layer (FastAPI Enterprise Backend)**: Enforces business logic, data persistence (PostgreSQL/SQLite), authentication, role-based authorization, and human-in-the-loop decision gating.
3. **Intelligence & Predictive Layer (FastAPI AI/ML Microservice)**: Independent predictive microservice hosting 4 scikit-learn models, SciPy Linear Programming optimizer, LangGraph stateful workflow agents, multilingual RAG (SentenceTransformers), and computer vision pipelines.

---

## 2. Architecture Topology

```
+---------------------------------------------------------------------------------------------------------+
|                                        PRESENTATION LAYER (PORT 5173)                                   |
|                                                                                                         |
|   +-------------------+  +-------------------+  +--------------------+  +---------------------------+   |
|   |  SHG Leader Hub   |  | SHG Member App    |  | Wholesale Buyer    |  | NRLM Federation / State   |   |
|   | (/leader)         |  | (/member)         |  | (/buyer)           |  | (/federation)             |   |
|   +-------------------+  +-------------------+  +--------------------+  +---------------------------+   |
|                                                 | Retail Marketplace (/marketplace)                 |   |
|                                                 +---------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     | HTTP / REST (JWT Bearer Token)
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                                    ENTERPRISE BACKEND (PORT 8000)                                       |
|                                                                                                         |
|   +--------------------+  +--------------------+  +--------------------+  +-------------------------+   |
|   | Auth & RBAC Guard  |  | Order & Allocations|  | Quality Review Gate|  | Finance & Quorum Payout |   |
|   +--------------------+  +--------------------+  +--------------------+  +-------------------------+   |
|   +--------------------+  +--------------------+  +--------------------+  +-------------------------+   |
|   | Inventory Control  |  | Logistics & Transit|  | Retail Orders      |  | Human Decision Registry |   |
|   +--------------------+  +--------------------+  +--------------------+  +-------------------------+   |
|                                                     |                                                   |
|                        +----------------------------+----------------------------+                      |
|                        |                                                         |                      |
|                        v                                                         v                      |
|          +----------------------------+                            +----------------------------+       |
|          | Primary Relational DB      |                            | AI Microservice Client     |       |
|          | (PostgreSQL / SQLite)      |                            | (HTTPX Connection Pool)    |       |
|          +----------------------------+                            +----------------------------+       |
+----------------------------------------------------------------------------------|----------------------+
                                                                                   |
                                                     HTTP / REST (X-SHG-Service-Key Header)
                                                                                   |
                                                                                   v
+---------------------------------------------------------------------------------------------------------+
|                                    AI/ML MICROSERVICE (PORT 8001)                                       |
|                                                                                                         |
|   +------------------------------------+  +-----------------------------------+                         |
|   | Predictive ML Models               |  | Optimization & Math Solvers       |                         |
|   | - Completion Likelihood Classifier |  | - SciPy HiGHS LP Fair Allocator   |                         |
|   | - Completion Duration Regressor    |  | - Economic Order Quantity (EOQ)   |                         |
|   | - Isolation Forest Anomaly Detector|  | - Safety Stock & Reorder Points   |                         |
|   | - Demand Forecasting Regressor     |  +-----------------------------------+                         |
|   +------------------------------------+                                                                |
|   +------------------------------------+  +-----------------------------------+                         |
|   | Computer Vision & Perception       |  | Cognitive Agents & Knowledge      |                         |
|   | - Defect Detection (Stitching)     |  | - LangGraph Workflow Orchestrator |                         |
|   | - Tesseract & Mock OCR Engine      |  | - Multilingual RAG (KN, HI, EN)   |                         |
|   | - Dimension & Seam Consistency     |  | - Voice Synthesis & Transcriber   |                         |
|   +------------------------------------+  +-----------------------------------+                         |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Communication Invariants & Rules

1. **Strict Client-Microservice Isolation**:
   - The React frontend **never** connects directly to the AI/ML microservice (`http://localhost:8001`).
   - All AI capabilities are invoked exclusively by the Enterprise Backend on port `8000`.
   - The backend validates, logs, enriches, and stores AI inferences in the transactional database before returning results to client dashboards.
2. **Mutual Service Authentication**:
   - Inter-service communication between Backend and AI microservice is secured via the shared secret header `X-SHG-Service-Key`.
   - Requests without this header are rejected with HTTP 401 Unauthorized.
3. **Human-in-the-Loop Governance**:
   - AI outputs are advisory recommendations, **never** autonomous decisions.
   - Work allocation requires explicit SHG Leader signature (`approvedBy` + `timestamp`).
   - Quality inspection flags require SHG Leader physical inspection review (`status`, `approvedQty`, `reworkQty`).
   - Financial payouts require **60% group quorum voting** among members before ledger release.
4. **Resilient Fallback Mode**:
   - The Backend AI client contains graceful fallback logic (`AI_SERVICE_USE_MOCK_FALLBACK=True`). If the AI microservice experiences transient downtime, deterministic rule-based algorithms provide uninterrupted business continuity.

---

## 4. End-to-End Data Flows

### A. Bulk Order & Intelligent Work Allocation Flow
1. Buyer submits purchase order (`POST /api/v1/orders`).
2. Backend triggers AI Feasibility & Optimization (`POST /api/v1/ai/workforce/optimize-allocation`).
3. AI solver runs **SciPy HiGHS Linear Programming**:
   - Minimizes completion variance while respecting capacity upper bounds and material availability.
4. AI Calibrated Classifier predicts individual completion likelihood ($P \ge 70\%$).
5. Backend stores proposed distribution with status `PENDING_REVIEW`.
6. SHG Leader inspects member workloads on `/leader/allocations` and clicks **Approve Allocation**.
7. Backend updates status to `APPROVED_BY_LEADER` and generates individual production cards on Member portals.

### B. Computer Vision Quality Inspection Flow
1. Member submits completed batch photos (`POST /api/v1/production/batches`).
2. Backend forwards images to AI Computer Vision (`POST /api/v1/ai/quality/inspect`).
3. Vision pipeline evaluates stitch alignment, fabric defects, and measurement tolerance.
4. AI returns defect severity: `CLEAN`, `MINOR_WARNING`, or `CRITICAL_REJECT`.
5. Backend flags the batch as `SUBMITTED` with AI inspection metadata.
6. SHG Leader conducts visual spot-check on `/leader/quality` and records formal decision:
   - `APPROVED`, `REJECTED`, or `APPROVED_WITH_REWORK`.

### C. Financial Quorum & Ledger Payout Flow
1. Order production finishes and all batches pass quality inspection.
2. Backend computes piece-rate earnings based on approved quantities minus rework penalties.
3. System posts payout proposal to all participating members (`POST /api/v1/finance/payouts/{order_id}/vote`).
4. Members cast votes via their smartphone or village kiosk.
5. Once affirmative quorum threshold ($\ge 60\%$) is reached, SHG Leader clicks **Confirm Bank Transfer**.
6. System runs **Isolation Forest ML Anomaly Detection** (`GET /api/v1/finance/anomalies`) to prevent fraud or miscalculation before bank ledger transmission.

