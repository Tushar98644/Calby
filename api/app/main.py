from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agents.summarizer.state import AgentState
from core import settings
from .agents.summarizer import summarizer_app
from .schemas import SummaryRequest, SummaryResponse

app = FastAPI(
    title="Calby",
    description="Backend service to manage LiveKit calls and LLM summarization",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Warm transfer backend running!"}

@app.post("/generate-summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest) -> SummaryResponse:
    inputs: AgentState = {"transcript": request.transcript}
    result = summarizer_app.invoke(inputs)
    
    return SummaryResponse(summary=result.get("summary", "No summary could be generated."))