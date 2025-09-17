from fastapi import APIRouter, HTTPException
from app.services import livekit_service

router = APIRouter()

@router.get('/get-livekit-token')
def get_livekit_token(room_name: str, identity: str):
    try:
        token = livekit_service.create_access_token(identity=identity, room_name=room_name)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")