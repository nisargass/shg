# SHG Saathi – AI/ML Microservice Integration Contract

**Document Version:** 1.0.0  
**Base URL:** Configured via `AI_SERVICE_BASE_URL` (Default: `http://localhost:8001`)  
**Protocol:** HTTP/1.1 REST JSON  
**Auth / Header:** `X-SHG-Service-Key` or Internal Network Token  
**Client Timeout:** 10.0 seconds (Default)

---

## 1. Architectural Principles

1. **Non-Blocking / Graceful Degradation:** The main backend must never crash or freeze if the AI/ML microservice is offline, experiencing high latency, or throwing internal errors. Manual workflows (e.g. manual work allocation, manual costing, manual visual inspection) remain fully operational.
2. **Separation of Verified Operational Truth & Predictions:** AI predictions (e.g., worker completion likelihood, anomaly flags, OCR candidates) are strictly stored with separate statuses (such as `NEEDS_REVIEW` or `PENDING_HUMAN_REVIEW`). AI output is NEVER automatically approved as verified legal, financial, or operational fact.
3. **No Fabricated Data Substitution:** When an AI endpoint fails, the backend records the failure explicitly (`status: FAILED` or `TIMEOUT`) and prompts the human operator, rather than silently injecting synthetic or spoofed predictions.

---

## 2. Capabilities & Endpoints

### 2.1 OCR Document Extraction
- **Endpoint:** `POST /api/v1/ai/ocr/extract`
- **Purpose:** Extracts structured fields from purchase orders, invoices, and material receipts.
- **Request Payload:**
```json
{
  "document_id": 101,
  "document_type": "PURCHASE_ORDER",
  "file_url": "/uploads/documents/po_789.pdf",
  "mime_type": "application/pdf"
}
```
- **Response Payload:**
```json
{
  "success": true,
  "confidence_score": 0.94,
  "extracted_data": {
    "buyer_name": "FabIndia Artisans Pvt Ltd",
    "po_number": "PO-2026-902",
    "order_date": "2026-11-01",
    "delivery_deadline": "2026-12-15",
    "items": [
      {
        "product_name": "Handmade Jute Bag with Block Print",
        "quantity": 500,
        "unit_price": 180.00,
        "specifications": "Dimensions: 38x42cm, 100% natural jute"
      }
    ],
    "total_amount": 90000.00
  },
  "raw_text": "...",
  "notes": "Handwritten signature detected in bottom right."
}
```

---

### 2.2 Worker Completion Likelihood Prediction
- **Endpoint:** `POST /api/v1/ai/workforce/completion-likelihood`
- **Purpose:** Predicts whether an individual member can feasibly finish an assigned quantity before a given deadline.
- **Request Payload:**
```json
{
  "member_id": 14,
  "product_id": 3,
  "proposed_quantity": 40,
  "deadline": "2026-11-20T18:00:00Z",
  "available_hours_per_day": 6.0,
  "current_workload": 10.0,
  "historical_completion_rate": 96.5,
  "skills": ["stitching", "embroidery"]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "member_id": 14,
  "completion_likelihood_percentage": 92.4,
  "estimated_completion_date": "2026-11-18T16:00:00Z",
  "confidence_score": 0.88,
  "factors": [
    "High historical completion rate (96.5%)",
    "Adequate daily working hours available",
    "Specialized stitching skills align with product"
  ],
  "explanation": "Member has reliable track record with similar batch sizes and low active backlog."
}
```

---

