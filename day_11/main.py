from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str
    result: str

def analyzer(state: State):
    print("\n------Analyzer running-----")

    return {
        "result": f"Analyzed: {state['input']}"
    }

def processor(state: State):
    print("\n----- Processor running----")

    return {
        "result": f"Processed: {state['result']}"
    }

subgraph_builder = StateGraph(State)

subgraph_builder.add_node("analyzer", analyzer)
subgraph_builder.add_node("processor", processor)

subgraph_builder.add_edge(START , "analyzer")

subgraph_builder.add_edge("analyzer", "processor")

subgraph_builder.add_edge("processor", END)

subgraph = subgraph_builder.compile()

result = subgraph.invoke(
    {
        "input" : "Langgraph",
        "result" : " "    

    }
)
print("\n =========Final Result=========")
print(result)

