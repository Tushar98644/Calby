import json

from .livekit_service import livekit_service

class TransferManager:
    def __init__(self):
        self.livekit_service = livekit_service

    async def initiate_transfer(self, customer_room_name: str, agent_a_identity: str, summary: str):
        print(f"🔥 TRANSFER MANAGER: Initiating in-room handoff in '{customer_room_name}'")

        summary_metadata = json.dumps({"summary": summary})

        try:
            print("🚀 Dispatching 'specialist-agent'...")
            await self.livekit_service.create_agent_dispatch(
                room_name=customer_room_name,
                agent_name="specialist-agent",
                metadata=summary_metadata
            )
            
            print(f"✅ Specialist agent dispatched to room '{customer_room_name}'.")
        except Exception as e:
            print(f"❌ Error dispatching agents: {e}")
            return {"success": False, "error": str(e)}

        return {"success": True, "room": customer_room_name}

transfer_manager = TransferManager()