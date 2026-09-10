from langgraph.graph import END, START, StateGraph
from langchain_groq import ChatGroq

from app.agents.state import ComplaintState
from app.database.database import settings
from app.schemas.complaint import ComplaintAIResult


llm = ChatGroq(
    model=settings.groq_model,
    temperature=0,
    api_key=settings.groq_api_key,
)

structured_llm = llm.with_structured_output(ComplaintAIResult)


def process_complaint(state: ComplaintState):
    result = structured_llm.invoke(
        f"""
You are an AI assistant for a pharmaceutical Customer Complaint
Management System.

Analyze the following customer complaint and extract all information
that is explicitly stated or can be directly inferred.

Rules:
1. Never invent information.
2. If information is unavailable, return null.
3. Extract customer, product, strength, batch, dates, quantity,
   defect information and other relevant complaint details.
4. Write a concise complaint description.
5. Assess complaint severity and risk.
6. Recommend an appropriate next action.
7. Explain the reasoning behind the risk assessment.

Complaint:
{state["complaint_text"]}
"""
    )

    return {
        "complaint_text": state["complaint_text"],
        "result": result,
    }


graph_builder = StateGraph(ComplaintState)

graph_builder.add_node("process_complaint", process_complaint)

graph_builder.add_edge(START, "process_complaint")
graph_builder.add_edge("process_complaint", END)

complaint_graph = graph_builder.compile()