from langchain_google_genai import ChatGoogleGenerativeAI
from .state import AgentState
from core import settings

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY)

def generate_summary_node(state: AgentState):
    print("Generating summary...")
    prompt = f"""
    You are an expert in summarizing conversations. Based on the following call transcript,
    please provide a concise summary for a warm transfer. The summary should capture the
    caller's issue, any steps already taken, and the key outcome needed.

    Transcript:
    "{state['transcript']}"

    Summary:
    """

    response = llm.invoke(prompt)
    summary_text = response.content

    print(f"---SUMMARY: {summary_text}---")
    
    return {"summary": summary_text}
