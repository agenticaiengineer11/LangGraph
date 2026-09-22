from typing import TypedDict

class AgentState(TypedDict):
    user_query: str
    research: str


def research_agent(state: AgentState):
    query = state["user_query"]
    if not query:
        raise ValueError("user_query cannot be empty")

    return {
        "research": f"Research completed for: {query}"
    }


try:
    research_agent({
        "user_query": ""
    })
    assert False, "Expected ValueError was not raised"
except ValueError as e:
    assert str(e) == "user_query cannot be empty"
    print("Failure-path test passed! ✅")


input_state = {
    "user_query": "AI agent market",
    "research": ""
}
result = research_agent(input_state)

print("Node output:")
print(result)
assert result["research"] == "Research completed for: AI agent market"

print("Test passed! ✅")
