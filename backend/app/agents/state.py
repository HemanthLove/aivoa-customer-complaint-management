from typing import Optional, TypedDict

from app.schemas.complaint import ComplaintAIResult


class ComplaintState(TypedDict):
    complaint_text: str
    result: Optional[ComplaintAIResult]