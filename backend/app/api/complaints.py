from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agents.completeness_graph import completeness_graph
from app.agents.complaint_graph import complaint_graph
from app.agents.edit_graph import edit_graph
from app.database.database import get_db
from app.schemas.completeness import ComplaintCompletenessResult
from app.schemas.complaint import ComplaintAIResult
from app.services.complaint_service import save_complaint, update_complaint
from app.services.pdf_extractor import extract_text_from_pdf


router = APIRouter(
    prefix="/api/complaints",
    tags=["Complaints"],
)


class ComplaintProcessRequest(BaseModel):
    complaint_text: str


class ComplaintEditRequest(BaseModel):
    current_complaint: ComplaintAIResult
    edit_instruction: str


class ComplaintCompletenessRequest(BaseModel):
    current_complaint: ComplaintAIResult


@router.post(
    "/process",
    response_model=ComplaintAIResult,
)
def process_complaint(
    request: ComplaintProcessRequest,
    db: Session = Depends(get_db),
):
    result = complaint_graph.invoke(
        {
            "complaint_text": request.complaint_text,
            "result": None,
        }
    )

    complaint_result = result["result"]

    save_complaint(
        db=db,
        result=complaint_result,
        source_type="text",
    )

    return complaint_result


@router.post(
    "/edit",
    response_model=ComplaintAIResult,
)
def edit_complaint(
    request: ComplaintEditRequest,
    db: Session = Depends(get_db),
):
    result = edit_graph.invoke(
        {
            "current_complaint": request.current_complaint,
            "edit_instruction": request.edit_instruction,
            "result": None,
        }
    )

    complaint_result = result["result"]

    update_complaint(
        db=db,
        result=complaint_result,
        original_complaint=request.current_complaint,
    )

    return complaint_result


@router.post(
    "/extract-document",
    response_model=ComplaintAIResult,
)
async def extract_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.content_type != "application/pdf":
        raise ValueError("Only PDF files are supported.")

    file_bytes = await file.read()

    extracted_text = extract_text_from_pdf(file_bytes)

    result = complaint_graph.invoke(
        {
            "complaint_text": extracted_text,
            "result": None,
        }
    )

    complaint_result = result["result"]

    save_complaint(
        db=db,
        result=complaint_result,
        source_type="pdf",
    )

    return complaint_result


@router.post(
    "/check-completeness",
    response_model=ComplaintCompletenessResult,
)
def check_completeness(
    request: ComplaintCompletenessRequest,
):
    result = completeness_graph.invoke(
        {
            "complaint": request.current_complaint,
            "result": None,
        }
    )

    return result["result"]