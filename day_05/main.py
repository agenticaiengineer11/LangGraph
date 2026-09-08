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

    print("LLM response generated.")

    return {
        "messages": [response]
    }

tool_node = ToolNode(tools)


# ==========================================
# 7. Router
# ==========================================

def should_continue(state: MessagesState):

    last_message = state["messages"][-1]

    print("\n--- ROUTER ---")

    # If LLM requested a tool
    if last_message.tool_calls:
        print("Tool call detected.")
        return "tools"

    # Otherwise finish
    print("No tool call detected. Ending.")
    return END

builder = StateGraph(MessagesState)


# Add nodes
builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)


# START → LLM
builder.add_edge(START, "llm")


# LLM → Router → Tools OR END
builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)


# Tool → LLM
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
print("FINAL MESSAGE HISTORY")
print("===================================")

for message in result["messages"]:

    print(f"\n{message.__class__.__name__}:")

    print(message.content)

    if getattr(message, "tool_calls", None):
        print("Tool Calls:")

        for tool_call in message.tool_calls:
            print(tool_call)


print("\n===================================")
print("FINAL RESPONSE")
print("===================================")

print(result["messages"][-1].content)