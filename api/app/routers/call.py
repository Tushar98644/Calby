from fastapi import APIRouter, HTTPException
from services import livekit_service
from agents import summarizer
from pydantic import BaseModel

class SummaryRequest(BaseModel):
    transcript: str
    
router = APIRouter()

@router.get('/get-livekit-token')
def get_livekit_token(room_name: str, identity: str):
    try:
        token = livekit_service.create_access_token(identity=identity, room_name=room_name)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")
    

@router.post("/generate-summary", tags=["AI Agent"])
def generate_summary_route(request: SummaryRequest):
    """
    Accepts a call transcript and returns an AI-generated summary.
    """
    if not request.transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")
    
    try:
        summary = summarizer.get_summary(request.transcript)
        return {"summary": summary}
    except Exception as e:
        print(f"Error during summary generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate summary.")