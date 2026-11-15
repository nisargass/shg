# SHG Saathi - Frontend to Backend API Mapping Specification

This document maps all user-facing features and pages in the React frontend to the main FastAPI backend endpoints (`http://localhost:8000/api/v1`).
All frontend API calls are centralized in `src/api/services.js` and use `src/api/apiClient.js` with automatic Bearer JWT token injection.

---

## 1. Authentication & Role Session

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `LoginPage.jsx` | User Login | `/auth/login` | `POST` | `{"email_or_phone": string, "password": string, "role": string}` | `{"access_token": string, "token_type": "bearer", "user": object}` | No | Ready for API (Mock Fallback Active) |
| `Navbar.jsx` | Session Verification | `/auth/me` | `GET` | Headers: `Authorization: Bearer <token>` | `{"id": string, "name": string, "role": string, "shg_id": string}` | Yes | Ready for API |
| `Navbar.jsx` | User Notifications | `/notifications` | `GET` | Headers: `Authorization` | `[{"id": string, "title": string, "message": string, "read": bool}]` | Yes | Ready for API |

---

## 2. Bulk Order Management & OCR Ingestion

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `OrdersPage.jsx` | List Bulk Orders | `/orders` | `GET` | Query: `?status=&category=` | `[{"id": string, "buyer_name": string, "product_name": string, "total_quantity": int, ...}]` | Yes (Leader, Buyer) | Ready for API |
| `OrdersPage.jsx` | Create Bulk Order | `/orders` | `POST` | `{"buyer_name": string, "product_name": string, "total_quantity": int, "unit_price": float, "deadline": string, "specifications": string}` | `{"id": string, "status": "PENDING_ALLOCATION", ...}` | Yes (Leader, Buyer) | Ready for API |
| `OrdersPage.jsx` | OCR PO Document Extraction | `/orders/ocr/extract` | `POST` | `FormData: { file: PDF/Image }` | `{"extracted_fields": {"buyer": string, "qty": int, "deadline": string}, "confidence": float, "unverified_fields": []}` | Yes (Leader) | Ready for API |
| `OrdersPage.jsx` | Confirm OCR Extraction | `/orders/{id}/verify-ocr` | `POST` | `{"verified_fields": object}` | `{"verified": true, "updated_order": object}` | Yes (Leader) | Ready for API |

---

## 3. Intelligent AI Work Allocation & Worker Prediction

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `AllocationPage.jsx` | Fetch Order Allocation & Predictions | `/orders/{id}/allocations` | `GET` | `order_id` in path | `[{"member_id": string, "allocated_qty": int, "feasible_qty": int, "completion_likelihood_percent": float, "prediction_confidence": string, "explanation": string, "factors": []}]` | Yes (Leader) | Ready for API |
| `AllocationPage.jsx` | Leader Approve Allocation | `/orders/{id}/allocations/approve` | `POST` | `{"approved_by": string, "locked": true}` | `{"success": true, "status": "APPROVED", "distributed_tasks_count": int}` | Yes (Leader) | Ready for API |
| `AllocationPage.jsx` | Request AI Rebalance | `/orders/{id}/allocations/rebalance` | `POST` | `{"feedback": string}` | `{"success": true, "revised_allocations": []}` | Yes (Leader) | Ready for API |

---

## 4. Production Monitoring & Shop-Floor Tracking

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `ProductionPage.jsx` | Order Burn-Up Timeline | `/production/orders/{id}/burnup` | `GET` | `order_id` in path | `[{"day": string, "planned": int, "actual": int, "predicted": int}]` | Yes (Leader, Buyer) | Ready for API |
| `ProductionPage.jsx` | Member Roster Progress | `/production/orders/{id}/members` | `GET` | `order_id` in path | `[{"member_id": string, "target": int, "completed": int, "approved": int, "rework": int, "predicted_finish": string}]` | Yes (Leader) | Ready for API |
| `MemberProductionPage.jsx`| Submit Daily Batch | `/production/batches/submit` | `POST` | `FormData: { order_id, units_count, photo }` | `{"batch_id": string, "status": "QUEUED_FOR_QC", "submitted_qty": int}` | Yes (Member) | Ready for API |

---

