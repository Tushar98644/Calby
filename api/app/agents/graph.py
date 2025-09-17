from langgraph.graph import StateGraph, END
from .state import ConversationState
from .nodes import process_message

def create_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("process", process_message)
    workflow.set_entry_point("process")
    workflow.add_edge("process", END)
    return workflow.compile()