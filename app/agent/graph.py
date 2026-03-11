from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import extract_intent, call_country_api, synthesize_answer


builder = StateGraph(AgentState)

builder.add_node("intent", extract_intent)
builder.add_node("api", call_country_api)
builder.add_node("answer", synthesize_answer)


builder.set_entry_point("intent")


def route_after_intent(state: AgentState):

    if state.get("error"):
        return "answer"

    if not state.get("country"):
        return "answer"

    return "api"


builder.add_conditional_edges(
    "intent",
    route_after_intent,
    {
        "api": "api",
        "answer": "answer"
    }
)

builder.add_edge("api", "answer")
builder.add_edge("answer", END)

graph = builder.compile()