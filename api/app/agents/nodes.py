from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .state import ConversationState
from core import settings

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=settings.GOOGLE_API_KEY, temperature=0.3)

def process_message(state: ConversationState) -> ConversationState:
    """Check if customer wants transfer"""
    latest_message = state["messages"][-1] if state["messages"] else ""
    
    # Simple check for transfer keywords
    transfer_words = ["manager", "supervisor", "transfer", "escalate"]
    state["needs_transfer"] = any(word in latest_message.lower() for word in transfer_words)
    
    return state
