# SHG Saathi – Frontend API Contract

**Base URL:** `/api/v1`  
**Authentication Scheme:** `Bearer <JWT_TOKEN>` in `Authorization` header  
**Response Format:** Standard Envelope
```json
{
  "success": true,
  "message": "Human readable confirmation message",
  "data": {},
  "errors": null
}
```

---

## 1. Authentication & Users

### 1.1 User Registration
- **Endpoint:** `POST /api/v1/auth/register`
- **Auth:** None
- **Request Body:**
```json
{
  "email": "laxmi.leader@shgsaathi.in",
  "password": "StrongPassword2026!",
  "full_name": "Laxmi Devi",
  "phone": "+919876543210",
  "role": "SHG_LEADER"
}
```
- **Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "email": "laxmi.leader@shgsaathi.in",
    "full_name": "Laxmi Devi",
    "phone": "+919876543210",
    "role": "SHG_LEADER",
    "is_active": true,
    "created_at": "2026-11-07T10:00:00Z"
  },
  "errors": null
}
```

### 1.2 User Login
- **Endpoint:** `POST /api/v1/auth/login`
- **Auth:** None (OAuth2 Password flow / Form-Data)
- **Request Form:** `username=laxmi.leader@shgsaathi.in&password=StrongPassword2026!`
- **Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "laxmi.leader@shgsaathi.in",
    "full_name": "Laxmi Devi",
    "role": "SHG_LEADER",
    "is_active": true,
    "created_at": "2026-11-07T10:00:00Z"
  }
}
```

### 1.3 Current User Profile
- **Endpoint:** `GET /api/v1/auth/me`
- **Auth:** Bearer Token

---

## 2. SHG Management

### 2.1 Create SHG
- **Endpoint:** `POST /api/v1/shgs`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Request Body:**
```json
{
  "name": "Prerana Mahila Sangha",
  "registration_number": "KA-MYS-2024-889",
  "address": "Hunsur Taluk, Mysuru District",
  "district": "Mysuru",
  "state": "Karnataka",
  "bank_account_details": "Canara Bank, A/C: 1234567890, IFSC: CNRB0001234"
}
```

### 2.2 List SHGs
- **Endpoint:** `GET /api/v1/shgs`
- **Auth:** Authenticated Users

