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

