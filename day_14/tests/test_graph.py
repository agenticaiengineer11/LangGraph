from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_query: str
    research: str


def research_agent(state: AgentState):
    return {
        "research": f"Research completed for: {state['user_query']}"
    }


builder = StateGraph(AgentState)

builder.add_node("research_agent", research_agent)

builder.add_edge(START, "research_agent")
builder.add_edge("research_agent", END)

app = builder.compile()

result = app.invoke({
    "user_query": "AI agent market",
    "research": ""
})


print("Final state:")
print(result)

assert result["research"] == "Research completed for: AI agent market"

print("Graph test passed! ✅")