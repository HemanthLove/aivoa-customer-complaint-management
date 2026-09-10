from typing import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from app.database.database import settings
from app.schemas.complaint import ComplaintAIResult


class EditComplaintState(TypedDict):
    current_complaint: ComplaintAIResult
    edit_instruction: str
    result: ComplaintAIResult


llm = ChatGroq(
    model=settings.groq_model,
    temperature=0,
    api_key=settings.groq_api_key,
)

structured_llm = llm.with_structured_output(ComplaintAIResult)


def edit_complaint(state: EditComplaintState):
    current = state["current_complaint"]
    instruction = state["edit_instruction"]

    result = structured_llm.invoke(
        f"""
You are an AI assistant for a pharmaceutical Customer Complaint
Management System.

The user wants to correct or update an existing complaint.

Existing complaint:
{current.model_dump_json(indent=2)}

User's requested correction:
{instruction}

Instructions:

1. Apply ONLY the changes requested by the user.
2. Preserve all existing complaint information that the user did
   not ask to change.
3. Never invent information.
4. If the user provides a new value, use that value exactly when
   appropriate.
5. Return the COMPLETE updated ComplaintAIResult, not only the
   changed fields.
6. Reassess the risk assessment after applying the correction.
7. Keep the risk assessment consistent with the updated complaint.
8. Do not remove existing information simply because it was not
   mentioned in the correction.

Return the updated complaint and updated risk assessment.
"""
    )

    return {
        "current_complaint": current,
        "edit_instruction": instruction,
        "result": result,
    }


graph_builder = StateGraph(EditComplaintState)

graph_builder.add_node("edit_complaint", edit_complaint)

graph_builder.add_edge(START, "edit_complaint")
graph_builder.add_edge("edit_complaint", END)

edit_graph = graph_builder.compile()