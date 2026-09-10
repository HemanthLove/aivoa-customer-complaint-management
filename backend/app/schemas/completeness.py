from pydantic import BaseModel, Field


class ComplaintCompletenessResult(BaseModel):
    completeness_score: int = Field(ge=0, le=100)
    is_complete: bool
    present_fields: list[str]
    missing_fields: list[str]
    notes: str