"""LangGraph Production Monitoring & Delay Prediction Workflow.

Coordinates 4 specialized agent nodes:
1. Progress Tracking Agent (analyzes completed units vs scheduled velocity)
2. Delay Risk Prediction Agent (computes timeline risk and milestone lag)
3. Corrective Action & Rebalancing Agent (proposes load shifting / overtime)
4. Leader Alert & Reporting Agent (formats structured alert for backend)
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
import numpy as np
from langgraph.graph import StateGraph, END
from app.services.agents.state import ProductionMonitoringState


def progress_tracker_node(state: ProductionMonitoringState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    updates = state.get("member_updates", [])
    target = state["target_quantity"]

    total_completed = sum(int(u.get("completed_quantity", 0)) for u in updates)
    pct = round((total_completed / max(1, target)) * 100.0, 1)

    # Time calculations
    now = datetime.now(timezone.utc)
    try:
        deadline_dt = datetime.fromisoformat(state["deadline"].replace("Z", "+00:00"))
        remaining_days = max(0.5, (deadline_dt - now).total_seconds() / 86400.0)
    except Exception:
        remaining_days = 7.0

    start_date_str = state.get("start_date")
    if start_date_str:
        try:
            start_dt = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
            elapsed_days = max(1.0, (now - start_dt).total_seconds() / 86400.0)
        except Exception:
            elapsed_days = 7.0
    else:
        elapsed_days = 7.0

    current_velocity = round(total_completed / max(0.5, elapsed_days), 1)
    uncompleted = max(0, target - total_completed)
    required_velocity = round(uncompleted / max(0.5, remaining_days), 1)

    logs.append({
        "agent": "ProgressTrackingAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_completed": total_completed,
        "completion_percentage": pct,
        "current_velocity_units_per_day": current_velocity,
        "required_velocity_units_per_day": required_velocity
    })

    return {
        "total_completed": total_completed,
        "completion_percentage": pct,
        "elapsed_days": elapsed_days,
        "remaining_days": remaining_days,
        "current_velocity_per_day": current_velocity,
        "required_velocity_per_day": required_velocity,
        "execution_log": logs
    }


def delay_prediction_node(state: ProductionMonitoringState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    cur_vel = state.get("current_velocity_per_day", 1.0)
    req_vel = state.get("required_velocity_per_day", 1.0)
    rem_days = state.get("remaining_days", 7.0)

    # Velocity ratio < 1 means lagging behind
    velocity_ratio = cur_vel / max(0.1, req_vel)

    if velocity_ratio < 0.65:
        risk_level = "CRITICAL"
        risk_score = 0.88
    elif velocity_ratio < 0.90:
        risk_level = "MEDIUM"
        risk_score = 0.55
    else:
        risk_level = "LOW"
        risk_score = 0.15

    delayed_members = []
    for u in state.get("member_updates", []):
        assigned = int(u.get("assigned_quantity", 0))
        completed = int(u.get("completed_quantity", 0))
        exp_val = u.get("expected_quantity_to_date")
        expected_to_date = int(exp_val) if exp_val is not None else int(assigned * 0.5)
        if completed < expected_to_date:
            delayed_members.append({
                "member_id": u.get("member_id"),
                "lag_units": expected_to_date - completed,
                "completed": completed,
                "assigned": assigned,
                "reason": u.get("notes") or "Production velocity behind schedule"
            })

    logs.append({
        "agent": "DelayPredictionAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "risk_level": risk_level,
        "risk_score": risk_score,
        "delayed_members_count": len(delayed_members)
    })

    return {
        "delay_risk_score": risk_score,
        "risk_level": risk_level,
        "delayed_members": delayed_members,
        "execution_log": logs
    }


def corrective_action_node(state: ProductionMonitoringState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    risk_level = state.get("risk_level", "LOW")
    delayed = state.get("delayed_members", [])
    actions = []
    reallocations = []

    if risk_level in ["CRITICAL", "MEDIUM"] and delayed:
        total_lag = sum(d["lag_units"] for d in delayed)
        actions.append(f"Identified production bottleneck of {total_lag} units across {len(delayed)} members.")

        # Propose redistributing lag units to high-capacity members
        reallocations.append({
            "action": "REBALANCE_WORKLOAD",
            "units_to_reallocate": min(total_lag, int(total_lag * 0.7)),
            "source_delayed_members": [d["member_id"] for d in delayed],
            "recommendation": "Transfer unfinished units to top available artisans with >85% past on-time delivery."
        })
        actions.append(f"Recommended reallocation of {min(total_lag, int(total_lag * 0.7))} units to prevent order breach.")
        actions.append("Advise SHG supervisor to conduct in-person check-in with delayed artisans.")
    else:
        actions.append("Production pacing is currently aligned with order milestone target.")

    logs.append({
        "agent": "CorrectiveActionAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actions_generated": len(actions)
    })

    return {
        "corrective_actions": actions,
        "reallocation_recommendations": reallocations,
        "execution_log": logs
    }


def leader_alert_node(state: ProductionMonitoringState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    risk = state.get("risk_level", "LOW")
    requires_action = risk in ["CRITICAL", "MEDIUM"]

    logs.append({
        "agent": "LeaderReportingAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "REPORT_READY",
        "requires_leader_action": requires_action
    })

    return {
        "requires_leader_action": requires_action,
        "status": "ACTION_REQUIRED" if requires_action else "ON_TRACK",
        "execution_log": logs
    }


def build_production_monitoring_graph():
    builder = StateGraph(ProductionMonitoringState)

    builder.add_node("progress_tracker_node", progress_tracker_node)
    builder.add_node("delay_prediction_node", delay_prediction_node)
    builder.add_node("corrective_action_node", corrective_action_node)
    builder.add_node("leader_alert_node", leader_alert_node)

    builder.set_entry_point("progress_tracker_node")
    builder.add_edge("progress_tracker_node", "delay_prediction_node")
    builder.add_edge("delay_prediction_node", "corrective_action_node")
    builder.add_edge("corrective_action_node", "leader_alert_node")
    builder.add_edge("leader_alert_node", END)

    return builder.compile()


production_monitoring_graph = build_production_monitoring_graph()
