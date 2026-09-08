import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


tools = [multiply]

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


def llm_node(state: MessagesState):
    print("\n--- LLM NODE ---")

    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def should_continue(state: MessagesState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


builder = StateGraph(MessagesState)

builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "llm")

builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools", "llm")

graph = builder.compile()


initial_state = {
    "messages": [
        HumanMessage(
            content="Calculate 15 multiplied by 8."
        )
    ]
}

result = graph.invoke(initial_state)


print("\n===================================")
print("FINAL RESPONSE")
print("===================================")

print(result["messages"][-1].content)
