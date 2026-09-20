from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    findings: Annotated[list[str], operator.add]

def research_agent(state: AgentState):
    print("\n----- RESEARCH AGENT -----")

    return {
        "findings": [
            f"Research findings for: {state['user_query']}"
        ]
    }


def competitor_agent(state: AgentState):
    print("\n----- COMPETITOR AGENT -----")

    return {
        "findings": [
            f"Competitor analysis for: {state['user_query']}"
        ]
    }


def market_agent(state: AgentState):
    print("\n----- MARKET AGENT -----")

    return {
        "findings": [
            f"Market analysis for: {state['user_query']}"
        ]
    }

def aggregator(state: AgentState):
    print("\n----- AGGREGATOR -----")

    combined = "\n\n".join(
        state["findings"]
    )

    print("\nCombined findings:")
    print(combined)

    return {}

builder = StateGraph(AgentState)

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
    "research_agent"
)

builder.add_edge(
    START,
    "competitor_agent"
)

builder.add_edge(
    START,
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

result = {"findings": []}

for update in app.stream(
    {
        "user_query": "Analyze the AI agent market",
        "findings": []
    },
    stream_mode="updates"
):
    print(update)

    for node_update in update.values():

        if node_update is None:
            continue

        result["findings"].extend(
            node_update.get("findings", [])
        )
print("\n========================================")
print("             FINAL FINDINGS")
print("========================================")

for finding in result["findings"]:
    print(f"\n- {finding}")