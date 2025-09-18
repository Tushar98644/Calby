import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from .state import ConversationState

load_dotenv(".env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

def decide_transfer_node(state: ConversationState) -> dict:
    messages = state.get("messages", [])

    if not messages:
        return {}

    one_pass_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a helpful and friendly customer service AI.
                Your primary goal is to resolve user issues. However, you must also identify when to escalate.
                
                Analyze the ENTIRE conversation history provided below.
                
                If a transfer IS required based on the user's request, you MUST generate a concise, one-sentence summary of the **entire conversation's context** for the specialist. Do not just summarize the last message.
                
                Your response MUST start with the exact phrase "[TRANSFER] Summary: [Provide a summary of the whole conversation]." followed by a polite, user-facing transfer message.
                Example: "[TRANSFER] Summary: The user initially reported a billing error, we discussed their last two invoices, and now they are requesting to speak to a manager. I am transferring you to a specialist who can look into your account details."
                
                If a transfer is NOT required, simply continue the conversation naturally and helpfully.
                """
            ),
            *messages,
        ]
    )

    chain = one_pass_prompt | llm 

    llm_response = chain.invoke({"messages": messages})
    response_content = llm_response.content

    new_messages = messages + [llm_response]
    
    needs_transfer = False
    summary = None
    if isinstance(response_content, str) and response_content.strip().startswith("[TRANSFER]"):
        summary_text = response_content.split("Summary:", 1)[1].strip().split("]")[0]
        needs_transfer = True
        summary = summary_text
        print(f"AGENT: Transfer initiated. Full conversation summary: {summary}")
    
    return {
        "messages": new_messages,
        "needs_transfer": needs_transfer,
        "summary": summary
    }

def specialist_node(state: ConversationState) -> dict:
    print("\n--- DEBUG (specialist_node) ---")
    print(f"Node entered. Full state received: {state}")
        
    messages = state.get("messages", [])
    
    if len(messages) <= 1:
        print("Result: Only initial instructions exist. Waiting for summary...")
        print("---------------------------------\n")
        return {}
            
    print("Result: Summary received. Proceeding to call LLM.")
    print("---------------------------------\n")

    specialist_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a specialist customer service representative with advanced training and authority to handle escalated issues.
                You have access to detailed account information and can resolve complex problems including billing issues, refunds, and policy exceptions.
                Be thorough, professional, and solution-oriented in your responses."""
            ),
            *messages,
        ]
    )

    chain = specialist_prompt | llm
    llm_response = chain.invoke({"messages": messages})

    new_messages = messages + [llm_response]

    return {"messages": new_messages}