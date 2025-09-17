from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/get-livekit-token')
def get_livekit_token(room_name: str, identity: str):
    try:
        token = 123
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")