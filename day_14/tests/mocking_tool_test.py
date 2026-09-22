def fake_search_tool(query: str):
    return "Mock search result"

result = fake_search_tool("Ai agents")

assert result == "Mock search result"
print("Mock tool test passed ")