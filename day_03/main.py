from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    product_name: str
    demand_score: int
    analysis: str
    final_response: str


# -------------------------
# Node 1: Analyze Product
# -------------------------

def product_analyzer(state: State):
    print("Analyzing product demand...")

    return {
        "analysis": (
            f"Analysis for {state['product_name']}: "
            f"Demand Score - {state['demand_score']}"
        )
    }


# -------------------------
# Router: Decide Path
# -------------------------

def demand_router(state: State):
    print("Calculating demand score...")

    if state["demand_score"] >= 80:
        return "excellent"

    elif state["demand_score"] >= 50:
        return "moderate"

    return "poor"

def excellent_analysis(state: State):
    print("Running excellent demand analysis...")

    return {
        "analysis": (
            f"{state['product_name']} has excellent demand. "
            f"Demand score: {state['demand_score']}. "
            "This product has strong e-commerce potential."
        )
    }

def moderate_analysis(state: State):
    print("Running moderate demand analysis...")

    return {
        "analysis": (
            f"{state['product_name']} has moderate demand. "
            f"Demand score: {state['demand_score']}. "
            "Further market research is recommended."
        )
    }

def poor_analysis(state: State):
    print("Running poor demand analysis...")

    return {
        "analysis": (
            f"{state['product_name']} has low demand. "
            f"Demand score: {state['demand_score']}. "
            "This product may require additional validation."
        )
    }

def formatter(state: State):
    print("Formatting response...")

    return {
        "final_response": (
            f"Product: {state['product_name']}\n"
            f"Demand Score: {state['demand_score']}\n\n"
            f"Analysis:\n{state['analysis']}"
        )
    }

graph = StateGraph(State)
graph.add_node("product_analyzer", product_analyzer)
graph.add_node("excellent_analysis", excellent_analysis)
graph.add_node("moderate_analysis", moderate_analysis)
graph.add_node("poor_analysis", poor_analysis)
graph.add_node("formatter", formatter)


# START → Product Analyzer
graph.add_edge(START, "product_analyzer")


# Product Analyzer → Conditional Router
graph.add_conditional_edges(
    "product_analyzer",
    demand_router,
    {
        "excellent": "excellent_analysis",
        "moderate": "moderate_analysis",
        "poor": "poor_analysis"
    }
)


# All analysis paths → Formatter
graph.add_edge("excellent_analysis", "formatter")
graph.add_edge("moderate_analysis", "formatter")
graph.add_edge("poor_analysis", "formatter")


# Formatter → END
graph.add_edge("formatter", END)


# Compile Graph
app = graph.compile()

initial_state = {
    "product_name": "Jewelry Box",
    "demand_score": 85,
    "analysis": "",
    "final_response": ""
}


result = app.invoke(initial_state)


print("\n----- Final Result -----")
print(result["final_response"])