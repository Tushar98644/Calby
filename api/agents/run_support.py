from dotenv import load_dotenv
from livekit import agents
from agents.livekit_agents.support_agent import support_agent_entrypoint

load_dotenv(".env")

if __name__ == "__main__":
    print("🚀 Starting LiveKit SUPPORT agent worker (automatic dispatch)...")
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=support_agent_entrypoint)
    )