### 2.3 Intelligent Work Allocation Recommendation
- **Endpoint:** `POST /api/v1/ai/allocation/recommend`
- **Purpose:** Proposes fair work distribution among available SHG members based on skills, capacity, workload, and deadlines.
- **Request Payload:**
```json
{
  "bulk_order_id": 22,
  "order_item_id": 45,
  "product_id": 3,
  "total_quantity": 100,
  "deadline": "2026-11-25T00:00:00Z",
  "members": [
    {
      "member_id": 1,
      "skills": ["weaving", "tailoring"],
      "available_hours_per_day": 6.0,
      "current_workload": 0.0,
      "max_feasible_daily_quantity": 8.0,
      "historical_completion_rate": 98.0
    },
    {
      "member_id": 2,
      "skills": ["tailoring"],
      "available_hours_per_day": 4.0,
      "current_workload": 5.0,
      "max_feasible_daily_quantity": 6.0,
      "historical_completion_rate": 85.0
    }
  ]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "bulk_order_id": 22,
  "order_item_id": 45,
  "total_allocated": 100,
  "unallocated_quantity": 0,
  "recommendations": [
    {
      "member_id": 1,
      "proposed_quantity": 60,
      "completion_likelihood_percentage": 95.0,
      "estimated_completion_date": "2026-11-22T00:00:00Z",
      "confidence_score": 0.91,
      "factors": ["Zero current backlog", "High daily output capability"],
      "explanation": "Member 1 can comfortably handle 60 units within 8 days."
    },
    {
      "member_id": 2,
      "proposed_quantity": 40,
      "completion_likelihood_percentage": 88.0,
      "estimated_completion_date": "2026-11-24T00:00:00Z",
      "confidence_score": 0.85,
      "factors": ["Moderate backlog", "Part-time capacity"],
      "explanation": "Member 2 can finish 40 units before deadline with 4 daily hours."
    }
  ],
  "fairness_index": 0.89
}
```

---

### 2.4 Computer Vision Quality Inspection
- **Endpoint:** `POST /api/v1/ai/quality/inspect-batch`
- **Purpose:** Analyzes uploaded batch photos against product specifications to detect visual defects and deviations.
- **Request Payload:**
```json
{
  "batch_id": 501,
  "product_id": 3,
  "photo_urls": [
    "https://storage.shgsaathi.in/batches/batch_501_photo1.jpg",
    "https://storage.shgsaathi.in/batches/batch_501_photo2.jpg"
  ],
  "specifications": [
    {"parameter_name": "Stitch Uniformity", "target_value": "8 stitches per inch", "tolerance_range": "+/- 1"},
    {"parameter_name": "Handle Seam Strength", "target_value": "Double-cross reinforced", "tolerance_range": "Exact"}
  ]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "batch_id": 501,
  "quality_score": 88.5,
  "confidence_score": 0.92,
  "defects_detected": [
    {
      "type": "minor_loose_thread",
      "location": "bottom seam right",
      "severity": "LOW"
    }
  ],
  "specification_deviations": [],
  "explanation": "Seams and dimensions meet target specifications. Minor loose trimming thread observed on outer rim.",
  "suggested_action": "TRIM_AND_APPROVE"
}
```

---

### 2.5 Product Pricing Assistance
- **Endpoint:** `POST /api/v1/ai/pricing/recommend`
- **Purpose:** Suggests competitive and sustainable selling prices, checking for missed overheads.
- **Request Payload:**
```json
{
  "bulk_order_id": 22,
  "material_cost": 45000.0,
  "labor_cost": 25000.0,
  "packaging_cost": 3000.0,
  "transport_cost": 4000.0,
  "operational_expenses": 2000.0,
  "quantity": 500,
  "target_margin_percentage": 15.0
}
```
- **Response Payload:**
```json
{
  "success": true,
  "recommended_selling_price_per_unit": 181.70,
  "recommended_total_order_value": 90850.0,
  "estimated_profit": 11850.0,
  "margin_percentage": 15.0,
  "missing_cost_warnings": [
    "Electricity/machine maintenance allowance recommended: approx INR 1.5/unit."
  ],
  "market_benchmark_range": {
    "min_unit_price": 170.0,
    "max_unit_price": 210.0
  }
}
```

---

