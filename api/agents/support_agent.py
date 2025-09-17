from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, silero, langchain
from langgraph.workflows.support_workflow import create_support_workflow

class SupportAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are Agent A, a friendly customer support agent.")

async def support_agent_entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(),
        llm=langchain.LLMAdapter(graph=create_support_workflow()),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
    )
    await session.start(room=ctx.room, agent=SupportAgent())
    await session.generate_reply(instructions="Greet the user warmly and offer your assistance.")
