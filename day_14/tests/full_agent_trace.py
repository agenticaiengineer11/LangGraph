import os

from dotenv import load_dotenv
from typing import Literal

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode


load_dotenv()

@tool
def product_search(product: str) -> str:
    """Search for basic product information."""

    return f"""
Product: {product}

Mock research:
- Category: Outdoor Decor
- Typical use: Home and garden decoration
- Seasonality: High during Halloween
"""

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

model_with_tools = model.bind_tools(
    [product_search]
)

def agent(state: MessagesState):

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def route(
    state: MessagesState
) -> Literal["tools", "__end__"]:

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END

tool_node = ToolNode(
    [product_search]
)

builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    route,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge(
    "tools",
    "agent"
)

app = builder.compile()

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Research this product: "
                    "Halloween solar garden light"
                )
            }
        ]
    }
)
print("\nFinal conversation:\n")

for message in result["messages"]:

    print(
        f"{message.__class__.__name__}:"
    )

    print(
        message.content
    )

    print("-" * 60)