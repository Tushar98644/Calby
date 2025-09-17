from livekit import models, api
from app.core.config import settings

token_service = api.AccessToken(
    api_key=settings.LIVEKIT_API_KEY,
    api_secret=settings.LIVEKIT_API_SECRET,
)

def create_access_token(identity: str, room_name: str) -> str:
    video_grant = models.VideoGrant(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True,
    )

    token = token_service.create(
        identity=identity,
        grants=[video_grant],
        name=identity  
    )
    
    return token