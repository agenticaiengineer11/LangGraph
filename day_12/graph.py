from typing import TypedDict, Literal
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

class AgentState(TypedDict):
    user_query: str
    research: str
    analysis: str
    report: str
    next_agent: str

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

class SupervisorDecision(TypedDict):
    next_agent: Literal[
        "research_agent",
        "analysis_agent",
        "report_agent",
        "FINISH"
    ]

structured_model = model.with_structured_output(
    SupervisorDecision
)

def research_agent(state: AgentState):

    print("\n----- RESEARCH AGENT -----")

    research = (
        f"Research completed for: "
        f"{state['user_query']}"
    )

    return {
        "research": research
    }

def analysis_agent(state: AgentState):

    print("\n----- ANALYSIS AGENT -----")

    analysis = (
        f"Analysis based on: "
        f"{state['research']}"
    )

    return {
        "analysis": analysis
    }
def report_agent(state: AgentState):

    print("\n----- REPORT AGENT -----")

    report = (
        f"Final Report: "
        f"{state['analysis']}"
    )

    return {
        "report": report
    }

def supervisor(state: AgentState):

    print("\n----- LLM SUPERVISOR -----")

    prompt = f"""
You are the supervisor of a multi-agent system.

Your job is to decide which agent should work next.

Available agents:

research_agent:
Performs research.

analysis_agent:
Analyzes the research.

report_agent:
Creates the final report.

FINISH:
Use this when the final report is complete.

User request:
{state["user_query"]}

Current research:
{state["research"]}

Current analysis:
{state["analysis"]}

Current report:
{state["report"]}

Choose exactly one next agent.
"""

    decision = structured_model.invoke(prompt)

    next_agent = decision["next_agent"]

    print(
        f"Supervisor decision: {next_agent}"
    )

    return {
        "next_agent": next_agent
    }

def supervisor_router(state: AgentState):

    return state["next_agent"]

builder = StateGraph(AgentState)


builder.add_node(
    "supervisor",
    supervisor
)

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
    "supervisor"
)

builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "research_agent": "research_agent",
        "analysis_agent": "analysis_agent",
        "report_agent": "report_agent",
        "FINISH": END
    }
)

builder.add_edge(
    "research_agent",
    "supervisor"
)

builder.add_edge(
    "analysis_agent",
    "supervisor"
)

builder.add_edge(
    "report_agent",
    "supervisor"
)

app = builder.compile()

result = app.invoke(
    {
        "user_query": "Analyze LangGraph",
        "research": "",
        "analysis": "",
        "report": "",
        "next_agent": ""
    }
)

print("\n========== FINAL STATE ==========")

print(result)