from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_query: str
    research: str
    analysis: str
    report: str


def research_agent(state: AgentState):
    print("\n----- RESEARCH AGENT -----")

    research = (
        f"Research findings for: "
        f"{state['user_query']}"
    )

    return {
        "research": research
    }


def analysis_agent(state: AgentState):
    print("\n----- ANALYSIS AGENT -----")

    analysis = (
        f"Analysis based on research: "
        f"{state['research']}"
    )

    return {
        "analysis": analysis
    }


def report_agent(state: AgentState):
    print("\n----- REPORT AGENT -----")

    report = (
        f"Final report:\n"
        f"{state['analysis']}"
    )

    return {
        "report": report
    }


builder = StateGraph(AgentState)

builder.add_node(
    "research_agent",
    research_agent
)

builder.add_node(
    "analysis_agent",
    analysis_agent
)

builder.add_node(
    "report_agent",
    report_agent
)


builder.add_edge(
    START,
    "research_agent"
)

builder.add_edge(
    "research_agent",
    "analysis_agent"
)

builder.add_edge(
    "analysis_agent",
    "report_agent"
)

builder.add_edge(
    "report_agent",
    END
)


app = builder.compile()


result = app.invoke({
    "user_query": "Analyze the AI agent market",
    "research": "",
    "analysis": "",
    "report": ""
})


print("\n========== FINAL STATE ==========")

print("User Query:")
print(result["user_query"])

print("\nResearch:")
print(result["research"])

print("\nAnalysis:")
print(result["analysis"])

print("\nReport:")
print(result["report"])