# SHG Saathi – Complete Backend Platform

> **AI-Powered Self-Help Group (SHG) Order Fulfilment, Workforce Coordination, Financial Transparency & Livelihood Management Platform**

---

## 1. System Overview

**SHG Saathi** addresses the critical operational barriers faced by women's Self-Help Groups (SHGs) executing bulk orders from institutional buyers. 

A bulk order of 500 to 5,000+ handmade or handloom units typically must be divided among 10 to 30 home-based women artisans. In the unorganised manual setup:
- Work allocation is verbal and uneven.
- Deadlines are missed due to untracked individual backlogs.
- Products are underpriced by 30–40% because overheads (packaging, thread waste, transport, electricity) are ignored.
- Quality rejections happen after consolidation, wasting time and materials.
- Payout calculations lack itemized transparency, eroding trust.

**SHG Saathi** coordinates production transparently:
1. **Intelligent Fair Work Allocation:** Recommends assignments matching capacity and skills; reviewed and approved by the SHG Leader.
2. **Real-time Verified Progress:** Progress is calculated directly from verified backend records—never spoofed or inferred from predictions.
3. **Quality Assurance with Human Authority:** Computer vision assists with defect detection, but human inspectors have sole decision-making authority over rejections.
4. **Smart Costing Engine:** Enforces full cost breakdown (materials, labour, packaging, transport, operational buffer, margin).
5. **Physical vs Reserved Inventory:** Strict barrier prevents retail marketplace orders from consuming inventory reserved for confirmed bulk orders.
6. **Transparent Earnings & Accountable Payouts:** Every artisan can inspect her own accepted units and itemized earnings. Payouts require committee approval and real bank/UPI transaction proof.

---

## 2. Tech Stack & Architecture

- **Backend Framework:** Python 3.10+ / FastAPI (REST API v1)
- **Database & ORM:** PostgreSQL / SQLite (for zero-setup local dev), SQLAlchemy 2.0 ORM
- **Database Migrations:** Alembic
- **Data Validation & Schemas:** Pydantic v2
- **Authentication & Security:** JWT (JSON Web Tokens), bcrypt password hashing
- **Role-Based Access Control (RBAC):** Five distinct operational roles
- **Real-Time Updates:** WebSocket manager (`/api/v1/notifications/ws/{user_id}`)
- **External AI Integration:** Dedicated adapter layer connecting to independent AI/ML microservice with local deterministic mock fallback

```
   ┌────────────────────────────────┐
   │         React Frontend         │
   └───────────────┬────────────────┘
                   │  REST / WebSocket
                   ▼
   ┌────────────────────────────────┐
   │    Main Backend (FastAPI)      │  <── State, Auth, Costing, Approvals, DB
   └───────────────┬────────────────┘
                   │  Service Adapter (`docs/AI_SERVICE_CONTRACT.md`)
                   ▼
   ┌────────────────────────────────┐
   │    AI/ML Microservice          │  <── Predictions, CV, OCR, Speech, RAG
   │ (http://localhost:8001 / mock) │
   └────────────────────────────────┘
```

---

## 3. User Roles & RBAC Matrix

| Role | Responsibilities & Access Boundary |
|---|---|
| **SHG_LEADER** | Create/manage orders, review capacity, request AI allocation, approve task distribution, review costing, approve batch quality, manage suppliers, approve group payouts. |
| **SHG_MEMBER** | View **only her own** assigned tasks, report progress, submit photo batches, report material shortages/delays, inspect **only her own** earnings and payment history. |
| **BUYER** | Create bulk orders, define specifications, track progress, review accepted consignments, download invoices. |
| **FEDERATION_OFFICER** | Aggregated operational reports, district-wide fulfillment monitoring, financial anomaly audits, dispute assistance. |
| **CUSTOMER** | Browse public catalog, place retail orders with automatic stock reservation, order tracking. |

> **Privacy Guarantee:** Under no circumstances can one member inspect another member's private earnings, capacity parameters, or personal likelihood scores.

---

## 4. 30 Relational Database Models

1. **User** – Core identity and authentication.
2. **SHG** – Self-Help Group organization, bank details, registration.
3. **SHGMember** – Membership linkage, skills array, bank account.
4. **Buyer** – Procurement organizations and GST verification.
5. **BulkOrder** – 13-state bulk order lifecycle.
6. **OrderItem** – Line items, targeted and completed quantities.
7. **Product** – Catalog master (dimensions, category, standard rate).
8. **ProductSpecification** – Inspection tolerances and quality guides.
9. **WorkAllocation** – Fair task assignments to individual members.
10. **MemberCapacity** – Available hours, daily output, active workload.
11. **ProductionRecord** – Verified member progress logs and issue alerts.
12. **ProductionBatch** – Consolidated batches submitted with photos.
13. **QualityInspection** – AI CV visual defect logs & mandatory human decision.
14. **PricingBreakdown** – Itemized costing (Material + Labour + Packaging + Transport + Ops + Margin).
15. **Inventory** – Physical, bulk-reserved, retail-reserved, damaged stock.
16. **InventoryReservation** – Active stock locks with order linkage.
17. **Supplier** – Raw material vendor directory and reliability ratings.
18. **MaterialPurchase** – Inbound procurement logs and invoices.
19. **LogisticsRecord** – Inbound/outbound transit status (no fake GPS).
20. **Shipment** – Consignment tracking and delivery proof links.
21. **MemberEarning** – Itemized gross earnings, deductions, net payable.
22. **Payout** – Fortnightly/monthly group payout batches.
23. **PayoutApproval** – Recorded decision votes with reasons.
24. **RetailOrder** – Retail orders for finished goods.
25. **RetailOrderItem** – Retail order line items.
26. **Notification** – In-app alerts with WebSocket dispatch.
27. **Document** – Uploaded receipts, POs with OCR status (`NEEDS_REVIEW`).
28. **AIAnalysisRecord** – Comprehensive audit log of all AI predictions.
29. **GroupApproval** – Committee voting ledger for major decisions.
30. **AuditLog** – Security and data change trail.

