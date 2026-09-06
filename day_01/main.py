from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    analysis: str
    answer: str
    final_response: str


def question_analyzer(state: State):
    print("Analyzing question...")

    return {
        "analysis": f"The user asked: {state['question']}"
    }


def answer_generator(state: State):
    print("Generating answer...")

    return {
        "answer": (
            f"LangGraph is a framework for building "
            f"stateful AI workflows and agents. "
            f"Analysis: {state['analysis']}"
        )
    }


def formatter(state: State):
    print("Formatting response...")

    return {
        "final_response": (
            f"Question: {state['question']}\n\n"
            f"Answer: {state['answer']}"
        )
    }


graph = StateGraph(State)

graph.add_node("question_analyzer", question_analyzer)
graph.add_node("answer_generator", answer_generator)
graph.add_node("formatter", formatter)

graph.add_edge(START, "question_analyzer")
graph.add_edge("question_analyzer", "answer_generator")
graph.add_edge("answer_generator", "formatter")
graph.add_edge("formatter", END)

app = graph.compile()


initial_state = {
    "question": "What is LangGraph?",
    "analysis": "",
    "answer": "",
    "final_response": ""
}

result = app.invoke(initial_state)

print("\n--- FINAL RESULT ---")
print(result["final_response"])