import os

from dotenv import load_dotenv
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

load_dotenv()

class State(TypedDict):
    message: str

def chatbot(state: State):
    return {
        "message": f"Processed: {state['message']}"
    }

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

app = builder.compile()

result = app.invoke({
    "message": "Hello LangSmith"
})


print("Final result:")
print(result)