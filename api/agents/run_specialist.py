from dotenv import load_dotenv
from livekit import agents
from livekit.agents import JobRequest
from agents.livekit_agents.specialist_agent import specialist_agent_entrypoint
import json

load_dotenv(".env")

async def request_fnc(req: JobRequest):
    await req.accept(metadata=json.dumps({"agent_role": "specialist"}))

if __name__ == "__main__":
    print("🚀 Starting LiveKit SPECIALIST agent worker...")
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=specialist_agent_entrypoint,
            request_fnc=request_fnc, 
            agent_name="specialist-agent"
        )
    )