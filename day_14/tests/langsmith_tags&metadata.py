import os

from dotenv import load_dotenv
from typing import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()


class State(TypedDict):
    question: str
    answer: str

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def llm_agent(state: State):

    response = model.invoke(state["question"])

    return {
        "answer": response.content
    }

builder = StateGraph(State)

builder.add_node("llm_agent", llm_agent)

builder.add_edge(START, "llm_agent")
builder.add_edge("llm_agent", END)

app = builder.compile()
config = {
    "tags": ["day14", "product-research"],
    "metadata": {
        "environment": "development",
        "project": "langgraph-learning",
        "agent_version": "1.0"
    }
}
result = app.invoke(
    {
        "question": "What is an AI agent?",
        "answer": ""
    },
    config=config
)

print("Final answer:")
print(result["answer"])