# SHG Saathi – AI/ML Model Evaluation & Benchmark Report

This document reports the formal machine learning evaluation results, model architectures, hyperparameters, error metrics, and operational limitations across the **SHG Saathi** AI/ML Microservice.

All metrics are computed on held-out test splits (`data/processed/*`) using `evaluation/evaluate_models.py`.

---

## 1. Summary of Evaluated Models

| Capability | Model Architecture | Hyperparameters | Target Variable | Primary Metric | Result |
|---|---|---|---|---|---|
| **Worker On-Time Feasibility** | Calibrated Random Forest Classifier | `n_estimators=120`, `max_depth=8`, `class_weight='balanced'`, Platt Sigmoid Calibration (`cv=5`) | `on_time_completion` (0/1) | **ROC-AUC** / **F1** | **0.8801** / **0.6282** |
| **Worker Completion Days** | Gradient Boosting Regressor | `n_estimators=100`, `learning_rate=0.08`, `max_depth=5` | `actual_completion_days` | **MAE** / **$R^2$** | **5.23 days** / **0.9587** |
| **Financial Anomaly Detection** | Isolation Forest + Standardized Outlier Scoring | `n_estimators=150`, `contamination=0.11` | `is_anomaly` (0/1) | **ROC-AUC** / **Precision** | **0.9961** / **0.8810** |
| **Retail & Bulk Demand Forecast** | Random Forest Regressor | `n_estimators=120`, `max_depth=7`, `min_samples_split=4` | `next_14d_demand` | **MAE** / **$R^2$** | **9.72 units** / **0.9738** |
| **Work Allocation Optimization** | SciPy Linear Programming (`linprog`) | HiGHS solver, proportional fairness objective | Work quantity per member | **Fairness Score** / **Constraint Satisfaction** | **100% Exact Sum Feasible / Explicit Infeasibility Diagnosis** |

---

## 2. Module 1: Worker Completion Likelihood & Production Time

### Classification Metrics (On-Time Completion)
Evaluated on $N=500$ held-out test instances:

- **Accuracy**: $88.40\%$
- **Precision**: $74.24\%$
- **Recall**: $54.44\%$
- **F1-Score**: $0.6282$
- **ROC-AUC**: $0.8801$
- **Brier Score Loss**: $0.0842$ (indicates well-calibrated, reliable posterior probabilities)

#### Confusion Matrix
```
                 Predicted Late (0)    Predicted On-Time (1)
Actual Late (0)         393                    17
Actual On-Time (1)       41                    49
```
*Note on class weighting*: The model prioritizes specificity (low False Positives = 17) to prevent overpromising artisan capacity to institutional buyers.

### Regression Metrics (Completion Duration in Days)
- **Mean Absolute Error (MAE)**: $5.23$ days
- **Root Mean Squared Error (RMSE)**: $7.66$ days
- **Coefficient of Determination ($R^2$)**: $0.9587$

### Feature Importance & Driving Factors
1. `days_to_deadline` ($38.4\%$ importance): Timeline buffer relative to volume.
2. `proposed_quantity` ($26.2\%$ importance): Workload assignment scale.
3. `current_workload` ($14.8\%$ importance): Existing backlog commitments.
4. `available_hours_per_day` ($11.3\%$ importance): Artisan physical hours.
5. `historical_completion_rate` ($9.3\%$ importance): Individual track record.

---

## 3. Module 7: Financial Anomaly Detection (Isolation Forest)

Evaluated on $N=360$ held-out financial records (42 ground-truth anomalies):

- **Precision**: $88.10\%$ (37 true anomalies correctly flagged out of 42 alarms)
- **Recall**: $88.10\%$
- **F1-Score**: $0.8810$
- **ROC-AUC**: $0.9961$

### Anomaly Flag Categories Identified
1. **`DUPLICATE_PAYMENT`**: Repeated entries with identical piece-rate and unit claims within the same payout period.
2. **`UNUSUAL_DEDUCTION`**: Deductions exceeding $40\%$ of gross wages (flagged for accountant review).
3. **`PIECE_RATE_MISMATCH`**: Payout rate deviating significantly ($>1.6\times$) from agreed SHG benchmark.
4. **`QUANTITY_ANOMALY`**: Output quantities exceeding maximum feasible individual artisan capacity ($>600$ units/period).

---

## 4. Module 5: Retail Demand Forecasting

Evaluated on $N=300$ periodic demand samples:

- **Mean Actual Demand**: $150.54$ units
- **Mean Absolute Error (MAE)**: $9.717$ units ($<6.5\%$ mean relative error)
- **Root Mean Squared Error (RMSE)**: $13.347$ units
- **$R^2$ Score**: $0.9738$

### Inventory Stock Separation
The forecasting engine strictly maintains distinction between:
- $\text{Physical Stock}$: Actual inventory physically present on shelves.
- $\text{Bulk-Reserved Stock}$: Locked for committed institutional orders.
- $\text{Retail-Reserved Stock}$: Locked for direct store sales.
- $\text{Free Stock} = \max(0, \text{Physical} - \text{Bulk Reserved} - \text{Retail Reserved})$.

---

## 5. Module 4: Work Allocation Optimization (Linear Programming)

- **Algorithm**: SciPy `scipy.optimize.linprog` with the dual simplex / HiGHS interior point solver.
- **Formulation**:
  $$\min \sum_{i=1}^n c_i x_i$$
  subject to:
  $$\sum_{i=1}^n x_i = Q \quad (\text{Exact order requirement})$$
  $$0 \le x_i \le \min(\text{DailyCapacity}_i \times D - \text{Workload}_i \times 0.4, \text{MaxCap}_i)$$
- **Guaranteed Infeasibility Diagnosis**: If $\sum_i \text{Cap}_i < Q$, the optimizer returns:
  - `is_feasible = False`
  - Exact `shortfall = Q - sum(Cap_i)`
  - Recommended minimum deadline extension or required artisan count.
  - Zero invented or fabricated assignments.

---

## 6. Known Model Limitations & Human-in-the-Loop Principles

1. **Advisory Role**: All ML predictions are advisory. No work is assigned, no batch is rejected, and no financial payout is disbursed without explicit SHG leader approval in the main backend.
2. **Exogenous Events**: Models do not anticipate sudden village-level power outages, agricultural sowing/harvest peaks, or local festivals not registered in the system calendar.
3. **Continuous Monitoring**: Model artifacts are stored versioned in `saved_models/` with immutable metadata JSON files.
