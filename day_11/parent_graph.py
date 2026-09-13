from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    user_query: str
    analysis: str
    final_report: str

def researcher(state: State):

    print("Researcher running...")

    return {
        "analysis": (
            f"Research completed for: "
            f"{state['user_query']}"
        )
    }


def analyzer(state: State):

    print("Analyzer running...")

    return {
        "analysis": (
            f"{state['analysis']} "
            f"| Analysis completed."
        )
    }

subgraph_builder = StateGraph(State)

subgraph_builder.add_node(
    "researcher",
    researcher
)

subgraph_builder.add_node(
    "analyzer",
    analyzer
)

subgraph_builder.add_edge(
    START,
    "researcher"
)

subgraph_builder.add_edge(
    "researcher",
    "analyzer"
)

subgraph_builder.add_edge(
    "analyzer",
    END
)

subgraph = subgraph_builder.compile()

def final_report(state: State):

    print("Final report running...")

    return {
        "final_report": (
            f"Final Report: "
            f"{state['analysis']}"
        )
    }

parent_builder = StateGraph(State)

parent_builder.add_node(
    "research",
    subgraph
)

parent_builder.add_node(
    "final_report",
    final_report
)

parent_builder.add_edge(
    START,
    "research"
)

parent_builder.add_edge(
    "research",
    "final_report"
)

parent_builder.add_edge(
    "final_report",
    END
)

app = parent_builder.compile()

result = app.invoke(
    {
        "user_query": "Analyze LangGraph",
        "analysis": "",
        "final_report": ""
    }
)

print("\n========== FINAL STATE ==========")

print(result)