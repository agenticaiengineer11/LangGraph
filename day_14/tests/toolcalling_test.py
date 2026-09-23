from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

load_dotenv()


@tool
def product_search(product: str) -> str:
    """Search for product information."""
    return f"Product research result for: {product}"

def agent(state: MessagesState):

    last_message = state["messages"][-1]

    if isinstance(last_message, HumanMessage):

        return {
            "messages": [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "product_search",
                            "args": {
                                "product": last_message.content
                            },
                            "id": "call_1",
                            "type": "tool_call",
                        }
                    ],
                )
            ]
        }

    return {}

tool_node = ToolNode([product_search])

builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_edge("agent", "tools")
builder.add_edge("tools", END)

app = builder.compile()

result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="Halloween solar garden light"
            )
        ]
    }
)

print("Final messages:")

for message in result["messages"]:
    print(
        f"{message.__class__.__name__}: "
        f"{message.content}"
    )