from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

def message_analyzer(state: MessagesState):

    messages = state["messages"]
    last_message = messages[-1]

    print("Analyzing message...")

    return {
        "messages": [
            AIMessage(
                content=f"I analyzed your message: {last_message.content}"
            )
        ]
    }

def response_generator(state: MessagesState):

    messages = state["messages"]
    last_message = messages[-1]

    print("Generating response...")

    return {
        "messages": [
            AIMessage(
                content=f"Final response based on: {last_message.content}"
            )
        ]
    }


builder = StateGraph(MessagesState)

builder.add_node("message_analyzer", message_analyzer)
builder.add_node("response_generator", response_generator)

builder.add_edge(START, "message_analyzer")
builder.add_edge("message_analyzer", "response_generator")
builder.add_edge("response_generator", END)

graph = builder.compile()

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="I want to learn LangGraph"
            )
        ]
    }
)

print("\n----- Message History -----")

for message in result["messages"]:
    print(f"{message.__class__.__name__}: {message.content}")
