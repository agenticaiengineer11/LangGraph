from typing import TypedDict


class AgentState(TypedDict):
    user_query: str
    research: str


def research_agent(state: AgentState):
    query = state["user_query"]

    return {
        "research": f"Research completed for: {query}"
    }
result = research_agent({
    "user_query": "AI agent Market",
    "research": ""
})
print(result)
assert result["research"] == "Research completed for: AI agent Market"
