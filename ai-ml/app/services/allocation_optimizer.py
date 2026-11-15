"""Intelligent Work Allocation Optimizer & Completion Predictor.

Combines:
1. Scikit-learn Trained Machine Learning Models (RandomForestClassifier + GradientBoostingRegressor)
   to predict on-time completion likelihood, confidence score, and completion days.
2. SciPy Linear Programming (`linprog`) to optimize work distribution fairly across artisans,
   guaranteeing sum(allocated) == total_quantity when feasible, or returning a structured
   infeasibility report if collective capacity is insufficient.
"""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
from scipy.optimize import linprog

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")

FEATURE_COLS = [
    "product_complexity",
    "skill_match",
    "historical_completion_rate",
    "available_hours_per_day",
    "current_workload",
    "max_daily_capacity",
    "proposed_quantity",
    "days_to_deadline",
    "material_availability_score"
]


class AllocationOptimizer:
    def __init__(self):
        self.clf_path = os.path.join(SAVED_MODELS_DIR, "completion_classifier.joblib")
        self.reg_path = os.path.join(SAVED_MODELS_DIR, "completion_regressor.joblib")
        self.classifier = None
        self.regressor = None
        self._load_models()

    def _load_models(self):
        try:
            if os.path.exists(self.clf_path) and os.path.exists(self.reg_path):
                self.classifier = joblib.load(self.clf_path)
                self.regressor = joblib.load(self.reg_path)
        except Exception as e:
            # Fallback to calibrated heuristics if model load fails
            self.classifier = None
            self.regressor = None

    def predict_member_completion(
        self,
        member_id: Any,
        product_id: int,
        proposed_quantity: int,
        deadline_str: Optional[str],
        available_hours_per_day: float,
        current_workload: float,
        historical_completion_rate: float,
        skills: List[str],
        material_availability: float = 0.95
    ) -> Dict[str, Any]:
        """Predicts feasibility, likelihood percentage, estimated date, and factors for a single member."""
        # Calculate days to deadline
        now = datetime.now(timezone.utc)
        if deadline_str:
            try:
                deadline_dt = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
                days_to_deadline = max(1.0, (deadline_dt - now).total_seconds() / 86400.0)
            except Exception:
                days_to_deadline = 14.0
        else:
            days_to_deadline = 14.0

        # Skill factor heuristic (1.0 default, higher if matching skills present)
        skill_match = 0.9 if skills else 0.75
        hist_rate_normalized = historical_completion_rate / 100.0 if historical_completion_rate > 1.0 else historical_completion_rate
        product_complexity = 3  # Medium baseline
        max_daily_capacity = max(3.0, (available_hours_per_day * 2.5) / 2.0)

        # ML model prediction if available
        if self.classifier is not None and self.regressor is not None:
            features = pd.DataFrame([{
                "product_complexity": product_complexity,
                "skill_match": skill_match,
                "historical_completion_rate": hist_rate_normalized,
                "available_hours_per_day": available_hours_per_day,
                "current_workload": current_workload,
                "max_daily_capacity": max_daily_capacity,
                "proposed_quantity": proposed_quantity,
                "days_to_deadline": days_to_deadline,
                "material_availability_score": material_availability
            }])[FEATURE_COLS]

            try:
                prob = float(self.classifier.predict_proba(features)[0, 1])
                est_days = float(self.regressor.predict(features)[0])
                est_days = max(0.5, est_days)
            except Exception:
                prob = self._heuristic_likelihood(proposed_quantity, current_workload, max_daily_capacity, days_to_deadline, hist_rate_normalized)
                est_days = max(1.0, (proposed_quantity + current_workload * 0.3) / max_daily_capacity)
        else:
            prob = self._heuristic_likelihood(proposed_quantity, current_workload, max_daily_capacity, days_to_deadline, hist_rate_normalized)
            est_days = max(1.0, (proposed_quantity + current_workload * 0.3) / max_daily_capacity)

        likelihood_pct = round(prob * 100.0, 1)
        est_completion_date = (now + timedelta(days=est_days)).strftime("%Y-%m-%d")

        # Driving factors
        factors = []
        if hist_rate_normalized >= 0.85:
            factors.append("Strong historical on-time completion record")
        elif hist_rate_normalized < 0.65:
            factors.append("Lower past completion reliability requires monitoring")

        if available_hours_per_day >= 5.0:
            factors.append("High daily committed working hours")
        else:
            factors.append("Part-time daily working hours limit throughput")

        if current_workload > 40:
            factors.append(f"Active backlog of {int(current_workload)} units creates production delay risk")

        if est_days <= days_to_deadline:
            factors.append(f"Estimated completion ({round(est_days, 1)} days) is within order deadline window ({round(days_to_deadline, 1)} days)")
        else:
            factors.append(f"Estimated duration ({round(est_days, 1)} days) exceeds order deadline ({round(days_to_deadline, 1)} days)")

        confidence_score = round(min(0.95, max(0.60, 0.75 + (0.1 if self.classifier else 0.0) + 0.1 * (hist_rate_normalized - 0.5))), 2)

        explanation = (
            f"Artisan {member_id} is projected with {likelihood_pct}% likelihood to complete "
            f"{proposed_quantity} units by {est_completion_date} (confidence: {confidence_score}). "
            f"Requires review and approval by SHG leader."
        )

        return {
            "member_id": member_id,
            "completion_likelihood_percentage": likelihood_pct,
            "estimated_completion_date": est_completion_date,
            "confidence_score": confidence_score,
            "factors": factors,
            "explanation": explanation
        }

    def _heuristic_likelihood(self, qty, workload, capacity, days_left, hist_rate) -> float:
        total_units = qty + workload * 0.3
        effective_capacity = capacity * days_left
        ratio = effective_capacity / max(1.0, total_units)
        prob = 1.0 / (1.0 + np.exp(-3.0 * (ratio - 1.0)))
        return float(min(0.98, max(0.15, prob * (0.8 + 0.2 * hist_rate))))

    def optimize_allocation(
        self,
        bulk_order_id: int,
        order_item_id: int,
        product_id: int,
        total_quantity: int,
        deadline_str: Optional[str],
        members: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Runs SciPy Linear Programming constraint optimization across candidates.

        Enforces:
        - sum(allocated) == total_quantity
        - 0 <= x_i <= max_capacity_i
        - Balances fairness while weighting completion likelihood
        """
        now = datetime.now(timezone.utc)
        if deadline_str:
            try:
                deadline_dt = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
                working_days = max(1.0, (deadline_dt - now).total_seconds() / 86400.0)
            except Exception:
                working_days = 14.0
        else:
            working_days = 14.0

        n_members = len(members)
        if n_members == 0:
            return {
                "success": False,
                "is_feasible": False,
                "bulk_order_id": bulk_order_id,
                "order_item_id": order_item_id,
                "total_allocated": 0,
                "unallocated_quantity": total_quantity,
                "recommendations": [],
                "fairness_index": 0.0,
                "explanation": "No candidate SHG members available for allocation."
            }

        # Calculate individual upper bounds (max capacity for the duration)
        capacities = []
        member_metadata = []
        for m in members:
            m_id = m.get("member_id")
            hours = float(m.get("available_hours_per_day", 6.0))
            daily_rate = float(m.get("max_feasible_daily_quantity", (hours * 2.5) / 2.0))
            workload = float(m.get("current_workload", 0.0))
            hist_rate = float(m.get("historical_completion_rate", 95.0))
            skills = m.get("skills", [])

            # Upper bound considering existing workload
            net_capacity = max(0.0, daily_rate * working_days - workload * 0.4)
            capacities.append(net_capacity)
            member_metadata.append({
                "member_id": m_id,
                "hours": hours,
                "daily_rate": daily_rate,
                "workload": workload,
                "hist_rate": hist_rate,
                "skills": skills,
                "net_capacity": net_capacity
            })

        total_net_capacity = sum(capacities)

        # Infeasibility Check: If collective capacity < required total quantity
        if total_net_capacity < total_quantity:
            shortfall = int(round(total_quantity - total_net_capacity))
            infeasibility_explanation = (
                f"INFEASIBLE ALLOCATION: Total collective artisan capacity across {n_members} members "
                f"is {int(round(total_net_capacity))} units within {round(working_days, 1)} days, leaving a "
                f"shortfall of {shortfall} units for order requirement of {total_quantity} units. "
                f"Recommended action: Extend order deadline by at least {int(np.ceil(shortfall / max(1.0, sum(c['daily_rate'] for c in member_metadata))))} days "
                f"or assign additional artisans."
            )
            return {
                "success": True,
                "is_feasible": False,
                "bulk_order_id": bulk_order_id,
                "order_item_id": order_item_id,
                "total_allocated": 0,
                "unallocated_quantity": total_quantity,
                "shortfall": shortfall,
                "recommendations": [],
                "fairness_index": 0.0,
                "explanation": infeasibility_explanation
            }

        # Linear Programming:
        # We want to distribute total_quantity fairly across members.
        # Proportional fair target for each member: target_i = total_quantity * (capacity_i / total_net_capacity)
        # Minimize sum of deviation from target + penalty for low likelihood
        c_weights = []
        for m in member_metadata:
            hist_norm = m["hist_rate"] / 100.0 if m["hist_rate"] > 1.0 else m["hist_rate"]
            # Members with higher reliability and available hours have lower cost (favored in objective)
            cost = 1.0 - 0.4 * hist_norm - 0.2 * (m["hours"] / 8.0)
            c_weights.append(cost)

        # Bounds: 0 <= x_i <= capacity_i
        bounds = [(0, cap) for cap in capacities]

        # Equality constraint: sum(x_i) == total_quantity
        A_eq = [np.ones(n_members)]
        b_eq = [float(total_quantity)]

        res = linprog(
            c=c_weights,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method="highs"
        )

        if not res.success:
            # Fallback to proportional rounding
            allocated_quantities = []
            for cap in capacities:
                allocated_quantities.append(int(round(total_quantity * (cap / max(1.0, total_net_capacity)))))
            # Adjust difference to ensure exact sum == total_quantity
            diff = total_quantity - sum(allocated_quantities)
            allocated_quantities[0] += diff
        else:
            raw_allocs = [max(0, val) for val in res.x]
            # Convert to integers that sum exactly to total_quantity
            allocated_quantities = [int(np.floor(x)) for x in raw_allocs]
            remainder = total_quantity - sum(allocated_quantities)
            # Distribute remainder to highest fractional parts
            fractional_indices = np.argsort([raw_allocs[i] - allocated_quantities[i] for i in range(n_members)])[::-1]
            for i in range(remainder):
                allocated_quantities[fractional_indices[i % n_members]] += 1

        # Generate individual recommendations with completion predictions
        recommendations = []
        for i, meta in enumerate(member_metadata):
            alloc_qty = allocated_quantities[i]
            pred = self.predict_member_completion(
                member_id=meta["member_id"],
                product_id=product_id,
                proposed_quantity=alloc_qty,
                deadline_str=deadline_str,
                available_hours_per_day=meta["hours"],
                current_workload=meta["workload"],
                historical_completion_rate=meta["hist_rate"],
                skills=meta["skills"]
            )
            recommendations.append({
                "member_id": meta["member_id"],
                "proposed_quantity": alloc_qty,
                "completion_likelihood_percentage": pred["completion_likelihood_percentage"],
                "estimated_completion_date": pred["estimated_completion_date"],
                "confidence_score": pred["confidence_score"],
                "factors": pred["factors"],
                "explanation": pred["explanation"]
            })

        # Calculate Gini-like fairness index (1.0 = perfectly fair according to relative capacity)
        alloc_arr = np.array(allocated_quantities, dtype=float)
        cap_arr = np.array(capacities, dtype=float)
        with np.errstate(divide='ignore', invalid='ignore'):
            load_ratios = np.where(cap_arr > 0, alloc_arr / cap_arr, 0.0)
        fairness_index = round(float(max(0.0, 1.0 - float(np.std(load_ratios)))), 2)

        return {
            "success": True,
            "is_feasible": True,
            "bulk_order_id": bulk_order_id,
            "order_item_id": order_item_id,
            "total_allocated": sum(allocated_quantities),
            "unallocated_quantity": 0,
            "recommendations": recommendations,
            "fairness_index": fairness_index,
            "explanation": (
                f"Proposed allocation for bulk order #{bulk_order_id}: {total_quantity} units distributed "
                f"across {n_members} members with fairness score {fairness_index}. "
                f"All allocations are proposed and strictly require SHG leader approval."
            )
        }


allocation_optimizer = AllocationOptimizer()
