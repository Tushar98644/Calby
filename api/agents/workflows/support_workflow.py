from langgraph.graph import StateGraph, END
from agents.nodes import decide_transfer
from agents.state import ConversationState
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro", 
    google_api_key=settings.GOOGLE_API_KEY, 
    temperature=0.3
)

def create_support_workflow():
    workflow = StateGraph(ConversationState)
    workflow.add_node("decide", decide_transfer)
    workflow.set_entry_point("decide")
    workflow.add_edge("decide", END)
    return workflow.compile()
