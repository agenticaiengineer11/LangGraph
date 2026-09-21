from typing import TypedDict

class AgentState(TypedDict):
    user_query: str
    research: str


def research_agent(state: AgentState):
    query = state["user_query"]

    return {
        "research": f"Research completed for: {query}"
    }
input_state = {
    "user_query": "AI agent market",
    "research": ""
}
result = research_agent(input_state)

print("Node output:")
print(result)
assert result["research"] == "Research completed for: AI agent market"

print("Test passed! ✅")