## 5. AI-Assisted Quality Inspection (Computer Vision)

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `QualityPage.jsx` | List Submitted Batches | `/quality/batches` | `GET` | Query: `?status=` | `[{"batch_id": string, "ai_inspection": {"defect_status": string, "confidence": float, "issues": []}, "human_review": object}]` | Yes (Leader) | Ready for API |
| `QualityPage.jsx` | Record Human Review Decision | `/quality/batches/{id}/decision` | `POST` | `{"decision": "APPROVED" \| "REWORK", "approved_qty": int, "rework_qty": int, "remarks": string}` | `{"success": true, "batch_id": string, "recorded_at": string}` | Yes (Leader) | Ready for API |
| `MemberQualityPage.jsx` | Member View Feedback | `/quality/members/my-batches` | `GET` | Headers: `Authorization` | `[{"batch_id": string, "approved_qty": int, "rework_qty": int, "remarks": string}]` | Yes (Member) | Ready for API |

---

## 6. Smart Pricing & Cost Calculator

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `PricingPage.jsx` | Calculate Unit Cost & Margins | `/pricing/costing/{order_id}` | `GET` | `order_id` in path | `{"cost_components": [], "total_production_cost": float, "buyer_price": float, "group_net_margin": float, "ai_underpricing_alert": bool}` | Yes (Leader) | Ready for API |

---

## 7. Unified Inventory & Stock Reservation

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `InventoryPage.jsx` | Unified Inventory Ledger | `/inventory` | `GET` | None | `[{"sku": string, "physical_stock": int, "reserved_bulk": int, "reserved_retail": int, "free_available": int, "reorder_level": int}]` | Yes (Leader) | Ready for API |

---

## 8. Supplier Management & Logistics

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `SuppliersPage.jsx` | Supplier List & Quotes | `/suppliers` | `GET` | None | `[{"id": string, "name": string, "materials": [], "last_quote": string, "rating": float}]` | Yes (Leader) | Ready for API |
| `LogisticsPage.jsx` | Inbound / Outbound Shipments | `/logistics/shipments` | `GET` | Query: `?type=INBOUND\|OUTBOUND` | `[{"id": string, "carrier": string, "vehicle": string, "status": string, "dispatch_date": string}]` | Yes (Leader, Buyer) | Ready for API |

---

## 9. Financial Transparency, Payouts & Anomalies

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `FinancePage.jsx` | Milestone Payout Ledger | `/finance/payouts/{order_id}` | `GET` | `order_id` in path | `{"milestone": string, "total_amount": float, "quorum_required": int, "votes_received": int, "members_list": []}` | Yes (Leader) | Ready for API |
| `MemberPaymentsPage.jsx`| Member Cast Quorum Vote | `/finance/payouts/{order_id}/vote`| `POST` | `{"vote": "APPROVED" \| "DISPUTED"}` | `{"success": true, "new_vote_count": int}` | Yes (Member) | Ready for API |
| `FinancePage.jsx` | Leader Authorize Bank Release| `/finance/payouts/{order_id}/confirm`| `POST` | None | `{"success": true, "bank_dispatch_status": "PROCESSED"}` | Yes (Leader) | Ready for API |
| `AnomaliesPage.jsx` | Financial Audit Anomalies | `/finance/anomalies` | `GET` | None | `[{"id": string, "category": string, "severity": "HIGH" \| "MEDIUM", "description": string, "status": string}]` | Yes (Leader) | Ready for API |

---

## 10. Voice & RAG Knowledge Assistant

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `VoiceAssistantPage.jsx` | RAG Query with Citations | `/assistant/rag/query` | `POST` | `{"query": string, "language": "English" \| "Hindi" \| "Kannada"}` | `{"answer": string, "sources": [{"title": string, "excerpt": string}], "confidence": float}` | Yes (Member, Leader) | Ready for API |

---

## 11. Retail Marketplace

| Frontend Page | Feature | Backend Endpoint | HTTP Method | Request Fields | Response Fields | Auth Required | Status |
|---|---|---|---|---|---|---|---|
| `MarketplacePage.jsx` | Public Product Catalog | `/retail/products` | `GET` | Query: `?category=` | `[{"id": string, "name": string, "price": float, "available_stock": int, "shg_name": string}]` | No | Ready for API |
| `CartPage.jsx` | Place Retail Order | `/retail/orders` | `POST` | `{"items": [{"product_id": string, "qty": int}], "shipping_address": string}` | `{"order_id": string, "status": "CONFIRMED", "estimated_delivery": string}` | No / Customer | Ready for API |

