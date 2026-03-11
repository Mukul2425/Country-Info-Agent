from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    extract_intent,
    call_country_api,
    synthesize_answer
)


builder = StateGraph(AgentState)

builder.add_node("intent", extract_intent)
builder.add_node("api", call_country_api)
builder.add_node("synthesis", synthesize_answer)

builder.set_entry_point("intent")

builder.add_edge("intent", "api")
builder.add_edge("api", "synthesis")
builder.add_edge("synthesis", END)

graph = builder.compile()