import json
from dotenv import load_dotenv
from livekit import agents
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
