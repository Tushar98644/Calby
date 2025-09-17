from langgraph.graph import StateGraph, END
from agents.langgraph.nodes import decide_transfer
from agents.langgraph.state import ConversationState

def create_support_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("decide_and_respond", decide_transfer)
    workflow.set_entry_point("decide_and_respond")
    workflow.add_edge("decide_and_respond", END)
    return workflow.compile()