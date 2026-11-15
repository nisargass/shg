# SHG Saathi – Complete React Frontend

> **Agentic AI-powered SHG Business Management, Production Coordination and Market Access Platform.**

SHG Saathi is an enterprise-grade digital platform engineered for Women's Self-Help Groups (SHGs). It solves the core challenges of fulfilling bulk orders: fair piece-rate work allocation, worker completion prediction, shop-floor production monitoring, AI-assisted visual quality control, anti-underpricing costing, unified inventory reservation, and democratic group-approved payouts.

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js (v18.0.0 or higher recommended)
- npm (v9.0.0 or higher)

### Installation
```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Create your environment configuration
cp .env.example .env
```

### Running the Development Server
```bash
npm run dev
```
Open your browser at `http://localhost:3000` (or the port specified by Vite).

### Production Build & Verification
```bash
npm run build
```
Builds the optimized production assets into `dist/` and runs full syntax and bundle verification.

---

## 🎨 Enterprise Design System
Designed specifically for rural business SaaS operations with accessible typography, clean layouts, and high-contrast indicators:
- **Primary Deep Navy Blue:** `#123B5D`
- **Secondary Teal:** `#168B80`
- **Amber Accent:** `#E6A23C`
- **Alert Crimson:** `#C83D43`
- **Background:** `#F5F7F9`
- **Cards & Surfaces:** `#FFFFFF`
- **Text Primary:** `#243746`

---

## 👥 Role-Based Portals & Key Features

### 1. SHG Leader Portal (`/leader`)
- **Executive Operations Dashboard:** Real-time KPI counters, production vs target Recharts bar charts, order lifecycle pie chart, and live autonomous agent feeds.
- **Bulk Order Management (`/leader/orders`):** Master-detail order view, specifications, PDF PO document upload, and OCR data verification.
- **Intelligent Work Allocation (`/leader/allocation`):** Multi-agent allocation matrix factoring in skill rating, daily hours, speed rate, and historical quality.
- **Worker Completion Likelihood Prediction:** Distinct separation of actual verified production progress from AI likelihood predictions.
- **Shop-Floor Production Monitor (`/leader/production`):** Cumulative burn-up tracking curves (planned vs actual vs predicted finish date).
- **Computer Vision Quality Control (`/leader/quality`):** Batch photo analysis with defect bounding boxes, confidence score, and human sign-off (Approve / Rework / Reject).
- **Smart Pricing & Cost Calculator (`/leader/pricing`):** Material, labor, packaging, freight and overheads itemization with automated underpricing warnings.
- **Unified Inventory (`/leader/inventory`):** Shared wholesale/retail inventory with mathematical reservation locks preventing double-selling.
- **Suppliers & Procurement (`/leader/suppliers`):** Vendor directory, quotation tracking, lead times, and rating benchmarks.
- **Transport & Logistics (`/leader/logistics`):** Inbound raw material consignments & Outbound carton dispatches with carrier tracking.
- **Democratic Group Payouts (`/leader/finance`):** Transparent piece-rate ledger requiring 60% affirmative member quorum voting before disbursement.
- **Financial Anomaly Review (`/leader/anomalies`):** Assistive audit flags for duplicate vendor invoices and excess cutting scrap.
- **Agentic AI Live Console (`/leader/ai`):** Activity streams for all 10 specialized agents with human-in-the-loop approvals.
- **NRLM Cluster Reports (`/leader/reports`):** Recharts longitudinal turnover and quality trends.

### 2. SHG Member Mobile Portal (`/member`)
- **Accessible & Mobile-First UI:** Large high-contrast touch buttons, clear counters, and friendly greetings.
- **Private Artisan Workspace:** Members strictly see only their personal tasks, feasible quotas, and private bank compensation records.
- **Two Distinct Metrics:** Displays verified actual progress side-by-side with AI completion likelihood.
- **Batch Submission (`/member/production`):** One-tap unit counters and photo capture upload.
- **My Quality Feedback (`/member/quality`):** Constructive feedback on submitted batches with leader remarks.
- **My Earnings Ledger (`/member/earnings`):** Transparent piece-rate breakdown without hidden deductions.
- **Quorum Voting (`/member/payments`):** Democratic ballot to approve or dispute group payout calculations.
- **Voice Saathi (`/member/assistant`):** Multilingual voice-first assistant in Kannada, Hindi, and English for low-literacy accessibility.

### 3. Wholesale Buyer Portal (`/buyer`)
- **Direct Institutional Sourcing:** Submit custom product specs, target volume, and delivery dates.
- **Milestone Production Tracker (`/buyer/orders`):** Live batch progress and export quality certification without exposing private member data.
- **Consignment Tracking:** Carrier partner, vehicle number, and dispatch waybills.

### 4. Federation Officer Portal (`/federation`)
- **Cluster Development Dashboard:** Oversight of 24 village SHGs across Ramanagara district.
- **Lakhpati Didi Mission Tracker (`/federation/reports`):** Progress toward elevating women artisans to sustained annual incomes > ₹1,00,000.
- **Comparative Cluster Analytics:** Turnover and on-time fulfillment rates across participating sanghas.

### 5. Public Retail Marketplace (`/marketplace`)
- **Direct-to-Consumer Storefront:** Authentic handloom tote bags, Kasuti embroidery, and pure Salem turmeric.
- **Shared Stock Guard:** Displays only freely available stock, never consuming stock reserved for bulk orders.
- **Full Shopping Cart & Checkout (`/marketplace/cart`):** Instant order placement with direct artisan collective credit.

---

## 📁 Complete Folder Structure

