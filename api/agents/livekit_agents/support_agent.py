import httpx
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, silero, langchain
from langchain_core.messages import AIMessage

from langgraph_agents.workflows import create_support_workflow

class SupportAgent(Agent):
    def __init__(self):
        super().__init__()

async def support_agent_entrypoint(ctx: agents.JobContext):
    http_client = httpx.AsyncClient()

    session = AgentSession(
        stt=deepgram.STT(),
        llm=langchain.LLMAdapter(graph=create_support_workflow()),
        tts=cartesia.TTS(),
        vad=silero.VAD.load(),
    )

    async def _on_ai_message_generated(message: AIMessage):
        if message.additional_kwargs.get("needs_transfer"):
            print("✅ Transfer signal detected in AI message!")

            summary = message.additional_kwargs.get("summary", "No summary was provided.")

            print("🤫 Placing customer on hold...")
            for participant in ctx.room.participants.values():
                if participant.identity != ctx.participant.identity:
                    for track_pub in participant.tracks.values():
                        track_pub.set_subscribed(False)
                    customer_identity = participant.identity
                    break
            else:
                print("❌ ERROR: Could not find a customer in the room to transfer.")
                return

            print(f"🚀 Preparing to call FastAPI to orchestrate warm transfer for '{customer_identity}'...")

            transfer_data = {
                "customer_room_name": ctx.room.name,
                "customer_identity": customer_identity,
                "summary": summary,
            }

            try:
                response = await http_client.post(
                    "http://localhost:8000/initiate-warm-transfer",
                    json=transfer_data,
                    timeout=20.0
                )
                response.raise_for_status()
                print(f"✅ Successfully notified FastAPI to start transfer. Status: {response.status_code}")
            except httpx.RequestError as e:
                print(f"❌ FAILED to send transfer request to FastAPI: {e}")

    session.on("ai_message", _on_ai_message_generated)

    await session.start(room=ctx.room, agent=SupportAgent())
