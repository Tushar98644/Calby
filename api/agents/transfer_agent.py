from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, silero, langchain
from langgraph.workflows.transfer_workflow import create_transfer_workflow

class TransferAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are Agent B, a specialist.")

async def transfer_agent_entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(),
        llm=langchain.LLMAdapter(graph=create_transfer_workflow()),
        tts=cartesia.TTS(voice="a167e0f3-df7e-4d52-a9c3-f949145efdab"),
        vad=silero.VAD.load(),
    )
    await session.start(room=ctx.room, agent=TransferAgent())
    await session.generate_reply(instructions="Greet the customer as a specialist.")
