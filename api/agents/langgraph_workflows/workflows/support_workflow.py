from langgraph.graph import StateGraph, END
from agents.langgraph_workflows.nodes import decide_transfer_node
from agents.langgraph_workflows.state import ConversationState

def create_support_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("decide_and_respond", decide_transfer_node)
    workflow.set_entry_point("decide_and_respond")
    workflow.add_edge("decide_and_respond", END)
    graph = workflow.compile()
    return graph