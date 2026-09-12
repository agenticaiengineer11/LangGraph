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


result_1 = app.invoke(
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
print(result_1["messages"][-1].content)


result_2 = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="I am learning LangGraph."
            )
        ]
    },
    config
)


print("\nSECOND RESPONSE:")
print(result_2["messages"][-1].content)


state = app.get_state(config)

print("\nCURRENT STATE:")
print(state.values)


print("\nCHECKPOINT HISTORY:")

for checkpoint in app.get_state_history(config):
    print(checkpoint)