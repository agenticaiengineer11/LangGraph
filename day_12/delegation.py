from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    research: str
    competitors: str
    final_answer: str


def research_agent(task: str) -> str:

    print("\n----- RESEARCH AGENT -----")

    result = (
        f"Research completed for the task: {task}"
    )

    return result

def competitor_agent(task: str) -> str:

    print("\n----- COMPETITOR AGENT -----")

    result = (
        f"Competitor analysis completed for the task: {task}"
    )

    return result

@tool
def delegate_research(task: str) -> str:
    """
    Delegate a research task to the specialized research agent.
    """

    return research_agent(task)

@tool
def delegate_competitor_analysis(task: str) -> str:
    """
    Delegate a competitor analysis task to the specialized
    competitor agent.
    """

    return competitor_agent(task)

def main_agent(state: AgentState):

    print("\n----- MAIN AGENT -----")

    research_result = delegate_research.invoke({
        "task": state["user_query"]
    })

    competitor_result = delegate_competitor_analysis.invoke({
        "task": state["user_query"]
    })
    final_answer = (
        "Final analysis:\n\n"
        f"Research:\n{research_result}\n\n"
        f"Competitor Analysis:\n{competitor_result}"
    )

    return {
        "research": research_result,
        "competitors": competitor_result,
        "final_answer": final_answer
    }

builder = StateGraph(AgentState)

builder.add_node(
    "main_agent",
    main_agent
)

builder.add_edge(
    START,
    "main_agent"
)

builder.add_edge(
    "main_agent",
    END
)

app = builder.compile()

result = app.invoke({
    "user_query": "Analyze the AI agent market",
    "research": "",
    "competitors": "",
    "final_answer": ""
})

print("\n========================================")
print("           FINAL ANSWER")
print("========================================")

print(result["final_answer"])