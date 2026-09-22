from typing import TypedDict

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_query: str
    response: str

fake_model = FakeListChatModel(
    responses=["This is a mocked AI response."]
)


def chatbot(state: AgentState):
    response = fake_model.invoke(state["user_query"])

    return {
        "response": response.content
    }

builder = StateGraph(AgentState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

app = builder.compile()


result = app.invoke({
    "user_query": "Explain AI agents",
    "response": ""
})


print("Graph result:")
print(result)

assert result["response"] == "This is a mocked AI response."

print("Mock LLM test passed! ✅")