### 2.6 Retail Demand Forecasting
- **Endpoint:** `POST /api/v1/ai/retail/forecast-demand`
- **Request Payload:**
```json
{
  "product_id": 3,
  "historical_sales": [
    {"month": "2026-08", "quantity": 120},
    {"month": "2026-09", "quantity": 150},
    {"month": "2026-10", "quantity": 190}
  ],
  "upcoming_festival_season": true
}
```
- **Response Payload:**
```json
{
  "success": true,
  "product_id": 3,
  "forecasted_monthly_demand": 240,
  "confidence_interval": [210, 275],
  "confidence_score": 0.84,
  "seasonal_factor": "Diwali artisan gifting surge"
}
```

---

### 2.7 Inventory Forecasting & Restocking Alerts
- **Endpoint:** `POST /api/v1/ai/inventory/forecast-restock`
- **Request Payload:**
```json
{
  "shg_id": 1,
  "inventory_id": 8,
  "current_physical_stock": 25.0,
  "bulk_committed_stock": 20.0,
  "lead_time_days": 7,
  "daily_burn_rate": 3.5
}
```
- **Response Payload:**
```json
{
  "success": true,
  "inventory_id": 8,
  "days_until_stockout": 1.4,
  "restock_recommended": true,
  "recommended_order_quantity": 75.0,
  "urgency": "HIGH"
}
```

---

### 2.8 Logistics Recommendations
- **Endpoint:** `POST /api/v1/ai/logistics/recommend-route`
- **Request Payload:**
```json
{
  "origin_pincode": "570001",
  "destination_pincode": "560001",
  "weight_kg": 85.0,
  "target_delivery_date": "2026-11-28"
}
```
- **Response Payload:**
```json
{
  "success": true,
  "recommended_carriers": [
    {
      "carrier_name": "KSRTC Cargo Logistics",
      "estimated_cost": 850.0,
      "estimated_transit_hours": 18,
      "reliability_rating": 4.6
    }
  ]
}
```

---

### 2.9 Financial Anomaly Detection
- **Endpoint:** `POST /api/v1/ai/finance/detect-anomalies`
- **Request Payload:**
```json
{
  "shg_id": 1,
  "earnings_records": [
    {"member_id": 1, "assigned_qty": 50, "accepted_qty": 50, "rate": 50.0, "net": 2500.0},
    {"member_id": 2, "assigned_qty": 40, "accepted_qty": 40, "rate": 50.0, "deductions": 1200.0, "net": 800.0}
  ]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "anomalies_flagged": [
    {
      "member_id": 2,
      "flag_type": "HIGH_DEDUCTION_RATIO",
      "severity": "WARNING",
      "detail": "Deductions account for 60% of gross earnings. Requires documented justification.",
      "requires_human_resolution": true
    }
  ]
}
```

---

### 2.10 RAG Knowledge Assistant
- **Endpoint:** `POST /api/v1/ai/assistant/query`
- **Request Payload:**
```json
{
  "query": "How do I claim reimbursement for thread materials under NRLM?",
  "language": "en",
  "user_role": "SHG_MEMBER",
  "user_context": {
    "shg_name": "Prerana Mahila Sangha",
    "active_orders": 1
  }
}
```
- **Response Payload:**
```json
{
  "success": true,
  "answer": "Under National Rural Livelihoods Mission (NRLM) CIF guidelines, raw material bills verified with GST receipts can be reimbursed through the SHG Revolving Fund ledger. Please upload your bill under Document Upload.",
  "language": "en",
  "references": [
    "NRLM Master Circular Section 4.2: Community Investment Fund Utilization",
    "SHG Saathi Procurement SOP v1"
  ]
}
```

---

### 2.11 Speech-to-Text & Text-to-Speech
- **Endpoint:** `POST /api/v1/ai/voice/stt`
  - Input: Audio binary (WAV/MP3/M4A), Language hint (kn, hi, en)
  - Output: `{"text": "ನನ್ನ ಇಂದಿನ ಮುಗಿದ ಕೆಲಸ 25 ಚೀಲಗಳು", "language": "kn", "confidence": 0.94}`
