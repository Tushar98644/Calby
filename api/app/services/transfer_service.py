import asyncio
import uuid
from livekit import api
from .livekit_service import livekit_service

class TransferManager:
    def __init__(self):
        self.livekit_api = livekit_service.livekit_api

    async def initiate_transfer(self, customer_room_name: str, customer_identity: str, summary: str):
        print(f"🔥 TRANSFER MANAGER: Initiating warm transfer for '{customer_identity}'")

        consult_room_name = f"consult-{uuid.uuid4().hex[:8]}"
        
        await livekit_service.create_room(
            consult_room_name,
            metadata=f'{{"summary": "{summary}"}}'
        )
        print(f"🔥 TRANSFER MANAGER: Created consult room '{consult_room_name}' with summary.")

        await asyncio.sleep(5) 
        print(f"🔥 TRANSFER MANAGER: Moving customer to consult room...")
        
        try:
            await self.livekit_api.room.move_participant(
                api.MoveParticipantRequest(
                    room=customer_room_name,
                    identity=customer_identity,
                    destination_room=consult_room_name,
                )
            )
            print(f"✅ TRANSFER MANAGER: Customer move successful!")
        except Exception as e:
            print(f"❌ TRANSFER MANAGER: Error moving participant: {e}")
            return {"success": False, "error": str(e)}

        print(f"🔥 TRANSFER MANAGER: Cleaning up original room '{customer_room_name}'...")
        await livekit_service.delete_room(customer_room_name)

        return {"success": True, "new_room": consult_room_name}

transfer_manager = TransferManager()