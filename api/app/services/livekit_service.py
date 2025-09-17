from livekit import api
from core import settings

class LiveKitService:
    def __init__(self):
        self.livekit_api = api.LiveKitAPI(
            host=settings.LIVEKIT_HOST,
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET,
        )

    def create_access_token(self, identity: str, room_name: str) -> str:
        print(f"SERVICE: Generating token for '{identity}' in room '{room_name}'...")
        
        at = api.AccessToken(
            self.livekit_api.api_key,
            self.livekit_api.api_secret,
        )
        
        video_grant = api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True, 
        )
        
        at.with_identity(identity).with_name(identity).with_grants(video_grant)
        
        return at.to_jwt()

    async def create_room(self, name: str, metadata: str = ""):
        print(f"SERVICE: Creating room '{name}'...")
        await self.livekit_api.room.create_room(api.CreateRoomRequest(name=name, metadata=metadata))
        print(f"SERVICE: Room '{name}' created.")

    async def delete_room(self, name: str):
        print(f"SERVICE: Deleting room '{name}'...")
        await self.livekit_api.room.delete_room(api.DeleteRoomRequest(room=name))
        print(f"SERVICE: Room '{name}' deleted.")

    async def close(self):
        await self.livekit_api.close()

livekit_service = LiveKitService()

