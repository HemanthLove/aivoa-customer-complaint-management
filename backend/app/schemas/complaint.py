from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ComplaintData(BaseModel):
    customer_name: Optional[str] = None
    customer_source: Optional[str] = None

    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None

    manufacturing_date: Optional[date] = None
    expiry_date: Optional[date] = None

    affected_quantity: Optional[float] = None
    affected_quantity_unit: Optional[str] = None

    complaint_description: Optional[str] = None

    facility_name: Optional[str] = None
    material_impact: Optional[str] = None

    defect_type: Optional[str] = None
    defect_description: Optional[str] = None


class RiskAssessment(BaseModel):
    severity: Optional[str] = None
    risk_level: Optional[str] = None
    recommended_action: Optional[str] = None
    rationale: Optional[str] = None


class ComplaintAIResult(BaseModel):
    complaint: ComplaintData
    risk_assessment: RiskAssessment