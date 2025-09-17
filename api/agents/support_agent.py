from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, langchain
from agents.langgraph_agents.workflows import create_support_workflow

class SupportAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are Agent A, a friendly customer support agent.")

async def support_agent_entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=langchain.LLMAdapter(graph=create_support_workflow()),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
    )

    await session.start(room=ctx.room, agent=SupportAgent())
    await session.generate_reply(instructions="Greet the user warmly and offer your assistance.")
