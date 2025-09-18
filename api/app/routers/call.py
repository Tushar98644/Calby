import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel

from services.transfer_service import transfer_manager
from services.livekit_service import livekit_service

class TransferRequest(BaseModel):
    customer_room_name: str
    agent_a_identity: str  
    summary: str

router = APIRouter()

@router.get("/get-livekit-token")
def get_livekit_token(
    room_name: str = Query(..., description="The room the user wants to join"),
    identity: str = Query(..., description="The unique identity of the user")
):
    try:
        token = livekit_service.create_access_token(identity=identity, room_name=room_name)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")

@router.post("/start-call")
async def start_call():
    room_name = f"customer-room-{uuid.uuid4().hex[:8]}"
    await livekit_service.create_room(room_name)
    return {"message": "Call initiated, room created.", "room_name": room_name}

@router.post("/initiate-warm-transfer")
async def handle_initiate_transfer(request: TransferRequest, background_tasks: BackgroundTasks):
    if not all([request.customer_room_name, request.agent_a_identity, request.summary]):
        raise HTTPException(status_code=400, detail="Missing required transfer information.")

    background_tasks.add_task(
        transfer_manager.initiate_transfer,
        customer_room_name=request.customer_room_name,
        agent_a_identity=request.agent_a_identity,
        summary=request.summary,
    )
    
    return {"message": "Warm transfer process acknowledged and has been initiated."}