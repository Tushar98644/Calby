from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import settings
from routers import call_router
from contextlib import asynccontextmanager
from services import livekit_service

@asynccontextmanager
async def lifespan(app: FastAPI):

    await livekit_service.connect()
    
    yield

    await livekit_service.close()

app = FastAPI(
    title="Calby",
    description="Backend service to manage LiveKit calls and LLM summarization",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(call_router, prefix="/api/v1", tags=["Call Management"])

@app.get("/")
async def root():
    return {"message": "Hello World"}