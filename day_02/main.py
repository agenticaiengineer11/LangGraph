from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    product_name: str
    product_category: str
    analysis: str
    recommendation: str
    final_response: str


def product_extractor(state: State):
    return {
        "product_name": state["product_name"],
        "product_category": state["product_category"],
    }


def product_analyzer(state: State):
    return {
        "analysis": (
            f"Product: {state['product_name']}\n"
            f"Category: {state['product_category']}\n"
            "This product can be evaluated for e-commerce potential."
        )
    }


def recommendation_generator(state: State):
    return {
        "recommendation": (
            f"Consider researching the market demand for "
            f"{state['product_name']}."
        )
    }


def formatter(state: State):
    return {
        "final_response": (
            f"Product: {state['product_name']}\n"
            f"Category: {state['product_category']}\n\n"
            f"Analysis:\n{state['analysis']}\n\n"
            f"Recommendation:\n{state['recommendation']}"
        )
    }


graph = StateGraph(State)

graph.add_node("product_extractor", product_extractor)
graph.add_node("product_analyzer", product_analyzer)
graph.add_node("recommendation_generator", recommendation_generator)
graph.add_node("formatter", formatter)

graph.add_edge(START, "product_extractor")
graph.add_edge("product_extractor", "product_analyzer")
graph.add_edge("product_analyzer", "recommendation_generator")
graph.add_edge("recommendation_generator", "formatter")
graph.add_edge("formatter", END)

app = graph.compile()


initial_state = {
    "product_name": "jewelry box",
    "product_category": "",
    "analysis": "",
    "recommendation": "",
    "final_response": ""
}

print("\n---- Final Result -----")
for event in app.stream(initial_state):
    print(event)


