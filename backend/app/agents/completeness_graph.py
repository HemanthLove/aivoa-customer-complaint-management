from typing import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from app.database.database import settings
from app.schemas.completeness import ComplaintCompletenessResult
from app.schemas.complaint import ComplaintAIResult


class CompletenessState(TypedDict):
    complaint: ComplaintAIResult
    result: ComplaintCompletenessResult | None


llm = ChatGroq(
    model=settings.groq_model,
    temperature=0,
    api_key=settings.groq_api_key,
)

structured_llm = llm.with_structured_output(ComplaintCompletenessResult)


CORE_FIELDS = {
    "customer_name": "Customer Name",
    "product_name": "Product Name",
    "batch_number": "Batch Number",
    "defect_type": "Defect Type",
    "affected_quantity": "Affected Quantity",
    "complaint_description": "Complaint Description",
}


def check_completeness(state: CompletenessState):
    complaint = state["complaint"].complaint

    field_values = {
        field_name: getattr(complaint, field_name)
        for field_name in CORE_FIELDS
    }

    missing_fields = [
        display_name
        for field_name, display_name in CORE_FIELDS.items()
        if field_values[field_name] is None
        or str(field_values[field_name]).strip() == ""
    ]

    present_fields = [
        display_name
        for field_name, display_name in CORE_FIELDS.items()
        if field_values[field_name] is not None
        and str(field_values[field_name]).strip() != ""
    ]

    total_fields = len(CORE_FIELDS)
    completeness_score = round(
        len(present_fields) / total_fields * 100
    )

    if missing_fields:
        notes = (
            "The complaint contains some key information, "
            "but additional details are required for a more complete record."
        )
    else:
        notes = (
            "The complaint contains all core fields required "
            "for the completeness check."
        )

    result = ComplaintCompletenessResult(
        completeness_score=completeness_score,
        is_complete=not missing_fields,
        present_fields=present_fields,
        missing_fields=missing_fields,
        notes=notes,
    )

    return {
        "complaint": complaint,
        "result": result,
    }


graph_builder = StateGraph(CompletenessState)

graph_builder.add_node(
    "check_completeness",
    check_completeness,
)

graph_builder.add_edge(
    START,
    "check_completeness",
)

graph_builder.add_edge(
    "check_completeness",
    END,
)

completeness_graph = graph_builder.compile()