from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import generate_summary_node

workflow = StateGraph(AgentState)

workflow.add_node("generate_summary", generate_summary_node)

workflow.set_entry_point("generate_summary")
workflow.add_edge("generate_summary", END)

summarizer_app = workflow.compile()