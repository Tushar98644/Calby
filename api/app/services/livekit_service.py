from livekit import api
from core import settings

def create_access_token(identity: str, room_name: str) -> str:
    at = api.AccessToken(
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET
    )
    
    at.with_identity(identity).with_name(identity)
    
    video_grant = api.VideoGrants(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True,
    )
    
    at.with_grants(video_grant)
    
    return at.to_jwt()
