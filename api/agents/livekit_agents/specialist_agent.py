import json
import asyncio
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentSession
from livekit.plugins import deepgram, cartesia, langchain
from agents.langgraph_agents.workflows.chat_workflow import create_chat_workflow

load_dotenv(".env")

class SpecialistAgent(Agent):
    def __init__(self):
        super().__init__(instructions="""You are a specialist taking over a call. The first thing you hear will be a summary from another agent.
                    Your first response to the customer MUST start by greeting them, then repeat the summary you heard and ask for confirmation.
                    For example, if you hear 'The user has a billing issue', your response should be: 'Hello, I understand you have a billing issue, is that correct?'"""
        )

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
                
    summary_text = "I'm a specialist who can help with your issue."
    if ctx.job.metadata:
        try:
            metadata = json.loads(ctx.job.metadata)
            summary_info = metadata.get('summary', 'you needed assistance')
            summary_text = f"I understand the issue is that {summary_info}, is that correct?"
        except (json.JSONDecodeError, TypeError):
            print(f"Could not parse summary from job metadata: {ctx.job.metadata}")

    graph = create_chat_workflow()
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en-US"),
        llm=langchain.LLMAdapter(graph=graph),
        tts=cartesia.TTS(voice="a167e0f3-df7e-4d52-a9c3-f949145efdab"),
    )
    
    await session.start(room=ctx.room, agent=SpecialistAgent())
   
    print("⏳ Specialist waiting for handoff completion...")
    try:
        await asyncio.wait_for(handoff_complete_event.wait(), timeout=30.0)
        await session.say(summary_text, allow_interruptions=False)
    except asyncio.TimeoutError:
           print("⚠️ Timed out waiting for handoff completion")
           
    await session.say(summary_text, allow_interruptions=False)
