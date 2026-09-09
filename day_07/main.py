from typing import Literal

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import RetryPolicy
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


@tool
def divide(a: int, b: int):
    """Divide a by b."""

    try:
        return a / b

    except ZeroDivisionError:
        return "Error: Cannot divide by zero."


tools = [add, multiply, divide]

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

model_with_tools = model.bind_tools(tools)

def llm_node(state: MessagesState):
    print("\n----- LLM NODE -----")

    response = model_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

tool_node = ToolNode(
    tools,
    handle_tool_errors=True
)

def should_continue(
    state: MessagesState
) -> Literal["tools", "fallback", "__end__"]:

    last_message = state["messages"][-1]

    print("\n----- ROUTER -----")

    if last_message.tool_calls:
        print("Tool call detected.")

        return "tools"

    print("No tool call detected.")

    return END

def fallback_node(state: MessagesState):

    print("\n----- FALLBACK NODE -----")

    return {
        "messages": [
            HumanMessage(
                content=(
                    "The requested operation could not be completed "
                    "because the tool failed. Please provide a safe "
                    "alternative response."
                )
            )
        ]
    }

builder = StateGraph(MessagesState)

builder.add_node(
    "llm",
    llm_node,
    retry_policy=RetryPolicy(
        max_attempts=3
    )
)

builder.add_node(
    "tools",
    tool_node
)

builder.add_node(
    "fallback",
    fallback_node
)

builder.add_edge(
    START,
    "llm"
)

builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge(
    "tools",
    "llm"
)

builder.add_edge(
    "fallback",
    END
)

app = builder.compile()

initial_state = {
    "messages": [
        HumanMessage(
            content="Calculate 15 multiplied by 8."
        )
    ]
}

final_state = app.invoke(
    initial_state
)

print("\n==============================")
print("FINAL MESSAGE HISTORY")
print("==============================")

for message in final_state["messages"]:

    print(
        f"\n{message.__class__.__name__}:"
    )

    print(
        message.content
    )