from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState
from core import settings

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=settings.GOOGLE_API_KEY, temperature=0.3)

def generate_summary_node(state: AgentState):
    print("---AGENT NODE: Generating summary---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an expert call summarization assistant. Your goal is to create a concise, "
         "bullet-pointed summary of a conversation between a caller and an agent. "
         "Focus on the key problem, the steps taken, and the final resolution or next steps. "
         "This summary will be read by the next agent in a warm transfer."),
        ("user", "Please summarize the following transcript:\n\n{transcript}")
    ])
    
    summarization_chain = prompt | llm

    response = summarization_chain.invoke({"transcript": state['transcript']})
    summary_text = response.content

    print(f"---AGENT NODE: Summary generated---")
    
    return {"summary": summary_text}
