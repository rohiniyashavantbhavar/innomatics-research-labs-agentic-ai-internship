from langgraph.graph import StateGraph
from src.utils.helpers import format_docs
from src.routing.router import route_decision
from src.hitl.human_loop import human_intervention

def build_graph(retriever, llm):
    class State(dict): pass

    def process_node(state):
        query = state["query"]
        docs = retriever.get_relevant_documents(query)

        if not docs:
            state["retrieved_docs"] = []
            state["confidence"] = 0.0
            return state

        context = format_docs(docs)
        response = llm.predict(f"Answer using context:\n{context}\n\nQuestion: {query}")

        state["retrieved_docs"] = docs
        state["answer"] = response
        state["confidence"] = 0.8
        return state

    builder = StateGraph(State)
    builder.add_node("process", process_node)
    builder.add_node("hitl", human_intervention)
    builder.set_entry_point("process")

    builder.add_conditional_edges("process", route_decision, {
        "hitl": "hitl",
        "auto": None
    })

    return builder.compile()
