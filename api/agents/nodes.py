
from .state import ConversationState

def decide_transfer(state: ConversationState, **context) -> ConversationState:    
    messages = context.get("messages", [])
    
    if not messages:
        state["needs_transfer"] = False
        state["response"] = "Hello! How can I help you today?"
        return state
    
    latest_message = messages[-1].content if messages else ""
    
    transfer_keywords = ["manager", "supervisor", "specialist", "escalate", "transfer"]
    needs_transfer = any(keyword in latest_message.lower() for keyword in transfer_keywords)
    
    state["needs_transfer"] = needs_transfer
    
    if needs_transfer:
        state["summary"] = f"Customer requested: {latest_message}"
        state["response"] = "I understand you need specialized help. Let me connect you with our specialist."
    else:
        state["response"] = "I'm here to help! What can I assist you with?"
    
    return state

def specialist_response(state: ConversationState, **context) -> ConversationState:
    state["needs_transfer"] = False
    state["response"] = "Hello! I'm a specialist and I'm here to help with your escalated request. What specific issue can I assist you with?"
    return state