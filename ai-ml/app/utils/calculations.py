import math
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


def calculate_pricing_breakdown(
    material_cost: float,
    labor_cost: float,
    packaging_cost: float,
    transport_cost: float,
    operational_expenses: float,
    quantity: int,
    target_margin_percentage: float
) -> Dict[str, Any]:
    """Calculates product pricing based on costs and target profit margin.

    Uses the standard margin formula:
    Selling Price = Unit Cost / (1 - Margin% / 100)
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    if target_margin_percentage < 0.0 or target_margin_percentage >= 100.0:
        raise ValueError("Target margin percentage must be >= 0% and < 100%.")

    total_cost = round(
        material_cost + labor_cost + packaging_cost + transport_cost + operational_expenses,
        2
    )
    unit_cost = round(total_cost / quantity, 2)

    # Standard commercial margin calculation
    margin_factor = 1.0 - (target_margin_percentage / 100.0)
    recommended_unit_price = round(unit_cost / margin_factor, 2)
    recommended_total_order_value = round(recommended_unit_price * quantity, 2)
    estimated_profit = round(recommended_total_order_value - total_cost, 2)
    actual_margin = round((estimated_profit / recommended_total_order_value) * 100.0, 2) if recommended_total_order_value > 0 else 0.0

    missing_cost_warnings = []
    if packaging_cost == 0.0:
        missing_cost_warnings.append("Packaging cost is zero. Ensure protective packaging allowance is included.")
    if transport_cost == 0.0:
        missing_cost_warnings.append("Transportation cost is zero. Consider freight or local delivery costs.")
    if operational_expenses == 0.0:
        missing_cost_warnings.append("Operational expenses are zero. Recommend setting 3-5% allowance for electricity and equipment wear.")

    return {
        "recommended_selling_price_per_unit": recommended_unit_price,
        "recommended_total_order_value": recommended_total_order_value,
        "estimated_profit": estimated_profit,
        "margin_percentage": actual_margin,
        "missing_cost_warnings": missing_cost_warnings,
        "market_benchmark_range": None  # Honest: no live market benchmark integration configured
    }


def calculate_inventory_stockout(
    current_physical_stock: float,
    bulk_committed_stock: float,
    lead_time_days: int,
    daily_burn_rate: Optional[float]
) -> Dict[str, Any]:
    """Calculates usable inventory, projected stockout timeline, and restocking urgency."""
    usable_stock = max(0.0, round(current_physical_stock - bulk_committed_stock, 2))
    
    # Default burn rate if none provided
    burn = daily_burn_rate if (daily_burn_rate is not None and daily_burn_rate > 0.0) else 2.5
    
    if burn > 0:
        days_until_stockout = round(usable_stock / burn, 1)
    else:
        days_until_stockout = 999.0

    # Restock recommendation rules
    reorder_point = burn * lead_time_days * 1.25  # 25% safety buffer
    restock_recommended = usable_stock <= reorder_point

    if days_until_stockout <= 0:
        urgency = "CRITICAL"
    elif days_until_stockout <= lead_time_days:
        urgency = "HIGH"
    elif days_until_stockout <= lead_time_days * 1.5:
        urgency = "MEDIUM"
    else:
        urgency = "LOW"

    # Order quantity: cover lead time + 14 days operational buffer minus usable stock
    target_stock = round((lead_time_days + 14) * burn, 2)
    recommended_order_quantity = max(0.0, round(target_stock - usable_stock, 2))

    explanation = (
        f"Usable stock is {usable_stock} units ({current_physical_stock} physical minus "
        f"{bulk_committed_stock} bulk committed). At {burn} units/day burn rate, "
        f"stock will deplete in {days_until_stockout} days against a supplier lead time of {lead_time_days} days."
    )

    return {
        "days_until_stockout": days_until_stockout,
        "restock_recommended": restock_recommended,
        "recommended_order_quantity": recommended_order_quantity,
        "urgency": urgency,
        "explanation": explanation
    }


def calculate_workforce_completion_likelihood(
    member_id: int,
    proposed_quantity: int,
    deadline_str: Optional[str],
    available_hours_per_day: float,
    current_workload: float,
    historical_completion_rate: float,
    skills: List[str]
) -> Dict[str, Any]:
    """Estimates the likelihood that an SHG member can complete assigned production before the deadline."""
    # Estimated units per working hour for handcrafted artisanal production
    units_per_hour = 1.25
    daily_capacity = max(1.0, available_hours_per_day * units_per_hour)
    
    # Total units to produce including backlog
    total_burden = proposed_quantity + current_workload
    days_needed = math.ceil(total_burden / daily_capacity)

    # Calculate days available until deadline
    days_available = 7.0  # default assumption if no deadline provided
    if deadline_str:
        try:
            # Handle ISO string with or without Z
            cleaned_deadline = deadline_str.replace("Z", "+00:00")
            dl_dt = datetime.fromisoformat(cleaned_deadline)
            now_dt = datetime.now(timezone.utc)
            delta = (dl_dt - now_dt).total_seconds() / 86400.0
            days_available = max(0.1, delta)
        except Exception:
            days_available = 7.0

    factors = []
    # 1. Capacity ratio: days available vs days needed
    capacity_ratio = days_available / max(0.1, days_needed)
    if capacity_ratio >= 1.2:
        capacity_score = 95.0
        factors.append(f"Comfortable timeline: {days_needed} days needed vs {round(days_available, 1)} days available")
    elif capacity_ratio >= 1.0:
        capacity_score = 85.0
        factors.append(f"Tight timeline: {days_needed} days needed vs {round(days_available, 1)} days available")
    elif capacity_ratio >= 0.7:
        capacity_score = 60.0
        factors.append(f"Capacity constrained: member needs {days_needed} days but deadline is in {round(days_available, 1)} days")
    else:
        capacity_score = 25.0
        factors.append(f"Severe deadline risk: {days_needed} days needed exceeds available window of {round(days_available, 1)} days")

    # 2. Historical completion rate weight (35% weight)
    hist_score = max(20.0, min(100.0, historical_completion_rate))
    factors.append(f"Historical completion rate: {historical_completion_rate}%")

    # 3. Workload burden penalty
    workload_penalty = min(25.0, (current_workload / max(1.0, daily_capacity * 3.0)) * 20.0)
    if current_workload > 0:
        factors.append(f"Active backlog burden: {current_workload} pending units")

    # 4. Skill synergy bonus
    skill_bonus = 5.0 if len(skills) > 0 else 0.0

    # Composite likelihood calculation
    composite = (0.55 * capacity_score) + (0.45 * hist_score) - workload_penalty + skill_bonus
    completion_likelihood = round(max(5.0, min(99.0, composite)), 1)

    est_completion_date = (datetime.now(timezone.utc) + timedelta(days=days_needed)).isoformat()
    confidence = 0.88 if deadline_str else 0.75

    explanation = (
        f"Member {member_id} produces ~{round(daily_capacity, 1)} units/day over {available_hours_per_day} hrs. "
        f"Completing {proposed_quantity} units requires {days_needed} days."
    )

    return {
        "member_id": member_id,
        "completion_likelihood_percentage": completion_likelihood,
        "estimated_completion_date": est_completion_date,
        "confidence_score": confidence,
        "factors": factors,
        "explanation": explanation
    }


def calculate_work_allocation(
    bulk_order_id: int,
    order_item_id: int,
    product_id: int,
    total_quantity: int,
    deadline_str: Optional[str],
    members: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Intelligently allocates production quantities among eligible members.

    Ensures:
    1. No member is assigned more than their feasible capacity.
    2. Work is distributed fairly to avoid overloading individuals.
    3. Minimizes unallocated quantity.
    4. Computes Jain's Fairness Index across allocations.
    """
    if not members:
        return {
            "bulk_order_id": bulk_order_id,
            "order_item_id": order_item_id,
            "total_allocated": 0,
            "unallocated_quantity": total_quantity,
            "recommendations": [],
            "fairness_index": 0.0,
            "explanation": "No eligible SHG members available for work allocation."
        }

    # Calculate days available until deadline
    days_available = 7.0
    if deadline_str:
        try:
            cleaned = deadline_str.replace("Z", "+00:00")
            dl = datetime.fromisoformat(cleaned)
            delta = (dl - datetime.now(timezone.utc)).total_seconds() / 86400.0
            days_available = max(1.0, delta)
        except Exception:
            days_available = 7.0

    # Step 1: Compute maximum feasible capacity for each member
    # Feasible capacity = (daily_capacity * days_available) - current_workload
    member_capacities = []
    for m in members:
        mid = m["member_id"] if isinstance(m, dict) else m.member_id
        hours = m["available_hours_per_day"] if isinstance(m, dict) else m.available_hours_per_day
        workload = m["current_workload"] if isinstance(m, dict) else m.current_workload
        max_daily = m["max_feasible_daily_quantity"] if isinstance(m, dict) else m.max_feasible_daily_quantity
        hist_rate = m["historical_completion_rate"] if isinstance(m, dict) else m.historical_completion_rate
        skills = m["skills"] if isinstance(m, dict) else m.skills

        effective_daily = min(max_daily, hours * 1.5)
        total_possible = max(0, int((effective_daily * days_available) - workload))

        member_capacities.append({
            "member_id": mid,
            "hours": hours,
            "workload": workload,
            "max_daily": max_daily,
            "hist_rate": hist_rate,
            "skills": skills,
            "feasible_capacity": total_possible
        })

    # Step 2: Proportional fair allocation respecting hard caps
    total_network_capacity = sum(mc["feasible_capacity"] for mc in member_capacities)
    
    allocated_quantities = {mc["member_id"]: 0 for mc in member_capacities}
    remaining_qty = total_quantity

    if total_network_capacity > 0:
        # First pass: allocate proportionally to feasible capacity
        for mc in member_capacities:
            if remaining_qty <= 0:
                break
            share = int(round((mc["feasible_capacity"] / total_network_capacity) * total_quantity))
            allocated = min(share, mc["feasible_capacity"], remaining_qty)
            allocated_quantities[mc["member_id"]] = allocated
            remaining_qty -= allocated

        # Second pass: distribute any rounding remainder to members with remaining capacity
        for mc in member_capacities:
            if remaining_qty <= 0:
                break
            cap_left = mc["feasible_capacity"] - allocated_quantities[mc["member_id"]]
            if cap_left > 0:
                add = min(cap_left, remaining_qty)
                allocated_quantities[mc["member_id"]] += add
                remaining_qty -= add

    total_allocated = sum(allocated_quantities.values())
    unallocated = max(0, total_quantity - total_allocated)

    # Step 3: Compute recommendations and completion likelihoods
    recommendations = []
    alloc_values = []
    for mc in member_capacities:
        mid = mc["member_id"]
        qty = allocated_quantities[mid]
        alloc_values.append(qty)

        if qty > 0:
            likelihood_res = calculate_workforce_completion_likelihood(
                member_id=mid,
                proposed_quantity=qty,
                deadline_str=deadline_str,
                available_hours_per_day=mc["hours"],
                current_workload=mc["workload"],
                historical_completion_rate=mc["hist_rate"],
                skills=mc["skills"]
            )
            recommendations.append({
                "member_id": mid,
                "proposed_quantity": qty,
                "completion_likelihood_percentage": likelihood_res["completion_likelihood_percentage"],
                "estimated_completion_date": likelihood_res["estimated_completion_date"],
                "confidence_score": likelihood_res["confidence_score"],
                "factors": likelihood_res["factors"],
                "explanation": (
                    f"Assigned {qty} units based on {mc['hours']} hrs/day capacity, "
                    f"{mc['workload']} current backlog, and {mc['hist_rate']}% track record."
                )
            })

    # Step 4: Calculate Jain's Fairness Index
    # J = (sum(x_i))^2 / (n * sum(x_i^2))
    n = len(alloc_values)
    sum_x = sum(alloc_values)
    sum_sq_x = sum(x ** 2 for x in alloc_values)
    if n > 0 and sum_sq_x > 0:
        fairness_index = round((sum_x ** 2) / (n * sum_sq_x), 2)
    else:
        fairness_index = 1.0

    explanation = (
        f"Allocated {total_allocated} of {total_quantity} units across {len(recommendations)} members. "
        f"Fairness index: {fairness_index}. "
    )
    if unallocated > 0:
        explanation += f"Note: {unallocated} units could not be allocated due to member capacity constraints."

    return {
        "bulk_order_id": bulk_order_id,
        "order_item_id": order_item_id,
        "total_allocated": total_allocated,
        "unallocated_quantity": unallocated,
        "recommendations": recommendations,
        "fairness_index": fairness_index,
        "explanation": explanation
    }


