from langgraph.graph import StateGraph, END
from agents.langgraph_agents.nodes import specialist_node
from agents.langgraph_agents.state import ConversationState

def create_support_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("respond", specialist_node)
    workflow.set_entry_point("respond")
    workflow.add_edge("respond", END)
    graph = workflow.compile()
    return graph