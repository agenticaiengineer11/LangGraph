from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
def chatbot(state: MessagesState):

    response = model.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
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

config_2 = {
    "configurable": {
        "thread_id": "user_2"
    }
}

result = app.invoke(
    {
        "messages": [
            HumanMessage(
                content="What is my name?"
            )
        ]
    },
    config_2
)
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
                content="What is my name?"
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