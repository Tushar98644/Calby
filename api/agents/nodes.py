
from .state import ConversationState
from app.core import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro", 
    google_api_key=settings.GOOGLE_API_KEY, 
    temperature=0.3
)

def decide_transfer(state: ConversationState, **context) -> ConversationState:    
    messages = context.get("messages", [])
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are a helpful customer service agent. Your job is to analyze the conversation and decide if it needs to be transferred to a specialist.
        
        Transfer criteria:
        - Customer explicitly asks for a 'manager', 'supervisor', or to 'escalate'.
        - Customer is angry, frustrated, or has a complex technical issue.
        - The issue involves billing, refunds, or legal matters.
        
        Respond with ONLY ONE of the following:
        - 'TRANSFER: [Reason for transfer]' if it needs to be escalated.
        - 'CONTINUE' if you can handle it.
        """),
        *messages
    ])
    
    llm_decision = llm.invoke(prompt).content
    
    if "TRANSFER" in llm_decision:
        state["needs_transfer"] = True
        state["summary"] = llm_decision.replace("TRANSFER:", "").strip()
        state["response"] = "I understand. Let me connect you with a specialist who can handle this for you."
    else:
        state["needs_transfer"] = False
        response_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful and friendly customer service agent. Continue the conversation naturally."),
            *messages
        ])
        state["response"] = llm.invoke(response_prompt).content
        
    return state