```
frontend/
├── .env.example                        # Environment variables template
├── FRONTEND_API_MAPPING.md             # Complete FastAPI endpoint mapping
├── MOCK_DATA_GUIDE.md                  # Mock data policy & persona guide
├── README.md                           # Documentation & quickstart
├── index.html                          # Vite entry HTML with Google fonts
├── package.json                        # Dependencies (React, Vite, Recharts, Lucide, Axios)
├── vite.config.js                      # Vite server & API proxy config
└── src/
    ├── App.jsx                         # Central Router & protected routes
    ├── index.css                       # Global design system & utility classes
    ├── main.jsx                        # React root entry point
    ├── api/
    │   ├── apiClient.js                # Central Axios client with JWT interceptor
    │   └── services.js                 # Unified services (orders, quality, finance, RAG)
    ├── context/
    │   └── AuthContext.jsx             # Auth, role switching, cart & notifications context
    ├── mock/
    │   └── mockData.js                 # Production-grade offline verification dataset
    ├── components/
    │   └── common/
    │       ├── Navbar.jsx              # Universal top navigation with role switcher & cart
    │       ├── Navbar.css
    │       ├── Sidebar.jsx             # Role-aware sidebar with Lucide icons
    │       ├── Sidebar.css
    │       ├── Footer.jsx              # Enterprise footer
    │       ├── Button.jsx
    │       ├── Card.jsx
    │       └── Badge.jsx
    ├── layouts/
    │   ├── PublicLayout.jsx            # Public pages wrapper (Nav + Footer)
    │   ├── LeaderLayout.jsx            # Leader dashboard wrapper (Nav + Sidebar)
    │   ├── MemberLayout.jsx            # Member mobile-first layout
    │   ├── BuyerLayout.jsx             # Buyer sourcing portal layout
    │   └── FederationLayout.jsx        # NRLM Federation layout
    └── pages/
        ├── landing/
        │   ├── LandingPage.jsx         # Complete marketing & workflow landing page
        │   └── LandingPage.css
        ├── auth/
        │   └── LoginPage.jsx           # Login with 1-click demo role tabs
        ├── leader/
        │   ├── Dashboard.jsx           # Leader overview & Recharts analytics
        │   ├── OrdersPage.jsx          # Bulk order management & OCR verification
        │   ├── AllocationPage.jsx      # AI work allocation & likelihood prediction
        │   ├── ProductionPage.jsx      # Production tracking & burn-up curve
        │   ├── QualityPage.jsx         # AI Computer Vision quality inspection
        │   ├── PricingPage.jsx         # Anti-underpricing cost calculator
        │   ├── InventoryPage.jsx       # Unified stock reservation management
        │   ├── SuppliersPage.jsx       # Supplier quotes & procurement
        │   ├── LogisticsPage.jsx       # Inbound / outbound freight tracking
        │   ├── MembersPage.jsx         # Artisan skill profiles & daily capacity
        │   ├── FinancePage.jsx         # Democratic group payout approval
        │   ├── AnomaliesPage.jsx       # Financial audit anomaly review
        │   ├── RetailManagementPage.jsx# Storefront inventory & sales manager
        │   ├── AgentInsightsPage.jsx   # 10 Multi-agent activity feeds
        │   ├── ReportsPage.jsx         # Executive analytics & turnover
        │   └── SettingsPage.jsx        # Group governance & quorum rules
        ├── member/
        │   ├── Dashboard.jsx           # Accessible artisan dashboard
        │   ├── MemberTasksPage.jsx     # Assigned tasks & deadline quotas
        │   ├── MemberProductionPage.jsx# Batch unit counter & photo submission
        │   ├── MemberQualityPage.jsx   # Visual defect feedback & leader remarks
        │   ├── MemberEarningsPage.jsx  # Private piece-rate compensation ledger
        │   ├── MemberPaymentsPage.jsx  # Democratic quorum ballot
        │   ├── VoiceAssistantPage.jsx  # Multilingual Voice Saathi (KN/HI/EN)
        │   └── MemberHelpPage.jsx      # NRLM Lakhpati Didi guidelines
        ├── buyer/
        │   ├── BuyerDashboard.jsx      # Sourcing overview
        │   ├── BuyerCreateOrderPage.jsx# Bulk PO submission
        │   ├── BuyerOrdersPage.jsx     # Production tracking without member leak
        │   └── BuyerCatalogPage.jsx    # Wholesale craft capabilities
        ├── federation/
        │   ├── FederationDashboard.jsx # Cluster overview & comparative charts
        │   ├── FederationShgsPage.jsx  # Registered SHG directory
        │   ├── FederationProductionPage.jsx # Aggregated orders tracker
        │   └── FederationReportsPage.jsx# Lakhpati Didi certified registry
        └── marketplace/
            ├── MarketplacePage.jsx     # Public artisan shopping catalog
            └── CartPage.jsx            # Cart, checkout & direct artisan credit
```

---

## 🏛️ Team Architecture & Integration

```
FRONTEND (React + Vite)
       │
       │ HTTP API (http://localhost:8000/api/v1)
       ▼
MAIN BACKEND (FastAPI + PostgreSQL)
       │
       │ Internal Microservice Calls
       ▼
AI / ML MICROSERVICE (LangGraph Agents, OCR, YOLO CV, Speech AI)
```

- The frontend communicates **strictly with the Main FastAPI backend** via `src/api/apiClient.js`.
- It never communicates directly with internal AI microservices or invents undocumented endpoints.
- Review `FRONTEND_API_MAPPING.md` for full request/response schemas.

