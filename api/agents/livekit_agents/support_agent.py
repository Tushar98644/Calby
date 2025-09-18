import httpx
import asyncio
import re
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import Agent, AgentSession, ConversationItemAddedEvent
from livekit.agents.llm import ChatMessage
from livekit.plugins import deepgram, cartesia, langchain
from agents.langgraph_agents.workflows.support_workflow import create_support_workflow

import json

load_dotenv(".env")

class SupportAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a support agent. Your goal is to help users with their issues.")

async def support_agent_entrypoint(ctx: agents.JobContext):
    http_client = httpx.AsyncClient()
    specialist_joined_event = asyncio.Event()

    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        print(f"Participant connected: {participant.identity}, metadata: {participant.metadata}")
        try:
            metadata = json.loads(participant.metadata)
            if metadata.get("agent_role") == "specialist":
                print("✅ Specialist Agent has joined the room (identified by metadata).")
                specialist_joined_event.set()
        except (json.JSONDecodeError, TypeError):
            pass

    async def handle_transfer(summary: str):        
        print("✅ Transfer signal detected. Requesting specialist agent...")
        agent_identity = ctx.room.local_participant.identity
        try:
            await http_client.post(
                "http://localhost:8000/api/v1/initiate-warm-transfer",
                json={
                    "customer_room_name": ctx.room.name,
                    "agent_a_identity": agent_identity,
                    "summary": summary,
                },
                timeout=20.0
            )
            print("✅ Backend notified to dispatch specialist.")
        except httpx.RequestError as e:
            print(f"❌ FAILED to send transfer request: {e}")
            ctx.shutdown()
            return
        
        print("⏳ Support Agent is waiting for the specialist to join...")
        try:
            await asyncio.wait_for(specialist_joined_event.wait(), timeout=25.0)
        except asyncio.TimeoutError:
            print("⚠️ Timed out waiting for specialist agent. Shutting down.")
            ctx.shutdown()
            return
            
        announcement = "Okay, I see the specialist has just joined the call. I will now brief them on our conversation."
        print(f"🗣️ Support Agent announcing: '{announcement}'")
        await session.say(text=announcement, allow_interruptions=False)
        
        summary_utterance = f"The summary is: {summary}"
        print(f"🗣️ Support Agent speaking summary: '{summary_utterance}'")
        await session.say(text=summary_utterance, allow_interruptions=False)
        
        await ctx.room.local_participant.publish_data(
            json.dumps({"type": "handoff_complete"}).encode('utf-8'),
        )
            
        print("👋 Summary delivered. Support Agent shutting down.")
        ctx.shutdown()

    graph = create_support_workflow()
    
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en-US"),
        llm=langchain.LLMAdapter(graph=graph),
        tts=cartesia.TTS(model="sonic-2"),
    )

    @session.on("conversation_item_added")
    def on_conversation_item_added(event: ConversationItemAddedEvent):
        if not isinstance(event.item, ChatMessage) or event.item.role != 'assistant':
            return
        
        content = event.item.text_content or ""
        if content.strip().startswith("[TRANSFER]"):
            match = re.search(r"Summary:\s*([^\]]+)", content, re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                asyncio.create_task(handle_transfer(summary))

    await session.start(room=ctx.room, agent=SupportAgent())
    
    await session.say(
        "Hello! Thank you for calling. How can I help you today?",
        allow_interruptions=False,
        add_to_chat_ctx=False
    )