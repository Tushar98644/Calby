from langgraph.graph import StateGraph, END
from agents.langgraph.nodes import specialist_response
from agents.langgraph.state import ConversationState

def create_transfer_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("respond", specialist_response)
    workflow.set_entry_point("respond")
    workflow.add_edge("respond", END)
    return workflow.compile()