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