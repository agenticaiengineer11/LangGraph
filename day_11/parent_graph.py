from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class ParentState(TypedDict):
    user_query: str
    final_report: str

class ResearchState(TypedDict):
    query: str
    sources: str
    findings: str

def search_node(state: ResearchState):

    print("\n----- SEARCH NODE -----")

    query = state["query"]

    sources = f"Sources found for: {query}"

    print(sources)

    return {
        "sources": sources
    }

def analysis_node(state: ResearchState):

    print("\n----- ANALYSIS NODE -----")

    sources = state["sources"]

    findings = f"Analysis based on: {sources}"

    print(findings)

    return {
        "findings": findings
    }

research_builder = StateGraph(ResearchState)


research_builder.add_node(
    "search",
    search_node
)


research_builder.add_node(
    "analysis",
    analysis_node
)

research_builder.add_edge(
    START,
    "search"
)


research_builder.add_edge(
    "search",
    "analysis"
)


research_builder.add_edge(
    "analysis",
    END
)

research_subgraph = research_builder.compile()

def research_node(state: ParentState):

    print("\n===== RESEARCH SUBGRAPH =====")

    # Parent state → Subgraph state

    research_input = {
        "query": state["user_query"],
        "sources": "",
        "findings": ""
    }

    research_result = research_subgraph.invoke(
        research_input
    )

    return {
        "final_report": research_result["findings"]
    }

def final_report_node(state: ParentState):

    print("\n----- FINAL REPORT NODE -----")

    final_report = (
        f"Final Report: "
        f"{state['final_report']}"
    )

    print(final_report)

    return {
        "final_report": final_report
    }

parent_builder = StateGraph(ParentState)


parent_builder.add_node(
    "research",
    research_node
)


parent_builder.add_node(
    "final_report",
    final_report_node
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
        "final_report": ""
    }
)

print("\n========== FINAL STATE ==========")

print(result)