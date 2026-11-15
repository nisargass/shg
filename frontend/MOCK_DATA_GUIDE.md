# SHG Saathi - Mock Data & Offline Verification Guide

## Purpose & Architecture
During hackathon development and independent frontend verification, the backend or AI microservice may be offline or undergoing schema migrations.

To ensure reviewers can explore **every operational screen, form, chart, and modal without broken screens or blank states**, SHG Saathi contains an isolated, production-grade demo dataset located strictly in:
```
src/mock/mockData.js
```

### Core Safety Rules
1. **Zero Mock Leakage into UI Logic**:
   Frontend components do not hardcode fake strings. All data fetching flows through `src/api/services.js`.
2. **Seamless Backend Handoff**:
   When the FastAPI backend is running at `http://localhost:8000/api/v1`, `apiClient` requests resolve to real PostgreSQL records. If the backend is offline, `services.js` intercepts the request and returns the verified demo state without throwing unhandled network crashes.
3. **Clearly Labelled Demo Indicators**:
   Every demo screen displays a prominent `DEMO ENVIRONMENT` or `SIMULATED RECORD` pill badge so observers know whether they are inspecting verified mock records or live production database tables.

---

## Personas Included in `src/mock/mockData.js`

| Persona Role | Account Name | Context & Responsibilities |
|---|---|---|
| **SHG Leader** | Savitribai Shinde | Leader of Pragati Mahila Sangha. Manages 8 artisans, reviews AI allocations, approves quality inspection, locks democratic payouts. |
| **SHG Member** | Sunita Rathod | Master artisan in Channapatna. Assigned 220 bags, has verified 180 units completed, accesses voice assistant, casts payout vote. |
| **Wholesale Buyer** | Arvind Deshmukh | Procurement Manager at EcoFab Bangalore Retailers Ltd. Contracts 1,200 tote bags, monitors production milestones. |
| **Federation Officer** | Deepa Narayan, KAS | Cluster Development Officer at Sanjeevini KSRLPS (NRLM). Tracks 24 SHGs, Lakhpati Didi metrics, cluster quality rates. |
| **Retail Shopper** | Pooja Hegde | Public retail consumer buying handicrafts and natural turmeric directly from rural artisan storefront. |

---

## 1-Click Role Switcher in Navigation Bar
In the top right navigation bar of the application, click **"Active Role"** to immediately switch live personas between **Leader, Member, Buyer, Federation Officer, and Customer**.

This allows evaluators to verify role isolation instantly:
- When logged in as **Sunita Rathod (Member)**, navigate to `/member/earnings` &mdash; only Sunita's personal piece-rate units and bank account are visible.
- When logged in as **Buyer**, navigate to `/buyer/orders` &mdash; aggregate production milestones are visible, while individual member names and private financial details remain concealed.

---

## How to Disable Mock Fallback and Enforce Strict Backend Calls

In `frontend/.env`:
```bash
# Set to false to disable mock fallback and require real FastAPI backend responses
VITE_ENABLE_MOCK_FALLBACK=false
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
When `VITE_ENABLE_MOCK_FALLBACK=false`, any offline API endpoint will surface standard HTTP 503 / network error banners in the UI.

