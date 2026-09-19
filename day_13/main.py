from typing import TypedDict


class AgentState(TypedDict):
    user_query: str
    research: str
    competitors: str
    market: str
def research_agent(state: AgentState):
    print("\n -----research agent----------")
    return{
        "research": (
            f"Findings research for: "
            f"{state['user_query']}"
        )
    }

def competitor_agent(state:AgentState):
    print("\n -----competitor agent---------")

    return {
        "competitors": (
            f"Competitor analysis for: "
            f"{state['user_query']}"
        )
    }
def market_agent(state: AgentState):
    print("\n -------Market agent---------")

    return{
        "market": (
            f"market analysis for: "
            f"{state['user_query']}"
        )
    }

