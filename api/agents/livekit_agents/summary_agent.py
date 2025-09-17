import asyncio
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import cartesia

class SummaryAgent(Agent):
    def __init__(self, summary: str):
        super().__init__()
        self._summary = summary

async def summary_agent_entrypoint(ctx: agents.JobContext):
    summary_text = ctx.room.metadata.get("summary", "No summary was provided.")
    
    session = AgentSession(
        tts=cartesia.TTS(),
    )

    await session.start(room=ctx.room, agent=SummaryAgent(summary_text))
    
    print(f"📢 SummaryAgent speaking: '{summary_text}'")
    
    await session.say(text=summary_text, wait_for_speech=False)
    
    await asyncio.sleep(5.0)
    print("✅ SummaryAgent finished speaking, disconnecting.")
    await ctx.disconnect()
