import os
from pathlib import Path
from dotenv import load_dotenv
from livekit import agents
from .support_agent import support_agent_entrypoint  
from .transfer_agent import transfer_agent_entrypoint

root_dir = Path(__file__).parent.parent
env_path = root_dir / ".env"
load_dotenv(env_path)

print(f"🔍 Loading .env from: {env_path}")
print(f"🔑 LIVEKIT_API_KEY found: {'✅' if os.getenv('LIVEKIT_API_KEY') else '❌'}")

async def main_entrypoint(ctx: agents.JobContext):
    room_name = ctx.room.name
    print(f"🎯 Agent requested for room: {room_name}")
    
    if "consult" in room_name or "specialist" in room_name:
        print("🔄 Starting Transfer Agent (Agent B)")
        await transfer_agent_entrypoint(ctx)
    else:
        print("📞 Starting Support Agent (Agent A)")  
        await support_agent_entrypoint(ctx)

if __name__ == "__main__":
    print("🚀 Starting LiveKit agent service...")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=main_entrypoint))
