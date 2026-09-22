from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
@tool
def mock_search(query: str) -> str:
    """Search for information using a mocked search service."""
    return f"Mock search result for: {query}"

def agent(state: MessagesState):

    messages = state["messages"]

    last_message = messages[-1]

    if isinstance(last_message, HumanMessage):

        return {
            "messages": [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "mock_search",
                            "args": {
                                "query": last_message.content
                            },
                            "id": "call_1",
                            "type": "tool_call",
                        }
                    ],
                )
            ]
        }

    if isinstance(last_message, HumanMessage):
        return {}

    return {}

tool_node = ToolNode([mock_search])

def route(state: MessagesState) -> Literal["tools", END]:

    last_message = state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"

    return END

builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

app = builder.compile()

result = app.invoke(
    {
        "messages": [
            HumanMessage(content="AI agents")
        ]
    }
)
messages = result["messages"]

assert len(messages) >= 3

assert any(
    message.type == "tool"
    and message.content == "Mock search result for: AI agents"
    for message in messages
)

print("Integration test passed! ✅")