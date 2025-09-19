import json
import asyncio
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram, cartesia, langchain
from agents.langgraph_workflows.workflows.chat_workflow import create_chat_workflow

load_dotenv(".env")

class SpecialistAgent(Agent):
    def __init__(self, summary_context: str = ""):
        instructions = f"""You are a specialist taking over a call. 
        
        CONTEXT: The previous agent handled: {summary_context}
        
        Your first response should be a natural greeting like "Hello, I'm here to help you today. I have recieved context on your previous conversation. What can I assist you with?"
        
        Use the context to provide informed responses, but don't repeat the summary unless the customer asks for clarification."""
        
        super().__init__(instructions=instructions)

async def specialist_agent_entrypoint(ctx: agents.JobContext):
    handoff_complete_event = asyncio.Event()
    
    @ctx.room.on("data_received")
    def on_data_received(data: rtc.DataPacket):
        try:
            message = json.loads(data.data.decode('utf-8'))
            if message.get("type") == "handoff_complete":
                print("✅ Received handoff completion signal")
                handoff_complete_event.set()
        except (json.JSONDecodeError, KeyError):
            pass
    
    summary_info = "general assistance"
    if ctx.job.metadata:
        try:
            metadata = json.loads(ctx.job.metadata)
            summary_info = metadata.get('summary', 'general assistance')
        except (json.JSONDecodeError, TypeError):
            print(f"Could not parse summary from job meta {ctx.job.metadata}")

    graph = create_chat_workflow()
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en-US"),
        llm=langchain.LLMAdapter(graph=graph),
        tts=cartesia.TTS(voice="a167e0f3-df7e-4d52-a9c3-f949145efdab"),
    )
    
    await session.start(room=ctx.room, agent=SpecialistAgent(summary_context=summary_info))
    
    print("⏳ Specialist waiting for handoff completion...")
    try:
        await asyncio.wait_for(handoff_complete_event.wait(), timeout=30.0)
        await session.say("Hello, I'm here to help you today. I have recieved context on your previous conversation. What can I assist you with?", allow_interruptions=False)
    except asyncio.TimeoutError:
        print("⚠️ Timed out waiting for handoff completion")
        await session.say("Hello, I'm here to help you today. What can I assist you with?", allow_interruptions=False)