- **Endpoint:** `POST /api/v1/ai/voice/tts`
  - Input: `{"text": "ನಿಮ್ಮ ಕೆಲಸವನ್ನು ನಾಯಕರು ಅನುಮೋದಿಸಿದ್ದಾರೆ.", "language": "kn"}`
  - Output: `{"audio_base64": "...", "mime_type": "audio/mp3"}`

---

### 2.12 Multilingual Response Generation
- **Endpoint:** `POST /api/v1/ai/translate`
- **Request Payload:**
```json
{
  "text": "Your batch #102 has been accepted with an 88% quality score.",
  "target_languages": ["kn", "hi"]
}
```
- **Response Payload:**
```json
{
  "translations": {
    "kn": "ನಿಮ್ಮ ಬ್ಯಾಚ್ #102 ಅನ್ನು 88% ಗುಣಮಟ್ಟದ ಅಂಕಗಳೊಂದಿಗೆ ಸ್ವೀಕರಿಸಲಾಗಿದೆ.",
    "hi": "आपका बैच #102 88% गुणवत्ता स्कोर के साथ स्वीकार कर लिया गया है।"
  }
}
```

### 2.13 LangGraph Multi-Agent Bulk Order Planning Workflow
- **Endpoints:** `POST /ai/v1/agents/order-planning` & `POST /api/v1/ai/agents/order-planning`
- **Purpose:** Coordinates 7 specialized LangGraph agent nodes: validates order parameters, extracts documents via OCR, estimates cost breakdown, predicts member completion using Scikit-learn, optimizes workforce allocation using Linear Programming, verifies material inventory, and synthesizes a proposed execution plan.
- **Request Payload:**
```json
{
  "bulk_order_id": 501,
  "order_item_id": 1,
  "product_id": 101,
  "total_quantity": 500,
  "deadline": "2026-12-15T00:00:00Z",
  "material_cost_estimate": 22500.0,
  "labor_rate": 12500.0,
  "target_margin_percentage": 20.0,
  "members": [
    {
      "member_id": 1,
      "available_hours_per_day": 6.5,
      "current_workload": 20.0,
      "max_feasible_daily_quantity": 12.0,
      "historical_completion_rate": 96.0,
      "skills": ["Weaving", "Embroidery"]
    },
    {
      "member_id": 2,
      "available_hours_per_day": 5.0,
      "current_workload": 10.0,
      "max_feasible_daily_quantity": 10.0,
      "historical_completion_rate": 90.0,
      "skills": ["Weaving"]
    }
  ]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "status": "PENDING_LEADER_APPROVAL",
  "bulk_order_id": 501,
  "total_quantity": 500,
  "requires_leader_approval": true,
  "execution_plan": {
    "total_allocated_units": 500,
    "unallocated_units": 0,
    "fairness_score": 0.94,
    "approval_required": true,
    "executive_summary": "Automated multi-agent planning completed for order #501. Plan is PROPOSED and requires explicit SHG leader approval."
  },
  "execution_log": [
    {"agent": "OrderValidationAgent", "status": "PASSED"},
    {"agent": "DocumentIntelligenceAgent", "status": "SKIPPED_NO_ATTACHMENT"},
    {"agent": "PricingAssistantAgent", "status": "SUCCESS"},
    {"agent": "CompletionPredictionAgent", "status": "COMPLETED"},
    {"agent": "WorkforceAllocationAgent", "status": "OPTIMIZATION_SUCCEEDED"},
    {"agent": "InventoryIntelligenceAgent", "status": "INVENTORY_VERIFIED"},
    {"agent": "PlanSynthesizerAgent", "status": "PLAN_GENERATED"}
  ]
}
```

