from typing import Literal

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from langchain_core.messages import HumanMessage, AIMessage

def request_node(state: MessagesState):

    print("\n----- REQUEST NODE -----")

    return {
        "messages": [
            AIMessage(
                content="Request prepared for human approval."
            )
        ]
    }

def human_approval_node(state: MessagesState):

    print("\n----- HUMAN APPROVAL NODE -----")

    decision = interrupt(
        "Do you approve this action? Reply with yes or no."
    )

    decision = str(decision).lower().strip()

    print(f"Human decision: {decision}")

    return {
        "messages": [
            AIMessage(
                content=f"Human decision: {decision}"
            )
        ]
    }

def approval_router(
    state: MessagesState
) -> Literal["action", "rejected"]:

    last_message = state["messages"][-1]

    content = last_message.content.lower().strip()

    print("\n----- APPROVAL ROUTER -----")

    if "yes" in content:
        print("Approved → ACTION")
        return "action"

    print("Not approved → REJECTED")
    return "rejected"

def action_node(state: MessagesState):

    print("\n----- ACTION NODE -----")

    return {
        "messages": [
            AIMessage(
                content="Action executed successfully."
            )
        ]
    }

def rejected_node(state: MessagesState):

    print("\n----- REJECTED NODE -----")

    return {
        "messages": [
            AIMessage(
                content="Action rejected by human."
            )
        ]
    }

builder = StateGraph(MessagesState)

builder.add_node(
    "request",
    request_node
)

builder.add_node(
    "human_approval",
    human_approval_node
)

builder.add_node(
    "action",
    action_node
)

builder.add_node(
    "rejected",
    rejected_node
)

builder.add_edge(
    START,
    "request"
)

builder.add_edge(
    "request",
    "human_approval"
)

builder.add_conditional_edges(
    "human_approval",
    approval_router,
    {
        "action": "action",
        "rejected": "rejected"
    }
)

builder.add_edge(
    "action",
    END
)

builder.add_edge(
    "rejected",
    END
)

checkpointer = InMemorySaver()

app = builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "approval_1"
    }
}

print("\n========== STARTING GRAPH ==========")

result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="I want to publish a product."
            )
        ]
    },
    config
)

print("\n========== GRAPH PAUSED ==========")

print(result)

human_decision = "yes"

print("\n========== RESUMING GRAPH ==========")

final_state = app.invoke(
    Command(
        resume=human_decision
    ),
    config
)

print("\n========== FINAL MESSAGE HISTORY ==========")

for message in final_state["messages"]:

    print(
        f"{message.__class__.__name__}: "
        f"{message.content}"
    )