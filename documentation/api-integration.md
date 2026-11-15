# SHG Saathi – API Integration & Contract Specification

## 1. Network Endpoints & Protocols

| Service | Protocol | Host / Port | API Root Prefix | Interactive Docs |
|---------|----------|-------------|-----------------|------------------|
| **React Frontend** | HTTP / SPA | `http://localhost:5173` | `/` | Browser UI |
| **Enterprise Backend** | HTTP / JSON | `http://localhost:8000` | `/api/v1` | `http://localhost:8000/docs` |
| **AI/ML Microservice** | HTTP / JSON | `http://localhost:8001` | `/ai/v1` & `/api/v1/ai` | `http://localhost:8001/docs` |

---

## 2. Authentication & Authorization Headers

### A. Client ↔ Backend (JWT Bearer Token)
Every frontend request to protected endpoints must pass the user's JWT token in the `Authorization` header:
```http
GET /api/v1/auth/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOi...
```

For local development only, the backend accepts the 5 preset 1-click persona tokens:
- `demo-jwt-token-leader` (Role: `SHG_LEADER`)
- `demo-jwt-token-member` (Role: `SHG_MEMBER`)
- `demo-jwt-token-buyer` (Role: `BUYER`)
- `demo-jwt-token-federation` (Role: `FEDERATION_OFFICER`)
- `demo-jwt-token-customer` (Role: `CUSTOMER`)

These are not real user credentials and are rejected when `ENV=production`.

### B. Backend ↔ AI Microservice (Shared Service Key)
All internal calls from the Backend to the AI Microservice pass the mutual secret header:
```http
POST /api/v1/ai/workforce/optimize-allocation HTTP/1.1
Host: localhost:8001
X-SHG-Service-Key: ${SHG_SERVICE_KEY}
Content-Type: application/json
```

---

## 3. Core API Endpoints

### 3.1 Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/login/json`
  - Body: `{"email": "savitribai@pragati-shg.org", "password": "Saathi@2026"}`
  - Returns: `{"access_token": "...", "token_type": "bearer", "user": {...}}`
- `GET /api/v1/auth/me`
  - Returns authenticated user profile, assigned SHG, role, and system permissions.

### 3.2 Bulk Orders & Allocations (`/api/v1/orders`)
- `GET /api/v1/orders`
  - Retrieves all active and historical bulk orders. Returns camelCase and snake_case computed properties.
- `POST /api/v1/orders`
  - Creates a new wholesale bulk order.
- `GET /api/v1/orders/{order_id}/allocations`
  - Fetches AI-optimized member allocation plan with feasibility probabilities, daily speed rates, and confidence scores.
- `POST /api/v1/orders/{order_id}/allocations/approve`
  - Human review approval gate by the SHG Leader.
  - Body: `{"approvedBy": "Savitribai Shinde", "timestamp": "2026-11-14T10:00:00Z"}`
- `POST /api/v1/orders/{order_id}/allocations/rebalance`
  - Rebalances workload dynamically if a member reports incapacity or emergency leave.

### 3.3 Quality Inspection & Decision Gate (`/api/v1/quality`)
- `GET /api/v1/quality/batches`
  - Retrieves batches undergoing inspection with AI computer vision outputs and human decision status.
- `POST /api/v1/quality/batches/{batch_id}/decision`
  - Records leader physical review decision.
  - Body: `{"status": "APPROVED_WITH_REWORK", "approvedQty": 29, "reworkQty": 6, "remarks": "Restitch zipper"}`

### 3.4 Dynamic Pricing & Cost Structure (`/api/v1/pricing`)
- `GET /api/v1/pricing/costing/{order_id}`
  - Returns complete 8-component cost breakdown (Raw Material, Handles, Zippers, Labor, Packaging, Logistics, Overhead, Margin) alongside AI market benchmark guidance.

### 3.5 Group Finance & Quorum Payouts (`/api/v1/finance`)
- `GET /api/v1/finance/payouts/{order_id}`
  - Returns payout roll with piece-rate earnings, deduction adjustments, and quorum voting status.
- `POST /api/v1/finance/payouts/{order_id}/vote`
  - Member casts quorum vote: `{"member_id": "mem_01", "vote": "APPROVED"}`.
- `POST /api/v1/finance/payouts/{order_id}/confirm`
  - Leader authorizes bank ledger transfer once $\ge 60\%$ quorum is validated.
- `GET /api/v1/finance/anomalies`
  - Scans payouts using Isolation Forest ML model and flags suspicious earnings or volume discrepancies.

### 3.6 Multilingual RAG Knowledge Assistant (`/api/v1/assistant`)
- `POST /api/v1/assistant/rag/query`
  - Body: `{"query": "How is piece-rate calculated?", "language": "English"}`
  - Returns: `{"answer": "...", "sources": ["SHG Bylaws Sec 4.2"], "language": "English"}`
  - Supports English, Hindi (हिंदी), and Kannada (ಕನ್ನಡ).

---

## 4. Standard Response Envelope

All standard responses adhere to the unified API envelope structure:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2026-11-14T22:00:00Z"
}
```
Errors return:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Detailed description of error",
    "details": []
  }
}
```
The React `frontend/src/api/apiClient.js` includes an automatic unwrapping interceptor that transparently unwraps `response.data.data` so legacy components operate without syntax disruption.

