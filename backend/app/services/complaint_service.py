from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintAIResult


def save_complaint(
    db: Session,
    result: ComplaintAIResult,
    source_type: str,
) -> Complaint:
    complaint_data = result.complaint
    risk_data = result.risk_assessment

    complaint = Complaint(
        customer_name=complaint_data.customer_name,
        customer_source=complaint_data.customer_source,
        product_name=complaint_data.product_name,
        product_strength=complaint_data.product_strength,
        batch_number=complaint_data.batch_number,
        manufacturing_date=complaint_data.manufacturing_date,
        expiry_date=complaint_data.expiry_date,
        affected_quantity=complaint_data.affected_quantity,
        affected_quantity_unit=complaint_data.affected_quantity_unit,
        complaint_description=complaint_data.complaint_description,
        facility_name=complaint_data.facility_name,
        material_impact=complaint_data.material_impact,
        defect_type=complaint_data.defect_type,
        defect_description=complaint_data.defect_description,
        severity=risk_data.severity,
        risk_level=risk_data.risk_level,
        recommended_action=risk_data.recommended_action,
        risk_rationale=risk_data.rationale,
        source_type=source_type,
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


def update_complaint(
    db: Session,
    result: ComplaintAIResult,
    original_complaint: ComplaintAIResult,
) -> Complaint:
    complaint_data = result.complaint
    risk_data = result.risk_assessment

    original_data = original_complaint.complaint

    # Find the existing complaint using its original
    # identifying information.
    complaint = (
        db.query(Complaint)
        .filter(
            Complaint.customer_name == original_data.customer_name,
            Complaint.product_name == original_data.product_name,
            Complaint.batch_number == original_data.batch_number,
        )
        .order_by(Complaint.id.desc())
        .first()
    )

    # If the original complaint cannot be found,
    # create it as a new record instead of failing.
    if complaint is None:
        return save_complaint(
            db=db,
            result=result,
            source_type="edit",
        )

    # Update the existing record.
    complaint.customer_name = complaint_data.customer_name
    complaint.customer_source = complaint_data.customer_source
    complaint.product_name = complaint_data.product_name
    complaint.product_strength = complaint_data.product_strength
    complaint.batch_number = complaint_data.batch_number
    complaint.manufacturing_date = complaint_data.manufacturing_date
    complaint.expiry_date = complaint_data.expiry_date
    complaint.affected_quantity = complaint_data.affected_quantity
    complaint.affected_quantity_unit = complaint_data.affected_quantity_unit
    complaint.complaint_description = complaint_data.complaint_description
    complaint.facility_name = complaint_data.facility_name
    complaint.material_impact = complaint_data.material_impact
    complaint.defect_type = complaint_data.defect_type
    complaint.defect_description = complaint_data.defect_description

    complaint.severity = risk_data.severity
    complaint.risk_level = risk_data.risk_level
    complaint.recommended_action = risk_data.recommended_action
    complaint.risk_rationale = risk_data.rationale

    complaint.source_type = "edit"

    db.commit()
    db.refresh(complaint)

    return complaint