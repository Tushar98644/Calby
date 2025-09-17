import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, AIMessage, BaseMessage

from .state import ConversationState

load_dotenv(".env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

def decide_transfer_node(state: ConversationState) -> dict:
    messages: list[BaseMessage] = state.get("messages", [])

    if not messages:
        initial_greeting = AIMessage(
            content="Hello! Welcome. How can I assist you today?"
        )
        return {"messages": [initial_greeting]}

    one_pass_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a helpful and friendly customer service AI.
Your primary goal is to resolve user issues. However, you must also identify when to escalate.

Analyze the user's latest message based on the following transfer criteria:
- The user explicitly asks for a 'manager', 'supervisor', or to 'escalate'.
- The user is expressing extreme anger or frustration.
- The issue involves sensitive topics like billing, refunds, or legal matters.

If a transfer IS required, you MUST start your response with the exact phrase "[TRANSFER] Summary: [Provide a one-sentence summary for the specialist]." and then a polite transfer message.
Example: "[TRANSFER] Summary: User is frustrated with a billing error. I am transferring you to a specialist who can look into your account details."

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

    if response_content.strip().startswith("[TRANSFER]"):
        summary = response_content.split("Summary:", 1)[1].strip().split("\n")[0]
        llm_response.additional_kwargs = {"needs_transfer": True, "summary": summary}
        print(f"AGENT: Transfer initiated. Summary: {summary}")
    else:
        llm_response.additional_kwargs = {"needs_transfer": False}

    return {"messages": new_messages}


def specialist_node(state: ConversationState) -> dict:
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None

    summary_brief = last_message.additional_kwargs.get("summary", "your request")

    greeting_content = f"Hello, I'm a specialist. I've been briefed that you need help with: '{summary_brief}'. How can I best assist you?"

    specialist_greeting = AIMessage(content=greeting_content)

    return {"messages": messages + [specialist_greeting]}
