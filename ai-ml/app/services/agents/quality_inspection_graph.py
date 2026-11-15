"""LangGraph Quality Inspection & Specification Compliance Workflow.

Coordinates 3 specialized agent nodes:
1. Image Quality Gate Agent (resolution, blur, underexposure/overexposure)
2. Computer Vision Inspection Agent (specifications, dimensions, defects)
3. Quality Report Synthesis Agent (compliance score, human review recommendation)
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from langgraph.graph import StateGraph, END
from app.services.agents.state import QualityInspectionState
from app.providers.vision_provider import get_vision_provider


def image_quality_gate_node(state: QualityInspectionState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    urls = state.get("photo_urls", [])

    if not urls:
        logs.append({
            "agent": "ImageQualityGateAgent",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "FAILED_NO_IMAGES"
        })
        return {
            "image_quality_passed": False,
            "image_quality_notes": "No photos provided for quality analysis.",
            "execution_log": logs
        }

    provider = get_vision_provider()
    res = provider.inspect_photos(photo_urls=urls, specifications=[])
    passed = res.get("image_quality_status") != "LOW_IMAGE_QUALITY"

    logs.append({
        "agent": "ImageQualityGateAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASSED" if passed else "LOW_IMAGE_QUALITY",
        "notes": res.get("explanation")
    })

    return {
        "image_quality_passed": passed,
        "image_quality_notes": res.get("explanation", ""),
        "execution_log": logs
    }


def cv_inspection_node(state: QualityInspectionState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    urls = state.get("photo_urls", [])
    specs = state.get("specifications", [])

    provider = get_vision_provider()
    res = provider.inspect_photos(photo_urls=urls, specifications=specs)

    logs.append({
        "agent": "CVInspectionAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "INSPECTED",
        "quality_score": res.get("quality_score", 85.0),
        "defects_count": len(res.get("defects_detected", []))
    })

    return {
        "quality_score": res.get("quality_score", 85.0),
        "confidence_score": res.get("confidence_score", 0.88),
        "detected_issues": res.get("detected_issues", []),
        "deviations": res.get("specification_deviations", []),
        "execution_log": logs
    }


def quality_report_synthesis_node(state: QualityInspectionState) -> Dict[str, Any]:
    logs = list(state.get("execution_log", []))
    q_score = state.get("quality_score", 85.0)
    img_pass = state.get("image_quality_passed", True)

    if not img_pass:
        action = "LOW_IMAGE_QUALITY"
        explanation = f"Inspection could not complete reliably: {state.get('image_quality_notes')}"
    else:
        action = "HUMAN_REVIEW"
        explanation = (
            f"Automated computer vision quality analysis scored batch #{state['batch_id']} at {q_score}/100. "
            f"Advisory decision: {action}. Final product acceptance or rejection strictly requires authorized human inspection."
        )

    report = {
        "batch_id": state["batch_id"],
        "product_id": state["product_id"],
        "quality_score": q_score,
        "confidence_score": state.get("confidence_score", 0.88),
        "detected_issues": state.get("detected_issues", []),
        "specification_deviations": state.get("deviations", []),
        "suggested_action": action,
        "explanation": explanation,
        "requires_human_review": True
    }

    logs.append({
        "agent": "QualityReportSynthesizerAgent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "REPORT_GENERATED",
        "action": action
    })

    return {
        "inspection_report": report,
        "suggested_action": action,
        "requires_human_review": True,
        "execution_log": logs
    }


def route_after_quality_gate(state: QualityInspectionState) -> str:
    if not state.get("image_quality_passed", True):
        return "quality_report_synthesis_node"
    return "cv_inspection_node"


def build_quality_inspection_graph():
    builder = StateGraph(QualityInspectionState)

    builder.add_node("image_quality_gate_node", image_quality_gate_node)
    builder.add_node("cv_inspection_node", cv_inspection_node)
    builder.add_node("quality_report_synthesis_node", quality_report_synthesis_node)

    builder.set_entry_point("image_quality_gate_node")

    builder.add_conditional_edges(
        "image_quality_gate_node",
        route_after_quality_gate,
        {
            "cv_inspection_node": "cv_inspection_node",
            "quality_report_synthesis_node": "quality_report_synthesis_node"
        }
    )
    builder.add_edge("cv_inspection_node", "quality_report_synthesis_node")
    builder.add_edge("quality_report_synthesis_node", END)

    return builder.compile()


quality_inspection_graph = build_quality_inspection_graph()
