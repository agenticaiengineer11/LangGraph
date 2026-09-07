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
        "analysis": f"Analysis for {state['product_name']}: Demand Score - {state['demand_score']}"
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
def demand_route(state: State):
    print("Calculating demand score....")
    if state['demand_score'] >= 80:
        return{
            "analysis": f"The product {state['product_name']} has a high demand score of {state['demand_score']}"
        }
    elif state['demand_score'] >= 50:
        return{
            "analysis": f"The product {state['product_name']} has a moderate demand score of {state['demand_score']}"

        }
    else:
        return{
            "analysis": f"The product {state['product_name']} has a low demand score of {state['demand_score']}"
        }
