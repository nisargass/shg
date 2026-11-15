from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EarningsRecordInput(BaseModel):
    member_id: int
    assigned_qty: float = Field(..., ge=0.0)
    accepted_qty: float = Field(..., ge=0.0)
    rate: float = Field(..., ge=0.0)
    gross_earnings: Optional[float] = None
    deductions: float = Field(0.0, ge=0.0)
    net: float = Field(...)
    record_id: Optional[str] = None
    standard_rate: Optional[float] = None
    corrections_count: Optional[int] = 0


class FinancialAnomalyRequest(BaseModel):
    shg_id: int
    earnings_records: List[EarningsRecordInput] = Field(default_factory=list, description="List of member earnings records for audit")


class AnomalyFlag(BaseModel):
    member_id: int
    flag_type: str = Field(..., description="e.g. HIGH_DEDUCTION_RATIO, ARITHMETIC_MISMATCH, NEGATIVE_PAYOUT, STATISTICAL_OUTLIER")
    severity: str = Field(..., description="INFO, WARNING, CRITICAL")
    detail: str = Field(..., description="Detailed objective explanation of calculation discrepancy")
    requires_human_resolution: bool = Field(True, description="Always requires human verification")
    record_id: Optional[str] = Field(None, description="Identifier of the specific payment or earnings record")
    risk_score: Optional[float] = Field(None, description="Calculated anomaly risk score from 0.0 to 1.0")
    recommended_review_action: Optional[str] = Field(None, description="Prescribed action for the SHG leader or accountant")
    supporting_evidence: Optional[Dict[str, Any]] = Field(None, description="Quantified factors contributing to anomaly flag")


class FinancialAnomalyResponse(BaseModel):
    success: bool = True
    anomalies_flagged: List[AnomalyFlag] = []
    anomalies_count: int = 0
    flags: List[str] = []
    human_resolution_required: bool = False
    summary: str