---

## 5. Project Directory Structure

```
shg/
├── backend/
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   │   └── 2caee798c629_initial_schema_30_models.py
│   │   └── env.py
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py               # Auth & RBAC dependencies
│   │   │   └── v1/
│   │   │       ├── api.py            # Route aggregator (58 endpoints)
│   │   │       └── endpoints/        # Auth, Orders, Pricing, Allocations, etc.
│   │   ├── core/
│   │   │   ├── config.py             # Pydantic BaseSettings
│   │   │   ├── security.py           # Bcrypt & JWT
│   │   │   └── permissions.py        # RBAC enforcer
│   │   ├── database/
│   │   │   ├── session.py            # Engine & sessionmaker
│   │   │   └── base.py               # Model registration
│   │   ├── models/                   # 30 SQLAlchemy domain models
│   │   ├── schemas/                  # Pydantic request & response schemas
│   │   ├── services/                 # Core business services
│   │   │   ├── ai_client/            # Microservice client & fallback provider
│   │   │   ├── order_service.py
│   │   │   ├── pricing_service.py
│   │   │   ├── allocation_service.py
│   │   │   ├── production_service.py
│   │   │   ├── quality_service.py
│   │   │   ├── inventory_service.py
│   │   │   ├── payout_service.py
│   │   │   ├── document_service.py
│   │   │   ├── retail_service.py
│   │   │   └── logistics_service.py
│   │   ├── utils/                    # WebSocket manager, responses
│   │   └── main.py                   # FastAPI application entrypoint
│   ├── scripts/
│   │   └── seed_data.py              # Realistic sample data populator
│   ├── tests/                        # Comprehensive test cases
│   ├── .env.example
│   ├── alembic.ini
│   └── requirements.txt
├── docs/
│   ├── FRONTEND_API_CONTRACT.md      # Full specification for React frontend
│   └── AI_SERVICE_CONTRACT.md        # Microservice integration contract
├── .gitignore                        # Secrets & build artifacts ignored
└── README.md
```

---

## 6. Quick Start Guide

### 6.1 Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- `pip` package manager

### 6.2 Installation
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

### 6.3 Environment Configuration
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```
Key settings in `.env`:
```ini
PROJECT_NAME="SHG Saathi Backend"
ENV="development"
DEBUG=true

# Database: SQLite for local dev; or postgresql://user:password@localhost:5432/shg_saathi
DATABASE_URL=sqlite:///./shg_saathi.db

# Authentication
SECRET_KEY=your_secure_random_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI/ML Microservice
# Set to 'mock' for standalone local dev when AI service is not running
AI_SERVICE_BASE_URL=mock
AI_SERVICE_TIMEOUT_SECONDS=10.0
AI_SERVICE_USE_MOCK_FALLBACK=true
```

### 6.4 Run Database Migrations
Apply the initial schema:
```bash
alembic upgrade head
```

### 6.5 Seed Realistic Demonstration Data
Run the seeding script to create sample users, orders, inventory, and workflows:
```bash
python scripts/seed_data.py
```

### 6.6 Start the Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```
- **API Base:** `http://localhost:8000/api/v1`
- **Interactive Swagger Documentation:** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

---

## 7. Demo Credentials

After running `seed_data.py`, use the following accounts for testing:

| Role | Email | Password |
|---|---|---|
| **SHG Leader** | `leader.radha@shgsaathi.in` | `LeaderPass2026!` |
| **SHG Member (Artisan 1)** | `sita.embroidery@shgsaathi.in` | `MemberPass2026!` |
| **SHG Member (Artisan 2)** | `geetha.weaver@shgsaathi.in` | `MemberPass2026!` |
| **Institutional Buyer** | `vikram.procurement@fabcraft.com` | `BuyerPass2026!` |
| **Federation Officer** | `officer.ramesh@nrlm.gov.in` | `OfficerPass2026!` |
| **Retail Customer** | `priya.shoppe@gmail.com` | `CustomerPass2026!` |

---

## 8. Contracts & Integration Reference

- [Frontend API Contract (React Developer Guide)](file:///docs/FRONTEND_API_CONTRACT.md)
- [AI/ML Microservice Contract (AI Engineer Guide)](file:///docs/AI_SERVICE_CONTRACT.md)
