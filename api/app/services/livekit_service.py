from livekit import api
from core import settings

class LiveKitService:
    def __init__(self):
        self.livekit_api: api.LiveKitAPI | None = None

    async def connect(self):
        """Initializes the LiveKit API client."""
        print("SERVICE: Connecting to LiveKit API...")
        self.livekit_api = api.LiveKitAPI(
            url=settings.LIVEKIT_URL,
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET,
        )

    async def close(self):
        """Closes the connection to the LiveKit API."""
        if self.livekit_api:
            print("SERVICE: Closing LiveKit API connection...")
            await self.livekit_api.close()  # type: ignore

    def create_access_token(self, identity: str, room_name: str) -> str:
        """Creates a new access token for a user."""
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
        
        at = api.AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET,
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
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
        await self.livekit_api.room.create_room(api.CreateRoomRequest(name=name, metadata=metadata))

    async def delete_room(self, name: str):
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
        await self.livekit_api.room.delete_room(api.DeleteRoomRequest(room=name))
        
    async def update_room_metadata(self, room_name: str, metadata: str):
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
              
        await self.livekit_api.room.update_room_metadata(
            api.UpdateRoomMetadataRequest(
                room=room_name,
                metadata=metadata
            )
        )
        
    async def remove_participant(self, room_name: str, identity: str):
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
            
        await self.livekit_api.room.remove_participant(
            api.RoomParticipantIdentity(room=room_name, identity=identity)
        )
    
    async def create_agent_dispatch(self, room_name: str, agent_name: str, metadata: str = ""):
        if not self.livekit_api:
            raise RuntimeError("LiveKitService is not connected.")
    
        await self.livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                room=room_name,
                agent_name=agent_name,
                metadata=metadata
            )
        )
        
livekit_service = LiveKitService()