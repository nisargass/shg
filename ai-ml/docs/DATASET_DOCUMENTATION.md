# SHG Saathi – AI/ML Dataset Documentation & Strategy

This document details the dataset strategy, generation methodology, schema specifications, train/test splits, and limitations for all machine learning models in the **SHG Saathi** AI/ML Microservice.

---

## 1. Dataset Overview & Strategy

Self-Help Groups (SHGs) operate in decentralized, rural, and semi-urban settings where historical digital records are frequently fragmented. To establish rigorous, deployable predictive models without assuming non-existent proprietary data:

1. **Synthetic Data Generation Grounded in Domain Realities**: Domain-calibrated synthetic datasets were generated using verified SHG production dynamics, piece-rate wage rules, and seasonal handicraft demand patterns.
2. **Transparent Labelling**: All synthetic data is explicitly labelled as synthetic (`data/synthetic/`), with realistic noise, class imbalance, and edge cases.
3. **Pluggable Architecture**: The data ingestion and feature engineering pipelines (`training/prepare_datasets.py`) accept real production records from the main backend database without code refactoring.

---

## 2. Dataset 1: Worker Completion Likelihood & Production Time

- **File Path**: `data/synthetic/member_completion_data.csv` (Split: `data/processed/train_completion.csv`, `test_completion.csv`)
- **Sample Count**: 2,500 records
- **Train/Test Split**: 80% Train (2,000 samples) / 20% Test (500 samples), stratified by `on_time_completion`.
- **License**: CC0 / MIT (Internal Synthetic Artifact)

### Features & Columns
| Column Name | Data Type | Range / Values | Description |
|---|---|---|---|
| `sample_id` | Integer | 1 – 2500 | Unique synthetic record ID |
| `member_id` | String | M001 – M100 | Artisan identifier |
| `product_id` | Integer | 101 – 108 | Product SKU identifier |
| `product_complexity` | Integer | 1 (Basic) – 5 (Intricate) | Skill and time intensity rating |
| `skill_match` | Float | 0.40 – 1.00 | Match score between artisan craft skills and product |
| `historical_completion_rate` | Float | 0.40 – 1.00 | Past on-time delivery ratio (Beta distribution $\alpha=7, \beta=2$) |
| `available_hours_per_day` | Float | 1.5 – 8.0 hrs | Daily hours committed by home-based artisan |
| `current_workload` | Integer | 0 – 120 units | Pre-existing committed backlog |
| `max_daily_capacity` | Integer | 3 – 30 units/day | Maximum physical throughput feasible |
| `proposed_quantity` | Integer | 10 – 220 units | Quantity proposed in new bulk order assignment |
| `days_to_deadline` | Integer | 2 – 25 days | Calendar days available until order shipment date |
| `material_availability_score` | Float | 0.60 – 1.00 | Proportion of raw yarn, fabric, or clay on-hand |

### Target Variables
1. **`on_time_completion`** (Binary: `0` or `1`): Ground truth whether all units were finished before deadline.
2. **`actual_completion_days`** (Continuous Float): Actual calendar days required to finish assignment.

### Preprocessing & Data Cleaning
- Missing values imputed using `SimpleImputer(strategy='median')`.
- Continuous features normalized using `StandardScaler`.
- Probabilities calibrated using Platt scaling (`CalibratedClassifierCV(method='sigmoid', cv=5)`).

### Known Limitations
- Does not account for sudden exogenous village events (monsoons, harvest festivals, severe power outages). SHG leader manual override is mandatory.

---

## 3. Dataset 2: Financial Payout & Anomaly Detection

- **File Path**: `data/synthetic/financial_payout_data.csv` (Split: `data/processed/train_financial.csv`, `test_financial.csv`)
- **Sample Count**: 1,800 payout records across 5 SHGs
- **Train/Test Split**: 80% Train (1,440 samples) / 20% Test (360 samples), stratified by anomaly flag.
- **Contamination Rate**: ~11.6% anomalies (210 anomalous records total).

