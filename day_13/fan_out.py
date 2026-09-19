from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_query: str
    research: str
    competitors: str
    market: str


def research_agent(state: AgentState):
    print("\n----- RESEARCH AGENT -----")

    return {
        "research": (
            f"Research findings for: "
            f"{state['user_query']}"
        )
    }


def competitor_agent(state: AgentState):
    print("\n----- COMPETITOR AGENT -----")

    return {
        "competitors": (
            f"Competitor analysis for: "
            f"{state['user_query']}"
        )
    }


def market_agent(state: AgentState):
    print("\n----- MARKET AGENT -----")

    return {
        "market": (
            f"Market analysis for: "
            f"{state['user_query']}"
        )
    }


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


# FAN-OUT
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
    END
)

builder.add_edge(
    "competitor_agent",
    END
)

builder.add_edge(
    "market_agent",
    END
)


app = builder.compile()


result = app.invoke({
    "user_query": "Analyze the AI agent market",
    "research": "",
    "competitors": "",
    "market": ""
})


print("\n========== FINAL STATE ==========")

print("\nResearch:")
print(result["research"])

print("\nCompetitors:")
print(result["competitors"])

print("\nMarket:")
print(result["market"])