def detect_financial_payout_anomalies(
    shg_id: int,
    earnings_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Inspects earnings records for arithmetic errors, high deduction ratios, or payout mismatches."""
    anomalies = []
    flags = []

    for idx, rec in enumerate(earnings_records):
        mid = rec.get("member_id", idx + 1)
        assigned = float(rec.get("assigned_qty", 0.0))
        accepted = float(rec.get("accepted_qty", 0.0))
        rate = float(rec.get("rate", 0.0))
        net = float(rec.get("net", 0.0))
        deductions = float(rec.get("deductions", 0.0))
        gross_reported = rec.get("gross_earnings")

        expected_gross = round(accepted * rate, 2)
        expected_net = round(expected_gross - deductions, 2)

        # 1. Accepted quantity exceeding assigned quantity
        if accepted > assigned and assigned > 0:
            anomalies.append({
                "member_id": mid,
                "flag_type": "QUANTITY_OVER_ASSIGNED",
                "severity": "WARNING",
                "detail": f"Accepted quantity ({accepted}) exceeds assigned quantity ({assigned}). Requires supervisor verification.",
                "requires_human_resolution": True
            })
            flags.append(f"MEMBER_{mid}_OVER_PRODUCTION")

        # 2. Arithmetic mismatch in gross earnings
        if gross_reported is not None and abs(float(gross_reported) - expected_gross) > 0.05:
            anomalies.append({
                "member_id": mid,
                "flag_type": "GROSS_CALCULATION_MISMATCH",
                "severity": "CRITICAL",
                "detail": f"Reported gross (INR {gross_reported}) does not match accepted_qty ({accepted}) * rate ({rate}) = INR {expected_gross}.",
                "requires_human_resolution": True
            })
            flags.append(f"MEMBER_{mid}_GROSS_MISMATCH")

        # 3. Arithmetic mismatch in net payable
        if abs(net - expected_net) > 0.05:
            anomalies.append({
                "member_id": mid,
                "flag_type": "NET_PAYOUT_MISMATCH",
                "severity": "CRITICAL",
                "detail": f"Recorded net (INR {net}) does not equal gross (INR {expected_gross}) minus deductions (INR {deductions}) = INR {expected_net}.",
                "requires_human_resolution": True
            })
            flags.append(f"MEMBER_{mid}_NET_MISMATCH")

        # 4. Excessive deduction ratio (over 40% of gross)
        if expected_gross > 0 and (deductions / expected_gross) > 0.40:
            deduction_pct = round((deductions / expected_gross) * 100.0, 1)
            anomalies.append({
                "member_id": mid,
                "flag_type": "HIGH_DEDUCTION_RATIO",
                "severity": "WARNING",
                "detail": f"Deduction of INR {deductions} accounts for {deduction_pct}% of gross earnings (INR {expected_gross}). Documented justification required.",
                "requires_human_resolution": True
            })
            flags.append(f"MEMBER_{mid}_HIGH_DEDUCTION")

        # 5. Negative net payout
        if net < 0:
            anomalies.append({
                "member_id": mid,
                "flag_type": "NEGATIVE_NET_PAYOUT",
                "severity": "CRITICAL",
                "detail": f"Net payable amount is negative (INR {net}). Deductions exceed total earned wages.",
                "requires_human_resolution": True
            })
            flags.append(f"MEMBER_{mid}_NEGATIVE_PAY")

    human_resolution_required = len(anomalies) > 0
    summary = (
        f"Audited {len(earnings_records)} records for SHG #{shg_id}. "
        f"Detected {len(anomalies)} anomalies requiring human review."
        if human_resolution_required else
        f"All {len(earnings_records)} earnings records for SHG #{shg_id} are mathematically consistent."
    )

    return {
        "anomalies_flagged": anomalies,
        "anomalies_count": len(anomalies),
        "flags": flags,
        "human_resolution_required": human_resolution_required,
        "summary": summary
    }


def forecast_retail_demand_statistical(
    product_id: int,
    historical_sales: List[Dict[str, Any]],
    upcoming_festival_season: bool = False
) -> Dict[str, Any]:
    """Generates demand forecast using regression/trend analysis over historical monthly sales."""
    quantities = [float(s.get("quantity", 0)) for s in historical_sales]
    
    if len(quantities) < 2:
        # Insufficient data
        base_demand = int(quantities[0]) if len(quantities) == 1 else 30
        return {
            "product_id": product_id,
            "forecasted_monthly_demand": base_demand,
            "confidence_interval": [max(0, base_demand - 15), base_demand + 25],
            "confidence_score": 0.40,
            "seasonal_factor": "Insufficient history for reliable seasonal modeling",
            "explanation": "Insufficient historical sales data (fewer than 2 data points provided). Forecast is based on minimal baseline volume."
        }

    # Trend calculation using linear regression / polyfit
    x = np.arange(len(quantities))
    y = np.array(quantities)
    
    # Linear fit: y = m*x + c
    slope, intercept = np.polyfit(x, y, 1)
    next_x = len(quantities)
    raw_projection = max(5.0, (slope * next_x) + intercept)

    seasonal_factor_explanation = None
    if upcoming_festival_season:
        # 30% festive artisan surge
        raw_projection *= 1.30
        seasonal_factor_explanation = "Diwali/Dasara festival artisan gifting surge (+30%)"

    forecast = int(round(raw_projection))

    # Standard error for confidence interval
    residuals = y - ((slope * x) + intercept)
    std_err = float(np.std(residuals)) if len(residuals) > 1 else (0.15 * forecast)
    margin_err = max(5, int(round(1.96 * max(std_err, 0.1 * forecast))))

    confidence_interval = [max(0, forecast - margin_err), forecast + margin_err]
    confidence_score = 0.85 if len(quantities) >= 4 else 0.65

    explanation = (
        f"Statistical trend projection from {len(quantities)} historical months with trend slope {round(slope, 2)}. "
    )
    if seasonal_factor_explanation:
        explanation += f"Adjusted with {seasonal_factor_explanation}."

    return {
        "product_id": product_id,
        "forecasted_monthly_demand": forecast,
        "confidence_interval": confidence_interval,
        "confidence_score": confidence_score,
        "seasonal_factor": seasonal_factor_explanation,
        "explanation": explanation
    }
