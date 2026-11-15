# SHG Saathi – AI/ML Microservice

**Independent AI/ML Microservice for Women's Self-Help Groups (SHGs)**  
*Port: 8001 | Protocol: REST JSON | FastAPI, LangGraph, Scikit-learn, SciPy & Python 3.12+*

---

## 1. Overview & Architecture

The **SHG Saathi AI Microservice** is an autonomous, standalone advisory service designed to empower Self-Help Groups (SHGs) managing bulk orders, fair work distribution, production schedules, product quality, costing, inventory, and financial transparency.

### Architecture Contract
```
+------------------------------------+        REST JSON         +------------------------------------+
|            Main Backend            |   (X-SHG-Service-Key)   |           AI Microservice          |
|      http://127.0.0.1:8000         | ----------------------> |        http://127.0.0.1:8001       |
+------------------------------------+                         +------------------------------------+
| - User Authentication (JWT)        |                         | 1. Document OCR & PO Extraction    |
| - Business Operations & Orders     |                         | 2. Worker Completion Likelihood ML |
| - PostgreSQL / SQLite Persistence  |                         | 3. LP Work Allocation Optimization |
| - Payment & Payout Releases        |                         | 4. CV Quality Inspection (Pillow)  |
| - Human Approval Control           |                         | 5. Smart Pricing Assistant         |
| - Audit Record Storage             |                         | 6. Retail Demand Forecasting ML    |
+------------------------------------+                         | 7. Inventory Restock Alerting      |
                                                               | 8. Regional Logistics Intelligence |
                                                               | 9. Financial Anomaly Detector (IF) |
                                                               | 10. Multilingual RAG (KN, HI, EN)  |
                                                               | 11. Voice STT & TTS Processing     |
                                                               | 12. LangGraph Multi-Agent Workflows|
                                                               +------------------------------------+
```

### Core Business Rules
- **Human Approval is Mandatory**: All AI recommendations (work allocation, quality ratings, financial anomalies) are advisory and require human SHG leader or reviewer sign-off.
- **Zero Direct Database Mutation**: The AI microservice returns structured JSON; the main backend is solely responsible for database transactions.
- **No Fabricated Allocations**: If collective capacity is less than required order volume, the system returns an explicit infeasibility diagnosis with shortfall and recommended deadline extension.
- **Member Privacy**: The assistant strictly blocks cross-member financial queries.

---

## 2. Directory Structure

```
ai-service/
├── app/
│   ├── main.py                        # FastAPI entrypoint (mounts /ai/v1 and /api/v1/ai)
│   ├── core/                          # Config, exceptions, logging, security
│   ├── api/v1/
│   │   ├── api.py                     # Backend-compatible router (/api/v1/ai/*)
│   │   ├── section14_router.py        # Direct Master Prompt Section 14 router (/ai/v1/*)
│   │   └── endpoints/                 # Route handlers (allocation, quality, pricing, agents, etc.)
│   ├── schemas/                       # Pydantic request and response models
│   ├── services/
│   │   ├── allocation_optimizer.py    # SciPy linprog + ML completion inference
│   │   ├── agents/                    # LangGraph Multi-Agent Workflows
│   │   │   ├── state.py               # TypedDict workflow states
│   │   │   ├── order_planning_graph.py
│   │   │   ├── production_monitoring_graph.py
│   │   │   └── quality_inspection_graph.py
│   │   └── ...                        # Specialized domain services
│   ├── providers/                     # Local CV, OCR, RAG, and Voice providers
│   └── rag/                           # Document chunking, embeddings, and vector store
├── data/
│   ├── synthetic/                     # Generated realistic SHG operational datasets
│   └── processed/                     # Stratified train/test splits
├── training/
│   ├── prepare_datasets.py            # Generates & splits domain-calibrated data
│   ├── train_completion_model.py      # Random Forest + Gradient Boosting
│   ├── train_anomaly_model.py         # Isolation Forest for financial payouts
│   └── train_demand_model.py          # Random Forest Regressor for demand
├── evaluation/
│   ├── evaluate_models.py             # Formal evaluation metrics computation
│   └── evaluation_report.json         # Persisted benchmark metrics
├── saved_models/                      # Versioned joblib model pipelines & metadata
├── knowledge_base/                    # NRLM schemes, pricing, workflows SOPs
├── tests/                             # Comprehensive 50-test Pytest suite
└── docs/
    ├── AI_SERVICE_CONTRACT.md         # Full endpoint schemas, error codes, and examples
    ├── DATASET_DOCUMENTATION.md       # Dataset schemas, features, distributions, limits
    └── MODEL_EVALUATION.md            # Benchmark report, hyperparameters, calibration
```

---

## 3. Machine Learning Models & Optimization

### 3.1 Worker Completion Prediction & Duration (Scikit-learn)
- **Classifier**: Calibrated `RandomForestClassifier` (`n_estimators=120`, `max_depth=8`, Sigmoid Platt calibration).
  - Accuracy: **88.40%** | ROC-AUC: **0.8801** | Brier Score: **0.0842**
- **Regressor**: `GradientBoostingRegressor` (`n_estimators=100`, `learning_rate=0.08`, `max_depth=5`).
  - MAE: **5.23 days** | $R^2$: **0.9587**

