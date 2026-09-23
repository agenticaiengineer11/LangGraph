from langchain_core.tools import tool

@tool
def failing_search(query: str) -> str:
    """A mock search tool that intentionally fails."""
    raise RuntimeError("Mock search service failed")
try:
    failing_search.invoke({"query": "AI agents"})
    assert False, "Expected RuntimeError was not raised"

except RuntimeError as e:
    assert str(e) == "Mock search service failed"
    print("Integration failure-path test passed! ✅")