### 2.14 LangGraph Multi-Agent Production Monitoring Workflow
- **Endpoints:** `POST /ai/v1/agents/production-monitoring` & `POST /api/v1/ai/agents/production-monitoring`
- **Purpose:** Tracks production milestone progress, computes delay risk scores, and generates workload rebalancing recommendations.
- **Request Payload:**
```json
{
  "order_id": 501,
  "target_quantity": 500,
  "deadline": "2026-12-15T00:00:00Z",
  "start_date": "2026-11-01T00:00:00Z",
  "member_updates": [
    {
      "member_id": 1,
      "assigned_quantity": 250,
      "completed_quantity": 180,
      "expected_quantity_to_date": 190
    },
    {
      "member_id": 2,
      "assigned_quantity": 250,
      "completed_quantity": 90,
      "expected_quantity_to_date": 190,
      "notes": "Delay due to handloom repair"
    }
  ]
}
```
- **Response Payload:**
```json
{
  "success": true,
  "order_id": 501,
  "status": "ACTION_REQUIRED",
  "total_completed": 270,
  "completion_percentage": 54.0,
  "delay_risk_score": 0.55,
  "risk_level": "MEDIUM",
  "delayed_members": [
    {
      "member_id": 2,
      "lag_units": 100,
      "completed": 90,
      "assigned": 250,
      "reason": "Delay due to handloom repair"
    }
  ],
  "reallocation_recommendations": [
    {
      "action": "REBALANCE_WORKLOAD",
      "units_to_reallocate": 70,
      "recommendation": "Transfer unfinished units to top available artisans with >85% past on-time delivery."
    }
  ],
  "requires_leader_action": true
}
```

### 2.15 Section 14 Direct Specification Path Mapping
The microservice exposes dual path mountings. In addition to the `/api/v1/ai/*` prefix, the following direct paths matching Master Prompt Section 14 are permanently active:
- `POST /ai/v1/documents/extract`
- `POST /ai/v1/allocation/predict`
- `POST /ai/v1/allocation/recommend`
- `POST /ai/v1/quality/inspect`
- `POST /ai/v1/pricing/recommend`
- `POST /ai/v1/inventory/forecast`
- `POST /ai/v1/retail/demand-forecast`
- `POST /ai/v1/logistics/recommend`
- `POST /ai/v1/finance/anomaly-detect`
- `POST /ai/v1/assistant/chat`
- `POST /ai/v1/assistant/speech-to-text`
- `POST /ai/v1/assistant/text-to-speech`
- `POST /ai/v1/agents/order-planning`
- `POST /ai/v1/agents/production-monitoring`
- `GET /health`

---

## 3. Error Handling and Status Codes

| HTTP Status | Meaning | Backend Behavior |
|-------------|---------|------------------|
| 200 OK | Prediction / Extraction successful | Stores result in `AIAnalysisRecord`, proceeds with next business step. |
| 422 Unprocessable | Invalid input payload | Logs schema issue, marks request failed, notifies developer. |
| 503 Service Unavailable | Model not loaded or server starting | Triggers graceful fallback / manual workflow mode. |
| 504 Gateway Timeout | Model inference took > 10.0 seconds | Cancels request, records timeout, notifies user to continue manually. |

---

## 4. Summary of Developer Contract Guarantees

1. The AI/ML service endpoints must strictly conform to the JSON payloads documented above.
2. The AI service MUST NOT mutate database state directly; it returns advisory predictions.
3. The main backend will store raw AI output in `ai_analysis_records` for full auditability.
4. **Offline / Pre-deployment Mode:** If `AI_SERVICE_BASE_URL` is omitted or set to `mock`, the backend operates in full standalone mode using local heuristic approximations, allowing frontend and business workflows to proceed unimpeded.
5. **Testing Architecture Note:** Direct network socket connections are skipped during isolated unit testing and mock mode to eliminate external latency and thread bridge timeouts.