### 3.2 Work Allocation Optimization (SciPy Linear Programming)
- **Engine**: `scipy.optimize.linprog(method='highs')`.
- Distributes work across members to maximize completion likelihood while enforcing:
  - Exact order quantity fulfillment: $\sum x_i = Q$.
  - Individual capacity limits: $0 \le x_i \le \text{MaxCapacity}_i$.
  - Load-balancing fairness: Minimizes Gini-like variance across capacity utilization.
  - **Infeasibility Diagnosis**: Returns structured shortfall report if collective capacity is insufficient.

### 3.3 Financial Anomaly Detection (Isolation Forest)
- **Model**: `IsolationForest(n_estimators=150, contamination=0.11)`.
- Flags piece-rate mismatches, excessive deductions ($>40\%$), duplicate entries, and output exceeding physical capacity.
  - Precision: **88.10%** | Recall: **88.10%** | ROC-AUC: **0.9961**

### 3.4 Retail Demand & Inventory Restock (Random Forest)
- **Model**: `RandomForestRegressor(n_estimators=120, max_depth=7)`.
  - MAE: **9.72 units** | $R^2$: **0.9738**
- Distinguishes **Physical**, **Bulk-Reserved**, **Retail-Reserved**, and **Free Stock**.

---

## 4. LangGraph Agentic Workflows

### 4.1 Bulk Order Planning Workflow (`/ai/v1/agents/order-planning`)
Coordinates 7 specialized agent nodes:
1. `OrderValidationAgent`: Validates order volume, deadlines, and candidate inputs.
2. `DocumentIntelligenceAgent`: Parses attached purchase orders or invoices (OCR).
3. `PricingAssistantAgent`: Analyzes cost breakdown, margins, and overheads.
4. `CapacityAndPredictionAgent`: Predicts completion probability for each candidate artisan.
5. `WorkforceAllocationAgent`: Solves Linear Program to allocate quantities fairly.
6. `InventoryIntelligenceAgent`: Checks raw material requirements and buffer allowances.
7. `PlanSynthesizerAgent`: Generates final proposed plan and audit trail; flags mandatory leader approval.

### 4.2 Production Monitoring Workflow (`/ai/v1/agents/production-monitoring`)
Coordinates 4 specialized agent nodes:
1. `ProgressTrackingAgent`: Evaluates completed units vs required velocity.
2. `DelayPredictionAgent`: Computes delay risk scores and identifies lagged artisans.
3. `CorrectiveActionAgent`: Proposes workload rebalancing to high-capacity members.
4. `LeaderReportingAgent`: Generates structured alerts for backend dispatch.

---

## 5. API Endpoints Matrix

### Master Prompt Section 14 Endpoints
| HTTP Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ai/v1/documents/extract` | OCR & field extraction from POs/invoices |
| `POST` | `/ai/v1/allocation/predict` | Single-member completion feasibility & duration prediction |
| `POST` | `/ai/v1/allocation/recommend` | Multi-member Linear Programming allocation optimization |
| `POST` | `/ai/v1/quality/inspect` | CV batch inspection, defect detection, and quality scoring |
| `POST` | `/ai/v1/pricing/recommend` | Cost breakdown, margin validation, and price recommendation |
| `POST` | `/ai/v1/inventory/forecast` | Inventory stockout estimation & restock alert |
| `POST` | `/ai/v1/retail/demand-forecast` | Retail demand forecasting with festival seasonality |
| `POST` | `/ai/v1/logistics/recommend` | Regional carrier recommendations and transit estimates |
| `POST` | `/ai/v1/finance/anomaly-detect` | Rule-based & Isolation Forest financial audit |
| `POST` | `/ai/v1/assistant/chat` | Multilingual RAG assistant (Kannada, Hindi, English) |
| `POST` | `/ai/v1/assistant/speech-to-text` | Speech-to-text transcription |
| `POST` | `/ai/v1/assistant/text-to-speech` | Text-to-speech audio synthesis |
| `POST` | `/ai/v1/agents/order-planning` | LangGraph 7-node bulk order planning workflow |
| `POST` | `/ai/v1/agents/production-monitoring` | LangGraph 4-node production monitoring workflow |
| `GET` | `/health` | Service uptime and provider diagnostic check |

*Note: All endpoints are also mounted under `/api/v1/ai/*` for 100% backward compatibility with the existing backend.*

---

## 6. How to Run, Train, and Test

### 6.1 Install Dependencies
```bash
pip install -r requirements.txt
```

### 6.2 Generate Synthetic Datasets
```bash
python training/prepare_datasets.py
```

### 6.3 Train All Machine Learning Models
```bash
python training/train_completion_model.py
python training/train_anomaly_model.py
python training/train_demand_model.py
```

### 6.4 Run Model Evaluation Suite
```bash
python evaluation/evaluate_models.py
```

### 6.5 Run the Test Suite
```bash
# Sets PYTHONPATH to ai-service and runs all 50 tests
pytest tests/
```

### 6.6 Run the Microservice
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```
Interactive OpenAPI documentation will be accessible at `http://127.0.0.1:8001/docs`.
