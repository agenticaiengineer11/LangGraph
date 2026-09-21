from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: str


async def chatbot(state: State):
    return {
        "message": f"Processed: {state['message']}"
    }


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

app = builder.compile()


async def main():

    async for update in app.astream(
        {"message": "Hello LangGraph"}
    ):
        print(update)


import asyncio

asyncio.run(main())