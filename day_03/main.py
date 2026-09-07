from langgraph.graph import StateGraph , START, END
from typing import TypedDict

class State(TypedDict):
    product_name: str
    demand_score: int
    analysis: str
    final_response: str

def product_analyzer(state: State):
    print("Analyzing product demand...")
    return {
        "Product_analyzer": f"Analysis for {state['product_name']}: Demand Score - {state['demand_score']}"
    }
def formatter(state: State):
    print("Formatting response....")
    return{
        "final_response": (
            f"product: {state['product_name']}\n"
            f"Demand Score: {state['demand_score']}\n\n"
            f"Analysis: {state['analysis']}"
        )
    }
def demand_router(state: State):
    print("Calculating demand score....")
    if state["demand_score"] >= 80:
        return "excellent"

    elif state["demand_score"] >= 50:
        return "moderate"

    return "poor"
graph = StateGraph(State)

graph.add_conditional_edges( "analyzer",
    demand_router,
    {
        "excellent": "excellent_analysis",
        "moderate": "moderate_analysis",
        "poor": "poor_analysis"
    })
graph.add_node("Product_analyzer", product_analyzer)
graph.add_node("demand_router", demand_router)
graph.add_node("formatter", formatter)

graph.add_edge(START, "Product_analyzer")
graph.add_edge("Product_analyzer", "demand_router")
graph.add_edge("demand_router", "formatter", condition = "excellent")
graph.add_edge("demand_router", "formatter", condition = "moderate")
graph.add_edge("demand_router", "formatter", condition = "poor")
graph.add_edge("formatter", END)

app = graph.compile()

initial_state = {
    "product_name": "LangGraph",
    "demand_score": 85,
    "analysis": "",
    "final_response": ""
}
result = app(initial_state)
print("Final Result: ", result["final_response"])
