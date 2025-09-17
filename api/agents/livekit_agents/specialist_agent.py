from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, silero, langchain

from langgraph_agents.workflows import create_chat_workflow

class SpecialistAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are Agent B, a specialist. Your first message will be a summary from another agent. Acknowledge it and then greet the customer.")

async def specialist_agent_entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(),
        llm=langchain.LLMAdapter(graph=create_chat_workflow()),
        tts=cartesia.TTS(voice="a167e0f3-df7e-4d52-a9c3-f949145efdab"),
        vad=silero.VAD.load(),
    )
    
    print("🎧 SpecialistAgent (Agent B) is online and listening for summary...")
    
    await session.start(room=ctx.room, agent=SpecialistAgent())
