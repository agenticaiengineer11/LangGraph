from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from langchain_core.messages import HumanMessage, AIMessage


def approval_node(state: MessagesState):

    print("\n----- APPROVAL NODE -----")

    decision = interrupt(
        "Do you approve this action?"
    )

    return {
        "messages": [
            AIMessage(
                content=f"Human decision: {decision}"
            )
        ]
    }


builder = StateGraph(MessagesState)

builder.add_node(
    "approval",
    approval_node
)

builder.add_edge(
    START,
    "approval"
)

builder.add_edge(
    "approval",
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


print("\n----- STARTING GRAPH -----")

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

print("\n----- GRAPH PAUSED -----")
print(result)


human_decision = "yes"

result = app.invoke(
    Command(
        resume=human_decision
    ),
    config
)

print("\n----- GRAPH RESUMED -----")
print(result)