### Features & Columns
| Column Name | Data Type | Description |
|---|---|---|
| `record_id` | String | Payout ledger entry identifier |
| `shg_id` | Integer | Self-Help Group organization ID |
| `member_id` | String | Artisan identifier |
| `units_produced` | Integer | Finished units submitted for payout period |
| `standard_piece_rate` | Float | Agreed benchmark wage per unit (INR 15 – 65) |
| `applied_piece_rate` | Float | Actual wage rate applied in payout entry |
| `rate_ratio` | Float | `applied_piece_rate / standard_piece_rate` |
| `gross_payout` | Float | `units_produced * applied_piece_rate` |
| `deductions` | Float | Material recovery, loan repayments, savings deductions |
| `deduction_ratio` | Float | `deductions / gross_payout` |
| `net_payout` | Float | `max(0, gross_payout - deductions)` |
| `corrections_count` | Integer | Number of manual accounting adjustments recorded |

### Target Variables
- **`is_anomaly`** (Binary: `0` = Normal, `1` = Flagged Outlier)
- **`anomaly_category`**: `NORMAL`, `DUPLICATE_PAYMENT`, `UNUSUAL_DEDUCTION`, `PIECE_RATE_MISMATCH`, `QUANTITY_ANOMALY`.

### Preprocessing & Model Strategy
- Dual strategy: Exact deterministic rule validation for arithmetic errors + Scikit-learn `IsolationForest` on multidimensional standardized features (`rate_ratio`, `deduction_ratio`, `units_produced`, `corrections_count`).
- **Ethical Rule**: Anomalies are flagged as *Review Flags*, never accusations or fraud convictions.

---

## 4. Dataset 3: Retail Demand & Inventory Time-Series

- **File Path**: `data/synthetic/demand_inventory_data.csv` (Split: `data/processed/train_demand.csv`, `test_demand.csv`)
- **Sample Count**: 1,500 periodic sales records across Handloom, Pottery, Food, and Jute crafts.
- **Train/Test Split**: 80% Train (1,200 samples) / 20% Test (300 samples).

### Features & Columns
| Column Name | Data Type | Description |
|---|---|---|
| `product_id` | Integer | SKU identifier |
| `product_category` | Categorical | Handloom, Terracotta, Food & Spice, Jute |
| `past_7d_sales` | Float | Units sold in the trailing 7 days |
| `past_30d_sales` | Float | Units sold in the trailing 30 days |
| `seasonality_index` | Float | Festive multiplier (1.0 = baseline, 2.1 = peak Diwali/Dasara) |
| `lead_time_days` | Integer | Supply lead time for raw material replenishment |
| `physical_stock` | Float | Total inventory physically in storage |
| `bulk_reserved_stock` | Float | Inventory locked for institutional bulk orders |
| `retail_reserved_stock` | Float | Inventory committed to retail showroom orders |
| `free_stock` | Float | Uncommitted inventory available for immediate fulfillment |

### Target Variable
- **`next_14d_demand`** (Continuous Float): Expected units demanded over the following 14 days.

---

## 5. Dataset 4: Computer Vision Quality Inspection Benchmarks

- **File Path**: `data/synthetic/quality_benchmark_data.json`
- **Contents**: Formal manufacturing tolerances, allowable variances, and critical defect lists for handmade products:
  - **Handloom Cotton Saree**: $\Delta E \le 4.5$, allowable thread variance, critical defects (weft tear, dye stain).
  - **Terracotta Clay Pot**: $\Delta E \le 6.0$, allowable kiln blush, critical defects (rim crack, asymmetry).
  - **Embroidered Jute Bag**: $\Delta E \le 5.0$, allowable fiber fray, critical defects (handle detachment, seam tear).
- **Image Quality Gates**: Minimum resolution $250 \times 250$, mean luminance $25 \le \bar{Y} \le 240$, standard deviation threshold $\ge 12.0$.
