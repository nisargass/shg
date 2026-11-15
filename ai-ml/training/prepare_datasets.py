"""SHG Saathi Dataset Preparation and Synthetic Data Generator.

Generates realistic, domain-grounded synthetic datasets for SHG operations:
1. Worker Completion & Production Time (classification & regression)
2. Financial Payout & Anomaly Records (rule-based + ML detection)
3. Inventory & Demand Time-Series (retail & bulk forecasting)
4. Quality Inspection Benchmarks

All datasets are created with realistic distributions based on real-world
Self-Help Group (SHG) artisan workflows in India.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_SYNTHETIC = os.path.join(BASE_DIR, "data", "synthetic")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(DATA_SYNTHETIC, exist_ok=True)
os.makedirs(DATA_PROCESSED, exist_ok=True)


def generate_completion_dataset(n_samples: int = 2500) -> pd.DataFrame:
    """Generates synthetic dataset for worker completion prediction and time estimation.

    Features:
    - member_id: Categorical artisan ID
    - product_id: Product SKU
    - product_complexity: 1 (basic) to 5 (intricate handloom/embroidery)
    - skill_match: 0.0 to 1.0 (artisan skill vs product requirements)
    - historical_completion_rate: past on-time delivery ratio (0.5 to 1.0)
    - available_hours_per_day: daily hours committed (1.5 to 8.0)
    - current_workload: already committed units across active orders (0 to 150)
    - max_daily_capacity: maximum feasible units per day (4 to 30)
    - proposed_quantity: units assigned in new order (10 to 300)
    - days_to_deadline: working days until required shipment (1 to 30)
    - material_availability_score: 0.5 to 1.0 (on-hand raw materials)

    Targets:
    - on_time_completion: 1 if completed within deadline, 0 otherwise
    - actual_completion_days: continuous estimation of required days
    """
    member_ids = [f"M{i:03d}" for i in range(1, 101)]
    product_ids = [101, 102, 103, 104, 105, 106, 107, 108]

    records = []
    for i in range(n_samples):
        m_id = np.random.choice(member_ids)
        p_id = int(np.random.choice(product_ids))
        complexity = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.25, 0.35, 0.15, 0.10])
        skill_match = round(np.random.uniform(0.4, 1.0), 2)
        hist_rate = round(np.random.beta(7, 2), 2)  # Mean ~0.77
        hist_rate = max(0.4, min(1.0, hist_rate))
        hours_per_day = round(np.random.uniform(2.0, 7.5), 1)
        current_workload = int(np.random.exponential(25))
        current_workload = min(120, current_workload)

        # Baseline capacity per day depends on complexity and hours
        base_rate = (hours_per_day * 2.5) / (complexity * 0.7 + 0.3)
        max_daily_capacity = max(3, int(round(base_rate * np.random.uniform(0.85, 1.15))))

        days_to_deadline = int(np.random.uniform(2, 25))
        proposed_quantity = int(np.random.uniform(10, 220))
        material_score = round(np.random.uniform(0.6, 1.0), 2)

        # Realistic physics of production time
        effective_capacity_per_day = max_daily_capacity * skill_match * (material_score ** 0.5)
        remaining_capacity = max(1.0, effective_capacity_per_day * 0.8)

        # Days required to finish existing workload + new proposed quantity
        days_needed = (proposed_quantity + current_workload * 0.4) / remaining_capacity
        actual_completion_days = round(days_needed * np.random.normal(1.0, 0.1), 1)
        actual_completion_days = max(0.5, actual_completion_days)

        # Probability of on-time completion based on deadline buffer
        buffer_ratio = days_to_deadline / max(0.1, actual_completion_days)
        prob = 1.0 / (1.0 + np.exp(-3.5 * (buffer_ratio - 1.05)))
        prob = prob * (0.8 + 0.2 * hist_rate)
        prob = min(0.99, max(0.01, prob))

        on_time = 1 if np.random.binomial(1, prob) == 1 else 0

        records.append({
            "sample_id": i + 1,
            "member_id": m_id,
            "product_id": p_id,
            "product_complexity": complexity,
            "skill_match": skill_match,
            "historical_completion_rate": hist_rate,
            "available_hours_per_day": hours_per_day,
            "current_workload": current_workload,
            "max_daily_capacity": max_daily_capacity,
            "proposed_quantity": proposed_quantity,
            "days_to_deadline": days_to_deadline,
            "material_availability_score": material_score,
            "actual_completion_days": actual_completion_days,
            "on_time_completion": on_time
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(DATA_SYNTHETIC, "member_completion_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} completion records at {csv_path}")
    return df


def generate_financial_anomaly_dataset(n_samples: int = 1800) -> pd.DataFrame:
    """Generates synthetic dataset for financial payout anomaly detection.

    Simulates normal artisan earnings plus realistic fraud/anomaly patterns:
    - Duplicate entries
    - Unexpected piece-rate deviation
    - Disproportionate deductions
    - Quantity produced far exceeding physical capacity
    - Repeated payment corrections
    """
    shg_ids = [1, 2, 3, 4, 5]
    records = []

    for i in range(n_samples):
        rec_id = f"PAY-{1000 + i}"
        shg_id = int(np.random.choice(shg_ids))
        member_id = f"M{np.random.randint(1, 101):03d}"
        units = int(np.random.uniform(20, 200))
        standard_piece_rate = round(np.random.choice([15.0, 25.0, 40.0, 65.0]), 2)

        is_anomaly = 0
        anomaly_category = "NORMAL"
        applied_rate = standard_piece_rate
        deductions = round(units * applied_rate * np.random.uniform(0.02, 0.08), 2)
        corrections_count = int(np.random.choice([0, 1, 2], p=[0.85, 0.12, 0.03]))

        # Inject anomalies in ~12% of records
        rand_val = np.random.random()
        if rand_val < 0.03:
            # Duplicate / ghost record anomaly
            is_anomaly = 1
            anomaly_category = "DUPLICATE_PAYMENT"
            corrections_count = 3
        elif rand_val < 0.06:
            # Disproportionate deductions (>40% of earnings)
            is_anomaly = 1
            anomaly_category = "UNUSUAL_DEDUCTION"
            deductions = round(units * applied_rate * np.random.uniform(0.45, 0.75), 2)
        elif rand_val < 0.09:
            # Piece rate mismatch / unexpected inflation
            is_anomaly = 1
            anomaly_category = "PIECE_RATE_MISMATCH"
            applied_rate = round(standard_piece_rate * np.random.uniform(1.6, 2.5), 2)
        elif rand_val < 0.12:
            # Unrealistic production quantity (> 600 units for single period)
            is_anomaly = 1
            anomaly_category = "QUANTITY_ANOMALY"
            units = int(np.random.uniform(650, 1200))

        gross_payout = round(units * applied_rate, 2)
        net_payout = round(max(0.0, gross_payout - deductions), 2)

        records.append({
            "record_id": rec_id,
            "shg_id": shg_id,
            "member_id": member_id,
            "units_produced": units,
            "standard_piece_rate": standard_piece_rate,
            "applied_piece_rate": applied_rate,
            "gross_payout": gross_payout,
            "deductions": deductions,
            "net_payout": net_payout,
            "corrections_count": corrections_count,
            "is_anomaly": is_anomaly,
            "anomaly_category": anomaly_category
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(DATA_SYNTHETIC, "financial_payout_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} financial records at {csv_path} (Anomalies: {df['is_anomaly'].sum()})")
    return df


def generate_demand_inventory_dataset(n_samples: int = 1500) -> pd.DataFrame:
    """Generates synthetic dataset for retail demand and inventory forecasting.

    Simulates daily/weekly sales across SHG product categories with seasonal factors.
    """
    categories = ["Handloom", "Terracotta Handicraft", "Organic Food & Spice", "Jute Craft"]
    records = []

    for i in range(n_samples):
        cat = str(np.random.choice(categories))
        product_id = int(np.random.choice([201, 202, 203, 204, 205, 206]))
        past_7d_sales = round(float(np.random.uniform(15, 120)), 1)
        past_30d_sales = round(past_7d_sales * np.random.uniform(3.8, 4.4), 1)

        # Festival / wedding season multiplier (1.0 to 2.2)
        seasonality = round(float(np.random.choice([1.0, 1.1, 1.3, 1.8, 2.1], p=[0.4, 0.25, 0.2, 0.1, 0.05])), 2)
        lead_time_days = int(np.random.choice([3, 5, 7, 10, 14]))

        physical_stock = round(float(np.random.uniform(20, 250)), 1)
        bulk_reserved = round(physical_stock * np.random.uniform(0.1, 0.5), 1)
        retail_reserved = round((physical_stock - bulk_reserved) * np.random.uniform(0.1, 0.3), 1)
        free_stock = round(max(0.0, physical_stock - bulk_reserved - retail_reserved), 1)

        # Target: future 14-day retail demand
        daily_velocity = (past_30d_sales / 30.0) * seasonality
        next_14d_demand = round(daily_velocity * 14.0 * np.random.normal(1.0, 0.08), 1)
        next_14d_demand = max(5.0, next_14d_demand)

        records.append({
            "record_id": i + 1,
            "product_id": product_id,
            "product_category": cat,
            "past_7d_sales": past_7d_sales,
            "past_30d_sales": past_30d_sales,
            "seasonality_index": seasonality,
            "lead_time_days": lead_time_days,
            "physical_stock": physical_stock,
            "bulk_reserved_stock": bulk_reserved,
            "retail_reserved_stock": retail_reserved,
            "free_stock": free_stock,
            "next_14d_demand": next_14d_demand
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(DATA_SYNTHETIC, "demand_inventory_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} demand records at {csv_path}")
    return df


def generate_quality_benchmark_specifications():
    """Generates reference specifications for computer vision quality inspection."""
    specs = {
        "products": [
            {
                "product_id": 101,
                "name": "Handloom Cotton Saree",
                "category": "Handloom",
                "color_tolerance_delta_e": 4.5,
                "min_resolution_width": 640,
                "min_resolution_height": 480,
                "min_sharpness_score": 35.0,
                "allowable_defect_types": ["minor_thread_variance"],
                "critical_defects": ["weft_tear", "stain", "misaligned_border"],
                "min_acceptable_quality_score": 80.0
            },
            {
                "product_id": 102,
                "name": "Terracotta Clay Pot",
                "category": "Pottery",
                "color_tolerance_delta_e": 6.0,
                "min_resolution_width": 640,
                "min_resolution_height": 480,
                "min_sharpness_score": 40.0,
                "allowable_defect_types": ["minor_kiln_blush"],
                "critical_defects": ["rim_crack", "structural_fracture", "asymmetric_neck"],
                "min_acceptable_quality_score": 85.0
            },
            {
                "product_id": 103,
                "name": "Embroidered Jute Shopping Bag",
                "category": "Jute",
                "color_tolerance_delta_e": 5.0,
                "min_resolution_width": 640,
                "min_resolution_height": 480,
                "min_sharpness_score": 30.0,
                "allowable_defect_types": ["minor_fiber_fray"],
                "critical_defects": ["handle_detachment", "broken_stitching", "logo_distortion"],
                "min_acceptable_quality_score": 82.0
            }
        ]
    }
    json_path = os.path.join(DATA_SYNTHETIC, "quality_benchmark_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(specs, f, indent=2)
    print(f"Saved quality benchmark specs at {json_path}")


def prepare_train_test_splits():
    """Reads synthetic datasets and creates train/test splits in data/processed."""
    # 1. Completion split
    df_comp = pd.read_csv(os.path.join(DATA_SYNTHETIC, "member_completion_data.csv"))
    train_comp, test_comp = train_test_split(df_comp, test_size=0.2, random_state=42, stratify=df_comp["on_time_completion"])
    train_comp.to_csv(os.path.join(DATA_PROCESSED, "train_completion.csv"), index=False)
    test_comp.to_csv(os.path.join(DATA_PROCESSED, "test_completion.csv"), index=False)

    # 2. Financial anomaly split
    df_fin = pd.read_csv(os.path.join(DATA_SYNTHETIC, "financial_payout_data.csv"))
    train_fin, test_fin = train_test_split(df_fin, test_size=0.2, random_state=42, stratify=df_fin["is_anomaly"])
    train_fin.to_csv(os.path.join(DATA_PROCESSED, "train_financial.csv"), index=False)
    test_fin.to_csv(os.path.join(DATA_PROCESSED, "test_financial.csv"), index=False)

    # 3. Demand split
    df_dem = pd.read_csv(os.path.join(DATA_SYNTHETIC, "demand_inventory_data.csv"))
    train_dem, test_dem = train_test_split(df_dem, test_size=0.2, random_state=42)
    train_dem.to_csv(os.path.join(DATA_PROCESSED, "train_demand.csv"), index=False)
    test_dem.to_csv(os.path.join(DATA_PROCESSED, "test_demand.csv"), index=False)

    print("Successfully created train/test splits in data/processed!")


if __name__ == "__main__":
    generate_completion_dataset()
    generate_financial_anomaly_dataset()
    generate_demand_inventory_dataset()
    generate_quality_benchmark_specifications()
    prepare_train_test_splits()
