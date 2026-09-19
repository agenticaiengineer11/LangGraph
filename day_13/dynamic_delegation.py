from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_query: str
    tasks: list[str]
    findings: Annotated[list[str], operator.add]
    final_report: str

def task_planner(state: AgentState):
    query = state["user_query"].lower()

    tasks = []

    if "research" in query or "analyze" in query:
        tasks.append("research")

    if "competitor" in query or "competition" in query:
        tasks.append("competitor")

    if "market" in query:
        tasks.append("market")

    print("\n----- TASK PLANNER -----")
    print("Selected tasks:", tasks)

    return {
        "tasks": tasks
    }

def research_agent(state: AgentState):

    if "research" not in state["tasks"]:
        return {}

    print("\n----- RESEARCH AGENT -----")

    research_result = (
        f"Research completed for: {state['user_query']}"
    )

    return {
        "findings": [research_result]
    }

def competitor_agent(state: AgentState):

    if "competitor" not in state["tasks"]:
        return {}

    print("\n----- COMPETITOR AGENT -----")

    competitor_result = (
        f"Competitor analysis completed for: {state['user_query']}"
    )

    return {
        "findings": [competitor_result]
    }

def market_agent(state: AgentState):

    if "market" not in state["tasks"]:
        return {}

    print("\n----- MARKET AGENT -----")

    market_result = (
        f"Market analysis completed for: {state['user_query']}"
    )

    return {
        "findings": [market_result]
    }


def aggregator(state: AgentState):

    print("\n----- AGGREGATOR -----")

    final_report = "\n\n".join(
        state["findings"]
    )

    return {
        "final_report": final_report
    }

builder = StateGraph(AgentState)


# Add nodes

builder.add_node(
    "task_planner",
    task_planner
)

builder.add_node(
    "research_agent",
    research_agent
)

builder.add_node(
    "competitor_agent",
    competitor_agent
)

builder.add_node(
    "market_agent",
    market_agent
)

builder.add_node(
    "aggregator",
    aggregator
)

builder.add_edge(
    START,
    "task_planner"
)

builder.add_edge(
    "task_planner",
    "research_agent"
)

builder.add_edge(
    "task_planner",
    "competitor_agent"
)

builder.add_edge(
    "task_planner",
    "market_agent"
)

builder.add_edge(
    "research_agent",
    "aggregator"
)

builder.add_edge(
    "competitor_agent",
    "aggregator"
)

builder.add_edge(
    "market_agent",
    "aggregator"
)

builder.add_edge(
    "aggregator",
    END
)

app = builder.compile()

initial_state = {
    "user_query": "Analyze the AI agent market and its competitors",
    "tasks": [],
    "findings": [],
    "final_report": ""
}

result = app.invoke(initial_state)

print("\n")
print("============================================")
print("              FINAL REPORT")
print("============================================")

print(result["final_report"])

print("\n")
print("============================================")
print("              SELECTED TASKS")
print("============================================")

print(result["tasks"])