### 2.3 List SHG Members
- **Endpoint:** `GET /api/v1/shgs/{shg_id}/members`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`

---

## 3. Members & Workforce Coordination

### 3.1 Register Member
- **Endpoint:** `POST /api/v1/members`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Request Body:**
```json
{
  "user_id": 2,
  "shg_id": 1,
  "skills": ["embroidery", "weaving", "packaging"],
  "bank_account_number": "98765432101",
  "ifsc_code": "SBIN0004567"
}
```

### 3.2 Member View Her Own Tasks
- **Endpoint:** `GET /api/v1/members/me/tasks`
- **Auth:** `SHG_MEMBER`
- **Response (200 OK):**
```json
{
  "success": true,
  "message": "My assigned tasks retrieved successfully",
  "data": [
    {
      "id": 10,
      "order_title": "Festive Jute Shopping Bags (500 units)",
      "order_number": "ORD-SHG-20261107-7A8B9C",
      "product_name": "Handmade Jute Bag",
      "allocated_quantity": 40,
      "completed_quantity": 15,
      "pending_quantity": 25,
      "unit_rate": 45.00,
      "deadline": "2026-11-20T18:00:00Z",
      "status": "IN_PROGRESS",
      "progress_percentage": 37.5
    }
  ]
}
```

### 3.3 Get Member Capacity
- **Endpoint:** `GET /api/v1/members/{member_id}/capacity`
- **Auth:** The member herself or her `SHG_LEADER`
- **Note:** Strict privacy: Members cannot view other members' capacity or private scores.

---

## 4. Bulk Orders & Products

### 4.1 Create Bulk Order
- **Endpoint:** `POST /api/v1/orders`
- **Auth:** `BUYER`, `SHG_LEADER`
- **Request Body:**
```json
{
  "title": "Corporate Diwali Artisan Gift Bags",
  "description": "500 eco-friendly jute bags with block printed logo",
  "target_delivery_date": "2026-11-30T00:00:00Z",
  "currency": "INR",
  "shg_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 500,
      "unit_price": 180.00,
      "specifications": "Reinforced double handles, natural jute, 38x42cm"
    }
  ]
}
```

### 4.2 Transition Order Status
- **Endpoint:** `POST /api/v1/orders/{order_id}/transition`
- **Auth:** `SHG_LEADER`, `BUYER`, `FEDERATION_OFFICER`
- **Permitted Lifecycle:**
  `DRAFT` → `SUBMITTED` → `ACCEPTED` → `PRICING_PENDING` → `ALLOCATION_PENDING` → `IN_PRODUCTION` → `QUALITY_CHECK` → `READY_FOR_SHIPMENT` → `SHIPPED` → `DELIVERED` → `COMPLETED` (plus `CANCELLED`, `REJECTED`)
- **Request Body:**
```json
{
  "new_status": "ACCEPTED",
  "reason": "SHG has verified raw material supply and capacity."
}
```

---

## 5. Pricing & Accurate Costing

### 5.1 Calculate Pricing Breakdown
- **Endpoint:** `POST /api/v1/pricing`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Formula:** Material + Labour + Packaging + Transportation + Operational Expenses + Profit Margin
- **Request Body:**
```json
{
  "bulk_order_id": 1,
  "total_material_cost": 45000.00,
  "labor_cost": 25000.00,
  "packaging_cost": 3500.00,
  "transportation_cost": 4000.00,
  "operational_expenses": 2500.00,
  "profit_margin_percentage": 15.0,
  "notes": "Includes 5% buffer for humidity-proof storage lining."
}
```

### 5.2 Leader Approve Pricing
- **Endpoint:** `PUT /api/v1/pricing/{pricing_id}/approve`
- **Auth:** `SHG_LEADER`
- **Request Body:**
```json
{
  "is_approved": true,
  "final_approved_price": 185.00,
  "notes": "Approved after negotiation with buyer representative."
}
```

---

## 6. Work Allocation & Capacity

### 6.1 Get AI Allocation Recommendations
- **Endpoint:** `GET /api/v1/allocations/ai-recommendations?bulk_order_id=1&order_item_id=1`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Output:** AI recommendations per member with likelihood percentages and factors.

### 6.2 Propose Work Allocations
- **Endpoint:** `POST /api/v1/allocations/propose`
- **Auth:** `SHG_LEADER`
- **Validation Rule:** Total proposed allocated quantity CANNOT exceed order item quantity.
- **Request Body:**
```json
{
  "bulk_order_id": 1,
  "order_item_id": 1,
  "allocations": [
    {
      "bulk_order_id": 1,
      "order_item_id": 1,
      "member_id": 1,
      "allocated_quantity": 40,
      "unit_rate": 50.00,
      "deadline": "2026-11-25T18:00:00Z",
      "ai_recommended": true
    }
  ]
}
```

### 6.3 Leader Approve or Edit Allocation
- **Endpoint:** `PUT /api/v1/allocations/{allocation_id}`
- **Auth:** `SHG_LEADER`
- **Request Body:**
```json
{
  "allocated_quantity": 40,
  "unit_rate": 50.00,
  "status": "APPROVED_BY_LEADER"
}
```

---

## 7. Production Monitoring

### 7.1 Record Production Progress
- **Endpoint:** `POST /api/v1/production/progress`
- **Auth:** `SHG_MEMBER`
- **Request Body:**
```json
{
  "work_allocation_id": 1,
  "quantity_produced": 10,
  "remarks": "Completed front pocket embroidery",
  "reported_shortage": null,
  "reported_delay": null
}
```

### 7.2 Submit Completed Batch
- **Endpoint:** `POST /api/v1/production/batch`
- **Auth:** `SHG_MEMBER`
- **Request Body:**
```json
{
  "work_allocation_id": 1,
  "quantity": 20,
  "photo_urls": [
    "/uploads/batch_1_front.jpg",
    "/uploads/batch_1_seam.jpg"
  ]
}
```

---

## 8. Quality Inspection

### 8.1 Trigger AI Computer Vision Inspection
- **Endpoint:** `POST /api/v1/quality/inspect/{inspection_id}/ai`
- **Auth:** `SHG_LEADER`, `BUYER`
- **Status Outcome:** Sets status to `PENDING_HUMAN_REVIEW` with visual defects and score.

### 8.2 Submit Human Quality Decision
- **Endpoint:** `PUT /api/v1/quality/inspect/{inspection_id}/decision`
- **Auth:** `SHG_LEADER`, `BUYER`
- **Rule:** AI NEVER makes the final rejection decision. Human decision is mandatory.
- **Request Body:**
```json
{
  "human_decision": "APPROVED",
  "rejection_reason": null
}
```

---

## 9. Inventory & Stock Reservations

### 9.1 Register Inventory
- **Endpoint:** `POST /api/v1/inventory`
- **Auth:** `SHG_LEADER`
- **Available Stock Formula:** `physical_stock - bulk_reserved - retail_reserved - damaged`

### 9.2 Stock Reservation (Bulk vs Retail Separation)
- **Endpoint:** `POST /api/v1/inventory/reserve`
- **Auth:** `SHG_LEADER`, `CUSTOMER`
- **Strict Rule:** Retail orders cannot consume bulk-reserved inventory.

---

## 10. Earnings & Transparent Group Payouts

### 10.1 Calculate Task Earnings
- **Endpoint:** `POST /api/v1/earnings/calculate/{allocation_id}`
- **Auth:** `SHG_LEADER`
- **Formula:** `gross = accepted_quantity * approved_rate`; `net = gross - deductions`

### 10.2 Member View Personal Earnings
- **Endpoint:** `GET /api/v1/earnings/me`
- **Auth:** `SHG_MEMBER`
- **Privacy Guarantee:** Returns ONLY the authenticated member's earnings.

### 10.3 Create Group Payout Batch
- **Endpoint:** `POST /api/v1/payouts`
- **Auth:** `SHG_LEADER`

### 10.4 Group Payout Approval
- **Endpoint:** `PUT /api/v1/payouts/{payout_id}/approval`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Status Outcome:** Moves to `PAYMENT_PENDING`

### 10.5 Confirm Genuine Payment
- **Endpoint:** `PUT /api/v1/payouts/{payout_id}/confirm-payment`
- **Auth:** `SHG_LEADER`
- **Rule:** Strict requirement for genuine bank/UPI transaction reference number.
- **Request Body:**
```json
{
  "payment_method": "Bank Transfer (NEFT)",
  "transaction_ref": "NEFT-SBI-20261107-88992",
  "payment_date": "2026-11-07T12:00:00Z",
  "notes": "Verified via Bank Statement page 3."
}
```

---

## 11. Document OCR & Verification

### 11.1 Upload Document
- **Endpoint:** `POST /api/v1/documents/upload`
- **Format:** `multipart/form-data`
- **Fields:** `title` (str), `document_type` (str), `file` (binary PDF/JPG/PNG)
- **Outcome:** Status `NEEDS_REVIEW`. Never auto-approved.

### 11.2 Verify OCR Data
- **Endpoint:** `PUT /api/v1/documents/{document_id}/verify`
- **Auth:** `SHG_LEADER`, `FEDERATION_OFFICER`
- **Outcome:** Status `VERIFIED`.

---

## 12. Multilingual Assistant & Notifications

### 12.1 Assistant Query
- **Endpoint:** `POST /api/v1/assistant/chat`
- **Auth:** Authenticated Users
- **Languages:** `kn` (Kannada), `hi` (Hindi), `en` (English)
- **Request Body:**
```json
{
  "query": "ನನ್ನ ಗಳಿಕೆಯನ್ನು ಯಾವಾಗ ಜಮಾ ಮಾಡಲಾಗುತ್ತದೆ?",
  "language": "kn"
}
```

### 12.2 Real-time Notifications WebSocket
- **URL:** `ws://localhost:8000/api/v1/notifications/ws/{user_id}`
- **Events:** Live notifications for work assignment, quality review, and payment confirmation.

---

## 13. Integration & Testing Notes

1. **AI Service Independence:** During frontend development or testing when the AI/ML microservice is offline or not yet deployed, the backend seamlessly runs with internal deterministic heuristic mocks (`AI_SERVICE_BASE_URL=mock`).
2. **Contract-First Testing:** The backend provides mock fallback payloads that mirror the exact shape and data structures expected from the live AI microservice.
3. **Automated Test Execution Note:** Automated unit test suites that exercise synchronous ASGI thread bridges (such as Starlette `TestClient` on Windows with Python 3.13) should be run in an asynchronous harness (`httpx.AsyncClient(transport=ASGITransport(app=app))`) or tested against a running server (`uvicorn app.main:app --port 8000`) to prevent local AnyIO thread bridge hangs.
4. **Seed Demonstration Data:** Complete realistic mock data across all 5 roles can be loaded instantly via `python scripts/seed_data.py` (or from workspace root `python backend/scripts/seed_data.py`).

