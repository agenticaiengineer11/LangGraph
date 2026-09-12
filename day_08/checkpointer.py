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

builder.add_node(
    "chatbot",
    chatbot
)

builder.add_edge(
    START,
    "chatbot"
)

builder.add_edge(
    "chatbot",
    END
)


checkpointer = InMemorySaver()


app = builder.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id": "user_1"
    }
}


result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="My name is Noman."
            )
        ]
    },
    config
)


print("\nFIRST RESPONSE:")
print(result["messages"][-1].content)


result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="What did I just say?"
            )
        ]
    },
    config
)


print("\nSECOND RESPONSE:")
print(result["messages"][-1].content)


state = app.get_state(config)


print("\nSAVED STATE:")
print(state.values)


print("\nCHECKPOINT HISTORY:")

for checkpoint in app.get_state_history(config):
    print(checkpoint)