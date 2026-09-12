from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage


def chatbot(state: MessagesState):

    messages = state["messages"]

    last_message = messages[-1]

    return {
        "messages": [
            AIMessage(
                content=f"You said: {last_message.content}"
            )
        ]
    }

builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

checkpointer = InMemorySaver()

app = builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

app.invoke(
    {
        "messages": [
            HumanMessage(
                content="My name is Noman."
            )
        ]
    },
    config
)

app.invoke(
    {
        "messages": [
            HumanMessage(
                content="I am learning LangGraph."
            )
        ]
    },
    config
)

current_state = app.get_state(config)

print("\n========== CURRENT STATE ==========")

for message in current_state.values["messages"]:
    print(
        f"{message.__class__.__name__}: "
        f"{message.content}"
    )

print("\n========== CHECKPOINT HISTORY ==========")

history = list(
    app.get_state_history(config)
)

for index, checkpoint in enumerate(history):

    print(f"\nCHECKPOINT {index}")

    print("Checkpoint ID:")
    print(checkpoint.config["configurable"]["checkpoint_id"])

    print("Messages:")

    for message in checkpoint.values["messages"]:
        print(
            f"  {message.__class__.__name__}: "
            f"{message.content}"
        )

old_checkpoint = history[2]

old_config = old_checkpoint.config

print("\n========== TIME TRAVEL ==========")

old_state = app.get_state(old_config)

for message in old_state.values["messages"]:
    print(
        f"{message.__class__.__name__}: "
        f"{message.content}"
    )