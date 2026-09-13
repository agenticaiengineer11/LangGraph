from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str
    result: str

def analyzer(state: State):
    print("Analyzer running...")

    return {
        "result": f"Analyzed: {state['input']}"
    }


def processor(state: State):
    print("Processor running...")

    return {
        "result": f"Processed: {state['result']}"
    }

subgraph_builder = StateGraph(State)

subgraph_builder.add_node(
    "analyzer",
    analyzer
)

subgraph_builder.add_node(
    "processor",
    processor
)

subgraph_builder.add_edge(
    START,
    "analyzer"
)

subgraph_builder.add_edge(
    "analyzer",
    "processor"
)

subgraph_builder.add_edge(
    "processor",
    END
)

subgraph = subgraph_builder.compile()

def request_node(state: State):

    print("Request node running...")

    return {
        "input": state["input"]
    }


def final_response(state: State):

    print("Final response node running...")

    return {
        "result": f"Final result: {state['result']}"
    }
parent_builder = StateGraph(State)


parent_builder.add_node(
    "request",
    request_node
)

parent_builder.add_node(
    "processing",
    subgraph
)


parent_builder.add_node(
    "final_response",
    final_response
)

parent_builder.add_edge(
    START,
    "request"
)

parent_builder.add_edge(
    "request",
    "processing"
)

parent_builder.add_edge(
    "processing",
    "final_response"
)

parent_builder.add_edge(
    "final_response",
    END
)


parent_app = parent_builder.compile()

result = parent_app.invoke(
    {
        "input": "LangGraph",
        "result": ""
    }
)

print("\n========== FINAL RESULT ==========")

print(result)